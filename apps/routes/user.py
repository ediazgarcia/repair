from flask import (
    render_template, Blueprint, abort, flash, g, redirect, request, session, url_for, jsonify
)

from werkzeug.security import generate_password_hash

from apps.models.user import User
from apps import db

user = Blueprint('user', __name__)


# CRUDS USERS

# GetAllUsers
@user.route('/', methods=('GET', 'POST'))
def index():
    users = User.query.all()
    return render_template('views/settings/index.html')
    
# create
@user.route('/create', methods=('GET', 'POST'))
def create_user():
    if request.method == 'POST':
        try:
            # receive data from the form
            name = request.form.get('fullname')
            username = request.form.get('username')
            email = request.form.get('email')
            password = request.form.get('password')
            role = bool(int(request.form.get('role')))
            active = bool(int(request.form.get('estado')))
        except (TypeError, ValueError):
            flash('Datos inválidos.')
            return redirect(url_for('user.create_user'))

        if not all((name, username, email, password)):
            flash('Faltan campos obligatorios.')
            return redirect(url_for('user.create_user'))

        user = User.query.filter_by(username=username).first()
        if user is not None:
            flash('El nombre de usuario ya está en uso.')
            return redirect(url_for('user.create_user'))
        
        # create a new Contact object
        new_user = User(name, username, email, generate_password_hash(password, method='sha256'), role, active)
         # save the object into the database
        db.session.add(new_user)
        db.session.commit()
        flash('Usuario creado correctamente.')
        return redirect(url_for('user.index'))

    return render_template('views/settings/index.html')