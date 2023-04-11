from .auth import set_role
from flask import (
    render_template, Blueprint, flash, g, redirect, request, session, url_for
)

from werkzeug.security import generate_password_hash


from sqlalchemy import func
from apps.models.vehicle_reception import VehicleReception
from apps.models.vehicle_reception_details import VehicleReceptionDetail
from apps.models.vehicle import Vehicle
from apps.models.employee import Employee
from apps import db

vehicle_reception = Blueprint(
    'vehicle_reception', __name__, url_prefix='/vehicle_reception')


@vehicle_reception.route("/list")
# función para verificar el rol del usuario
@set_role
def get_vehicle_reception(user=None):
    vehicle_reception = VehicleReception.query.all()
    vehicle_reception_detail = VehicleReceptionDetail.query.all()

    if g.role == 'Administrador':
        return render_template('admin/workshop/vehiclereception/list.html', vehicle_reception=vehicle_reception, vehicle_reception_detail=vehicle_reception_detail)
    else:
        return render_template('views/workshop/vehiclereception/list.html', vehicle_reception=vehicle_reception, vehicle_reception_detail=vehicle_reception_detail)


@vehicle_reception.route("/create", methods=['GET', 'POST'])
@set_role
def create_vehicle_reception(user=None):
    if request.method == 'POST':
        reception_reason = request.form['reception_reason']
        vehicle_id = request.form['vehicle_id']
        employee_id = request.form['employee_id']
        # Campos Detalle
        problem_description = request.form['problem_description']
        front_condition = request.form['front_condition']
        back_condition = request.form['back_condition']
        left_condition = request.form['left_condition']
        right_condition = request.form['right_condition']
        roof_condition = request.form['roof_condition']
        accessories = request.form['accessories']
        tools = request.form['tools']
        objects = request.form['objects']

        # fetch the vehicle name from the database
        vehicle = Vehicle.query.filter_by(id=vehicle_id).first()

        # fetch the user name from the database
        employee = Employee.query.filter_by(id=employee_id).first()

        new_vehicle_reception = VehicleReception(reception_reason=reception_reason, vehicle=vehicle,
                                                 employee=employee)

        db.session.add(new_vehicle_reception)
        db.session.commit()

        # Obtener id de la ultima recepcion
        max_id = db.session.query(func.max(VehicleReception.id)).scalar()

        # Insertar Detalle
        new_vehicle_reception_detail = VehicleReceptionDetail(problem_description=problem_description, front_condition=front_condition, back_condition=back_condition, left_condition=left_condition,
                                                              right_condition=right_condition, roof_condition=roof_condition, accessories=accessories, tools=tools, objects=objects, vehicle_reception_id=max_id)
        db.session.add(new_vehicle_reception_detail)
        db.session.commit()

        flash('¡Recepción de Vehículo añadida con éxito!')
    vehicle = Vehicle.query.all()
    employee = Employee.query.all()
    vehicle_reception = VehicleReception.query.all()
    return render_template('admin/workshop/vehiclereception/create.html', vehicle=vehicle, employee=employee, vehicle_reception=vehicle_reception)
