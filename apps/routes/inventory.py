from .auth import set_role
from flask import (
    render_template, Blueprint, flash, g, redirect, request, session, url_for
)

from werkzeug.security import generate_password_hash
from werkzeug.exceptions import BadRequestKeyError

from apps.models.user import User
from apps.models.products import Product
from apps.models.inventory import Inventory
from apps import db

inventory = Blueprint('inventory', __name__, url_prefix='/inventory')


@inventory.route("/list")
# función para verificar el rol del usuario
@set_role
def get_inventory(user=None):
    inventory = Inventory.query.all()
    if g.role == 'Administrador':
        return render_template('admin/products/inventory/list.html', inventory=inventory)
    else:
        return render_template('views/products/inventory/list.html', inventory=inventory)

@inventory.route("/create", methods=['GET', 'POST'])
@set_role
def create_inventory(user=None):
    products = Product.query.filter(Product.type=='Producto').filter(Product.status=='Activo').all()

    if request.method == "POST":
            min_stock = request.form['min_stock']
            set_stock = request.form['set_stock']
            type = request.form['type']
            location = request.form['location']
            product_id = request.form['product_id']
            
            product = Product.query.filter_by(id=product_id).first()

            new_inventory=Inventory(min_stock=min_stock, set_stock=set_stock, type=type, location=location, product=product)

            db.session.add(new_inventory)
            db.session.commit()
            flash('¡Producto añadido al inventario con éxito!')
            return redirect(url_for('inventory.get_inventory'))
        
    if g.role == 'Administrador':
        return render_template('admin/products/inventory/create.html', products=products)
    else:
        return render_template('views/products/inventory/create.html', products=products)

@inventory.route("/update/<int:id>", methods=["GET", "POST"])
@set_role
def update_inventory(id, user=None):
     inventory=Inventory.query.get_or_404(id)

     if request.method == "POST":
            min_stock = request.form['min_stock']
            set_stock = request.form['set_stock']
            type = request.form['type']
            location = request.form['location']

            inventory.min_stock=min_stock
            inventory.set_stock=set_stock
            inventory.type=type
            inventory.location=location

            db.session.commit()

            flash('¡Producto en inventario actualizado con éxito!')
            return redirect(url_for('inventory.get_inventory'))
      
     return render_template('admin/products/inventory/update.html', inventory=inventory) 

@inventory.route("/delete/<int:id>", methods=["GET"])
@set_role
def delete_inventory(id, user=None):
    inventory = Inventory.query.get(id)

    if not inventory:
        flash('Producto no encontrado en inventario', category='error')
        return redirect(url_for('inventory.get_inventory'))

    try:
        db.session.delete(inventory)
        db.session.commit()

        flash('¡Producto eliminado con éxito del inventario!')
        return redirect(url_for('inventory.get_inventory'))

    except Exception as err:
        flash(
            f'Error al eliminar el producto de inventario: {str(err)}', category='error')
        return redirect(url_for('inventory.get_inventory'))