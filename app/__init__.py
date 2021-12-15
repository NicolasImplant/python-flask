from flask import Flask
from flask_bootstrap import Bootstrap

from .config import Config
from .auth import auth

def create_app():
    # Se crea una instancia de flask
    app = Flask(__name__)
    # Se instancia Bootstrap para implementarlo en la navigation bar
    bootstrap = Bootstrap(app)
    # Configuramos la llave secreta 
    app.config.from_object(Config)
    # Registramos el blueprint
    app.register_blueprint(auth)
    return app
