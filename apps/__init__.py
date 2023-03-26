from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config, DevelopmentConfig, ProductionConfig


# inicializar la aplicación Flask
app = Flask(__name__)

# Cargar las configuraciones
app.config.from_object(DevelopmentConfig)


# inicializar la base de datos
db = SQLAlchemy(app)

# inicializar el gestor de inicio de sesión


# importar las vistas y los modelos de datos
from apps.routes.auth import auth
from apps.routes.dash import dash
from apps.routes.user import user

app.register_blueprint(auth)
app.register_blueprint(dash)
app.register_blueprint(user)

app.add_url_rule("/", endpoint="index")

# Ejecutar todas las consultas SQL
with app.app_context():
    db.create_all()
