from flask import (
    render_template, Blueprint, flash, g, redirect, request, session, url_for
)

from werkzeug.security import generate_password_hash

from apps.models.payments import Payments
from apps.models.user import User
from apps import db

payments = Blueprint('payments', __name__, url_prefix='/payments')

# función para verificar el rol del usuario
@payments.before_request
def set_role():
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        g.role = session['role']
        g.username = session['username']
        g.fullname = session['fullname']
        g.email = session['email']
    else:
        g.role = None
        g.username = None
        g.fullname = None
        g.email = None

@payments.route("/list", methods=('GET','POST'))
def get_payments():
    payments= Payments.query.all()
    return render_template('admin/settings/payments/list.html', payments=payments)

@payments.route("/create", methods=('GET', 'POST'))
def create_payments():
    if request.method=='POST':
        try:
            description=request.form['description']
            type=request.form['type']

            new_payment=Payments(description=description,type=type)

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
def delete_payments(id):
    payments=Payments.query.get(id)

    if not payments:
        flash('Método de pago no encontrado', category='error')
        return redirect(url_for('payments.get_payments'))

    try:
        db.session.delete(payments)
        db.session.commit()

        flash('¡Método de pago eliminado con éxito!')
        return redirect(url_for('payments.get_payments'))

    except Exception as err:
        flash(f'Error al eliminar el método de pago: {str(err)}', category='error')
        return redirect(url_for('payments.get_payments'))