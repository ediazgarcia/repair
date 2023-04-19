from .auth import set_role
from flask import (
    render_template, Blueprint, flash, g, redirect, request, session, url_for
)

from werkzeug.security import generate_password_hash
from werkzeug.exceptions import BadRequestKeyError

from apps.models.employee import Employee
from apps.models.company import Company
from apps.models.user import User
from apps import db

employee = Blueprint('employee', __name__, url_prefix='/employee')


@employee.route("/list")
# función para verificar el rol del usuario
@set_role
def get_employee(user=None):
    employees = Employee.query.all()
    if g.role == 'Administrador':
        return render_template('admin/directory/employees/list.html', employees=employees)
    else:
        return render_template('views/directory/employees/list.html', employees=employees)


@employee.route("/create", methods=['GET', 'POST'])
@set_role
def create_employee(user=None):

    if request.method == 'POST':
        try:
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            email = request.form['email']
            phone = str(request.form['phone'])
            document_type = request.form['document_type']
            document_number = request.form['document_number']
            birth_date = str(request.form['birth_date'])
            gender = request.form['gender']
            salary = str(request.form['salary'])
            address = request.form['address']
            city = request.form['city']
            state = request.form['state']
            position = request.form['position']
            # Obtener los días laborales seleccionados del formulario
            work_day = request.form.getlist('work_day[]')
            # Convertir la lista de días laborales a una cadena de texto
            work_days_str = ', '.join(work_day)
            # Actualizar el campo work_day del modelo de datos del empleado
            start_time = str(request.form['start_time'])
            end_time = str(request.form['end_time'])
            hire_date = str(request.form['hire_date'])
            company_id = request.form['company_id']
            user_id = request.form['user_id']

            # fetch the company name from the database
            company = Company.query.filter_by(id=company_id).first()
            company_name = company.trade_name if company else None

            # fetch the user name from the database
            user = User.query.filter_by(id=user_id).first()
            user_name = user.username if user else None

            # check if the email already exists in the database
            if Employee.query.filter_by(email=email).first() is not None:
                flash('Este correo electrónico ya está registrado.')
                return redirect(url_for('employee.create_employee'))

            # check if the document number already exists in the database
            if Employee.query.filter_by(document_number=document_number).first() is not None:
                flash('Este número de cédula ya está registrado.')
                return redirect(url_for('employee.create_employee'))

            # Crear un nuevo objeto Employee con los datos obtenidos
            new_employee = Employee(first_name=first_name, last_name=last_name, email=email, phone=phone, document_type=document_type, document_number=document_number, birth_date=birth_date,
                                    gender=gender, salary=salary, address=address, city=city, state=state, position=position, work_day=work_day, start_time=start_time, end_time=end_time,
                                    hire_date=hire_date, company=company, user=user)

            # add the company name to the employee object
            new_employee.company_name = company_name

            # add the user name to the employee object
            new_employee.user_name = user_name

            # Actualizar el campo work_day del modelo de datos del empleado
            new_employee.work_day = work_days_str
            # add the new customer to the database
            db.session.add(new_employee)
            db.session.commit()
            flash('¡Empleado añadido con éxito!')
            return redirect(url_for('employee.get_employee'))

        except BadRequestKeyError as e:
            flash(
                'Error en la solicitud revisa que no hay campos vacios: {}'.format(str(e)))
            return redirect(url_for('employee.create_employee'))

    companies = Company.query.all()
    users = User.query.filter(User.active).all()

    if g.role == 'Administrador':
        return render_template('admin/directory/employees/create.html', companies=companies, users=users, employee=employee)
    else:
        return render_template('views/directory/employees/create.html', companies=companies, users=users, employee=employee)


@employee.route("/update/<int:id>", methods=['GET', 'POST'])
@set_role
def update_employee(id, user=None):
    employee = Employee.query.get(id)
    if employee is None:
        flash('El empleado no existe.')
        return redirect(url_for('employee.get_employee'))

    if request.method == 'POST':
        try:
            # Obtener los datos del formulario
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            email = request.form['email']
            phone = str(request.form['phone'])
            document_type = request.form['document_type']
            document_number = request.form['document_number']
            birth_date = str(request.form['birth_date'])
            gender = request.form['gender']
            salary = str(request.form['salary'])
            address = request.form['address']
            city = request.form['city']
            state = request.form['state']
            position = request.form['position']
            work_day = request.form.getlist('work_day[]')
            work_days_str = ', '.join(work_day)
            start_time = str(request.form['start_time'])
            end_time = str(request.form['end_time'])
            hire_date = str(request.form['hire_date'])
            company_id = request.form['company_id']
            user_id = request.form['user_id']

            # Actualizar los campos del empleado existente
            employee.first_name = first_name
            employee.last_name = last_name
            employee.email = email
            employee.phone = phone
            employee.document_type = document_type
            employee.document_number = document_number
            employee.birth_date = birth_date
            employee.gender = gender
            employee.salary = salary
            employee.address = address
            employee.city = city
            employee.state = state
            employee.position = position
            employee.work_day = work_days_str
            employee.start_time = start_time
            employee.end_time = end_time
            employee.hire_date = hire_date
            employee.company_id = company_id
            employee.user_id = user_id

            # Hacer commit a la base de datos para guardar los cambios
            db.session.commit()
            flash('¡Empleado actualizado con éxito!')
            return redirect(url_for('employee.get_employee'))
        except BadRequestKeyError as e:
            flash(
                'Error en la solicitud revisa que no hay campos vacíos: {}'.format(str(e)))
            return redirect(url_for('employee.update_employee', id=id))

    companies = Company.query.all()
    users = User.query.filter(User.active).all()

    if g.role == 'Administrador':
        return render_template('admin/directory/employees/update.html', employee=employee, companies=companies, users=users)
    else:
        return render_template('views/directory/employees/update.html', employee=employee, companies=companies, users=users)


# Delete
@employee.route("/delete/<id>", methods=["GET"])
@set_role
def delete_employee(id, user=None):
    employee = Employee.query.get(id)

    if not employee:
        flash('Empleado no encontrado', category='error')
        return redirect(url_for('employee.get_employee'))

    try:
        db.session.delete(employee)
        db.session.commit()

        flash('¡Empleado eliminado con éxito!')
        return redirect(url_for('employee.get_employee'))

    except Exception as err:
        flash(f'Error al eliminar el empleado: {str(err)}', category='error')
        return redirect(url_for('employee.get_employee'))
