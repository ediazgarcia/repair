from .auth import set_role
from flask import (
    render_template, Blueprint, flash, g, redirect, request, session, url_for
)
# Importar el contador
from itertools import count
from werkzeug.security import generate_password_hash

from apps.models.orders_services import ServiceOrder
from apps.models.user import User
from apps.models.vehicle_reception import VehicleReception
from apps.models.employee import Employee
from apps.models.products import Product
from apps import db

orders_services = Blueprint(
    'orders_services', __name__, url_prefix='/orders_services')


@orders_services.route("/list")
# función para verificar el rol del usuario
@set_role
def get_orders_services(user=None):
    orders_services = ServiceOrder.query.all()
    if g.role == 'Administrador':
        return render_template('admin/workshop/ordersservices/list.html', orders_services=orders_services)
    else:
        return render_template('views/workshop/ordersservices/list.html', orders_services=orders_services)


@orders_services.route("/create", methods=['GET', 'POST'])
@set_role
def create_orders_services(user=None):
    try:
        if request.method == 'POST':
            description = request.form['description']
            observations = request.form['observations']
            start_date = str(request.form['start_date'])
            end_date = str(request.form['end_date'])
            status = request.form['status']
            vehicle_reception_id = request.form['vehicle_reception_id']
            employee_id = request.form['employee_id']
            product_id = request.form['product_id']

            # Generar un nuevo número de orden
            # Crear un contador que inicie en 100
            order_num_counter_service = count(start=100)
            order_num = "OS-" + str(next(order_num_counter_service))

            # Verificar si el número de orden ya existe en la base de datos
            while ServiceOrder.numero_orden_existe_en_bd(order_num):
                order_num = "OS-" + str(next(order_num_counter_service))

            vehicle_reception = VehicleReception.query.filter_by(
                id=vehicle_reception_id).first()
            employee = Employee.query.filter_by(id=employee_id).first()
            product = Product.query.filter_by(id=product_id).first()

            new_order = ServiceOrder(order_num=order_num, description=description, observations=observations, start_date=start_date,
                                     end_date=end_date, status=status, vehicle_reception=vehicle_reception, employee=employee, product=product)

            db.session.add(new_order)
            db.session.commit()
            flash('¡Orden asignada con éxito!')
            return redirect(url_for('orders_services.create_orders_services'))
    except Exception as err:
        flash(f'Error inesperado: {str(err)}', category='error')

    vehicle_reception = VehicleReception.query.all()
    product = Product.query.filter(Product.type=="Servicio").filter(Product.status=="Activo").all()
    employee = Employee.query.filter(Employee.position=="Mecánico").filter(Employee.state=="Activo").all()
    if g.role == 'Administrador':
        return render_template('admin/workshop/ordersservices/create.html', orders_services=orders_services, employee=employee, product=product, vehicle_reception=vehicle_reception)
    else:
        return render_template('views/workshop/ordersservices/create.html', orders_services=orders_services, employee=employee, product=product, vehicle_reception=vehicle_reception)


@orders_services.route("/update/<int:id>", methods=["GET", "POST"])
@set_role
def update_orders_services(id, user=None):
    orders_services = ServiceOrder.query.get(id)

    if request.method == 'POST':
        description = request.form['description']
        observations = request.form['observations']
        start_date = str(request.form['start_date'])
        end_date = str(request.form['end_date'])
        status = request.form['status']

        orders_services.description = description
        orders_services.observations = observations
        orders_services.start_date = start_date
        orders_services.end_date = end_date
        orders_services.status = status

        db.session.commit()

        flash('¡Orden actualizada con éxito!')
        return redirect(url_for('orders_services.get_orders_services'))

    return render_template('admin/workshop/ordersservices/update.html', orders_services=orders_services)


@orders_services.route("/delete/<id>", methods=["GET"])
@set_role
def delete_orders_services(id, user=None):
    orders_services = ServiceOrder.query.get(id)

    if not orders_services:
        flash('Orden no encontrada', category='error')
        return redirect(url_for('orders_services.get_orders_services'))
    try:
        db.session.delete(orders_services)
        db.session.commit()

        flash('¡Orden eliminada con éxito!')
        return redirect(url_for('orders_services.get_orders_services'))

    except Exception as err:
        flash(
            f'Error al eliminar la orden: {str(err)}', category='error')
        return redirect(url_for('orders_services.get_orders_services'))
