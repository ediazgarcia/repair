from flask import (
    render_template, Blueprint, abort, flash, g, redirect, request, session, url_for
)
import phonenumbers
from werkzeug.exceptions import BadRequestKeyError


from apps.models.client import Customer
from apps.models.company import Company
from apps.models.user import User
from apps import db

client = Blueprint('client', __name__, url_prefix='/client')

# función para verificar el rol del usuario
@client.before_request
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


# CRUDS Customer
# GetAllCustomer
@client.route("/list", methods=('GET', 'POST'))
def get_client():
    customers = Customer.query.all()
    return render_template('admin/directory/clients/list.html', customers=customers)



#create
@client.route('/create', methods=['GET', 'POST'])
def create_client():
    if request.method == 'POST':
        try:
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            document_type = request.form['document_type']
            document_number = request.form['document_number']

            # get the document type and validate the document number
            # if document_type == 'Cédula':
            #     if len(document_number) != 11 or not document_number.isdigit():
            #         flash('El número de cédula no es válido.')
            #         return redirect(url_for('client.create_client'))
            #     else:
            #         document_number = '-'.join([document_number[slice(0, 3)], document_number[slice(3, 10)], document_number[slice(10, 11)]])
            # elif document_type == 'Pasaporte':
            #     if len(document_number) < 6 or len(document_number) > 12:
            #         flash('El número de pasaporte no es válido.')
            #         return redirect(url_for('client.create_client'))

            email = request.form['email']
            phone = str(request.form['phone'])
            # format the phone number for Dominican Republic
            # try:
            #     parsed_number = phonenumbers.parse(phone, "DO")
            #     formatted_phone_number = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.NATIONAL)
            #     print("Formatted phone number:", formatted_phone_number)  # add this line for debugging
            # except phonenumbers.phonenumberutil.NumberParseException:
            #     formatted_phone_number = phone

            # if len(formatted_phone_number) == 10:
            #     flash('El número de teléfono debe tener exactamente 10 caracteres')
            #     return redirect(url_for('client.create_client'))

            city = request.form['city']
            address = request.form['address']
            company_id = request.form['company_id']

            # fetch the company name from the database
            company = Company.query.filter_by(id=company_id).first()
            company_name = company.trade_name if company else None

            # check if the email already exists in the database
            if Customer.query.filter_by(email=email).first() is not None:
                flash('Este correo electrónico ya está registrado.')
                return redirect(url_for('client.create_client'))
            
            # check if the document number already exists in the database
            if Customer.query.filter_by(document_number=document_number).first() is not None:
                flash('Este número de cédula ya está registrado.')
                return redirect(url_for('client.create_client'))

            # create a new customer object
            new_customer = Customer(first_name=first_name, last_name=last_name, document_type=document_type,
                                    document_number=document_number, email=email, phone=phone, city=city,
                                    address=address, company=company)
            new_customer.company_name = company_name  # add the company name to the customer object

            # add the new customer to the database
            db.session.add(new_customer)
            db.session.commit()
            flash('¡Cliente añadido con éxito!')
            return redirect(url_for('client.get_client'))

        except BadRequestKeyError as e:
            flash('Error en la solicitud revisa que no hay campos vacios: {}'.format(str(e)))
            return redirect(url_for('client.create_client'))

    companies = Company.query.all()
    return render_template('admin/directory/clients/create.html', companies=companies)


#update
@client.route('/update/<int:id>', methods=['GET', 'POST'])
def update_client(id):
    client = Customer.query.get_or_404(id)
    companies = Company.query.all()

    if request.method == 'POST':
        # obtener los valores actualizados del formulario
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        document_type = request.form['document_type']
        document_number = request.form['document_number']
        email = request.form['email']
        phone = str(request.form['phone'])
        city = request.form['city']
        address = request.form['address']
        company_id = request.form['company_id']


        # actualizar los atributos del cliente
        client.first_name = first_name
        client.last_name = last_name
        client.document_type = document_type
        client.document_number = document_number
        client.email = email
        client.phone = phone
        client.city = city
        client.address = address
        client.company_id = company_id

        db.session.commit()

        flash('¡Cliente actualizado con éxito!')
        return redirect(url_for('client.get_client'))

    # pasar el valor actual del tipo de documento al renderizado de la plantilla
    document_type_value = client.document_type

    return render_template('admin/directory/clients/update.html', client=client, companies=companies, document_type_value=document_type_value)




# Delete
@client.route("/delete/<id>", methods=["GET"])
def delete_client(id):
    customer = Customer.query.get(id)
    
    if not customer:
        flash('Cliente no encontrado', category='error')
        return redirect(url_for('client.get_client'))
    
    try:
        db.session.delete(customer)
        db.session.commit()

        flash('¡Cliente eliminado con éxito!')
        return redirect(url_for('client.get_client'))
    
    except Exception as err:
        flash(f'Error al eliminar el cliente: {str(err)}', category='error')
        return redirect(url_for('client.get_client'))


    