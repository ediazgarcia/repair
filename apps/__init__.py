from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config, DevelopmentConfig, ProductionConfig

app = Flask(__name__)

# Cargar las configuraciones
app.config.from_object(DevelopmentConfig)
db = SQLAlchemy(app)

# Importar routes

from apps.routes.dash import dash
from apps.routes.auth import auth

app.register_blueprint(auth)

app.register_blueprint(dash)

app.add_url_rule("/", endpoint="index")

# Ejecutar todas las consultas SQL
with app.app_context():
    db.create_all()
