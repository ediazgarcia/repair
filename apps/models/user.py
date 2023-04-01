from datetime import datetime
from apps import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fullname = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    role = db.Column(db.String(25), nullable=False)
    active = db.Column(db.Boolean, default=True)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow,)
    updated = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __init__(self, fullname, username, email, password, role, active) -> None:
        self.fullname = fullname
        self.username = username
        self.email = email
        self.password = password
        self.role = role
        self.active = active

    def __repr__(self) -> str:
        return f'User: {self.username}'
