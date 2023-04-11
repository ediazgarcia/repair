from datetime import datetime
from .client import Customer
from apps import db


class Vehicle(db.Model):
    __tablename__ = 'vehicles'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    client_id = db.Column(db.Integer, db.ForeignKey(
        'customers.id', onupdate='restrict', ondelete='cascade'))
    client = db.relationship(
        'Customer', backref=db.backref('vehicles', lazy=True))
    brand = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    # Gasoline / Diesel / Electric / Gas/LPG / Hybrid
    fuel_type = db.Column(db.String(50), nullable=False)
    plate_number = db.Column(db.String(50), unique=True, nullable=False)
    chassis_number = db.Column(db.String(50), unique=True, nullable=False)
    color = db.Column(db.String(256), nullable=False)
    transmission = db.Column(db.String(50), nullable=False)
    cylinder = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(25), nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow,)
    updated = db.Column(db.DateTime, nullable=False,
                        default=datetime.utcnow, onupdate=datetime.utcnow)


    def __init__(self, client, brand, model, year, fuel_type, plate_number, chassis_number, color, transmission, cylinder, status):
        self.client = client
        self.brand = brand
        self.model = model
        self.year = year
        self.fuel_type = fuel_type
        self.plate_number = plate_number
        self.chassis_number = chassis_number
        self.color = color
        self.transmission = transmission
        self.cylinder = cylinder
        self.status = status

    def __repr__(self):
        return f'{self.brand} {self.model} {self.year} {self.plate_number}'
