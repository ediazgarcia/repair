from datetime import datetime
from apps import db
from .company import Company
from .provider import Provider
from .products import Product

class Shopping(db.Model):
    __tablename__ = 'shoppings'
    id = db.Column(db.Integer, primary_key=True)
    order_num = db.Column(db.String(20), unique=True)
    total = db.Column(db.Numeric(10, 2))
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow,)
    company_id = db.Column(db.Integer, db.ForeignKey(
        'companies.id', onupdate='RESTRICT', ondelete='CASCADE'))
    company = db.relationship(
        'Company', backref=db.backref('shoppings', lazy=True))
    provider_id= db.Column(db.Integer, db.ForeignKey(
        'suppliers.id', onupdate='RESTRICT', ondelete='CASCADE'))
    provider= db.relationship(
        'Provider', backref=db.backref('shoppings', lazy=True))
    details = db.relationship('ShoppingDetail', backref='shoppings', lazy=True)

    def __init__(self, order_num, total, company, provider):
        self.order_num = order_num
        self.total = total
        self.created = datetime.utcnow()
        self.company = company
        self.provider = provider

class ShoppingDetail(db.Model):
    __tablename__ = 'shoppings_details'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey(
        'products.id'), nullable=False)
    product = db.relationship('Product', backref=db.backref('shoppings_details', lazy=True))
    quantity = db.Column(db.Integer, nullable=False)
    unt_cost = db.Column(db.Float, nullable=False)
    total_cost = db.Column(db.Float, nullable=False)
    shopping_id = db.Column(db.Integer, db.ForeignKey(
        'shoppings.id'), nullable=False)

    def __init__(self, shopping_id, quantity, unt_cost, total_cost , product_id):
        self.shopping_id = shopping_id
        self.product_id=product_id
        self.quantity = quantity
        self.unt_cost = unt_cost
        self.total_cost=total_cost