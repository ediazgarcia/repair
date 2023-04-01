from flask import (
    render_template, Blueprint, flash, g, redirect, request, session, url_for
)

from werkzeug.security import generate_password_hash

#from apps.models.inventory import inventory
from apps import db

inventory = Blueprint('inventory', __name__, url_prefix='/inventory')

@inventory.route("/list")
def get_inventory():
    return render_template('admin/products/inventory/list.html')

@inventory.route("/create")
def create_inventory():
    return render_template('admin/products/inventory/create.html')