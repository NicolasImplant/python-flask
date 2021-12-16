# Desde flask_login importamos UserMixin que contiene los metodos necesarios para la implementacion del login
from flask_login import UserMixin
# Importamos el metodo get_user desde firestore service
from app.firestore_service import get_user
# User data es la clase que contendrá usuario y contraseña para realizar el login
class UserData:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        
# La clase UserModel heredará todos los metodos ya implementados en UserMixin y validará los datos que han sido ingresados al usuario
class UserModel(UserMixin):
    '''
    Param: user_data: UserData
    '''
    def __init__(self, user_data):
        self.id = user_data.username
        self.password = user_data.password

    # Implementamos el metodo get_user() declarado en firestore service a traves de un metodo estatico
    @staticmethod
    def query(user_id):
        # Traemos los datos de usuario con el metodo get_user() en una nueva variable
        user_doc = get_user(user_id)
        # En una nueva variable expandimos los datos del usuario, en este caso su ID y el password
        user_data = UserData(
            username=user_doc.id,
            password=user_doc.to_dict()['password']
        )
        # Finalemente retornamos una nueva instancia de la clase UserModel con la informacion de user_data
        return UserModel(user_data)
