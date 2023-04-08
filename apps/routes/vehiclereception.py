from .auth import set_role
from flask import (
    render_template, Blueprint, flash, g, redirect, request, session, url_for
)

from werkzeug.security import generate_password_hash

# from apps.models.vehiclereception import VehicleReception
from apps.models.user import User
from apps import db

vehiclereception = Blueprint(
    'vehiclereception', __name__, url_prefix='/vehiclereception')


@vehiclereception.route("/list")
# función para verificar el rol del usuario
@set_role
def get_vehiclereception(user=None):
    return render_template('admin/workshop/vehiclereception/list.html')


@vehiclereception.route("/create")
@set_role
def create_vehiclereception(user=None):
    return render_template('admin/workshop/vehiclereception/create.html')
