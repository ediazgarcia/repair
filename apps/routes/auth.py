from flask import (
    render_template, Blueprint, flash, g, redirect, request, session, url_for
)


# from apps import db

auth = Blueprint('auth', __name__, url_prefix='/auth')

