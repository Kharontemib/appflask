from ..config.default import *
from os.path import join

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + join(BASE_DIR, 'app\\app_test2.sqlite3')