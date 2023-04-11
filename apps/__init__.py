from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from config import Config, DevelopmentConfig, ProductionConfig


app = Flask(__name__)

# Cargar las configuraciones
app.config.from_object(DevelopmentConfig)
db = SQLAlchemy(app)

# Importar routes
from apps.routes.auth import auth
from apps.routes.user import user
from apps.routes.company import company
from apps.routes.payments import payments
from apps.routes.client import client
from apps.routes.provider import provider
from apps.routes.employee import employee
from apps.routes.vehicle import vehicle
from apps.routes.product import product
from apps.routes.inventory import inventory
from apps.routes.vehicle_reception import vehicle_reception
from apps.routes.assigments import assigments
from apps.routes.billing import billing
from apps.routes.quotation import quotation
from apps.routes.shopping import shopping

app.register_blueprint(auth)
app.register_blueprint(user)
app.register_blueprint(company)
app.register_blueprint(payments)
app.register_blueprint(client)
app.register_blueprint(provider)
app.register_blueprint(employee)
app.register_blueprint(vehicle)
app.register_blueprint(product)
app.register_blueprint(inventory)
app.register_blueprint(vehicle_reception)
app.register_blueprint(assigments)
app.register_blueprint(billing)
app.register_blueprint(quotation)
app.register_blueprint(shopping)


# Importar modelos
from apps.models.user import User

# Crear todas las tablas en la base de datos
with app.app_context():
    try:
        db.create_all()
        print("Todas las tablas fueron creadas exitosamente")

        # Crear un usuario admin por defecto si no existe
        admin_username = 'admin'
        admin_password = 'admin123'
        admin_fullname = 'admin'
        admin_email = 'admin@gmail.com'
        admin_role = 'Administrador'
        admin = User.query.filter_by(username=admin_username).first()
        if not admin:
            admin_password_hash = generate_password_hash(admin_password)
            admin = User(username=admin_username, password=admin_password_hash, fullname=admin_fullname, email=admin_email, active=True, role=admin_role)
            db.session.add(admin)
            db.session.commit()
            print(f"El usuario admin '{admin_username}' ha sido creado con la contraseña '{admin_password}' y el rol '{admin_role}'")

        # Verificar que el usuario admin está en la base de datos
        users = User.query.all()
        print(f"Existen {len(users)} usuarios en la base de datos")

    except Exception as e:
        print(f"Error creando las tablas: {str(e)}")