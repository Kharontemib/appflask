
from .default import *
from os.path import join

# Parámetros para activar el modo debug
TESTING = True
DEBUG = True

APP_ENV = APP_ENV_TESTING

WTF_CSRF_ENABLED = False

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + join(BASE_DIR, 'app\\app_test.sqlite3')