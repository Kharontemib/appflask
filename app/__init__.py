import logging
from logging.handlers import SMTPHandler
from flask import Flask, render_template
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
import os

from app.common.filters import format_datetime

# Obtener el directorio base del proyecto
BASEDIR = os.path.abspath(os.path.dirname(__file__))

#Instaciar objecto Login para gestionar el acceso de los usuarios
login_manager = LoginManager()

# object Alchemy para gestionar la BBDD
db = SQLAlchemy()
migrate = Migrate()

# object flask_mail para enviar emails
mail = Mail()

def create_app(settings_module):

    print('Ejecutando con settings: {0}'.format(settings_module))

    app = Flask(__name__, instance_relative_config=True)  # True => directorio instance al mismo nivel que app

    # Cargar del py de configuracion (llega en settings_module) los valores de configuración
    app.config.from_object(settings_module)

    # Cargar resto de configuración de la carpete de instance (silent=True , no falla si no existe directorio)
    if app.config.get('TESTING', False):
        app.config.from_pyfile('config-testing.py', silent=True)
    else:
        app.config.from_pyfile('config.py', silent=True)

    # configurar logging
    configure_logging(app)

    app.logger.info(f'Cadena de conexion BD: {app.config["SQLALCHEMY_DATABASE_URI"]}')


    #clave para generar los tokens CSRF que lo hace automaticamente los forms FLASK-WTF
    #app.config['SECRET_KEY'] = 'En Un LUGAR de la mancha de cuyo nombr3 no qui3ro acordarme no hace mucho que vivia un hidalgo'
    #app.config['SECRET_KEY'] = '7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe'
    # URI de conexión para la BBDD
    #app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASEDIR, 'app.sqlite3')
    #app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False     #evitar generar una señal cada vez que se modifica un objeto ????

    login_manager.init_app(app)         #Iniciar el login para la app de flask
    db.init_app(app)                    #Iniciar sqlalchemy para la app de flask
    migrate.init_app(app, db)           # Se inicializa el objeto migrate
    mail.init_app(app)                  # Inicializar mail para la app de flask
    register_filters(app)               # Registro de los filtros JINJA2

    # personalizar pantalla a mostrar cuando no se esta autorizado
    login_manager.login_view = "auth.login"

    # Registrar los Blueprints
    from .auth import auth_bp
    app.register_blueprint(auth_bp)

    from .admin import admin_bp
    app.register_blueprint(admin_bp)

    from .public import public_bp
    app.register_blueprint(public_bp)

    #registrar los manejadores de error
    register_error_handlers(app)

    return app

# manejadores de errores
def register_error_handlers(app:Flask):
    
    @app.errorhandler(500)
    def base_error_handler(e):
        return render_template('500.html'), 500
    
    @app.errorhandler(404)
    def error_404_handler(e):
        return render_template('404.html'), 404
    
    @app.errorhandler(401)
    def error_401_handler(e):
        return render_template('401.html'), 401
    
    @app.errorhandler(ZeroDivisionError)
    def error_dividide_by_zero(e):
        return render_template('Zero.html'), 500
    

# configurador del logger
def configure_logging(app:Flask):
    
    print ('entro en configure_logging')
    #Eliminar los manejadores que existisen por defecto en el logging de la app Flask
    del app.logger.handlers[:]

    # Crear lista de logger (añadir logger x defecto) y de handlers
    loggers=[app.logger, 
             logging.getLogger('sqlalchemy.engine.Engine.x')    # añador el logger de alchemy se llama sqlalchemy
            ]
    handlers=[]

    # crear manejador para escribir en consola
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formateador())

    # nivel del log en función del entorno, para produccion <= INFO, resto <= DEBUG
    if app.config['APP_ENV'] == app.config['APP_ENV_PRODUCTION']:
        console_handler.setLevel(logging.INFO)
        # crear handler para enviar correos para errores
        mail_handler = SMTPHandler((app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                                   app.config['DONT_REPLY_FROM_EMAIL'],
                                   app.config['ADMINS'],
                                   '[Error][{}] La aplicación falló'.format(app.config['APP_ENV']),
                                   (app.config['MAIL_USERNAME'],
                                    app.config['MAIL_PASSWORD']),
                                   ())
        mail_handler.setLevel(logging.ERROR)
        mail_handler.setFormatter(mail_handler_formatter())
        handlers.append(mail_handler)
    else:
        console_handler.setLevel(logging.DEBUG)

    # añadir handler a la lista
    handlers.append(console_handler)

    # asociar cada uno de los handlers a los loggers
    for l in loggers:
        for h in handlers:
            l.addHandler(h)
        l.propagate = False  # si graba este log no se propaga al resto de loggers
        l.setLevel(logging.INFO)   # prevalece este nivel al del handler


# formateador del manejador de logging
def formateador():
    return logging.Formatter(
        '[%(asctime)s.%(msecs)d]\t %(levelname)s \t[%(name)s.%(funcName)s:%(lineno)d]\t %(message)s',
        datefmt='%d/%m/%Y %H:%M:%S')

def formateador2():
    return logging.Formatter(
        '[%(asctime)s.%(msecs)d]\t %(levelname)s ***** \t[%(name)s.%(funcName)s:%(lineno)d]\t %(message)s',
        datefmt='%d/%m/%Y %H:%M:%S')

# formateador para mensajes email
def mail_handler_formatter():
    return logging.Formatter(
        '''
            Message type:       %(levelname)s
            Location:           %(pathname)s:%(lineno)d
            Module:             %(module)s
            Function:           %(funcName)s
            Time:               %(asctime)s.%(msecs)d
            Message:
            %(message)s
        ''',
        datefmt='%d/%m/%Y %H:%M:%S'
    )

# Registro de filtros JINJA2  para formatear campos en los templates
def register_filters(app):

    #registrar formateo de fechas
    app.jinja_env.filters['datetime'] = format_datetime