from flask import (
    render_template, Blueprint, flash, g, redirect, request, session, url_for
)

from werkzeug.security import generate_password_hash

#from apps.models.shopping import shopping
from apps.models.user import User
from apps import db
from .auth import set_role

shopping = Blueprint('shopping', __name__, url_prefix='/shopping')

@shopping.route("/list")
# función para verificar el rol del usuario
@set_role
def get_shopping(user=None):
    return render_template('admin/workshop/shopping/list.html')


@shopping.route("/create")
@set_role
def create_shopping(user=None):
    return render_template('admin/workshop/shopping/create.html')