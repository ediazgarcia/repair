from flask import (
    render_template, Blueprint, flash, g, redirect, request, session, url_for
)

from werkzeug.security import generate_password_hash

from apps.models.user import User
from apps import db

user = Blueprint('user', __name__, url_prefix='/user')


# función para verificar el rol del usuario
def set_role():
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        g.role = session['role']


# asignar la función set_role a la función before_request
@user.before_request
def before_request():
    set_role()

# GetAllUsers
@user.route('/list', methods=('GET', 'POST'))
def get_user():
    user = User.query.all()
    return render_template('admin/settings/users/list.html', user=user)
    

# create
@user.route('/create', methods=('GET', 'POST'))
def create_user():
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
            new_user = User(fullname, username, email, generate_password_hash(password, method='sha256'), role, active)
            
            # save the object into the database
            db.session.add(new_user)
            db.session.commit()

            flash('¡Usuario añadido con éxito!')
            return redirect(url_for('user.get_user'))
        
        except ValueError as err:
            flash(f'Error: {str(err)}', category='error')
        except Exception as err:
            flash(f'Error inesperado: {str(err)}', category='error')
        
    return render_template('admin/settings/users/create.html')

    

@user.route("/update/<string:id>", methods=["GET", "POST"])
def update_user(id):
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
        
    return render_template('admin/settings/users/update.html', user=user)

    
    
@user.route("/delete/<id>", methods=["GET"])
def delete_user(id):
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


    