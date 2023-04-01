from datetime import datetime
from apps import db

class Customer(db.Model):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    document_type = db.Column(db.String(20), nullable=False)
    document_number = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    phone = db.Column(db.String(12), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    address = db.Column(db.Text)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow,)
    updated = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id', onupdate='restrict', ondelete='cascade'))
    
    
    def __init__(self, first_name, last_name, document_type, document_number, email, phone, city, address, company_id):
        self.first_name = first_name
        self.last_name = last_name
        self.document_type = document_type
        self.document_number = document_number
        self.email = email
        self.phone = phone
        self.city = city
        self.address = address
        self.company_id = company_id
        self.created = datetime.utcnow()
        self.updated = datetime.utcnow()
    
    
    # define methods here
    def __repr__(self):
        return f'<Customer {self.first_name} {self.last_name}>'
