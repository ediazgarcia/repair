from flask import (
    render_template, Blueprint, flash, g, redirect, request, session, url_for
)

from werkzeug.security import generate_password_hash

#from apps.models.vehiclereception import VehicleReception
from apps.models.user import User
from apps import db

vehiclereception = Blueprint('vehiclereception', __name__, url_prefix='/vehiclereception')

# función para verificar el rol del usuario
@vehiclereception.before_request
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

@vehiclereception.route("/list")
def get_vehiclereception():
    return render_template('admin/workshop/vehiclereception/list.html')

@vehiclereception.route("/create")
def create_vehiclereception():
    return render_template('admin/workshop/vehiclereception/create.html')