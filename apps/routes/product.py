from flask import (
    render_template, Blueprint, flash, g, redirect, request, session, url_for
)

from werkzeug.security import generate_password_hash

#from apps.models.product import Product
from apps import db

product = Blueprint('product', __name__, url_prefix='/product')

@product.route("/list")
def get_product():
    return render_template('admin/products/product/list.html')

@product.route("/create")
def create_product():
    return render_template('admin/products/product/create.html')