from datetime import datetime
from apps import db
from .payments import Payments

class PaymentsDetails(db.Model):
    _tablename_ = 'payments_details'

    id = db.Column(db.Integer, primary_key=True)
    received = db.Column(db.Numeric(10, 2), nullable=False)
    change = db.Column(db.Numeric(10, 2), nullable=False)
    total = db.Column(db.Numeric(10, 2), nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    payment_id=db.Column(db.Integer, db.ForeignKey('payments.id', onupdate='RESTRICT', ondelete='CASCADE'))
    payment=db.relationship('Payments', backref=db.backref('payments_details', lazy=True))

    
    def _init_(self,received,change,total,payment):
        self.received=received
        self.change=change
        self.total=total
        self.payment=payment

    def __repr__(self):
        return f'Tipo de Pago {self.payment} Recibido {self.received} Cambio{self.change} Total{self.total}'