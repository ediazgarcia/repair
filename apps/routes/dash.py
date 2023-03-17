from flask import (
    render_template, Blueprint, flash, g, redirect, request, session, url_for
)

dash = Blueprint('dash', __name__)


@dash.route("/")
def index():
    return render_template("admin/index.html")


@dash.route("/directory")
def directory():
    return render_template("admin/directory.html")


@dash.route("/vehicles")
def vehicles():
    return render_template("admin/vehicles.html")

@dash.route("/settings")
def settings():
    return render_template("admin/settings.html")