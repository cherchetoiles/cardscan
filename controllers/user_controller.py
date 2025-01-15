from config.firebase_utils import get_firestore_client
from models.User import User

db = get_firestore_client()

class UserController:
    @staticmethod
    def create_user(user):
        try:
            doc_ref = db.collection("users").document(user.id_card_number)
            doc_ref.set(user.to_dict())
            return True
        except Exception as e:
            print(f"Erreur lors de l'ajout d'utilisateur : {e}")
            return False

    @staticmethod
    def get_user(id_card_number):
        try:
            doc_ref = db.collection("users").document(id_card_number)
            doc = doc_ref.get()
            return doc.to_dict() if doc.exists else None
        except Exception as e:
            print(f"Erreur lors de la récupération d'utilisateur : {e}")
            return None

    @staticmethod
    def update_user(id_card_number, updated_data):
        try:
            db.collection("users").document(id_card_number).update(updated_data)
            return True
        except Exception as e:
            print(f"Erreur lors de la mise à jour d'utilisateur : {e}")
            return False
