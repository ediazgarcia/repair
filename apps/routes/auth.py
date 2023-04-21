from datetime import datetime, timedelta
from functools import wraps

import hashlib

from flask import (
    render_template, Blueprint, flash, g, redirect, request, session, url_for
)
from werkzeug.security import check_password_hash

from sqlalchemy import func
from apps import db

from apps.models.user import User
from apps.models.vehicle_reception import VehicleReception
from apps.models.vehicle import Vehicle
from apps.models.inventory import Inventory
from apps.models.billing import Factura
auth = Blueprint('auth', __name__)



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

# Autorization (login)


def set_role(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Obtener la marca de tiempo actual
        now = datetime.now()
        # Establecer el tiempo máximo de inactividad permitido (por ejemplo, 30 minutos)
        max_inactivity = timedelta(minutes=30)

        if 'user_id' in session:
            # Obtener la marca de tiempo de la última actividad del usuario
            last_activity = session.get('last_activity')
            if last_activity:
                last_activity = datetime.strptime(
                    last_activity, '%Y-%m-%d %H:%M:%S')
                # Verificar si ha pasado suficiente tiempo desde la última actividad del usuario
                if now - last_activity > max_inactivity:
                    # Si ha pasado suficiente tiempo, cerrar la sesión y redirigir al usuario a la página de inicio de sesión
                    session.clear()
                    return redirect(url_for('auth.login'))

            # Actualizar la marca de tiempo de la última actividad del usuario
            session['last_activity'] = now.strftime('%Y-%m-%d %H:%M:%S')

            user = User.query.get(session['user_id'])

            # Actualizar las variables de sesión con la información del usuario
            session['role'] = user.role
            session['username'] = user.username
            session['fullname'] = user.fullname
            session['email'] = user.email

            g.role = session['role']
            g.username = session['username']
            # Capitalizar el nombre completo del usuario
            g.fullname = session['fullname'].title()
            g.email = session['email']

            # Generar el avatar utilizando el correo electrónico del usuario
            email_hash = hashlib.md5(g.email.encode()).hexdigest()
            g.avatar_url = f"https://robohash.org/{email_hash}.png"
            return f(user=user, *args, **kwargs)
        return redirect(url_for('auth.login'))
    return decorated_function


# Página principal (home)


@auth.route('/', methods=['GET', 'POST'])
@set_role
def home(user):
    fecha_actual = datetime.now()
    fecha_24_horas_atras = fecha_actual - timedelta(hours=24)
    fecha_7_dias_atras = fecha_actual - timedelta(days=7)
    reception_vehicle = VehicleReception.query.all()
    vehicle=Vehicle.query.all()
    inventory=db.session.query(func.sum(Inventory.set_stock)).scalar()
    ventas=db.session.query(func.sum(Factura.total)).scalar()
    ventas_semana=db.session.query(func.sum(Factura.total)).filter(Factura.created >= fecha_7_dias_atras).scalar()
    ventas_dia=db.session.query(func.sum(Factura.total)).filter(Factura.created >= fecha_24_horas_atras).scalar()
    if g.role == 'Administrador':
        return render_template('admin/index.html',ventas_semana=ventas_semana,ventas_dia=ventas_dia,ventas=ventas,inventory=inventory,vehicle=vehicle ,reception_vehicle=reception_vehicle, user=user, role=g.role, username=g.username, fullname=g.fullname, email=g.email, avatar_url=g.avatar_url)
    elif g.role == 'Usuario':
        return render_template('views/index.html',ventas_semana=ventas_semana,ventas_dia=ventas_dia,ventas=ventas,inventory=inventory,vehicle=vehicle ,reception_vehicle=reception_vehicle, user=user, role=g.role, username=g.username, fullname=g.fullname, email=g.email, avatar_url=g.avatar_url)
    return redirect(url_for('auth.login'))


@auth.route('/profile')
@set_role
def profile(user):
    if g.role == 'Administrador':
        return render_template('admin/profile.html')
    elif g.role == 'Usuario':
        return render_template('views/profile.html')
    return redirect(url_for('auth.login'))

# Cierre de sesión (logout)


@auth.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))
