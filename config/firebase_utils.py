import firebase_admin
from firebase_admin import credentials, firestore

def init_firebase():
    """Initialise Firebase avec la clé de service."""
    cred = credentials.Certificate("/config/serviceAccountKey.json")
    firebase_admin.initialize_app(cred)

def get_firestore_client():
    """Récupère le client Firestore."""
    return firestore.client()
