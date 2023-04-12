from datetime import datetime
from apps import db
from .vehicle import Vehicle
from .employee import Employee


class VehicleReception(db.Model):
    __tablename__ = 'vehicle_receptions'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_num = db.Column(db.String(20), unique=True)
    reception_reason = db.Column(db.String(100), nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated = db.Column(db.DateTime, nullable=False,
                        default=datetime.utcnow, onupdate=datetime.utcnow)
    vehicle_id = db.Column(db.Integer, db.ForeignKey(
        'vehicles.id', onupdate='RESTRICT', ondelete='CASCADE'))
    employee_id = db.Column(db.Integer, db.ForeignKey(
        'employees.id', onupdate='RESTRICT', ondelete='CASCADE'))
    vehicle = db.relationship('Vehicle', backref=db.backref(
        'vehicle_receptions', lazy=True))
    employee = db.relationship(
        'Employee', backref=db.backref('vehicle_receptions', lazy=True))

    def __init__(self, order_num, reception_reason, vehicle, employee):
        self.order_num = order_num
        self.reception_reason = reception_reason
        self.vehicle = vehicle
        self.employee = employee

    def __repr__(self):
        return f'Orden {self.order_num} {self.reception_reason} del {self.vehicle}'
