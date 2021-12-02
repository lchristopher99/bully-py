import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

class Firebase:
    # initialize database and set reference
    def init_db():
        # connect to firebase
        db_url = "https://bully-py-default-rtdb.firebaseio.com/"
        cred = credentials.Certificate("./db/bully-py_firebase.json")
        default_app = firebase_admin.initialize_app(cred, {'databaseURL': db_url})
