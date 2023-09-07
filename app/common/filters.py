from datetime import datetime

# formatear fecha para todas las plantillas
def format_datetime(value, format='short'):
    value_str = ''

    if isinstance(value, datetime):
        if format == 'short':
            value_str = value.strftime('%d/%m/%Y')
        elif format == 'full':
            value_str = value.strftime('%d de %m de %Y')

    return value_str
    """
    value_str = None
    if not value:
        value_str = ''
    if format == 'short':
        value_str = value.strftime('%d/%m/%Y')
    elif format == 'full':
        value_str = value.strftime('%d de %m de %Y')
    else:
        value_str = ''
    return value_str
    """