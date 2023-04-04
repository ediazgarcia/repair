from flask import (
    render_template, Blueprint, flash, g, redirect, request, session, url_for
)

from apps import app
from werkzeug.security import check_password_hash
from functools import wraps

from apps.models.user import User

auth = Blueprint('auth', __name__)

# Autenticación (login)
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if not username or not password:
            flash('Los campos nombre de usuario y contraseña son obligatorios.')
            return render_template(url_for('auth.login'))
        
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            if user.active:  # Verificar si el usuario está activo
                session['user_id'] = user.id
                session['username'] = user.username
                session['fullname'] = user.fullname
                session['email'] = user.email
                session['role'] = user.role
                return redirect(url_for('auth.home'))
            else:
                flash('Tu cuenta está inactiva. Contacta con un administrador.')
                return render_template('auth/login.html')
        else:
            flash('Tu nombre de usuario o contraseña son incorrectos.')
            return render_template('auth/login.html')
    else:
        return render_template('auth/login.html')


def set_role(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' in session:
            user = User.query.get(session['user_id'])
            g.role = session['role']
            g.username = session['username']
            g.fullname = session['fullname']
            g.email = session['email']
            return f(user=user, *args, **kwargs)
        return redirect(url_for('auth.login'))
    return decorated_function

# Página principal (home)
@auth.route('/', methods=['GET', 'POST'])
@set_role
def home(user):
    if g.role == 'Administrador':
        return render_template('admin/index.html', username=session['username'], user=user, role=g.role)
    elif g.role == 'Usuario':
        return render_template('views/index.html', username=session['username'], user=user, role=g.role)
    return redirect(url_for('auth.login'))

# Cierre de sesión (logout)
@auth.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))
