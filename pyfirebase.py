#I'm importing pyrebase but installed pyrebase4 cuz it was compatible with Flask.
import pyrebase

#This file contain my own firebase dirpath
# you MUST use your own firebase configuration.
#Don't know how to config just search the for "Connecting Python to Firebase storage"

config = {
    'apiKey': "AIzaSyD6Dh9kEZNAba3o6FWne0rIINNiUB6qc0Y",
    'authDomain': "smart-motorbike-system.firebaseapp.com",
    'databaseURL': "https://smart-motorbike-system-default-rtdb.asia-southeast1.firebasedatabase.app",
    'projectId': "smart-motorbike-system",
    'storageBucket': "smart-motorbike-system.appspot.com",
    'serviceAccount':"serviceAccountKey.json"
}

firebase_storage = pyrebase.initialize_app(config)
auth = firebase.auth
storage = firebase_storage.storage()

# Use for store a file to firebase storage
def store(file_name):
    storage.child(file_name).put(file_name)


# Use for download a file to firebase storage
def download(file_name):
    storage.child(file_name).download(file_name)