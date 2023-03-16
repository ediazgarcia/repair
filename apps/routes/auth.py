from flask import (
    render_template, Blueprint, flash, g, redirect, request, session, url_for
)

from apps.models.role import Role
from apps import db

auth = Blueprint('auth', __name__, url_prefix='/auth')

# Registrar un role


@auth.route('/regiter', methods=('GET', 'POST'))
def register():

    if request.method == 'POST':
        name = request.form.get('name')

        role = Role(name)

        error = None
        if not name:
            error = 'Se requiere nombre de rol'

        rol_name = Role.query.filter_by(name=name).first()
        if rol_name == None:
            db.session.add(role)
            db.session.commit()
        else:
            error = f'El nombre de rol {name} esta registrado'
        flash(error)

    return render_template('admin/role.html')
