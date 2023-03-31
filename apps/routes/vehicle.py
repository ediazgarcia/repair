from flask import (
    render_template, Blueprint, flash, g, redirect, request, session, url_for
)

from werkzeug.security import generate_password_hash

#from apps.models.vehicle import Vehicle
from apps import db

vehicle = Blueprint('vehicle', __name__, url_prefix='/vehicle')

@vehicle.route("/list")
def get_vehicle():
    return render_template('admin/vehicles/vehicle/list.html')

@vehicle.route("/create")
def create_vehicle():
    return render_template('admin/vehicles/vehicle/create.html')