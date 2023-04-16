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
        # Obtener los datos del formulario
        type = str(request.form['type'])
        total = request.form['total']
        company_id = request.form['company_id']
        client_id = request.form['client_id']
        orders_services_id = request.form['orders_services_id']

        # Campos Detalle Facturas
        # Crear una nueva instancia de la clase BillingDetail para cada producto en la factura
        products_id = request.form.getlist('product_id[]')
        quantity = request.form.getlist('quantity[]')
        unit_price = request.form.getlist('unit_price[]')
        total = request.form.getlist('total[]')

        # Generar el order_num con prefijo "RV-"
        order_num = "FT-" + str(next(order_num_counter))

        # Fetch los objetos relacionados desde la base de datos
        company = Company.query.filter_by(id=company_id).first()
        client = Customer.query.filter_by(id=client_id).first()
        # employee = Employee.query.filter_by(id=employee_id).first()
        orders_service = ServiceOrder.query.filter_by(
            id=orders_services_id).first()
        # payments = ServiceOrder.query.filter_by(id=payments_id).first()

        # Crear una instancia de la clase Billing
        billing = Billing(order_num=order_num, type=type, total=total,
                          company=company, client=client,
                          orders_service=orders_service)

        # Guardar la factura en la base de datos
        db.session.add(billing)
        db.session.commit()

        # Obtener id de la ultima recepcion
        # max_id = db.session.query(func.max(BillingDetail.id)).scalar()

        # Crear instancias de la clase BillingDetail y asociarlas con la factura creada anteriormente
        for i in range(len(products_id)):
            product = Product.query.filter_by(id=products_id[i]).first()
            billing_detail = BillingDetail(unit_price=unit_price[i], quantity=quantity[i],
                                           total=total[i], product=product, billing=billing)
            db.session.add(billing_detail)

        db.session.commit()

    billings = Billing.query.all()
    billing_detail = BillingDetail.query.all()
    customers = Customer.query.all()
    employees = Employee.query.all()
    companies = Company.query.all()
    orders_services = ServiceOrder.query.all()
    # payments = Payments.query.all()
    product = Product.query.all()

    if g.role == 'Administrador':
        return render_template('admin/workshop/billing/create.html', billings=billings, billing_detail=billing_detail,
                               customers=customers, companies=companies, orders_services=orders_services, product=product)
    else:
        return render_template('views/workshop/billing/create.html', billings=billings, billing_detail=billing_detail,
                               customers=customers, companies=companies, orders_services=orders_services, product=product)
