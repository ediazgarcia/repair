
from flask import (render_template, Blueprint, flash, g,
                   redirect, request, session, url_for, jsonify, Response)

from flask import json
# Importar el contador
from itertools import count
from werkzeug.security import generate_password_hash

from sqlalchemy import func, MetaData, Table, select, engine

from apps.models.billing import Factura, DetalleFactura
from apps.models.user import User
from apps.models.client import Customer
from apps.models.company import Company
from apps.models.employee import Employee
from apps.models.products import Product
from apps.models.inventory import Inventory
from apps.models.payments import Payments
from apps.models.orders_services import ServiceOrder
from apps import db
from .auth import set_role

from io import BytesIO
from reportlab.pdfgen import canvas


billing = Blueprint('billing', __name__, url_prefix='/billing')


@billing.route("/list")
# función para verificar el rol del usuario
@set_role
def get_billing(user=None):
    factura = Factura.query.all()
    if g.role == 'Administrador':
        return render_template('admin/workshop/billing/list.html', factura=factura)
    else:
        return render_template('views/workshop/billing/list.html', factura=factura)

# Crear un contador que inicie en 100
# order_num_counter = count(start=100)


@billing.route("/create", methods=['GET', 'POST'])
@set_role
def create_billing(user=None):
    if request.method == 'POST':
        company_id = request.form['company_id']
        client_id = request.form['client_id']
        orders_services_id = request.form['orders_services_id']
        payments_id = request.form['payments_id']
        # order_num = "FT-" + str(next(order_num_counter))
        payments = Payments.query.filter_by(id=payments_id).first()
        company = Company.query.filter_by(id=company_id).first()
        client = Customer.query.filter_by(id=client_id).first()
        orders_services = ServiceOrder.query.filter_by(
            id=orders_services_id).first()

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
        order_num = "FT-" + str(next(order_num_counter_service))

        # Verificar si el número de orden ya existe en la base de datos
        while Factura.numero_orden_existe_en_bd(order_num):
            order_num = "FT-" + str(next(order_num_counter_service))

        factura = Factura(order_num=order_num, client=client, total=total,
                          orders_services=orders_services, company=company, payments=payments)
        factura.details = []
        db.session.add(factura)
        db.session.commit()

        # Procesar los detalles de la factura
        for i in range(len(detalles)):
            factura_id = factura.id
            product_id = detalles[i]
            cantidad = cantidades[i]
            precio_unitario = precios_unitarios[i]
            precio_total = precios_totales[i]

            detalle_factura = DetalleFactura(
                factura_id=factura_id, producto_id=product_id, cantidad=cantidad, precio_unitario=precio_unitario, precio_total=precio_total)
            factura.details.append(detalle_factura)
            db.session.add(detalle_factura)
        db.session.commit()  # Commit después de agregar todos los detalles
        factura.update_inventory()

        flash('Factura creada exitosamente')
        return redirect(url_for('billing.ready_billing'))

    customers = Customer.query.all()
    payments = Payments.query.all()
    companies = Company.query.all()
    order_service = ServiceOrder.query.filter(
        ServiceOrder.status == "Finalizada").all()
    product = db.session.query(Product).join(Inventory).filter(
        Inventory.set_stock > Inventory.min_stock).all()
    if g.role == 'Administrador':
        return render_template('admin/workshop/billing/create.html',
                               customers=customers, companies=companies, order_service=order_service, product=product, payments=payments)
    else:
        return render_template('views/workshop/billing/create.html',
                               customers=customers, companies=companies, order_service=order_service, product=product, payments=payments)


@billing.route("/done")
# función para verificar el rol del usuario
@set_role
def ready_billing(user=None):
    ultimo_id = Factura.query.order_by(db.desc(Factura.id)).first().id
    if g.role == 'Administrador':
        return render_template('admin/workshop/billing/done.html', ultimo_id=ultimo_id)
    else:
        return render_template('views/workshop/billing/done.html', ultimo_id=ultimo_id)

# Delete


@billing.route("/delete/<int:id>", methods=["GET"])
@set_role
def delete_billing(id, user=None):
    facturas = Factura.query.get(id)

    if not facturas:
        flash('Factura no encontrada', category='error')
        return redirect(url_for('billing.get_billing'))

    try:
        # Obtener los registros relacionados en la tabla de los detalles
        factura_detalles = DetalleFactura.query.filter_by(
            factura_id=id).all()

        # Eliminar los registros en la tabla de los detalles
        for factura_detalle in factura_detalles:
            db.session.delete(factura_detalle)

        # Confirmar los cambios en la base de datos
        db.session.commit()

        # Eliminar la recepción de vehículo
        db.session.delete(facturas)
        db.session.commit()

        flash('¡Factura eliminada con éxito!')
        return redirect(url_for('billing.get_billing'))

    except Exception as err:
        db.session.rollback()  # Deshacer los cambios en caso de error
        flash(
            f'Error al eliminar la factura:: {str(err)}', category='error')
        return redirect(url_for('billing.get_billing'))


@billing.route("/print/<int:id>", methods=["GET"])
@set_role
def print_billing(id, user=None):
    factura = Factura.query.get(id)
    detalles = DetalleFactura.query.filter_by(factura_id=id).all()

    # Crear el documento PDF utilizando ReportLab
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer)

    # Agregar la información de la factura al documento
    pdf.drawString(270, 750, f'{factura.company}')
    pdf.drawString(275, 725, 'Factura')
    pdf.drawString(60, 700, f'{factura.order_num}')
    pdf.drawString(60, 675, f'Cliente: {factura.client}')

    # Agregar los detalles de la factura al documento
    pdf.drawString(60, 630, 'Descripción')
    pdf.drawString(300, 630, 'Cantidad')
    pdf.drawString(380, 630, 'Precio Unitario')
    pdf.drawString(480, 630, 'Precio Total')
    y = 600
    for detalle in detalles:
        product = detalle.product
        cantidad = detalle.cantidad
        precio_unitario = detalle.precio_unitario
        precio_total = detalle.precio_total
        pdf.drawString(300, y, f'{cantidad}')
        pdf.drawString(60, y, f'{product}')
        pdf.drawString(380, y, f'{precio_unitario}')
        pdf.drawString(480, y, f'{precio_total}')
        y -= 30

    pdf.drawString(400, 200, f'Total a Pagar: {factura.total}')
    pdf.drawString(400, 240, f'Método de Pago: {factura.payments}')
    pdf.drawString(250, 80, 'Gracias por preferirnos!')

    # Guardar y cerrar el documento
    pdf.showPage()
    pdf.save()

    # Generar la respuesta con el PDF generado
    buffer.seek(0)
    response = Response(buffer.getvalue(), mimetype='application/pdf')
    response.headers['Content-Disposition'] = f'inline; filename=factura_{factura.id}.pdf'
    return response
