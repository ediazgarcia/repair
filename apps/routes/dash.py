from flask import (
    render_template, Blueprint, flash, g, redirect, request, session, url_for
)

dash = Blueprint('dash', __name__)


@dash.route("/home")
def home():
    return render_template("admin/index.html")

@dash.route("/")
def login():
    return render_template("auth/login.html")
