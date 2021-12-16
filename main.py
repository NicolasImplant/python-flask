from flask import request, make_response ,redirect, render_template, session, url_for, flash
import unittest
from app import create_app
from app.firestore_service import get_users


app = create_app()

to_do = ['Add filter in coffee maker',
         'Grind coffee beans',
         'Pour enough water into the filter',
         'Let it drain into your cup or coffee pot']


# Generamos comandos del command line interface
@app.cli.command()
def test():
    # Los test van a ser todo el contenido del directorio test
    tests = unittest.TestLoader().discover('tests')
    # Ejecutamos todos los test que fueron encontrados
    run = unittest.TextTestRunner()
    run.run(tests)

# Se crean los metodos de error para manejar los errores de busqueda y de código
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', error=error)

@app.errorhandler(500)
def internal_server_error(error):
    return render_template('500.html', error=error)

@app.route('/')
# Establecemos el home de nuestra aplicación web
def index():
    # El metodo .remote_addr permite identificar la IP del ususario que ingresa en nuestra app
    user_ip = request.remote_addr
    # Importamos el metodo make_response para generar una respuesta y redirect con la ruta destino
    response = make_response(redirect('/hello'))
    # Finalmente con el metodo .set_cookie generamos una cookie para el IP del usuario cuyo nombre es el mismo user_ip
    # response.set_cookie('user_ip', user_ip)

    # Utilizamos el metodo sesion para porteger los datos del usuario
    session['user_ip'] = user_ip
    return response

# En los argumentos de la ruta agregamos una lista de metodos que va a aceptar, en este caso GET - POST
@app.route('/hello', methods = ['GET'])
def Hello():
    # Modificamos la ruta hello para que obtenga la IP del ususario desde la cookie y no desde el request
    # user_ip =  request.cookies.get('user_ip')

    user_ip = session.get('user_ip')

    # Creamos una nueva instancia de la LoginForm y la enviamos al contexto
    #login_form = LoginForm()

    # obtenemos el username directamente de la sesion y lo agregamos al contexto
    username = session.get('username')

    # Creamos un diccionario con las variables de contexto necesarias en el funcionamiento del template
    context = {
        'user_ip': user_ip,
        'to_do_list': to_do,
        'username' : username
    }
    # Importamos el metodo get users e imprimimos en consola su contenido con un ciclo for
    users = get_users()

    for user in users:
        print(user)

    # El doble '**' indica que el diccionario context será expandido para acceder a las keys:values, sin uso de la notacion .value
    return render_template('hello.html', **context)

