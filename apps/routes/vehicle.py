from flask import (
    render_template, Blueprint, flash, g, redirect, request, session, url_for
)

from werkzeug.security import generate_password_hash

#from apps.models.vehicle import Vehicle
from apps.models.user import User
from apps import db

vehicle = Blueprint('vehicle', __name__, url_prefix='/vehicle')



# función para verificar el rol del usuario
@vehicle.before_request
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

@vehicle.route("/list")
def get_vehicle():
    return render_template('admin/vehicles/vehicle/list.html')

@vehicle.route("/create")
def create_vehicle():
    return render_template('admin/vehicles/vehicle/create.html')