import logging
import os
from flask import abort, current_app, render_template, redirect, request, url_for
from flask_login import login_required, current_user
from app.auth.decorators import admin_requerido
from werkzeug.utils import secure_filename

from app.models import Post
from . import admin_bp
from .forms import PostForm

logger=logging.getLogger(__name__)

@admin_bp.route("/admin/post/", methods=['GET', 'POST'])
@login_required
@admin_requerido
def post_form():
   """ Crear nuevo post """
   form = PostForm()

   if form.validate_on_submit():
      title = form.title.data
      content = form.content.data
      image_name = None

      #comprobar si la petición viene con el fichero
      if 'post_image' in request.files:
         file = request.files['post_image']
         # Si no se eligió fichero esto estará vacio
         if file.filename:
            image_name = secure_filename(file.filename)   #generar un numero de fichero seguro 
            images_dir = current_app.config['POST_IMAGES_DIR']
            os.makedirs(images_dir, exist_ok=True)
            file_path = os.path.join(images_dir, image_name)
            file.save(file_path)

      post = Post(user_id=current_user.id, title=title, content=content)
      post.image_name = image_name
      post.save()
      logger.info(f'Guardando nuevo post {title}')
      return redirect(url_for('admin.list_posts'))
  
   return render_template('admin/post_form.html',form=form)

@admin_bp.route('/admin/post/<int:post_id>/', methods=['GET', 'POST'])
@login_required
@admin_requerido
def update_post_form(post_id : int):
   """Actualiza un post existente """
   
   post:Post = Post.get_by_id(post_id)
   if post is None:
      logger.info(f'El post {post_id} no existe')
      abort(404)

   # Crear un form y cargarlo con los valores recuperados del post 
   form = PostForm(obj=post)
   
   if form.validate_on_submit():
      # pasar datos del form al post existente y actualizar
      post.title = form.title.data
      post.content = form.content.data
      post.save()
      logger.info(f'Actualizado el post {post.id}-{post.title}')

      return redirect(url_for('admin.list_posts'))
   
   return render_template('admin/post_form.html',form=form, post=post)

@admin_bp.route('/admin')
@login_required
@admin_requerido
def list_posts():
   #posts = Post.get_all()

   page = int(request.args.get('page', 1))
   per_page = current_app.config['ITEMS_PER_PAGE']
   post_pagination = Post.all_paginated(page,per_page)

   return render_template("admin/posts.html",post_pagination=post_pagination)
   #return render_template('admin/posts.html', posts=posts)

@admin_bp.route('/admin/post/delete/<int:post_id>/', methods=['POST',])
@login_required
@admin_requerido
def delete_post(post_id : int):
   """Borrado de un post"""
   logger.info(f'Solicitud eliminar post {post_id}')

   post : Post = Post.get_by_id(post_id)
   if post is None:
      logger.info(f'El post {post_id} no existe')
      abort(404)
   
   post.delete()
   logger.info(f'El post {post_id} ha sido eliminado')
   return redirect(url_for('admin.list_posts'))
