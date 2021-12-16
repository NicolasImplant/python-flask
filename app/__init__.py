from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager

from .config import Config
from .auth import auth
from .models import UserModel

# Inicializamos la clase Login Manager
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

# Este decorador hace que cada vez que flask-login quiera cargar el usuario sea la funcion query quien valide la información
@login_manager.user_loader
# Enviamos al modelo de usuario username que en este caso esta configurado como el id de usuario
def load_user(username):
    # El user name será el parametro de la funcion query declarada en el UserModel
    return UserModel.query(username)

def create_app():
    # Se crea una instancia de flask
    app = Flask(__name__)
    # Se instancia Bootstrap para implementarlo en la navigation bar
    bootstrap = Bootstrap(app)
    # Configuramos la llave secreta 
    app.config.from_object(Config)
    # Le pedimos a login manager que inicialize la aplicación y como parametro ingresamos la app
    login_manager.init_app(app)
    # Registramos el blueprint
    app.register_blueprint(auth)
    return app
