from datetime import datetime
from apps import db

# define Empresa class that inherits


class Company(db.Model):
    __tablename__ = 'companies'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    business_name = db.Column(db.String(50), nullable=False)
    rnc_id = db.Column(db.String(20), unique=True, nullable=False)
    trade_name = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(30), unique=True, nullable=False)
    phone = db.Column(db.String(12), nullable=False)
    branch_name = db.Column(db.String(100))
    address = db.Column(db.Text, nullable=False)
    province = db.Column(db.String(50), nullable=False)
    municipality = db.Column(db.String(50), nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow,)
    updated = db.Column(db.DateTime, nullable=False,
                        default=datetime.utcnow, onupdate=datetime.utcnow)

    # define constructor

    def __init__(self, business_name, rnc_id, trade_name, email, phone, branch_name, address, province, municipality):
        self.business_name = business_name
        self.rnc_id = rnc_id
        self.trade_name = trade_name
        self.email = email
        self.phone = phone
        self.branch_name = branch_name
        self.address = address
        self.province = province
        self.municipality = municipality

    def __repr__(self) -> str:
        return f'Business_name: {self.business_name} y {self.rnc_id}'
