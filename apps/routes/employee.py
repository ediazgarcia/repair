from .auth import set_role
from flask import (
    render_template, Blueprint, flash, g, redirect, request, session, url_for
)

from werkzeug.security import generate_password_hash

# from apps.models.employee import Employee
from apps.models.user import User
from apps import db

employee = Blueprint('employee', __name__, url_prefix='/employee')


@employee.route("/list")
# función para verificar el rol del usuario
@set_role
def get_employee(user=None):
    return render_template('admin/directory/employees/list.html')


@employee.route("/create")
@set_role
def create_employee(user=None):
    return render_template('admin/directory/employees/create.html')
