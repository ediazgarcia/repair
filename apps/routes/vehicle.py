from .auth import set_role
from flask import (
    render_template, Blueprint, flash, g, redirect, request, session, url_for
)

from werkzeug.security import generate_password_hash

# from apps.models.vehicle import Vehicle
from apps.models.user import User
from apps import db

vehicle = Blueprint('vehicle', __name__, url_prefix='/vehicle')


@vehicle.route("/list")
# función para verificar el rol del usuario
@set_role
def get_vehicle(user=None):
    return render_template('admin/vehicles/vehicle/list.html')


@vehicle.route("/create")
@set_role
def create_vehicle(user=None):
    return render_template('admin/vehicles/vehicle/create.html')
