from datetime import datetime
from .provider import Provider
from .company import Company
from apps import db


class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.Text, nullable=False)
    type = db.Column(db.String(30), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    cost = db.Column(db.Numeric(10, 2), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated = db.Column(db.DateTime, nullable=False,
                        default=datetime.utcnow, onupdate=datetime.utcnow)
    supplier_id = db.Column(db.Integer, db.ForeignKey(
        'suppliers.id', onupdate='RESTRICT', ondelete='CASCADE'))
    company_id = db.Column(db.Integer, db.ForeignKey(
        'companies.id', onupdate='RESTRICT', ondelete='CASCADE'))

    supplier = db.relationship('Provider', backref=db.backref(
        'products', lazy=True))
    company = db.relationship('Company', backref=db.backref(
        'products', lazy=True))

    def __init__(self, description, type, category, cost, price, status, supplier, company):
        self.description = description
        self.type = type
        self.category = category
        self.cost = cost
        self.price = price
        self.status = status
        self.created = datetime.utcnow()
        self.updated = datetime.utcnow()
        self.supplier = supplier
        self.company = company

    def __repr__(self) -> str:
        return f'{self.description}'
