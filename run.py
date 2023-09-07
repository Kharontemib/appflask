from flask import Flask, abort, redirect, url_for,render_template,request
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
#from models import User
from werkzeug.urls import url_parse
from flask_sqlalchemy import SQLAlchemy
import os

from forms import LoginForm, PostForm, SignupForm

# Obtener el directorio base del proyecto
BASEDIR = os.path.abspath(os.path.dirname(__file__))


app = Flask(__name__)
#clave para generar los tokens CSRF que lo hace automaticamente los forms FLASK-WTF
app.config['SECRET_KEY'] = 'En Un LUGAR de la mancha de cuyo nombr3 no qui3ro acordarme no hace mucho que vivia un hidalgo'
#app.config['SECRET_KEY'] = '7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe'

#Instaciar objecto Login para gestionar el acceso de los usuarios
login_manager = LoginManager(app)

# personalizar pantalla a mostrar cuando no se esta autorizado
login_manager.login_view = "login"

# URI de conexión para la BBDD
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASEDIR, 'app.sqlite3')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False     #evitar generar una señal cada vez que se modifica un objeto ????


# object Alchemy para gestionar la BBDD
db = SQLAlchemy(app)

from models import User,Post         #se declara despues de DB porque sino daria error se arreglará con los Blueprint ???


# callback del login_manager, este solicita el usuario y le devolvemos el usuario o None
@login_manager.user_loader
def load_user(user_id):
   print('Llama a callback load_user con ID:{}'.format(user_id))

   return User.get_by_id(int(user_id))

   """
   for user in users:
      if user.id == int(user_id):
         return user
   return None
   """

@app.route('/')
def index():
   posts = Post.get_all()
   return render_template("index.html",posts=posts)

@app.route('/p/<string:slug>/')
def show_post(slug):
   
   post = Post.get_by_slug(slug)
   
   if post is None:
      abort(404)

   return render_template("post_view.html",post=post)

@app.route("/admin/post/", methods=['GET', 'POST'], defaults={'post_id': None})
@app.route('/admin/post/<int:post_id>/', methods=['GET', 'POST'])
@login_required
def post_form(post_id : int):

   form = PostForm()
      
   if form.validate_on_submit():
      title = form.title.data
      content = form.content.data

      post = Post(user_id=current_user.id, title=title, content=content)
      post.save()

      return redirect(url_for('index'))
   #print(url_for("post_form",post_id=12,juan='SI lo es',pedro=1))
   return render_template('admin/post_form.html',form=form)

@app.route("/signup/", methods=["GET", "POST"])
def show_signup_form():
    
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    # Con WTF, siempre se genera un nuevo objeto, si es un post
    # se inicializan los campos con lo que hay en la pagina web, si es GET en blancos
    form = SignupForm()     #Instanciar clase de flask-WTF que gestiona el form
    error = None
  
    if form.validate_on_submit():
      name = form.name.data
      email = form.email.data
      password = form.password.data

      # Comprobar si ya hay un usuario con igual email
      user = User.get_by_email(email)

      if user is not None:
         error = f'El email {email} ya está siendo utilizado por otro usuario'
      else:
         # Crear usuario en la BBDD
         user = User(name=name, email=email)
         user.set_password(password)
         user.save()
               
         # Dejamos al usuario logueado
         login_user(user, remember=True)
         next_page = request.args.get('next', None)
         if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')             
         return redirect(next_page)
    
    return render_template('signup_form.html', form=form, error=error)

    # Tratamiento para el GET -> mostrar la pantalla
    return render_template("signup_form.html", form=form)

    """  --- sin WTF
    # Tratamiento para el POST -> alta y volver x defecto a index sino se indica otra pagina
    if request.method=='POST':
       name = request.form['name']
       email = request.form['email']
       password = request.form['password']
       # redirección del post
       next = request.args.get('next', None)
       if next:
          return redirect(next)             #   volver a la pagina indicada en el parametro del path next
       return redirect(url_for('index'))    #   volver a index x defecto

    # Tratamiento para el GET -> mostrar la pantalla
    return render_template("signup_form.html")
    """
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_email(form.email.data)
        if user is not None and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('index')
            return redirect(next_page)
    return render_template('login_form.html', form=form)

@app.route('/logout')
def logout():
   logout_user()
   return redirect(url_for('index'))

if __name__ == '__main__':
   app.run()