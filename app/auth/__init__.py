from flask import Blueprint

# El prefijo 'url_prefix' indica que todas las rutas que empiecen con /auth serán ruteadas o dirigidas a este Blueprint
auth = Blueprint('auth', __name__, url_prefix='/auth' )

# Se importa despues de declarar auth para que primero cree los blueprints de la aplicacion

from . import views