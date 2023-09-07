"""
 Este fichero contiene la configuración común a todos los entornos, aunque
 después se puede sobre escribir en los otros ficheros

"""
from os.path import abspath, dirname, join

# Define the application directory
BASE_DIR = dirname(dirname(abspath(__file__)))

# definir donde se van a almacenar las imagenes en el server
MEDIA_DIR = join(BASE_DIR, 'media')
POST_IMAGES_DIR = join(MEDIA_DIR, 'posts')

#clave para generar los tokens CSRF que lo hace automaticamente los forms FLASK-WTF
SECRET_KEY = 'En Un LUGAR de la mancha de cuyo nombr3 no qui3ro acordarme no hace mucho que vivia un hidalgo'

# Database configuration
SQLALCHEMY_DATABASE_URI = ''
SQLALCHEMY_TRACK_MODIFICATIONS = False  #evitar generar una señal cada vez que se modifica un objeto ????

# App environments
APP_ENV_LOCAL = 'local'                 # desarrollo local por programador con SQLITE
APP_ENV_TESTING = 'testing'             # entorno de testing donde se activa el DEBUG
APP_ENV_DEVELOPMENT = 'development'     # común de desarrollo, donde probar en conjunto todos los cambios MYSQL
APP_ENV_STAGING = 'staging'
APP_ENV_PRODUCTION = 'production'
APP_ENV = ''

#print(BASE_DIR)
#print(SQLALCHEMY_DATABASE_URI)

# Configuración del email
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USERNAME = 'jmmjuradoborak@gmail.com'
MAIL_PASSWORD = 'qzobimdifbagxhfj x'
DONT_REPLY_FROM_EMAIL = 'jmmjuradoborak@gmail.com'
#ADMINS = ('juanjo@j2logo.com', )
MAIL_USE_TLS = True
MAIL_DEBUG = False

#configuracion propia paginacion
ITEMS_PER_PAGE = 3



