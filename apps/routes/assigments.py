from .auth import set_role
from flask import (
    render_template, Blueprint, flash, g, redirect, request, session, url_for
)

from werkzeug.security import generate_password_hash

# from apps.models.assigments import Assigments
from apps.models.user import User
from apps import db

assigments = Blueprint('assigments', __name__, url_prefix='/assigments')


@assigments.route("/list")
# función para verificar el rol del usuario
@set_role
def get_assigments(user=None):
    return render_template('admin/workshop/assigments/list.html')


@assigments.route("/create")
@set_role
def create_assigments(user=None):
    return render_template('admin/workshop/assigments/create.html')

@assigments.route("/create")
def create_assigments():
    return render_template('admin/workshop/assigments/create.html')