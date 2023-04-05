from flask import (
    render_template, Blueprint, flash, g, redirect, request, session, url_for
)

from werkzeug.security import generate_password_hash

#from apps.models.assigments import Assigments
from apps.models.user import User
from apps import db

assigments = Blueprint('assigments', __name__, url_prefix='/assigments')

# función para verificar el rol del usuario
@assigments.before_request
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

@assigments.route("/list")
def get_assigments():
    return render_template('admin/workshop/assigments/list.html')

@assigments.route("/create")
def create_assigments():
    return render_template('admin/workshop/assigments/create.html')