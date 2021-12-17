from flask import render_template, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user
from app.forms import LoginForm
from . import auth
from app.firestore_service import get_user
from app.models import UserData, UserModel

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
        password = login_form.password.data

        # Importamos el metodo get_user() y como parametro ingresamos el username del usuario
        user_doc = get_user(username)

        # En caso de que el ususario exista, es decir que no sea nula la informacion nos pedirá el password para realizar el login
        if user_doc.to_dict() is not None:
            password_from_db = user_doc.to_dict()['password']

            # Validamos que las dos contraseñas sean iguales y, si lo son, creamos Generamos una nueva instancia del modelo UserData
            if  password == password_from_db:
                user_data = UserData(username, password)
                # Finalmente la autenticacion sera realizada generando una nueva instancia del UserModel con los parametros de user data
                user = UserModel(user_data)

                # Realizamos el login del usuario
                login_user(user)

                # Flasheamos un mensaje para el login
                flash('Welcome Again')

                # Redirigimos al home de la aplicación
                redirect(url_for('hello'))
            
            # Contraseña incorrecta
            else:
                flash('Invalid password')
    # Usuario no encontrado
    else:
        flash('The user not found')

        # Realizamos una redireccion directo a index, debemos importar el url_for desde flask para usarlo en main
        # si nos realizan un post y la forma es valida vamos a guardar en username en la sesion
        return redirect(url_for('index'))

    return render_template('login.html', **context)

# funcion para salir de la aplicacion se encuentra en el endpoint /logout
@auth.route('logout')
@login_required
def logout():
    # Metodo de logout 
    logout_user()
    # Mensaje en pantalla
    flash('I hope to see you soon')    
    return redirect(url_for('auth.login'))