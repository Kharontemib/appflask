from flask import current_app, redirect, url_for,render_template,request
from flask_login import current_user, login_user, logout_user
from werkzeug.urls import url_parse

from app import login_manager
from app.common.mail import send_email
from . import auth_bp
from . forms import SignupForm, LoginForm
from . models import User



@auth_bp.route("/signup/", methods=["GET", "POST"])
def show_signup_form():
    
    if current_user.is_authenticated:
        return redirect(url_for('public.index'))
    
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

         # Enviar correo de bienvenida al nuevo usuario
         send_email(subject='Bienvenid@ al miniblog',
                       sender=current_app.config['DONT_REPLY_FROM_EMAIL'],
                       recipients=[email, ],
                       text_body=f'Hola {name}, bienvenid@ al miniblog de Flask',
                       html_body=f'<p>Hola <strong>{name}</strong>, bienvenid@ al miniblog de Flask</p>')
               
         # Dejamos al usuario logueado
         login_user(user, remember=True)
         next_page = request.args.get('next', None)
         if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('public.index')             
         return redirect(next_page)
    
    return render_template('auth/signup_form.html', form=form, error=error)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('public.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_email(form.email.data)
        if user is not None and user.check_password(form.password.data):
            print(f'valor de rember_me es:{form.remember_me.data}')
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('public.index')
            return redirect(next_page)
    return render_template('auth/login_form.html', form=form)

@auth_bp.route('/logout')
def logout():
   logout_user()
   return redirect(url_for('public.index'))


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