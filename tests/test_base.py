# Importamos testcase 
from flask_testing import TestCase
# Importamos nuesra app desde el main de nuestra aplicacion
from main import app
from flask import current_app, url_for

# Creamos una nueva clase que se llama main test
class MainTest(TestCase):
    # Creamos el metodo create app que retorna una aplicacion de flask
    def create_app(self):
        # Configuramos nuestra app para testing de esta manera flask reconoce que se trata de un ambiente de pruebas
        app.config['TESTING'] = True
        # Indicamos que no vamos a utilizar el Cross-site request forgery toquen
        # porque en este caso no tenemos una sesión activa del usuario.
        app.config['WTF_CSRF_ENABLED'] = False
        return app

    # Probamos que de hecho nuestra app de Flash existe
    def test_app_exist(self):
        self.assertIsNotNone(current_app)

    # Validamos que nuestra app de flask se encuente en modo testing
    def test_app_in_test_mode(self):
        self.assertTrue(current_app.config['TESTING'])

    # Validamos que la redireccion del index sea correcta
    def test_index_redirect(self):
        response = self.client.get(url_for('index'))
        self.assertRedirects(response, url_for('Hello'))

    # Validamos que Hello nos regrese 200 en cuanto hacemos un get()
    def test_hello_get(self):
        response = self.client.get(url_for('Hello'))
        self.assert200(response)
    
    # Validamos como realizar un post de la manera correcta
    def test_hello_post(self):
        # En este caso es necesario crear una forma para los espacios del formulario
        fake_form = {
            'username': 'Fakeusername',
            'password': 'Fakepassword'
        }
        # Generamos un response donde en la funcion Hello posteamos los datos de la forma
        response = self.client.post(url_for('Hello', data=fake_form))
        # Y con assert validamos que al ingresar los datos correctos seamos redirigidos al index
        self.assertRedirects(response, url_for('index'))