from flask import (render_template, Blueprint, flash, g,
                   redirect, request, session, url_for,)

import json
# Importar el contador
from itertools import count
from werkzeug.security import generate_password_hash

from sqlalchemy import func

from apps.models.billing import Billing, BillingDetail
from apps.models.user import User
from apps.models.client import Customer
from apps.models.company import Company
from apps.models.employee import Employee
# from apps.models.payments import Payments
from apps.models.products import Product
from apps.models.inventory import Inventory
from apps.models.orders_services import ServiceOrder
from apps import db
from .auth import set_role

billing = Blueprint("billing", __name__, url_prefix="/billing")


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
order_num_counter = count(start=100)


@billing.route("/create", methods=['GET', 'POST'])
@set_role
def create_billing(user=None):
    if request.method == 'POST':
        # Obtener datos de la cabecera de la factura
        total = request.form['total']
        company_id = request.form['company_id']
        client_id = request.form['client_id']
        orders_services_id = request.form['orders_services_id']

        # Generar el order_num con prefijo "RV-"
        order_num = "FT-" + str(next(order_num_counter))

        # Fetch los objetos relacionados desde la base de datos
        company = Company.query.filter_by(id=company_id).first()
        client = Customer.query.filter_by(id=client_id).first()
        orders_services = ServiceOrder.query.filter_by(
            id=orders_services_id).first()
        # payments = ServiceOrder.query.filter_by(id=payments_id).first()

        # Crear una instancia de la clase Billing
        billing = Billing(order_num=order_num, total=total, company=company,
                          client=client, orders_services=orders_services)

        # Guardar la factura en la base de datos
        db.session.add(billing)
        db.session.commit()

        # Obtener id de la ultima factura
        max_id = db.session.query(func.max(Billing.id)).scalar()
        billing_id = max_id
        billing = Billing.query.filter_by(id=billing_id).first()

        # Confirmar los cambios en la base de datos
        db.session.commit()
        flash('¡Factura emitida con éxito!')
        return redirect(url_for('billing.create_billing'))

    billings = Billing.query.all()
    billing_detail = BillingDetail.query.all()
    customers = Customer.query.all()
    companies = Company.query.all()
    order_service = ServiceOrder.query.all()
    # payments = Payments.query.all()
    product = db.session.query(Product).join(Inventory).filter(
        Inventory.set_stock > Inventory.min_stock).all()
    if g.role == 'Administrador':
        return render_template('admin/workshop/billing/create.html', billings=billings, billing_detail=billing_detail,
                               customers=customers, companies=companies, order_service=order_service, product=product)
    else:
        return render_template('views/workshop/billing/create.html', billings=billings, billing_detail=billing_detail,
                               customers=customers, companies=companies, order_service=order_service, product=product)
