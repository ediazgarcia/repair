from apps import db
from .billing import Billing
from .products import Product

class BillingDetail(db.Model):
    _tablename_='billings_details'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    lot=db.Column(db.Integer, nullable=False)
    itbis = db.Column(db.Numeric(10, 2), nullable=False)
    discount = db.Column(db.Numeric(10, 2), nullable=False)
    sub_total = db.Column(db.Numeric(10, 2), nullable=False)
    total = db.Column(db.Numeric(10, 2), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id', onupdate='RESTRICT', ondelete='CASCADE'))
    product = db.relationship('Product', backref=db.backref('billings_details', lazy=True))
    billing_id= db.Column(db.Integer, db.ForeignKey('billings.id', onupdate='RESTRICT', ondelete='CASCADE'))
    billing= db.relationship('Billing', backref=db.backref('billings_details', lazy=True))

    def _init_(self,lot,itbis,discount,sub_total,total,product,billing):
        self.lot=lot
        self.itbis=itbis
        self.discount=discount
        self.sub_total=sub_total
        self.total=total
        self.product=product
        self.billing=billing

    def __repr__(self):
        return f'Payment: {self.lot} {self.product} {self.discount} {self.itbis} {self.sub_total} {self.total}'
