from flask import (
    render_template, Blueprint, flash, g, redirect, request, session, url_for
)

from werkzeug.security import generate_password_hash

#from apps.models.shopping import shopping
from apps.models.user import User
from apps import db
from .auth import set_role
from apps.models.company import Company
from apps.models.shopping import Shopping, ShoppingDetail
from apps.models.provider import Provider
from apps.models.products import Product
from apps.models.inventory import Inventory

shopping = Blueprint('shopping', __name__, url_prefix='/shopping')

@shopping.route("/list")
# función para verificar el rol del usuario
@set_role
def get_shopping(user=None):
    shopping=Shopping.query.all()
    if g.role == 'Administrador':
        return render_template('admin/workshop/shopping/list.html',shopping=shopping)
    else:
        return render_template('views/workshop/shopping/list.html',shopping=shopping)


@shopping.route("/create", methods=['GET', 'POST'])
@set_role
def create_shopping(user=None):
    if request.method == 'POST':
        company_id = request.form['company_id']
        provider_id = request.form['provider_id']
        #order_num = "FT-" + str(next(order_num_counter))
        company = Company.query.filter_by(id=company_id).first()
        provider = Provider.query.filter_by(id=provider_id).first()
        # Obtener una lista de los valores del campo "detalle"
        detalles = request.form.getlist('detalle')
        # Obtener una lista de los valores del campo "cantidad"
        cantidades = request.form.getlist('cantidad')
        # Obtener una lista de los valores del campo "precio_unitario"
        precios_unitarios = request.form.getlist('precio_unitario')
        # Obtener una lista de los valores del campo "subtotal"
        precios_totales = request.form.getlist('subtotal')
        subtotal = []
        for num in precios_totales:
            try:
                subtotal.append(float(num))
            except ValueError:
                pass
        total = sum(subtotal)
        
        new_shopping = Shopping(total=total,order_num=None,company=company, provider=provider)

        db.session.add(new_shopping)
        db.session.commit()
        # Procesar los detalles de la factura
        for i in range(len(detalles)):
            shopping_id = new_shopping.id
            product_id = detalles[i]
            quantity = cantidades[i]
            #cantidad_inv = int(cantidades[i])
            unt_cost = precios_unitarios[i]
            total_cost = precios_totales[i] 

            new_detail = ShoppingDetail(
                shopping_id=shopping_id, product_id=product_id, quantity=quantity, unt_cost=unt_cost, total_cost=total_cost)

            db.session.add(new_detail)
        db.session.commit()  # Commit después de agregar todos los detalles

        flash('Compra creada exitosamente')
        return redirect(url_for('shopping.ready_shopping'))
    companies = Company.query.all()
    provider= Provider.query.all()
    product = db.session.query(Product).join(Inventory).filter(
        Inventory.set_stock > 0).all()
    return render_template('admin/workshop/shopping/create.html',companies=companies,product=product,provider=provider)

@shopping.route("/done")
# función para verificar el rol del usuario
@set_role
def ready_shopping(user=None):

    if g.role == 'Administrador':
        return render_template('admin/workshop/shopping/done.html')
    else:
        return render_template('views/workshop/shopping/done.html')