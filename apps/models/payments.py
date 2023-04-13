from datetime import datetime
from apps import db


class Payments(db.Model):
    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(20), nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, description, type):
        self.description = description
        self.type = type

    def __repr__(self):
        return f'Payment: {self.description}'


class PaymentsDetails(db.Model):
    __tablename__ = 'payments_details'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    received = db.Column(db.Numeric(10, 2), nullable=False)
    change = db.Column(db.Numeric(10, 2), nullable=False)
    total = db.Column(db.Numeric(10, 2), nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    payments_id = db.Column(db.Integer, db.ForeignKey(
        'payments.id', onupdate='restrict', ondelete='cascade'))
    payment = db.relationship(
        'Payments', backref=db.backref('payments_details', lazy=True))

    def __init__(self, received, change, total, payment):
        self.received = received
        self.change = change
        self.total = total
        self.payment = payment

    def __repr__(self):
        return f'Tipo de Pago {self.payment} Recibido {self.received} Cambio{self.change} Total{self.total}'
