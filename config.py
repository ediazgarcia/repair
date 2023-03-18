from dotenv import load_dotenv
import os

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    DEBUG = os.getenv('FLASK_DEBUG') == 'development'
    TESTING = True

    # Configuración de base dedatos
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    SECRET_KEY = os.getenv('SECRET_KEY')

class ProductionConfig(Config):
    DEBUG = False


class DevelopmentConfig(Config):
    SECRET_KEY = os.getenv('SECRET_KEY')
    DEBUG = True
    TESTING = True
