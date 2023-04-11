from datetime import datetime
from .products import Product
from apps import db

class Inventory(db.Model):
    __tablename__ = 'inventories'

    id=db.Column(db.Integer,primary_key=True, autoincrement=True)
    min_stock=db.Column(db.Integer, nullable=False)
    set_stock=db.Column(db.Integer, nullable=False)
    type=db.Column(db.String(50), nullable=False)
    location=db.Column(db.String(100), nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id', onupdate='restrict', ondelete='cascade'))
    product = db.relationship('Product', backref=db.backref('inventories', lazy=True))

    def __init__(self, min_stock, set_stock ,type ,location ,product):
        self.min_stock=min_stock
        self.set_stock=set_stock
        self.type=type
        self.location=location
        self.created = datetime.utcnow()
        self.updated = datetime.utcnow()
        self.product=product