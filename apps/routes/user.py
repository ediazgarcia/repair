from .auth import set_role
from flask import (
    render_template, Blueprint, flash, g, redirect, request, session, url_for
)

from werkzeug.security import generate_password_hash, check_password_hash

from apps.models.user import User
from apps import db

user = Blueprint('user', __name__, url_prefix='/user')

# GetAllUsers


@user.route('/list', methods=('GET', 'POST'))
@set_role
def get_user(user=None):
    user = User.query.all()
    if g.role == 'Administrador':
        return render_template('admin/settings/users/list.html', user=user)
    else:
        return render_template('views/settings/users/list.html', user=user)


# create
@user.route('/create', methods=('GET', 'POST'))
@set_role
def create_user(user=None):
    if request.method == 'POST':
        try:
            # receive data from the form
            fullname = request.form['fullname']
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']
            role = request.form['role']
            active = bool(int(request.form.get('active')))

            # validate form data
            if not fullname:
                raise ValueError('El nombre completo es requerido.')
            if not username:
                raise ValueError('El nombre de usuario es requerido.')
            if not email:
                raise ValueError('El correo electrónico es requerido.')
            if not password:
                raise ValueError('La contraseña es requerida.')
            if not role:
                raise ValueError('El rol es requerido.')

            # create a new User object
            new_user = User(fullname, username, email, generate_password_hash(
                password, method='sha256'), role, active)

            # save the object into the database
            db.session.add(new_user)
            db.session.commit()

            flash('¡Usuario añadido con éxito!')
            return redirect(url_for('user.get_user'))

        except ValueError as err:
            flash(f'Error: {str(err)}', category='error')
        except Exception as err:
            flash(f'Error inesperado: {str(err)}', category='error')

    if g.role == 'Administrador':
        return render_template('admin/settings/users/create.html')
    else:
        return render_template('views/settings/users/create.html')


@user.route("/update/<string:id>", methods=["GET", "POST"])
@set_role
def update_user(id, user=None):
    # get contact by Id
    user = User.query.get(id)

    if request.method == "POST":
        try:
            # validate form data
            if not request.form['fullname']:
                raise ValueError('El nombre completo es requerido.')
            if not request.form['username']:
                raise ValueError('El nombre de usuario es requerido.')
            if not request.form['email']:
                raise ValueError('El correo electrónico es requerido.')
            if not request.form['role']:
                raise ValueError('El rol es requerido.')

            # update user object
            user.fullname = request.form['fullname']
            user.username = request.form['username']
            user.email = request.form['email']
            user.role = request.form['role']
            user.active = bool(int(request.form.get('active')))

            db.session.commit()

            flash('¡Usuario actualizado con éxito!')
            return redirect(url_for('user.get_user'))

        except ValueError as err:
            flash(f'Error: {str(err)}', category='error')
        except Exception as err:
            flash(f'Error inesperado: {str(err)}', category='error')

    if g.role == 'Administrador':
        return render_template('admin/settings/users/update.html', user=user)
    else:
        return render_template('views/settings/users/update.html', user=user)


# change_password
@user.route('/change_password', methods=('GET', 'POST'))
@set_role
def change_password(user=None):
    # Obtén el usuario actual
    if request.method == 'POST':
        try:
            # Obtener el usuario actual
            user = User.query.filter_by(id=session['user_id']).first()

            # Obtener la contraseña actual y la nueva contraseña del formulario
            current_password = request.form['current_password']
            new_password = request.form['new_password']

            # Validar que se proporcionen ambas contraseñas
            if not current_password or not new_password:
                flash('Se requiere la contraseña actual y la nueva contraseña.')
                return redirect(url_for('user.change_password'))

            # Verificar que la contraseña actual sea correcta
            if not check_password_hash(user.password, current_password):
                flash('La contraseña actual es incorrecta.')
                return redirect(url_for('user.change_password'))

            # Actualizar la contraseña del usuario en la base de datos
            user.password = generate_password_hash(
                new_password, method='sha256')
            db.session.commit()

            flash('¡Contraseña cambiada exitosamente!')
            return redirect(url_for('auth.profile'))

        except ValueError as err:
            flash(f'Error: {str(err)}', category='error')
            return redirect(url_for('user.change_password'))

    return render_template('/change_password.html', decrypted_current_password=session.get('current_password', ''), user=user)


@user.route("/delete/<id>", methods=["GET"])
@set_role
def delete_user(id, user=None):
    user = User.query.get(id)

    if not user:
        flash('Usuario no encontrado', category='error')
        return redirect(url_for('user.get_user'))

    try:
        db.session.delete(user)
        db.session.commit()

        flash('¡Usuario eliminado con éxito!')
        return redirect(url_for('user.get_user'))

    except Exception as err:
        flash(f'Error al eliminar el usuario: {str(err)}', category='error')
        return redirect(url_for('user.get_user'))
