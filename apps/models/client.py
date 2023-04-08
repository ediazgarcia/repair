# import phonenumbers
# import re
from datetime import datetime
from apps import db
from .company import Company
from sqlalchemy.orm import validates


class Customer(db.Model):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    document_type = db.Column(db.String(20), nullable=False)
    document_number = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    address = db.Column(db.Text)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow,)
    updated = db.Column(db.DateTime, nullable=False,
                        default=datetime.utcnow, onupdate=datetime.utcnow)
    company_id = db.Column(db.Integer, db.ForeignKey(
        'companies.id', onupdate='restrict', ondelete='cascade'))
    company = db.relationship(
        'Company', backref=db.backref('customers', lazy=True))

    def __init__(self, first_name, last_name, document_type, document_number, email, phone, city, address, company):
        self.first_name = first_name
        self.last_name = last_name
        self.document_type = document_type
        self.document_number = document_number
        self.email = email
        self.phone = phone
        self.city = city
        self.address = address
        self.company = company
        self.created = datetime.utcnow()
        self.updated = datetime.utcnow()

    # @validates('document_number')
    # def validate_document_number(self, key, value):
    #     if self.document_type == 'Cédula':
    #         # validar el formato de cédula
    #         if not re.match(r'^\d{3}-\d{7}-\d{1}$', value):
    #             raise ValueError('El número de cédula no tiene un formato válido')
    #     elif self.document_type == 'Pasaporte':
    #         # validar el formato de pasaporte
    #         if not re.match(r'^[A-Z]{2}\d{7}$', value):
    #             raise ValueError('El número de pasaporte no tiene un formato válido')
    #     else:
    #         raise ValueError('Tipo de documento no válido')

    #     return value

    # define methods here
    def __repr__(self):
        #Customer
        return f' {self.first_name} {self.last_name}'
