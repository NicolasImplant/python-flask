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