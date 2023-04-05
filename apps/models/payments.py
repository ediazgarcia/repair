from apps import db
from datetime import datetime

class Payments(db.Model):
    _tablename_='payments'

    id=db.Column(db.Integer, primary_key=True)
    description=db.Column(db.String(100),nullable=False)
    type=db.Column(db.String(20),nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow,)

    def _init_ (self,description,type):
        self.description=description
        self.type=type
        
    def __repr__(self):
        return f'Payment: {self.description}'