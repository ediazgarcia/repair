from flask import (
    render_template, Blueprint, flash, g, redirect, request, session, url_for
)

from apps.models.company import Company
from apps.models.user import User
from apps import db

company = Blueprint('company', __name__, url_prefix='/company')

# función para verificar el rol del usuario
@company.before_request
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

# GetAllCompanies
@company.route('/list', methods=('GET', 'POST'))
def get_company():
    companies = Company.query.all()
    return render_template('admin/settings/company/list.html', companies=companies)
    
    
# create
@company.route('/create', methods=('GET', 'POST'))
def create_company():
    if request.method == 'POST':
        try:
            # receive data from the form
            business_name = request.form['business_name']
            rnc_id = request.form['rnc_id']
            trade_name = request.form['trade_name']
            email = request.form['email']
            phone = request.form['phone']
            branch_name = request.form['branch_name']
            address = request.form['address']
            province = request.form['province']
            municipality = request.form['municipality']

            # validate form data
            # if not business_name or not rnc_id or not email:
            #     flash('Faltan campos obligatorios.')
            #     return redirect(url_for('company.create_company'))

            # create a new Company object
            new_company = Company(business_name, rnc_id, trade_name, email, phone, branch_name, address, province, municipality)

            # save the object into the database
            db.session.add(new_company)
            db.session.commit()

            flash('Empresa añadida con éxito!')
            return redirect(url_for('company.get_company'))
        
        except ValueError as err:
            flash(f'Error: {str(err)}', category='error')
        except Exception as err:
            flash(f'Error inesperado: {str(err)}', category='error')

    return render_template('admin/settings/company/create.html')


#update
@company.route("/update/<string:id>", methods=["GET", "POST"])
def update_company(id):
    # get company by Id
    company = Company.query.get(id)

    if not company:
        flash('Empresa no encontrada.')
        return redirect(url_for('company.get_company'))

    if request.method == "POST":
        try:
            # receive data from the form
            company.business_name = request.form['business_name']
            company.rnc_id = request.form['rnc_id']
            company.trade_name = request.form['trade_name']
            company.email = request.form['email']
            company.phone = request.form['phone']
            company.branch_name = request.form['branch_name']
            company.address = request.form['address']
            company.province = request.form['province']
            company.municipality = request.form['municipality']

            # validate form data
            if not company.business_name or not company.rnc_id or not company.email:
                flash('Faltan campos obligatorios.')
                return redirect(url_for('company.update_company', id=id))

            db.session.commit()

            flash('¡Empresa actualizada con éxito!')
            return redirect(url_for('company.get_company'))

        except Exception as e:
            flash('Ha ocurrido un error al actualizar la empresa. Por favor, inténtelo de nuevo.')
            return redirect(url_for('company.update_company', id=id))

    return render_template('admin/settings/company/update.html', company=company)




#delete
@company.route("/delete/<id>", methods=["GET"])
def delete_company(id):
    # get company by Id
    company = Company.query.get(id)

    if not company:
        flash('Empresa no encontrada.', category='error')
        return redirect(url_for('company.get_company'))

    try:
        db.session.delete(company)
        db.session.commit()

        flash('¡Empresa eliminada con éxito!')
        return redirect(url_for('company.get_company'))

    except Exception as e:
        flash(f'Error al eliminar la empresa: {str(e)}', category='error')
        return redirect(url_for('company.get_company'))
