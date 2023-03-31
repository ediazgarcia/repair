from flask import (
    render_template, Blueprint, flash, g, redirect, request, session, url_for
)

from werkzeug.security import generate_password_hash

#from apps.models.employee import Employee
from apps import db

employee = Blueprint('employee', __name__, url_prefix='/employee')

@employee.route("/list")
def get_employee():
    return render_template('admin/directory/employees/list.html')

@employee.route("/create")
def create_employee():
    return render_template('admin/directory/employees/create.html')