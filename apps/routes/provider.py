from .auth import set_role
from flask import (
    render_template, Blueprint, flash, g, redirect, request, session, url_for
)

from werkzeug.security import generate_password_hash
from werkzeug.exceptions import BadRequestKeyError

from apps.models.provider import Provider
from apps.models.user import User
from apps.models.company import Company
from apps import db

provider = Blueprint('provider', __name__, url_prefix='/provider')


@provider.route("/list")
# función para verificar el rol del usuario
@set_role
def get_provider(user=None):
    providers = Provider.query.all()
    if g.role == 'Administrador':
        return render_template('admin/directory/providers/list.html', providers=providers)
    else:
        return render_template('views/directory/providers/list.html', providers=providers)


@provider.route("/create", methods=['GET', 'POST'])
@set_role
def create_provider(user=None):

    if request.method == 'POST':
        try:
            business_name = request.form['business_name']
            trade_name = request.form['trade_name']
            document_type = request.form['document_type']
            document_number = request.form['document_number']
            email = request.form['email']
            phone = str(request.form['phone'])
            city = request.form['city']
            address = request.form['address']
            company_id = request.form['company_id']

            # fetch the company name from the database
            company = Company.query.filter_by(id=company_id).first()
            company_name = company.trade_name if company else None

            # check if the email already exists in the database
            if Provider.query.filter_by(email=email).first() is not None:
                flash('Este correo electrónico ya está registrado.')
                return redirect(url_for('provider.create_provider'))

            # check if the document number already exists in the database
            if Provider.query.filter_by(document_number=document_number).first() is not None:
                flash('Este número de cédula ya está registrado.')
                return redirect(url_for('provider.create_provider'))

            # create a new customer object
            new_provider = Provider(business_name=business_name, trade_name=trade_name, document_type=document_type,
                                    document_number=document_number, email=email, phone=phone, city=city,
                                    address=address, company=company)
            # add the company name to the customer object
            new_provider.company_name = company_name

            # add the new customer to the database
            db.session.add(new_provider)
            db.session.commit()
            flash('¡Proveedor añadido con éxito!')
            return redirect(url_for('provider.get_provider'))

        except BadRequestKeyError as e:
            flash(
                'Error en la solicitud revisa que no hay campos vacios: {}'.format(str(e)))
            return redirect(url_for('provider.create_provider'))

    companies = Company.query.all()

    if g.role == 'Administrador':
        return render_template('admin/directory/providers/create.html', companies=companies)
    else:
        return render_template('admin/directory/providers/create.html', companies=companies)


# update
@provider.route('/update/<int:id>', methods=['GET', 'POST'])
@set_role
def update_provider(id, user=None):
    provider = Provider.query.get_or_404(id)
    companies = Company.query.all()

    if request.method == 'POST':
        # obtener los valores actualizados del formulario
        business_name = request.form['business_name']
        trade_name = request.form['trade_name']
        document_type = request.form['document_type']
        document_number = request.form['document_number']
        email = request.form['email']
        phone = str(request.form['phone'])
        city = request.form['city']
        address = request.form['address']
        company_id = request.form['company_id']

        # actualizar los atributos del cliente
        provider.business_name = business_name
        provider.trade_name = trade_name
        provider.document_type = document_type
        provider.document_number = document_number
        provider.email = email
        provider.phone = phone
        provider.city = city
        provider.address = address
        provider.company_id = company_id

        db.session.commit()

        flash('¡Proveedor actualizado con éxito!')
        return redirect(url_for('provider.get_provider'))

    # pasar el valor actual del tipo de documento al renderizado de la plantilla
    document_type_value = provider.document_type

    if g.role == 'Administrador':
        return render_template('admin/directory/providers/update.html', provider=provider, companies=companies, document_type_value=document_type_value)
    else:
        return render_template('views/directory/providers/update.html', provider=provider, companies=companies, document_type_value=document_type_value)


# Delete
@provider.route("/delete/<id>", methods=["GET"])
@set_role
def delete_provider(id, user=None):
    provider = Provider.query.get(id)

    if not provider:
        flash('Proveedor no encontrado', category='error')
        return redirect(url_for('provider.get_provider'))

    try:
        db.session.delete(provider)
        db.session.commit()

        flash('Proveedor eliminado con éxito!')
        return redirect(url_for('provider.get_provider'))

    except Exception as err:
        flash(f'Error al eliminar el Proveedor: {str(err)}', category='error')
        return redirect(url_for('provider.get_provider'))
