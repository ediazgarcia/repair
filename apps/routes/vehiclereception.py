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

vehiclereception = Blueprint(
    'vehiclereception', __name__, url_prefix='/vehiclereception')


@vehiclereception.route("/list")
# función para verificar el rol del usuario
@set_role
def get_vehiclereception(user=None):
    vehiclereception=VehicleReception.query.all()
    vehiclereception_detail=VehicleReceptionDetail.query.all()
    return render_template('admin/workshop/vehiclereception/list.html', vehiclereception=vehiclereception, vehiclereception_detail=vehiclereception_detail)


@vehiclereception.route("/create", methods=['GET', 'POST'])
@set_role
def create_vehiclereception(user=None):
    if request.method == 'POST':
            employee_id = request.form['employee_id']
            vehicle_id = request.form['vehicle_id']
            reception_reason = request.form['reception_reason']
            #Campos Detalle
            problem_description = request.form['problem_description']
            front_condition = request.form['front_condition']
            back_condition = request.form['back_condition']
            left_condition = request.form['left_condition']
            right_condition = request.form['right_condition']
            roof_condition = request.form['roof_condition']
            accessories = request.form['accessories']
            tools =  request.form['tools']
            objects =  request.form['objects']

            new_vehiclereception = VehicleReception (employee_id = employee_id, vehicle_id = vehicle_id, reception_reason = reception_reason)

            db.session.add(new_vehiclereception)
            db.session.commit()
            #Obtener id de la ultima recepcion
            max_id = db.session.query(func.max(VehicleReception.id))
            vehicle_reception_id = max_id
            
            #Insertar Detalle
            new_vehiclereception_detail = VehicleReceptionDetail (problem_description = problem_description, front_condition = front_condition, back_condition = back_condition, left_condition = left_condition, right_condition = right_condition, roof_condition = roof_condition, accessories = accessories, tools = tools, objects = objects, vehicle_reception_id = vehicle_reception_id)
            db.session.add(new_vehiclereception_detail)
            db.session.commit()
            
            flash('¡Recepción de Vehículo añadida con éxito!')
    vehicle=Vehicle.query.all()
    employee=Employee.query.all()
    return render_template('admin/workshop/vehiclereception/create.html', vehicle=vehicle, employee=employee)
