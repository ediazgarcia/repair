from flask import (
    render_template, Blueprint, flash, g, redirect, request, session, url_for
)

from werkzeug.security import generate_password_hash

#from apps.models.quotation import quotation
from apps.models.user import User
from apps import db
from .auth import set_role

quotation = Blueprint('quotation', __name__, url_prefix='/quotation')

@quotation.route("/list")
# función para verificar el rol del usuario
@set_role
def get_quotation(user=None):
    return render_template('admin/workshop/quotation/list.html')


@quotation.route("/create")
@set_role
def create_quotation(user=None):
    return render_template('admin/workshop/quotation/create.html')