from flask import (
    render_template, Blueprint, flash, g, redirect, request, session, url_for
)

dash = Blueprint('dash', __name__)


@dash.route("/")
def index():
    return render_template("views/index.html")

# Usuarios
@dash.route('/settings')
def setting():
    return render_template('views/settings/index.html')