import unittest

from app import create_app, db
from app.auth.models import User


class BaseTestClass(unittest.TestCase):

    def setUp(self) -> None:
        self.app = create_app(settings_module='config.testing')
        self.client = self.app.test_client()

        # Crear un contexto de aplicacion
        with self.app.app_context():
            #Crear las tablas de la BBDD
            db.create_all()
             # Creamos un usuario administrador
            BaseTestClass.create_user('admin', 'admin@xyz.com', '1111', True)
            # Creamos un usuario invitado
            BaseTestClass.create_user('guest', 'guest@xyz.com', '1111', False)

    def tearDown(self) -> None:
        #elimina toda las tablas de la base de datos
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    @staticmethod
    def create_user(name, email, password, is_admin):
        user = User(name=name, email=email)
        user.set_password(password)
        user.is_admin = is_admin
        user.save()
        return user
    
    def login(self, email, password):
        return self.client.post('/login', data=dict(
            email=email,
            password=password
        ), follow_redirects=True)