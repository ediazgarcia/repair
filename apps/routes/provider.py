from flask import (
    render_template, Blueprint, flash, g, redirect, request, session, url_for
)

from werkzeug.security import generate_password_hash

#from apps.models.provider import Provider
from apps import db

provider = Blueprint('provider', __name__, url_prefix='/provider')

@provider.route("/list")
def get_provider():
    return render_template('admin/directory/providers/list.html')

@provider.route("/create")
def create_provider():
    return render_template('admin/directory/providers/create.html')