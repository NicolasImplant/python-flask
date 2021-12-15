from flask import Flask, request, make_response ,redirect, render_template, session, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

# Se crea una instancia de flask
app = Flask(__name__)
# Se instancia Bootstrap para implementarlo en la navigation bar
bootstrap = Bootstrap(app)
# Utilizamos una propiedad de app para generar sesions, de esta manera es posible proteger la información de usuario
app.config['SECRET_KEY'] = 'TOP SECRET'


to_do = ['Add filter at coffee maker',
         'Grind coffee beans',
         'Pour enough water into the filter',
         'Let it drain into your cup or coffee pot']

# Se crea la clase para realizar el formulario login, en este caso se pide al ususario y contraseña, el parametro validators
# genera el caracter oblifatorio de los parametros ingresados a traves de crear instancias de DataRequired
class LoginForm(FlaskForm):
    username = StringField('Username:', validators=[DataRequired()])
    password = PasswordField('Password:', validators=[DataRequired()])
    submit = SubmitField('Submit')


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
def Hello():
    # Modificamos la ruta hello para que obtenga la IP del ususario desde la cookie y no desde el request
    # user_ip =  request.cookies.get('user_ip')

    user_ip = session.get('user_ip')

    # Creamos una nueva instancia de la LoginForm y la enviamos al contexto
    login_form = LoginForm()

    # obtenemos el username directamente de la sesion y lo agregamos al contexto
    username = session.get('username')

    # Creamos un diccionario con las variables de contexto necesarias en el funcionamiento del template
    context = {
        'user_ip': user_ip,
        'to_do_list': to_do,
        'login_form': login_form,
        'username' : username
    }

    # Agregamos el username en la sesion, utilizamos el metodo .validate_on_submit, que detecta cuando realizamos un post
    # y validamos la forma

    if login_form.validate_on_submit():
        username = login_form.username.data
        # Guardamos el user name en la sesion como lo hicimos para user_ip
        session['username'] = username

        # Realizamos una redireccion directo a index, debemos importar el url_for desde flask para usarlo en main
        # si nos realizan un post y la forma es valida vamos a guardar en username en la sesion
        return redirect(url_for('index'))

    # El doble '**' indica que el diccionario context será expandido para acceder a las keys:values, sin uso de la notacion .value
    return render_template('hello.html', **context)

