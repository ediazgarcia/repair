from datetime import datetime
from apps import db
from .company import Company
from .client import Customer
from .employee import Employee
from .orders_services import ServiceOrder


from .products import Product


class Billing(db.Model):
    __tablename__ = 'billings'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_num = db.Column(db.String(20), unique=True)
    total = db.Column(db.Numeric(10, 2), nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow,)
    company_id = db.Column(db.Integer, db.ForeignKey(
        'companies.id', onupdate='RESTRICT', ondelete='CASCADE'))
    company = db.relationship(
        'Company', backref=db.backref('billings', lazy=True))
    client_id = db.Column(db.Integer, db.ForeignKey(
        'customers.id', onupdate='RESTRICT', ondelete='CASCADE'))
    client = db.relationship(
        'Customer', backref=db.backref('billings', lazy=True))
    orders_services_id = db.Column(db.Integer, db.ForeignKey(
        'services_orders.id', onupdate='RESTRICT', ondelete='CASCADE'))
    orders_services = db.relationship(
        'ServiceOrder', backref=db.backref('billings', lazy=True))

    def __init__(self, order_num, total, company, client, orders_services):
        self.order_num = order_num
        self.total = total
        self.created = datetime.utcnow()
        self.company = company
        self.client = client
        self.orders_services = orders_services

    def __repr__(self):
        return f'Factura {self.order_num}'


class BillingDetail(db.Model):
    __tablename__ = 'billings_details'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    quantity = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(100), nullable=False)
    unit_price = db.Column(db.Float, nullable=False)
    total_price = db.Column(db.Numeric(10, 2), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey(
        'products.id', onupdate='RESTRICT', ondelete='CASCADE'))
    product = db.relationship(
        'Product', backref=db.backref('billings_details', lazy=True))
    billing_id = db.Column(db.Integer, db.ForeignKey(
        'billings.id'), nullable=False)
    billing = db.relationship(
        'Billing', backref=db.backref('billings_details', lazy=True))

    def __init__(self, unit_price, quantity, total_price, product, billing):
        self.unit_price = unit_price
        self.quantity = quantity
        self.total_price = total_price
        self.product = product
        self.billing = billing

    def __repr__(self):
        return f'Payment: {self.unit_price} {self.quantity}'
