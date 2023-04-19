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

    @staticmethod
    def numero_orden_existe_en_bd(order_num):
        # Verificar si el número de orden ya existe en la base de datos
        order = VehicleReception.query.filter_by(order_num=order_num).first()
        if order:
            return True
        else:
            return False


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
