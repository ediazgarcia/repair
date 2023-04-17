
from flask import (render_template, Blueprint, flash, g,
                   redirect, request, session, url_for, jsonify)

from flask import json
# Importar el contador
from itertools import count
from werkzeug.security import generate_password_hash

from sqlalchemy import func

from apps.models.billing import Billing, BillingDetail

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

billing = Blueprint("billing", __name__)


@billing.route("/list")
# función para verificar el rol del usuario
@set_role
def get_billing(user=None):
    billings = Billing.query.all()
    billing_detail = BillingDetail.query.all()
    customers = Customer.query.all()
    employees = Employee.query.all()
    company = Company.query.all()
    orders_services = ServiceOrder.query.all()
    product = Product.query.all()

    if g.role == 'Administrador':
        return render_template('admin/workshop/billing/list.html', billings=billings, billing_detail=billing_detail, customers=customers, employees=employees, company=company, orders_services=orders_services, product=product)
    else:
        return render_template('views/workshop/billing/list.html', billings=billings, billing_detail=billing_detail, customers=customers, employees=employees, company=company, orders_services=orders_services, product=product)


# Crear un contador que inicie en 100
# order_num_counter = count(start=100)


@billing.route("/billing/create", methods=['GET', 'POST'])
@set_role
def create_billing(user=None):
    if request.method == 'POST':
        numero = request.form['numero']
        fecha = request.form['fecha']
        # Obtener una lista de los valores del campo "detalle"
        detalles = request.form.getlist('detalle')
        # Obtener una lista de los valores del campo "cantidad"
        cantidades = request.form.getlist('cantidad')
        # Obtener una lista de los valores del campo "precio_unitario"
        precios_unitarios = request.form.getlist('precio_unitario')

        factura = Factura(numero=numero, fecha=fecha)
        db.session.add(factura)
        db.session.commit()

        # Procesar los detalles de la factura
        for i in range(len(detalles)):
            factura_id = factura.id
            descripcion = detalles[i]
            cantidad = cantidades[i]
            precio_unitario = precios_unitarios[i]

            detalle_factura = DetalleFactura(
                factura_id=factura_id, descripcion=descripcion, cantidad=cantidad, precio_unitario=precio_unitario)

            db.session.add(detalle_factura)

        db.session.commit()  # Commit después de agregar todos los detalles

        flash('Factura creada exitosamente')
        return redirect(url_for('billing.create_billing'))

    billings = Billing.query.all()
    billing_detail = BillingDetail.query.all()
    customers = Customer.query.all()
    companies = Company.query.all()
    order_service = ServiceOrder.query.all()
    product = db.session.query(Product).join(Inventory).filter(
        Inventory.set_stock > Inventory.min_stock).all()
    if g.role == 'Administrador':
        return render_template('admin/workshop/billing/create.html', billings=billings, billing_detail=billing_detail,
                               customers=customers, companies=companies, order_service=order_service, product=product)
    else:
        return render_template('views/workshop/billing/create.html', billings=billings, billing_detail=billing_detail,
                               customers=customers, companies=companies, order_service=order_service, product=product)
