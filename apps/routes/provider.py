from .auth import set_role
from flask import (
    render_template, Blueprint, flash, g, redirect, request, session, url_for
)

from werkzeug.security import generate_password_hash

# from apps.models.provider import Provider
from apps.models.user import User
from apps import db

provider = Blueprint('provider', __name__, url_prefix='/provider')


@provider.route("/list")
# función para verificar el rol del usuario
@set_role
def get_provider(user=None):
    return render_template('admin/directory/providers/list.html')


@provider.route("/create")
@set_role
def create_provider(user=None):
    return render_template('admin/directory/providers/create.html')
