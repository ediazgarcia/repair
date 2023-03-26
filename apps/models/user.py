from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from apps import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), nullable=False)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(10))
    active = db.Column(db.Boolean())
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow,)
    updated = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __init__(self, name, username, email, password_hash, role, active) -> None:
        self.name = name
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.role = role
        self.active = active

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)