from flask import (
    render_template, Blueprint, flash, g, redirect, request, session, url_for, jsonify
)

from werkzeug.security import generate_password_hash

from apps.models.user import User
from apps import db

users = Blueprint('users', __name__)


@users.route('/list', methods=('GET', 'POST'))
def get_users():
    users = User.query.all()
    return render_template('views/settings/index.html', users=users)

# create
@users.route('/create', methods=['POST'])
def create_user():
    if request.method == 'POST':
        # receive data from the form
        full_name = request.form['fullname']
        user_name = request.form['username']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']
        active = bool(int(request.form.get('estado')))
       

        # create a new Users object
        new_user = User(full_name, user_name, email, generate_password_hash(password), role, active)
        print(new_user)

        # save the object into the database
        db.session.add(new_user)
        db.session.commit()

    return redirect(url_for('users.get_users'))

#Obtner un ususario
# def get_user(id):
#     user = User.query.get_or_404(id)
#     return user


# Update Users
@users.route("/update", methods=["GET", "POST"])
def update_user():
    
    # get user by Id
    user = User.query.get(id)
    
    if request.method == 'POST':
        fullname = request.form['fullname']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        estado = request.form['estado']
        role = request.form['role']

        user.fullname = fullname
        user.email = email
        user.username = username
        user.password = password
        user.active = estado
        user.role = role
        db.session.commit()
        return redirect(url_for('users.get_users'))

    return render_template('views/settings/index.html', user=user)


# Delete users
@users.route('/delete/<id>')
def delete_user(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    
    return redirect(url_for('users.get_users'))






    
    
# # create
# @user.route('/create', methods=('GET', 'POST'))
# def create_user():
#     if request.method == 'POST':
#         try:
#             # receive data from the form
#             name = request.form.get('fullname')
#             username = request.form.get('username')
#             email = request.form.get('email')
#             password = request.form.get('password')
#             role = bool(int(request.form.get('role')))
#             active = bool(int(request.form.get('estado')))
#         except (TypeError, ValueError):
#             flash('Datos inválidos.')
#             return redirect(url_for('user.create_user'))

#         if not all((name, username, email, password)):
#             flash('Faltan campos obligatorios.')
#             return redirect(url_for('user.create_user'))

#         user = User.query.filter_by(username=username).first()
#         if user is not None:
#             flash('El nombre de usuario ya está en uso.')
#             return redirect(url_for('user.create_user'))
        
#         # create a new Contact object
#         new_user = User(name, username, email, generate_password_hash(password, method='sha256'), role, active)
#          # save the object into the database
#         db.session.add(new_user)
#         db.session.commit()
#         flash('Usuario creado correctamente.')
#         return redirect(url_for('user.index'))

#     return render_template('views/settings/index.html')

# def get_users(id):
#     userId = User.query.filter_by(id=id).first()
#     print(userId)
#     return userId


# #Eliminar un user
# @users.route('/delete/<int:id>')
# def delete_user(id):
#     user = get_users(id)
#     db.session.delete(user)
#     db.session.commit()

#     return redirect(url_for('user.get_users'))