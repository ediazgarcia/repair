from datetime import datetime
from apps import db
from .inventory import Inventory
from .company import Company
from .client import Customer
from .orders_services import ServiceOrder
from .products import Product

# Definir el modelo de Factura


class Factura(db.Model):
    __tablename__ = 'factura'
    id = db.Column(db.Integer, primary_key=True)
    order_num = db.Column(db.String(20), unique=True)
    total = db.Column(db.Numeric(10, 2))
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow,)
    company_id = db.Column(db.Integer, db.ForeignKey(
        'companies.id', onupdate='RESTRICT', ondelete='CASCADE'))
    company = db.relationship(
        'Company', backref=db.backref('factura', lazy=True))
    client_id = db.Column(db.Integer, db.ForeignKey(
        'customers.id', onupdate='RESTRICT', ondelete='CASCADE'))
    client = db.relationship(
        'Customer', backref=db.backref('factura', lazy=True))
    orders_services_id = db.Column(db.Integer, db.ForeignKey(
        'services_orders.id', onupdate='RESTRICT', ondelete='CASCADE'))
    orders_services = db.relationship(
        'ServiceOrder', backref=db.backref('factura', lazy=True))
    payments_id = db.Column(db.Integer, db.ForeignKey(
        'payments.id', onupdate='RESTRICT', ondelete='CASCADE'))
    payments = db.relationship(
        'Payments', backref=db.backref('billings', lazy=True))
    detalles = db.relationship('DetalleFactura', backref='factura', lazy=True)

    def __init__(self, order_num, total, company, client, orders_services, payments):
        self.order_num = order_num
        self.total = total
        self.created = datetime.utcnow()
        self.company = company
        self.client = client
        self.orders_services = orders_services
        self.payments=payments
        
    def update_inventory(self):
        for detail in self.detalles:
            inventory = Inventory.query.filter_by(product_id=detail.product_id).first()
            if inventory:
                inventory.set_stock -= detail.cantidad
                db.session.commit()

    @staticmethod
    def numero_orden_existe_en_bd(order_num):
        # Verificar si el número de orden ya existe en la base de datos
        order = Factura.query.filter_by(order_num=order_num).first()
        if order:
            return True
        else:
            return False

# Definir el modelo de DetalleFactura


class DetalleFactura(db.Model):
    __tablename__ = 'factura_detalles'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey(
        'products.id'), nullable=False)
    product = db.relationship(
        'Product', backref=db.backref('factura_detalles', lazy=True))
    cantidad = db.Column(db.Integer, nullable=False)
    precio_unitario = db.Column(db.Float, nullable=False)
    precio_total = db.Column(db.Float, nullable=False)
    factura_id = db.Column(db.Integer, db.ForeignKey(
        'factura.id'), nullable=False)

    def __init__(self, factura_id, cantidad, precio_unitario, precio_total, producto_id):
        self.factura_id = factura_id
        self.product_id = producto_id
        self.cantidad = cantidad
        self.precio_unitario = precio_unitario
        self.precio_total = precio_total
