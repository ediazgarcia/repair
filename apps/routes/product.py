from flask import (
    render_template, Blueprint, flash, g, redirect, request, session, url_for
)

from werkzeug.security import generate_password_hash

#from apps.models.product import Product
from apps.models.user import User
from apps import db

product = Blueprint('product', __name__, url_prefix='/product')


# función para verificar el rol del usuario
@product.before_request
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

@product.route("/list")
def get_product():
    return render_template('admin/products/product/list.html')

@product.route("/create")
def create_product():
    return render_template('admin/products/product/create.html')