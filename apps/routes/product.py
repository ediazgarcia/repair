from .auth import set_role
from flask import (
    render_template, Blueprint, flash, g, redirect, request, session, url_for
)

from werkzeug.security import generate_password_hash
from werkzeug.exceptions import BadRequestKeyError

from apps.models.products import Product
from apps.models.provider import Provider
from apps.models.company import Company
from apps.models.user import User
from apps import db

product = Blueprint('product', __name__, url_prefix='/product')


# función para verificar el rol del usuario

@product.route("/list")
# función para verificar el rol del usuario
@set_role
def get_product(user=None):
    products = Product.query.all()
    provider = Provider.query.all()
    company = Company.query.all()
    if g.role == 'Administrador':
        return render_template('admin/products/product/list.html', products=products, provider=provider, company=company)
    else:
        return render_template('views/products/product/list.html', products=products, provider=provider, company=company)


@product.route("/create", methods=['GET', 'POST'])
@set_role
def create_product(user=None):

    if request.method == "POST":
        try:
            description = request.form['description']
            type = request.form['type']
            category = request.form['category']
            cost = request.form['cost']
            price = request.form['price']
            status = request.form['status']
            supplier_id = request.form['supplier_id']
            company_id = request.form['company_id']

            # fetch the provider name from the database
            provider = Provider.query.filter_by(id=supplier_id).first()

            # fetch the company name from the database
            company = Company.query.filter_by(id=company_id).first()

            new_product = Product(
                description, type, category, cost, price, status, provider, company)

            db.session.add(new_product)
            db.session.commit()
            flash('¡Producto añadido con éxito!')
            return redirect(url_for('product.get_product'))

        except BadRequestKeyError as err:
            flash(f'Error: {str(err)}', category='error')
            return redirect(url_for('product.create_product'))

    company = Company.query.all()
    providers = Provider.query.all()
    if g.role == 'Administrador':
        return render_template('admin/products/product/create.html', company=company, providers=providers)
    else:
        return render_template('views/products/product/create.html', company=company, providers=providers)


@product.route("/update/<int:id>", methods=["GET", "POST"])
@set_role
def update_product(id, user=None):
    product = Product.query.get_or_404(id)

    if request.method == "POST":
        description = request.form['description']
        type = request.form['type']
        category = request.form['category']
        cost = request.form['cost']
        price = request.form['price']
        status = request.form['status']

        product.description = description
        product.type = type
        product.category = category
        product.cost = cost
        product.price = price
        product.status = status

        db.session.commit()

        flash('¡Producto actualizado con éxito!')
        return redirect(url_for('product.get_product'))

    if g.role == 'Administrador':
        return render_template('admin/products/product/update.html', product=product)
    else:
        return render_template('views/products/product/update.html', product=product)


@product.route("/delete/<int:id>", methods=["GET"])
@set_role
def delete_product(id, user=None):
    product = Product.query.get(id)

    if not product:
        flash('Producto no encontrado', category='error')
        return redirect(url_for('product.get_product'))

    try:
        db.session.delete(product)
        db.session.commit()

        flash('¡Producto eliminado con éxito!')
        return redirect(url_for('product.get_product'))

    except Exception as err:
        flash(
            f'Error al eliminar el producto: {str(err)}', category='error')
        return redirect(url_for('product.get_product'))
