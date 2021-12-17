from flask import request, make_response ,redirect, render_template, session, url_for, flash
import unittest
from app import create_app
from app.firestore_service import get_users, get_to_do_list, put_ToDo, delete_to_do, update_to_do
from flask_login import login_required, current_user
from app.forms import DeleteToDoForm, ToDoForm, UpdateToDoForm

app = create_app()

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
@app.route('/hello', methods = ['GET', 'POST'])
# Este decorador protege la ruta para que siempre sea necesario iniciar una sesion para acceder. 
@login_required
def Hello():
    # Modificamos la ruta hello para que obtenga la IP del ususario desde la cookie y no desde el request
    # user_ip =  request.cookies.get('user_ip')

    user_ip = session.get('user_ip')

    # Creamos una nueva instancia de la LoginForm y la enviamos al contexto
    #login_form = LoginForm()

    # obtenemos el username directamente de la sesion y lo agregamos al contexto
    username = current_user.id

    to_do_form = ToDoForm()
    delete_form = DeleteToDoForm()
    update_form = UpdateToDoForm()

    # Creamos un diccionario con las variables de contexto necesarias en el funcionamiento del template
    context = {
        'user_ip': user_ip,
        'to_do_list': get_to_do_list(user_id=username),
        'username' : username,
        'to_do_form': to_do_form,
        'delete_form': delete_form,
        'update_form': update_form,
    }
    # Si la figura de tarea es valida se guarda en firestore y en pantalla aparece un mensaje de comprobación
    if to_do_form.validate_on_submit():
        put_ToDo(user_id=username, description=to_do_form.description.data)
        flash('Task created successfully ')

        return redirect(url_for('hello'))

    # El doble '**' indica que el diccionario context será expandido para acceder a las keys:values, sin uso de la notacion .value
    return render_template('hello.html', **context)

# La ruta delete unicamente requiere el metodo post
@app.route('/to_do/delete/<to_do_id>', methods = ['POST'])
# La funcion delete recibe el id de la tarea
def delete(to_do_id):
    # EL id de l usuario lo obtenemos con el metodo curret_user
    user_id = current_user.id
    # importamos y ejecutamos la funcion que se va a encargar de borrar la tarea
    delete_to_do(user_id=user_id, to_do_id=to_do_id)
    # Finalemente redirigimos al inicio    
    return redirect(url_for('hello'))

@app.route('/to_do/update/<to_do_id>/<int:done>', methods = ['POST'])
def update(to_do_id, done):
    user_id = current_user.id
    update_to_do(user_id=user_id, to_do_id=to_do_id, done=done)
    return redirect(url_for('hello'))

