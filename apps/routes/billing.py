
from flask import (render_template, Blueprint, flash, g,
                   redirect, request, session, url_for, jsonify)

from flask import json
# Importar el contador
from itertools import count
from werkzeug.security import generate_password_hash

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

from sqlalchemy import func, MetaData, Table, select

from apps.models.billing import Factura, DetalleFactura
from apps.models.user import User
from apps.models.client import Customer
from apps.models.company import Company
from apps.models.employee import Employee
from apps.models.products import Product
from apps.models.inventory import Inventory
from apps.models.orders_services import ServiceOrder
from apps import db
from .auth import set_role

billing = Blueprint('billing', __name__, url_prefix='/billing')


@billing.route("/list")
# función para verificar el rol del usuario
@set_role
def get_billing(user=None):
    factura=Factura.query.all()
    if g.role == 'Administrador':
        return render_template('admin/workshop/billing/list.html', factura=factura)
    else:
        return render_template('views/workshop/billing/list.html', factura=factura)


# Crear un contador que inicie en 100
order_num_counter = count(start=100)

@billing.route("/create", methods=['GET', 'POST'])
@set_role
def create_billing(user=None):
    if request.method == 'POST':
        company_id = request.form['company_id']
        client_id = request.form['client_id']
        orders_services_id = request.form['orders_services_id']
        #order_num = "FT-" + str(next(order_num_counter))
        company = Company.query.filter_by(id=company_id).first()
        client = Customer.query.filter_by(id=client_id).first()
        orders_services= ServiceOrder.query.filter_by(id=orders_services_id).first()
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

        factura = Factura(total=total,order_num=None,company=company, client=client,orders_services=orders_services)

        db.session.add(factura)
        db.session.commit()
        
        #Añadir orden de servicio al detalle factura
        #if orders_services_id != None:
            #orders_services_id=factura.orders_services_id
            #product_id=ServiceOrder.product
            #factura_id = factura.id
            #cantidad=1
            #precio_unitario=Product.price
            #precio_total=precio_unitario
            #detalle_factura = DetalleFactura(
            #factura_id=factura_id, producto_id=product_id, cantidad=cantidad, precio_unitario=precio_unitario, precio_total=precio_total)
            #db.session.add(detalle_factura)

        # Procesar los detalles de la factura
        for i in range(len(detalles)):
            factura_id = factura.id
            product_id = detalles[i]
            cantidad = cantidades[i]
            #cantidad_inv = int(cantidades[i])
            precio_unitario = precios_unitarios[i]
            precio_total = precios_totales[i] 

            detalle_factura = DetalleFactura(
                factura_id=factura_id, producto_id=product_id, cantidad=cantidad, precio_unitario=precio_unitario, precio_total=precio_total)

            db.session.add(detalle_factura)
        db.session.commit()  # Commit después de agregar todos los detalles

        flash('Factura creada exitosamente')
        return redirect(url_for('billing.ready_billing'))
    
    customers = Customer.query.all()
    companies = Company.query.all()
    order_service = ServiceOrder.query.all()
    product = db.session.query(Product).join(Inventory).filter(
        Inventory.set_stock > Inventory.min_stock).all()
    if g.role == 'Administrador':
        return render_template('admin/workshop/billing/create.html',
                               customers=customers, companies=companies, order_service=order_service, product=product)
    else:
        return render_template('views/workshop/billing/create.html',
                               customers=customers, companies=companies, order_service=order_service, product=product)
    
@billing.route("/done")
# función para verificar el rol del usuario
@set_role
def ready_billing(user=None):

    if g.role == 'Administrador':
        return render_template('admin/workshop/billing/done.html')
    else:
        return render_template('views/workshop/billing/done.html')
    
# Delete
@billing.route("/delete/<id>", methods=["GET"])
@set_role
def delete_billing(id, user=None):
    factura = Factura.query.get(id)

    if not factura:
        flash('Factura no encontrada', category='error')
        return redirect(url_for('billing.get_billing'))

    try:
        # Obtener la clave foránea de la factura

        # Buscar todos los registros relacionados con esa clave foránea
        eliminar_detalles = DetalleFactura.query.filter_by(factura_id=factura).all()

        # Eliminar cada uno de los registros relacionados
        for registro in eliminar_detalles:
            db.session.delete(registro)
        # Eliminar el registro principal
        db.session.delete(factura)

        # Guardar los cambios en la base de datos
        db.session.commit()

        flash('¡factura eliminada con éxito!')
        return redirect(url_for('billing.get_billing'))

    except Exception as err:
        flash(f'Error al eliminar la factura: {str(err)} {str (factura)}', category='error')
        return redirect(url_for('billing.get_billing'))

