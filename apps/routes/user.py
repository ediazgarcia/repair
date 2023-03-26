from flask import (
    render_template, Blueprint, abort, flash, g, redirect, request, session, url_for, jsonify
)

from werkzeug.security import generate_password_hash, check_password_hash

from apps.models.user import User
from apps import db

user = Blueprint('user', __name__)


# Vista de Crear usuario
# create
@user.route('/create', methods=('GET', 'POST'))
# @login_required
def create_user():
    if request.method == 'POST':
        try:
            name = request.form.get('fullName')
            username = request.form.get('username')
            email = request.form.get('email')
            password = request.form.get('password')
            role = bool(int(request.form.get('role')))
            active = bool(int(request.form.get('estado')))
        except (TypeError, ValueError):
            flash('Datos inválidos.')
            return redirect(url_for('user.create_user'))

        if not all((name, username, email, password, role, active)):
            flash('Faltan campos obligatorios.')
            return redirect(url_for('user.create_user'))

        user = User.query.filter_by(username=username).first()
        if user is not None:
            flash('El nombre de usuario ya está en uso.')
            return redirect(url_for('user.create_user'))

        new_user = User(name, username, email, generate_password_hash(password, method='sha256'),  role, active)
        db.session.add(new_user)
        db.session.commit()
        flash('Usuario creado correctamente.')
        return redirect(url_for('user.list_users'))

    return render_template('views/setting/index.html')


# GetAllUsers
@user.route('/list', methods=('GET', 'POST'))
def list_users():
    users = User.query.all()
    return render_template('views/settings/index.html', users=users)