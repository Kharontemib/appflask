from flask import Blueprint

#print(f'nombre del blueprint de auth es {__name__}')

auth_bp = Blueprint('auth', __name__, template_folder='templates')

from . import routes