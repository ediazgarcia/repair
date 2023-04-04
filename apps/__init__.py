from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config, DevelopmentConfig, ProductionConfig


app = Flask(__name__)


# Cargar las configuraciones
app.config.from_object(DevelopmentConfig)
db = SQLAlchemy(app)

# Importar routes

from apps.routes.auth import auth
from apps.routes.user import user
from apps.routes.company import company
from apps.routes.client import client
from apps.routes.provider import provider
from apps.routes.employee import employee
from apps.routes.vehicle import vehicle
from apps.routes.product import product
from apps.routes.inventory import inventory

app.register_blueprint(auth)
app.register_blueprint(user)
app.register_blueprint(company)
app.register_blueprint(client)
app.register_blueprint(provider)
app.register_blueprint(employee)
app.register_blueprint(vehicle)
app.register_blueprint(product)
app.register_blueprint(inventory)

# app.add_url_rule("/", endpoint="index")

# Crear todas las tablas en la base de datos
with app.app_context():
    try:
        db.create_all()
        print("Todas las tablas fueron creadas exitosamente")
    except Exception as e:
        print(f"Error creando las tablas: {str(e)}")