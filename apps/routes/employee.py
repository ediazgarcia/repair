from flask import (
    render_template, Blueprint, flash, g, redirect, request, session, url_for
)

from werkzeug.security import generate_password_hash

# from apps.models.employee import Employee
from apps.models.user import User
from apps import db

employee = Blueprint('employee', __name__, url_prefix='/employee')

# función para verificar el rol del usuario
@employee.before_request
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

@employee.route("/list")
def get_employee():
    return render_template('admin/directory/employees/list.html')

@employee.route("/create")
def create_employee():
    return render_template('admin/directory/employees/create.html')