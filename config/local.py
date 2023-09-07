from .default import *
from os.path import join

APP_ENV = APP_ENV_LOCAL

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + join(BASE_DIR, 'app\\app.sqlite3')

#print(SQLALCHEMY_DATABASE_URI)