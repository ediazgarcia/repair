from flask import (
    render_template, Blueprint, flash, g, redirect, request, session, url_for, Response
)
# Importar el contador
from itertools import count
from werkzeug.security import generate_password_hash

# from apps.models.shopping import shopping
from apps.models.user import User
from apps import db
from .auth import set_role
from apps.models.company import Company
from apps.models.shopping import Shopping, ShoppingDetail
from apps.models.provider import Provider
from apps.models.products import Product
from apps.models.inventory import Inventory

from io import BytesIO
from reportlab.pdfgen import canvas

shopping = Blueprint('shopping', __name__, url_prefix='/shopping')


@shopping.route("/list")
# función para verificar el rol del usuario
@set_role
def get_shopping(user=None):
    shopping = Shopping.query.all()
    if g.role == 'Administrador':
        return render_template('admin/workshop/shopping/list.html', shopping=shopping)
    else:
        return render_template('views/workshop/shopping/list.html', shopping=shopping)


@shopping.route("/create", methods=['GET', 'POST'])
@set_role
def create_shopping(user=None):
    if request.method == 'POST':
        company_id = request.form['company_id']
        provider_id = request.form['provider_id']
        # order_num = "FT-" + str(next(order_num_counter))
        company = Company.query.filter_by(id=company_id).first()
        provider = Provider.query.filter_by(id=provider_id).first()
        # Obtener una lista de los valores del campo "detalle"
        detalles = request.form.getlist('detalle')
        # Obtener una lista de los valores del campo "cantidad"
        cantidades = request.form.getlist('cantidad')
        # Obtener una lista de los valores del campo "precio_unitario"
        precios_unitarios = request.form.getlist('precio_unitario')
        # Obtener una lista de los valores del campo "subtotal"
        precios_totales = request.form.getlist('subtotal')
        subtotal = []
        for num in precios_totales:
            try:
                subtotal.append(float(num))
            except ValueError:
                pass
        total = sum(subtotal)

        # Generar un nuevo número de orden
        # Crear un contador que inicie en 100
        order_num_counter_service = count(start=100)
        order_num = "CM-" + str(next(order_num_counter_service))

        # Verificar si el número de orden ya existe en la base de datos
        while Shopping.numero_orden_existe_en_bd(order_num):
            order_num = "CM-" + str(next(order_num_counter_service))

        new_shopping = Shopping(
            total=total, order_num=order_num, company=company, provider=provider)

        db.session.add(new_shopping)
        db.session.commit()
        # Procesar los detalles de la compra
        for i in range(len(detalles)):
            shopping_id = new_shopping.id
            product_id = detalles[i]
            quantity = cantidades[i]
            # cantidad_inv = int(cantidades[i])
            unt_cost = precios_unitarios[i]
            total_cost = precios_totales[i]

            new_detail = ShoppingDetail(
                shopping_id=shopping_id, product_id=product_id, quantity=quantity, unt_cost=unt_cost, total_cost=total_cost)

            db.session.add(new_detail)
        db.session.commit()  # Commit después de agregar todos los detalles

        flash('Compra creada exitosamente')
        return redirect(url_for('shopping.ready_shopping'))
    companies = Company.query.all()
    provider = Provider.query.all()
    product = db.session.query(Product).join(Inventory).filter(
        Inventory.set_stock > 0).all()
    return render_template('admin/workshop/shopping/create.html', companies=companies, product=product, provider=provider)


@shopping.route("/done")
# función para verificar el rol del usuario
@set_role
def ready_shopping(user=None):
    ultimo_id = Shopping.query.order_by(db.desc(Shopping.id)).first().id
    if g.role == 'Administrador':
        return render_template('admin/workshop/shopping/done.html', ultimo_id=ultimo_id)
    else:
        return render_template('views/workshop/shopping/done.html', ultimo_id=ultimo_id)


@shopping.route("/delete/<int:id>", methods=["GET"])
@set_role
def delete_shopping(id, user=None):
    shoppings = Shopping.query.get(id)

    if not shoppings:
        flash('Compra no encontrada', category='error')
        return redirect(url_for('shopping.get_shopping'))

    try:
        # Obtener los registros relacionados en la tabla de los detalles
        shoppings_details = ShoppingDetail.query.filter_by(
            shopping_id=id).all()

        # Eliminar los registros en la tabla de los detalles
        for shopping_detail in shoppings_details:
            db.session.delete(shopping_detail)

        # Confirmar los cambios en la base de datos
        db.session.commit()

        # Eliminar la recepción de vehículo
        db.session.delete(shoppings)
        db.session.commit()

        flash('¡Compra eliminada con éxito!')
        return redirect(url_for('shopping.get_shopping'))

    except Exception as err:
        db.session.rollback()  # Deshacer los cambios en caso de error
        flash(
            f'Error al eliminar la compra: {str(err)}', category='error')
        return redirect(url_for('shopping.get_shopping'))


@shopping.route("/print/<int:id>", methods=["GET"])
@set_role
def print_shopping(id, user=None):
    shopping = Shopping.query.get(id)
    detalles = ShoppingDetail.query.filter_by(shopping_id=id).all()

    # Crear el documento PDF utilizando ReportLab
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer)

    # Agregar la información de la factura al documento
    pdf.drawString(270, 750, f'{shopping.company}')
    pdf.drawString(275, 725, 'Compra')
    pdf.drawString(60, 700, f'{shopping.order_num}')
    pdf.drawString(60, 675, f'Proveedor: {shopping.provider}')

    # Agregar los detalles de la factura al documento
    pdf.drawString(60, 630, 'Descripción')
    pdf.drawString(300, 630, 'Cantidad')
    pdf.drawString(380, 630, 'Costo Unitario')
    pdf.drawString(480, 630, 'Costo Total')
    y = 600
    for detalle in detalles:
        product = detalle.product
        quantity = detalle.quantity
        unt_cost = detalle.unt_cost
        total_cost = detalle.total_cost
        pdf.drawString(300, y, f'{quantity}')
        pdf.drawString(60, y, f'{product}')
        pdf.drawString(380, y, f'{unt_cost}')
        pdf.drawString(480, y, f'{total_cost}')
        y -= 30

    pdf.drawString(400, 200, f'Total de la Compra: {shopping.total}')

    # Guardar y cerrar el documento
    pdf.showPage()
    pdf.save()

    # Generar la respuesta con el PDF generado
    buffer.seek(0)
    response = Response(buffer.getvalue(), mimetype='application/pdf')
    response.headers['Content-Disposition'] = f'inline; filename=compra_{shopping.id}.pdf'
    return response
