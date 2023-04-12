from flask import (render_template,Blueprint,flash,g,redirect,request,session,url_for,)

from werkzeug.security import generate_password_hash

# from apps.models.billing import Billing
from apps.models.user import User
from apps.models.client import Customer
from apps.models.company import Company
from apps.models.employee import Employee
from apps.models.payments import Payments
from apps.models.products import Product
from apps.models.orders_services import ServiceOrder
from apps import db
from .auth import set_role

billing = Blueprint("billing", __name__, url_prefix="/billing")


@billing.route("/list")
# función para verificar el rol del usuario
@set_role
def get_billing(user=None):
    return render_template("admin/workshop/billing/list.html")


@billing.route("/create")
@set_role
def create_billing(user=None):
    customers = Customer.query.all()
    employees = Employee.query.all()
    company = Company.query.all()
    orders_services = ServiceOrder.query.all()
    payments = Payments.query.all()
    product = Product.query.all()
    return render_template(
        "admin/workshop/billing/create.html",
        customers=customers,
        employees=employees,
        orders_services=orders_services,
        company=company,
        payments=payments,
        product=product,
    )
