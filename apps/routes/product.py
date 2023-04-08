from .auth import set_role
from flask import (
    render_template, Blueprint, flash, g, redirect, request, session, url_for
)

from werkzeug.security import generate_password_hash

# from apps.models.product import Product
from apps.models.user import User
from apps import db

product = Blueprint('product', __name__, url_prefix='/product')


# función para verificar el rol del usuario

@product.route("/list")
# función para verificar el rol del usuario
@set_role
def get_product(user=None):
    return render_template('admin/products/product/list.html')


@product.route("/create")
@set_role
def create_product(user=None):
    return render_template('admin/products/product/create.html')
