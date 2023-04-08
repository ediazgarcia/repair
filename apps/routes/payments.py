from .auth import set_role
from flask import (
    render_template, Blueprint, flash, g, redirect, request, session, url_for
)

from werkzeug.security import generate_password_hash

from apps.models.payments import Payments
from apps.models.user import User
from apps import db

payments = Blueprint('payments', __name__, url_prefix='/payments')


@payments.route("/list", methods=('GET', 'POST'))
# función para verificar el rol del usuario
@set_role
def get_payments(user=None):
    payments = Payments.query.all()
    return render_template('admin/settings/payments/list.html', payments=payments)


@payments.route("/create", methods=('GET', 'POST'))
@set_role
def create_payments(user=None):
    if request.method == 'POST':
        try:
            description = request.form['description']
            type = request.form['type']

            new_payment = Payments(description=description, type=type)

            db.session.add(new_payment)
            db.session.commit()

            flash('¡Método de pago añadido con éxito!')
            return redirect(url_for('payments.get_payments'))

        except ValueError as err:
            flash(f'Error: {str(err)}', category='error')
        except Exception as err:
            flash(f'Error inesperado: {str(err)}', category='error')

    return render_template('admin/settings/payments/create.html')


@payments.route("/delete/<id>", methods=["GET"])
@set_role
def delete_payments(id, user=None):
    payments = Payments.query.get(id)

    if not payments:
        flash('Método de pago no encontrado', category='error')
        return redirect(url_for('payments.get_payments'))

    try:
        db.session.delete(payments)
        db.session.commit()

        flash('¡Método de pago eliminado con éxito!')
        return redirect(url_for('payments.get_payments'))

    except Exception as err:
        flash(
            f'Error al eliminar el método de pago: {str(err)}', category='error')
        return redirect(url_for('payments.get_payments'))
