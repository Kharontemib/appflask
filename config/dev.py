import urllib
from .default import *

APP_ENV = APP_ENV_DEVELOPMENT

DATA_PASS = 'p@ssw0rd1'

DATA_PASS_BUENA = urllib.parse.quote_plus(DATA_PASS)

print(DATA_PASS_BUENA)

SQLALCHEMY_DATABASE_URI = 'mysql://root:p%40ssw0rd1@localhost/mysql'

SECRET_KEY = '7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fea'