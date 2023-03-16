from apps import db


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    def __init__(self, name) -> None:
        self.name = name

    def __repr__(self) -> str:
        return f'Role: {self.name}'
