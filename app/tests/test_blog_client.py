from app.auth.models import User
from app.models import Post
from . import BaseTestClass

class BlogClientTestCase(BaseTestClass):

    def test_index_with_no_post(self):
        res = self.client.get('/')
        self.assertEqual(200, res.status_code,msg='No funciona la página principal')
        self.assertIn(b'No hay entradas', res.data)

    def test_index_with_posts(self):
        with self.app.app_context():
            admin = User.get_by_email('admin@xyz.com')
            post = Post(user_id=admin.id, title="Post de prueba", content='Lorem Ipsum')
            post.save()

            res = self.client.get('/')
            self.assertEqual(200, res.status_code, msg='No encontrado Posts en index')
            self.assertNotIn(b'No hay entradas', res.data)

    def test_redirect_to_login(self):
        res = self.client.get('/admin')
        self.assertEqual(302, res.status_code,msg='No se ha redireccionado a login')
        self.assertIn('login', res.location)

    def test_unautorized_access_to_admin(self):
        self.login('guest@xyz.com', '1111')
        res=self.client.get('/admin')
        self.assertEqual(401, res.status_code,msg='Usuario no debería estar autorizado')
        self.assertIn(b'Ooops!! No tienes autorizaci\xc3\xb3n de administrador para hacer esta operaci\xc3\xb3n', res.data)

    def test_autorized_access_to_admin(self):
        self.login('admin@xyz.com', '1111')
        res=self.client.get('/admin')
        self.assertEqual(200, res.status_code,msg='Usuario debería estar autorizado')
        self.assertIn(b'Listado', res.data)
        #self.assertIn(b'Usuarios', res.data)
