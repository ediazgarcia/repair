from flask import (
    render_template, Blueprint, flash, g, redirect, request, session, url_for
)

from werkzeug.security import generate_password_hash

#from apps.models.provider import Provider
from apps.models.user import User
from apps import db

provider = Blueprint('provider', __name__, url_prefix='/provider')

# función para verificar el rol del usuario
@provider.before_request
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

@provider.route("/list")
def get_provider():
    return render_template('admin/directory/providers/list.html')

@provider.route("/create")
def create_provider():
    return render_template('admin/directory/providers/create.html')