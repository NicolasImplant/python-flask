# Se debe importar la libreria firebase
import firebase_admin

# De firebase admin importamos credentials, y firestore, necesitamos crendencials para firmarnos
# con firestore 
from firebase_admin import credentials, firestore

project_id = 'flask-with-python-335223'
# Este es el metodo mediante el cual creamos nuestras credenciales
credential = credentials.ApplicationDefault()
# Firebase admin es la función que permite realizar el login con nuestra credencial
firebase_admin.initialize_app(credential, {
    'projectId': project_id
})
# Creamos una nueva instancia de firestore para comunicarnos con nuestra base de datos
db = firestore.client()

# Validamos que el servicio este funcionando de manera adecuada

# Este metodo trae consigo todas las colecciones de users de firestore
def get_users():
    # con el metodo .get() traemos la coleccion users de firestore
    return db.collection('users').get()

# Este metodo trae consigo al usuario que se identifique con el id que ingresamos como parametro
def get_user(user_id):
    # Es importante siempre finalizar con el metodo .get() dado que de otra manera solo realizará una referencia al objeto
    return db.collection('users').document(user_id).get()

# Este metodo trae consigo todos los To Do list de la coleccion de cada usuario
def get_to_do_list(user_id):
    # Manejamos la misma estructura de Firestore basada en colecciones documentos y colecciones.
    return db.collection('users').document(user_id).collection('To do').get()

# Este metodo no retorna nada en especifico, unicamente con los datos de usuario referencia el username en el documento users
def user_put(user_data):
    user_ref = db.collection('users').documents(user_data.username)
    # adicionalmente envia un diccionario con la contraseña para su sub colecion password
    user_ref.set({'password': user_data.password})