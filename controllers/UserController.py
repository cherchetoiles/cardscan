from config.firebase_utils import get_firestore_client
from models.User import User

db = get_firestore_client()

class UserController:
    @staticmethod
    def create_user(user):
        try:
            doc_ref = db.collection("users").document(user.id_card_number)
            doc_ref.set(user.to_dict())
            return {"success": True, "message": "Utilisateur créé avec succès"}
        except Exception as e:
            return {"success": False, "message": f"Erreur : {str(e)}"}

    @staticmethod
    def get_user(id_card_number):
        try:
            doc_ref = db.collection("users").document(id_card_number)
            doc = doc_ref.get()
            if doc.exists:
                return {"success": True, "data": doc.to_dict()}
            return {"success": False, "message": "Utilisateur non trouvé"}
        except Exception as e:
            return {"success": False, "message": f"Erreur : {str(e)}"}

    @staticmethod
    def update_user(id_card_number, updated_data):
        try:
            doc_ref = db.collection("users").document(id_card_number)
            if not doc_ref.get().exists:
                return {"success": False, "message": "Utilisateur non trouvé"}
            doc_ref.update(updated_data)
            return {"success": True, "message": "Utilisateur mis à jour"}
        except Exception as e:
            return {"success": False, "message": f"Erreur : {str(e)}"}

    @staticmethod
    def delete_user(id_card_number):
        try:
            db.collection("users").document(id_card_number).delete()
            return {"success": True, "message": "Utilisateur supprimé avec succès"}
        except Exception as e:
            return {"success": False, "message": f"Erreur : {str(e)}"}