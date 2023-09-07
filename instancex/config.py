from config.default import *
from os.path import join

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + join(BASE_DIR, 'app\\app2.sqlite3')

#print(SQLALCHEMY_DATABASE_URI)