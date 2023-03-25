from datetime import datetime
from apps import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role = db.Column(db.Boolean, nullable=False)
    name = db.Column(db.String(30), nullable=False)
    username = db.Column(db.String(25), nullable=False, unique=True)
    email = db.Column(db.String(30), nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    isActive = db.Column(db.Boolean, nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow,)
    updated = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __init__(self, role, name, username, email, password, isActive) -> None:
        self.role = role
        self.name = name
        self.username = username
        self.email = email
        self.password = password
        self.isActive = isActive

    def __repr__(self) -> str:
        return f'User: {self.username}'