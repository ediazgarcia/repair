from .auth import set_role
from flask import (
    render_template, Blueprint, flash, g, redirect, request, session, url_for
)

from werkzeug.security import generate_password_hash

from apps.models.vehicle import Vehicle
from apps.models.client import Customer
from apps import db

vehicle = Blueprint('vehicle', __name__, url_prefix='/vehicle')


@vehicle.route("/list")
# función para verificar el rol del usuario
@set_role
def get_vehicle(user=None):
    vehicle=Vehicle.query.all()
    return render_template('admin/vehicles/vehicle/list.html',vehicle=vehicle)


@vehicle.route("/create", methods=['GET', 'POST'])
@set_role
def create_vehicle(user=None):
    if request.method == 'POST':
        try:
            client_id = request.form['client_id']
            brand = request.form['brand']
            model = request.form['model']
            year = request.form['year']
            fuel_type = request.form['fuel_type']
            plate_number = request.form['plate_number']
            chassis_number = request.form['chassis_number']
            color = request.form['color']
            transmission = request.form['transmission']
            cylinder = request.form['cylinder']
            status = request.form['status']

            new_vehicle = Vehicle (client_id=client_id,brand=brand,model=model,year=year,fuel_type=fuel_type,plate_number=plate_number,chassis_number=chassis_number,color=color,transmission=transmission,cylinder=cylinder,status=status)

            db.session.add(new_vehicle)
            db.session.commit()

            flash('¡Vehículo añadido con éxito!')
            return redirect(url_for('vehicle.get_vehicle'))

        except ValueError as err:
            flash(f'Error: {str(err)}', category='error')
        except Exception as err:
            flash(f'Error inesperado: {str(err)}', category='error')
            
    customers = Customer.query.all()
    return render_template('admin/vehicles/vehicle/create.html', customers=customers)


@vehicle.route("/update/<int:id>", methods=["GET", "POST"])
@set_role
def update_vehicle(id, user=None):
    vehicle = Vehicle.query.get_or_404(id)

    if request.method=="POST":
            brand = request.form['brand']
            model = request.form['model']
            year = request.form['year']
            fuel_type = request.form['fuel_type']
            plate_number = request.form['plate_number']
            chassis_number = request.form['chassis_number']
            color = request.form['color']
            transmission = request.form['transmission']
            cylinder = request.form['cylinder']
            status = request.form['status']

            vehicle.brand=brand
            vehicle.model=model
            vehicle.year=year
            vehicle.fuel_type=fuel_type
            vehicle.plate_number=plate_number
            vehicle.chassis_number=chassis_number
            vehicle.color=color 
            vehicle.transmission=transmission
            vehicle.cylinder=cylinder
            vehicle.status=status

            db.session.commit()

            flash('¡Vehículo actualizado con éxito!')
            return redirect(url_for('vehicle.get_vehicle'))
    
    return render_template('admin/vehicles/vehicle/update.html', vehicle=vehicle)

@vehicle.route("/delete/<id>", methods=["GET"])
@set_role
def delete_vehicle(id, user=None):
    vehicle = Vehicle.query.get(id)

    if not vehicle:
        flash('Vehículo no encontrado', category='error')
        return redirect(url_for('vehicle.get_vehicle'))

    try:
        db.session.delete(vehicle)
        db.session.commit()

        flash('¡Vehículo eliminado con éxito!')
        return redirect(url_for('vehicle.get_vehicle'))

    except Exception as err:
        flash(
            f'Error al eliminar el vehículo: {str(err)}', category='error')
        return redirect(url_for('vehicle.get_vehicle'))