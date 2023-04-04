from flask import (
    render_template, Blueprint, flash, g, redirect, request, session, url_for
)

from werkzeug.security import generate_password_hash

#from apps.models.inventory import inventory
from apps.models.user import User
from apps import db

inventory = Blueprint('inventory', __name__, url_prefix='/inventory')

# función para verificar el rol del usuario
@inventory.before_request
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

@inventory.route("/list")
def get_inventory():
    return render_template('admin/products/inventory/list.html')

@inventory.route("/create")
def create_inventory():
    return render_template('admin/products/inventory/create.html')