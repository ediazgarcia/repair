from .auth import set_role
from flask import (
    render_template, Blueprint, flash, g, redirect, request, session, url_for
)
# Importar el contador
from itertools import count
from werkzeug.security import generate_password_hash


from sqlalchemy import func
from apps.models.vehicle_reception import VehicleReception, VehicleReceptionDetail
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


# Crear un contador que inicie en 100
# order_num_counter = count(start=100)


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

        # Generar el order_num con prefijo "RV-"
        # order_num = "RV-" + str(next(order_num_counter))

        # Generar un nuevo número de orden
        # Crear un contador que inicie en 100
        order_num_counter_service = count(start=100)
        order_num = "RV-" + str(next(order_num_counter_service))

        # Verificar si el número de orden ya existe en la base de datos
        while VehicleReception.numero_orden_existe_en_bd(order_num):
            order_num = "RV-" + str(next(order_num_counter_service))

        # fetch the vehicle name from the database
        vehicle = Vehicle.query.filter_by(id=vehicle_id).first()

        # fetch the user name from the database
        employee = Employee.query.filter_by(id=employee_id).first()

        new_vehicle_reception = VehicleReception(order_num=order_num, reception_reason=reception_reason, vehicle=vehicle,
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


@vehicle_reception.route("/update/<int:id>", methods=["GET", "POST"])
@set_role
def update_vehicle_reception(id, user=None):
    vehicle_reception = VehicleReception.query.get(id)
    vehicle_reception_detail = VehicleReceptionDetail.query.filter_by(
        vehicle_reception_id=id).first()

    if request.method == 'POST':
        reception_reason = request.form['reception_reason']

        # Detalle de Recepción
        problem_description = request.form['problem_description']
        front_condition = request.form['front_condition']
        back_condition = request.form['back_condition']
        left_condition = request.form['left_condition']
        right_condition = request.form['right_condition']
        roof_condition = request.form['roof_condition']
        accessories = request.form['accessories']
        tools = request.form['tools']
        objects = request.form['objects']

        # Actualizar la recepción de vehículo existente en la base de datos
        vehicle_reception.reception_reason = reception_reason

        # Actualizar el detalle de la recepción de vehículo existente en la base de datos
        vehicle_reception_detail.problem_description = problem_description
        vehicle_reception_detail.front_condition = front_condition
        vehicle_reception_detail.back_condition = back_condition
        vehicle_reception_detail.left_condition = left_condition
        vehicle_reception_detail.right_condition = right_condition
        vehicle_reception_detail.roof_condition = roof_condition
        vehicle_reception_detail.accessories = accessories
        vehicle_reception_detail.tools = tools
        vehicle_reception_detail.objects = objects

        db.session.commit()

        flash('¡Recepción de Vehículo actualizada con éxito!')
        return redirect(url_for('vehicle_reception.get_vehicle_reception'))

    vehicle = Vehicle.query.all()
    employee = Employee.query.all()
    # print(
    #     f' DETALLES RECEPCION VEHICLE: {vehicle_reception_detail.problem_description}')
    if g.role == 'Administrador':
        return render_template('admin/workshop/vehiclereception/update.html', vehicle_reception=vehicle_reception, vehicle_reception_detail=vehicle_reception_detail, vehicle=vehicle, employee=employee)
    else:
        return render_template('views/workshop/vehiclereception/update.html', vehicle_reception=vehicle_reception, vehicle_reception_detail=vehicle_reception_detail, vehicle=vehicle, employee=employee)


# Delete
@vehicle_reception.route("/delete/<id>", methods=["GET"])
@set_role
def delete_vehicle_reception(id, user=None):
    vehicle_reception = VehicleReception.query.get(id)

    if not vehicle_reception:
        flash('Recepción de Vehículo no encontrada', category='error')
        return redirect(url_for('vehicle_reception.get_vehicle_reception'))

    try:
        # Obtener los registros relacionados en la tabla vehicle_reception_details
        vehicle_reception_details = VehicleReceptionDetail.query.filter_by(
            vehicle_reception_id=id).all()

        # Eliminar los registros en la tabla vehicle_reception_details
        for vehicle_reception_detail in vehicle_reception_details:
            db.session.delete(vehicle_reception_detail)

        # Confirmar los cambios en la base de datos
        db.session.commit()

        # Eliminar la recepción de vehículo
        db.session.delete(vehicle_reception)
        db.session.commit()

        flash('¡Recepción de Vehículo eliminada con éxito!')
        return redirect(url_for('vehicle_reception.get_vehicle_reception'))

    except Exception as err:
        db.session.rollback()  # Deshacer los cambios en caso de error
        flash(
            f'Error al eliminar la Recepción de Vehículo: {str(err)}', category='error')
        return redirect(url_for('vehicle_reception.get_vehicle_reception'))
