from datetime import datetime
from .company import Company
from .user import User
from apps import db


class Employee(db.Model):
    __tablename__ = 'employees'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(30), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    document_type = db.Column(db.String(20), nullable=False)
    document_number = db.Column(db.String(20), unique=True, nullable=False)
    birth_date = db.Column(db.Date)
    gender = db.Column(db.String(20), nullable=False)
    salary = db.Column(db.Float, nullable=False)
    address = db.Column(db.Text)
    city = db.Column(db.String(30), nullable=False)
    state = db.Column(db.String(25))  # Contractor/Fixed
    position = db.Column(db.String(50), nullable=False)
    work_day = db.Column(db.String(30), nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    hire_date = db.Column(db.Date, nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated = db.Column(db.DateTime, nullable=False,
                        default=datetime.utcnow, onupdate=datetime.utcnow)
    company_id = db.Column(db.Integer, db.ForeignKey(
        'companies.id', onupdate='restrict', ondelete='cascade'))
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.id', onupdate='restrict', ondelete='cascade'))

    company = db.relationship(
        'Company', backref=db.backref('employees', lazy=True))
    user = db.relationship('User', backref=db.backref('employees', lazy=True))

    def __init__(self, first_name, last_name, email, phone, document_type, document_number, birth_date, gender,
                 salary, address, city, state, position, work_day, start_time, end_time, hire_date, company, user):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.document_type = document_type
        self.document_number = document_number
        self.birth_date = birth_date
        self.gender = gender
        self.salary = salary
        self.address = address
        self.city = city
        self.state = state
        self.position = position
        self.work_day = work_day
        self.start_time = start_time
        self.end_time = end_time
        self.hire_date = hire_date
        self.created = datetime.utcnow()
        self.updated = datetime.utcnow()
        self.company = company
        self.user = user
    
        def __repr__(self):
        #Employee
            return f' {self.first_name} {self.last_name}'
