from flask import (
    render_template, Blueprint, flash, g, redirect, request, session, url_for
)

from werkzeug.security import generate_password_hash

#from apps.models.billing import Billing
from apps.models.user import User
from apps import db
from .auth import set_role

billing = Blueprint('billing', __name__, url_prefix='/billing')

@billing.route("/list")
# función para verificar el rol del usuario
@set_role
def get_billing(user=None):
    return render_template('admin/workshop/billing/list.html')


@billing.route("/create")
@set_role
def create_billing(user=None):
    return render_template('admin/workshop/billing/create.html')