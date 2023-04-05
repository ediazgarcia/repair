from flask import (
    render_template, Blueprint, flash, g, redirect, request, session, url_for
)

from werkzeug.security import generate_password_hash

#from apps.models.billing import Billing
from apps.models.user import User
from apps import db

billing = Blueprint('billing', __name__, url_prefix='/billing')

# función para verificar el rol del usuario
@billing.before_request
def set_role():
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        g.role = session['role']
        g.username = session['username']
        g.fullname = session['fullname']
        g.email = session['email']
    else:
        g.role = None
        g.username = None
        g.fullname = None
        g.email = None

@billing.route("/list")
def get_billing():
    return render_template('admin/workshop/billing/list.html')

@billing.route("/create")
def create_billing():
    return render_template('admin/workshop/billing/create.html')