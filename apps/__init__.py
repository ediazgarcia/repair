from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config, DevelopmentConfig, ProductionConfig

app = Flask(__name__)

# Cargar las configuraciones
app.config.from_object(DevelopmentConfig)
db = SQLAlchemy(app)

# Importar routes

from apps.routes.auth import auth
from apps.routes.dash import dash
from apps.routes.user import user
from apps.routes.company import company

app.register_blueprint(auth)
app.register_blueprint(dash)
app.register_blueprint(user)
app.register_blueprint(company)


app.add_url_rule("/", endpoint="index")

# Ejecutar todas las consultas SQL
with app.app_context():
    db.create_all()
