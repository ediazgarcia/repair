from datetime import datetime
from .vehicle_reception import VehicleReception
from apps import db


class VehicleReceptionDetail(db.Model):
    __tablename__ = 'vehicle_reception_details'

    id = db.Column(
        db.Integer, primary_key=True, autoincrement=True)
    problem_description = db.Column(db.Text, nullable=False)
    front_condition = db.Column(db.String(100), nullable=False)
    back_condition = db.Column(db.String(100), nullable=False)
    left_condition = db.Column(db.String(100), nullable=False)
    right_condition = db.Column(db.String(100), nullable=False)
    roof_condition = db.Column(db.String(100), nullable=False)
    accessories = db.Column(db.String(100), nullable=False)
    tools = db.Column(db.String(100), nullable=False)
    objects = db.Column(db.String(100), nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated = db.Column(db.DateTime, nullable=False,
                        default=datetime.utcnow, onupdate=datetime.utcnow)
    vehicle_reception_id = db.Column(
        db.Integer, db.ForeignKey('vehicle_receptions.id'))

    # Constructor
    def __init__(self, problem_description, front_condition, back_condition, left_condition, right_condition, roof_condition, accessories, tools, objects, vehicle_reception_id):
        self.problem_description = problem_description
        self.front_condition = front_condition
        self.back_condition = back_condition
        self.left_condition = left_condition
        self.right_condition = right_condition
        self.roof_condition = roof_condition
        self.accessories = accessories
        self.tools = tools
        self.objects = objects
        self.created = datetime.utcnow()
        self.updated = datetime.utcnow()
        self.vehicle_reception_id = vehicle_reception_id
