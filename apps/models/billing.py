from datetime import datetime
from apps import db
from .company import Company
from .employee import Employee
from .client import Customer
from .orders_services import ServiceOrder
from .payments import Payments

class Billing(db.Model):
    _tablename_='billings'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_num = db.Column(db.String(20), unique=True)
    type = db.Column(db.String(30), nullable=False)
    itbis = db.Column(db.Numeric(10, 2), nullable=False)
    discount = db.Column(db.Numeric(10, 2), nullable=False)
    sub_total = db.Column(db.Numeric(10, 2), nullable=False)
    total = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id', onupdate='RESTRICT', ondelete='CASCADE'))
    company = db.relationship('Company', backref=db.backref('billings', lazy=True))
    client_id= db.Column(db.Integer, db.ForeignKey('customers.id', onupdate='RESTRICT', ondelete='CASCADE'))
    client = db.relationship('Customer', backref=db.backref('billings', lazy=True))
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id', onupdate='RESTRICT', ondelete='CASCADE'))
    employee = db.relationship('Employee', backref=db.backref('billings', lazy=True))
    orders_services_id=db.Column(db.Integer, db.ForeignKey('services_orders.id', onupdate='RESTRICT', ondelete='CASCADE'))
    orders_services=db.relationship('ServiceOrder', backref=db.backref('billings', lazy=True))
    payments_id= db.Column(db.Integer, db.ForeignKey('payments.id', onupdate='RESTRICT', ondelete='CASCADE'))
    payments = db.relationship('Payments', backref=db.backref('billings', lazy=True))

    def _int_(self,order_num,type,itbis,discount,sub_total,total,status,company,client,employee,order_services,payments):
        self.order_num=order_num
        self.type=type
        self.itbis=itbis
        self.discount=discount
        self.sub_total=sub_total
        self.total=total
        self.status=status
        self.company=company
        self.client=client
        self.employee=employee
        self.orders_services=order_services
        self.payments=payments

    def __repr__(self):
        return f'Factura {self.order_num}'