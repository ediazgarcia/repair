from datetime import datetime
from .vehicle import Vehicle
from .employee import Employee
from apps import db


class VehicleReception(db.Model):
    __tablename__ = 'vehicle_receptions'

    id = db.Column(
        db.Integer, primary_key=True, autoincrement=True)
    reception_reason = db.Column(db.String(50), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow,)
    updated = db.Column(db.DateTime, nullable=False,
                        default=datetime.utcnow, onupdate=datetime.utcnow)
    vehicle_id = db.Column(db.Integer, db.ForeignKey(
        'vehicles.id', onupdate='RESTRICT', ondelete='CASCADE'))
    employee_id = db.Column(db.Integer, db.ForeignKey(
        'employees.id', onupdate='RESTRICT', ondelete='CASCADE'))

    vehicle = db.relationship('Vehicle', backref='vehicle_receptions')
    employee = db.relationship('Employee', backref='vehicle_receptions')

    def __init__(self, reception_reason, date, vehicle, employee):
        self.reception_reason = reception_reason
        self.date = date
        self.vehicle = vehicle
        self.employee = employee
