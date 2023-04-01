from flask import (
    render_template, Blueprint, flash, g, redirect, request, session, url_for
)


from apps.models.client import Customer
from apps.models.company import Company
from apps.models.user import User
from apps import db

client = Blueprint('client', __name__, url_prefix='/client')

# función para verificar el rol del usuario
def set_role():
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        g.role = session['role']


# asignar la función set_role a la función before_request
@client.before_request
def before_request():
    set_role()



# CRUDS Customer
# GetAllCustomer
@client.route("/list", methods=('GET', 'POST'))
def get_client():
    customers = Customer.query.all()
    # customer_data = []
    # for customer in customers:
    #     # fetch the company name from the database
    #     company = Company.query.filter_by(id=customer.company_id).first()
    #     company_name = company.trade_name if company else None
    #     customer_data.append({'customer': customer, 'company_name': company_name})
    return render_template('admin/directory/clients/list.html', customers=customers)

#create
@client.route('/create', methods=['GET', 'POST'])
def create_client():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        document_type = request.form['document_type']
        document_number = request.form['document_number']
        email = request.form['email']
        phone = request.form['phone']
        city = request.form['city']
        address = request.form['address']
        company_id = request.form['company_id']
        
        # fetch the company name from the database
        company = Company.query.filter_by(id=company_id).first()
        company_name = company.trade_name if company else None
        
    # create a new customer object
        new_customer = Customer(first_name=first_name, last_name=last_name, document_type=document_type,
                            document_number=document_number, email=email, phone=phone, city=city,
                            address=address, company_id=company_id)
        new_customer.company_name = company_name  # add the company name to the customer object

        # add the new customer to the database
        db.session.add(new_customer)
        db.session.commit()
        flash('¡Cliente añadido con éxito!')
        return redirect(url_for('client.get_client'))

    companies = Company.query.all()
    return render_template('admin/directory/clients/create.html', companies=companies)