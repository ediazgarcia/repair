from flask import (
    render_template, Blueprint, flash, g, redirect, request, session, url_for
)

from apps import app
from werkzeug.security import check_password_hash
from functools import wraps


from apps.models.user import User

auth = Blueprint('auth', __name__)

# Autentication (login)
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            if user.active:  # Verificar si el usuario está activo
                session['user_id'] = user.id
                session['username'] = user.username
                session['role'] = user.role
                return redirect(url_for('auth.home'))
            else:
                return render_template('auth/login.html', error='Your account is inactive. Please contact the administrator to activate your account.')
        else:
            return render_template('auth/login.html', error='Invalid username or password')
    else:
        return render_template('auth/login.html')

    
    
    
def set_role(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' in session:
            user = User.query.get(session['user_id'])
            g.role = session['role']
            return f(user=user, *args, **kwargs)
        return redirect(url_for('auth.login'))
    return decorated_function

    
@auth.route('/', methods=['GET', 'POST'])
@set_role
def home(user):
    if g.role == 'Administrador':
        return render_template('admin/index.html', username=session['username'], user=user, role=g.role)
    elif g.role == 'Usuario':
        return render_template('views/index.html', username=session['username'], user=user, role=g.role)
    return redirect(url_for('auth.login'))

    
@auth.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))