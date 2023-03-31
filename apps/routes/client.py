from flask import (
    render_template, Blueprint, flash, g, redirect, request, session, url_for
)

from werkzeug.security import generate_password_hash

#from apps.models.client import Client
from apps import db

client = Blueprint('client', __name__, url_prefix='/client')

@client.route("/list")
def get_client():
    return render_template('admin/directory/clients/list.html')

@client.route("/create")
def create_client():
    return render_template('admin/directory/clients/create.html')