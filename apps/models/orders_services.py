from datetime import datetime
from .vehicle_reception import VehicleReception
from .employee import Employee
from .products import Product
from apps import db


class ServiceOrder(db.Model):
    __tablename__ = 'services_orders'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.Text, nullable=False)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    status = db.Column(db.String(30), nullable=False)
    observations = db.Column(db.Text)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated = db.Column(db.DateTime, nullable=False,
                        default=datetime.utcnow, onupdate=datetime.utcnow)
    vehicle_reception_id = db.Column(db.Integer, db.ForeignKey(
        'vehicle_receptions.id', onupdate='RESTRICT', ondelete='CASCADE'))
    employee_id = db.Column(db.Integer, db.ForeignKey(
        'employees.id', onupdate='RESTRICT', ondelete='CASCADE'))

    product_id = db.Column(db.Integer, db.ForeignKey(
        'products.id', onupdate='RESTRICT', ondelete='CASCADE'))

    vehicle_reception = db.relationship(
        'VehicleReception',  backref=db.backref('services_orders', lazy=True))
    employee = db.relationship(
        'Employee', backref=db.backref('services_orders', lazy=True))
    product = db.relationship(
        'Product', backref=db.backref('services_orders', lazy=True))

    def __init__(self, description, start_date, end_date, status, observations, vehicle_reception, employee):
        self.description = description
        self.start_date = start_date
        self.end_date = end_date
        self.status = status
        self.observations = observations
        self.vehicle_reception = vehicle_reception
        self.employee = employee
