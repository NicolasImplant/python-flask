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


# Este metodo no retorna nada en especifico, unicamente con los datos de usuario referencia el username en el documento users
def user_put(user_data):
    user_ref = db.collection('users').documents(user_data.username)
    # adicionalmente envia un diccionario con la contraseña para su sub colecion password
    user_ref.set({'password': user_data.password})

# Este metodo trae consigo todos los To Do list de la coleccion de cada usuario
def get_to_do_list(user_id):
    # Manejamos la misma estructura de Firestore basada en colecciones documentos y colecciones.
    return db.collection('users').document(user_id).collection('To do').get()

# Este metodo permite enviar una nueva tarea a firesote services
def put_ToDo(user_id, description):
    # Accedemos a la coleccion de firestore, al documento de nuestro user_id y a la collection de tareas
    to_do_collection_ref = db.collection('users').documents(user_id).collection('To do')
    # añadimos la nueva tarea 
    to_do_collection_ref.add({'description': description, 'done': False})

# Metodo para eliminar las tareas en firestore service
def delete_to_do(user_id, to_do_id):
    # Accedemos a la tarea
    to_do_ref = _get_todo_ref(user_id=user_id, to_do_id=to_do_id)
    # Utilizamos el metodo delete
    to_do_ref.delete()

# Metodo para acutualizar el estado de una tarea
def update_to_do(user_id, to_do_id, done):
    to_do_done = not bool(done)
    # Accedemos a la tarea
    to_do_ref = _get_todo_ref(user_id=user_id, to_do_id=to_do_id)
    # Actualizamos el estado
    to_do_ref.update({'done': to_do_done})

# Funcion privada para encontar al ususario y su coleccion a taves de su id
def _get_todo_ref(user_id, to_do_id):
    return db.collection('users').document(user_id).collection('To do').document(to_do_id)
