from flask import (
    render_template, Blueprint, flash, g, redirect, request, session, url_for
)

from werkzeug.security import generate_password_hash

from apps.models.user import User
from apps import db

user = Blueprint('user', __name__, url_prefix='/user')


# CRUDS USERS

# GetAllUsers
@user.route('/list', methods=('GET', 'POST'))
def get_user():
    user = User.query.all()
    return render_template('admin/settings/users/list.html', user=user)
    

# create
@user.route('/create', methods=('GET', 'POST'))
def create_user():
    if request.method == 'POST':

        # receive data from the form
        fullname = request.form['fullname']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']
        active = bool(int(request.form.get('active')))

        # create a new Contact object
        new_user = User(fullname, username, email, generate_password_hash(password, method='sha256'), role, active )
        
        # save the object into the database
        db.session.add(new_user)
        db.session.commit()

        # flash('Contact added successfully!')

        return redirect(url_for('user.get_user'))
    return render_template('admin/settings/users/create.html')
    
    
@user.route("/update/<string:id>", methods=["GET", "POST"])
def update_user(id):
    # get contact by Id
    print(id)
    user = User.query.get(id)

    if request.method == "POST":
        user.fullname = request.form['fullname']
        user.username = request.form['username']
        user.email = request.form['email']
        # user.password = request.form['password']
        user.role = request.form['role']
        user.active = bool(int(request.form.get('active')))

        db.session.commit()

        # flash('Contact updated successfully!')

        return redirect(url_for('user.get_user'))
    return render_template('admin/settings/users/update.html', user=user)
    
    
    

@user.route("/delete/<id>", methods=["GET"])
def delete_user(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()

    # flash('Contact deleted successfully!')

    return redirect(url_for('user.get_user'))
    
# # create
# @user.route('/create', methods=('GET', 'POST'))
# def create_user():
#     if request.method == 'POST':
#         try:
#             # receive data from the form
#             fullname = request.form['fullname']
#             username = request.form['username']
#             email = request.form['email']
#             password = request.form['password']
#             role = request.form['role']
#             active = bool(int(request.form.get('active')))
#         except (TypeError, ValueError):
#             flash('Datos inválidos.')
#             return redirect(url_for('user.create_user'))

#         if not all((fullname, username, email, password, role, active)):
#             flash('Faltan campos obligatorios.')
#             return redirect(url_for('user.create_user'))

#         users = User.query.filter_by(username=username).first()
        
#         if users is not None:
#             flash('El nombre de usuario ya está en uso.')
#             return redirect(url_for('user.create_user'))

#         new_user = User(fullname, username, email, generate_password_hash(password, method='sha256'), role, active )
#         db.session.add(new_user)
#         db.session.commit()
#         flash('Usuario creado correctamente.')
        
#         return redirect(url_for('user.get_user'))

#     return render_template('admin/settings/users/create.html')