from .auth import set_role
from flask import (
    render_template, Blueprint, flash, g, redirect, request, session, url_for
)

from werkzeug.security import generate_password_hash

# from apps.models.inventory import inventory
from apps.models.user import User
from apps import db

inventory = Blueprint('inventory', __name__, url_prefix='/inventory')


@inventory.route("/list")
# función para verificar el rol del usuario
@set_role
def get_inventory(user=None):
    return render_template('admin/products/inventory/list.html')


@inventory.route("/create")
@set_role
def create_inventory(user=None):
    return render_template('admin/products/inventory/create.html')
