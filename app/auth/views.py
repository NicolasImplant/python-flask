from flask import render_template, session, flash, redirect, url_for
from app.forms import LoginForm
from . import auth

@auth.route('/login', methods = ['GET', 'POST'])
def login():
    login_form = LoginForm()
    context = {
        'login_form': login_form
    }

    # Agregamos el username en la sesion, utilizamos el metodo .validate_on_submit, que detecta cuando realizamos un post
    # y validamos la forma

    if login_form.validate_on_submit():
        username = login_form.username.data
        # Guardamos el user name en la sesion como lo hicimos para user_ip
        session['username'] = username
        flash('Username register with successful')

        # Realizamos una redireccion directo a index, debemos importar el url_for desde flask para usarlo en main
        # si nos realizan un post y la forma es valida vamos a guardar en username en la sesion
        return redirect(url_for('index'))

    return render_template('login.html', **context)