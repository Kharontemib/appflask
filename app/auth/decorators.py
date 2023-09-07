from functools import wraps
import logging
from flask import abort
from flask_login import current_user

logger = logging.getLogger(__name__)

def admin_requerido(f):
    @wraps(f)
    def funcion_decorada(*args, **kws):
        is_admin = getattr(current_user, 'is_admin', False)
        name = getattr(current_user, 'name', 'NO LOGIN')
        logger.info(f'Usuario {name} valor admin {is_admin}')
        if not is_admin:
            abort(401)
        return f(*args, **kws)
    return funcion_decorada