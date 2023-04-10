from datetime import datetime
from .company import Company
from apps import db


class Provider(db.Model):
    __tablename__ = 'suppliers'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    business_name = db.Column(db.String(50), nullable=False)
    trade_name = db.Column(db.String(50), nullable=False)
    document_type = db.Column(db.String(20), nullable=False)
    document_number = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    address = db.Column(db.Text)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated = db.Column(db.DateTime, nullable=False,
                        default=datetime.utcnow, onupdate=datetime.utcnow)
    company_id = db.Column(db.Integer, db.ForeignKey(
        'companies.id', onupdate='restrict', ondelete='cascade'))
    company = db.relationship(
        'Company', backref=db.backref('suppliers', lazy=True))

    def __init__(self, business_name, trade_name, document_type, document_number, email, phone, city, address, company):
        self.business_name = business_name
        self.trade_name = trade_name
        self.document_type = document_type
        self.document_number = document_number
        self.email = email
        self.phone = phone
        self.city = city
        self.address = address
        self.company = company

    def __repr__(self) -> str:
        return f'{self.trade_name}'
