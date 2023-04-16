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
