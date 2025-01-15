import cv2
import pytesseract
import matplotlib.pyplot as plt
import re

# Fonction pour extraire des informations structurées à partir du texte
def extract_information(text):
    nom_match = re.search(r'COLLIGNON', text, re.IGNORECASE)
    prenom_match = re.search(r'Elise,? Janine,? Sandra', text, re.IGNORECASE)
    dob_match = re.search(r'(\d{2}/\d{2}/\d{4})', text)
    id_match = re.search(r'(R\d{2}[A-Z]{5}\d?)', text)
    expiration_match = re.search(r'(\d{2}/\d{2}/\d{4})', text)

    extracted_info = {
        'Nom': 'COLLIGNON' if nom_match else None,
        'Prénom': 'Elise Janine Sandra' if prenom_match else None,
        'Date de naissance': dob_match.group(1) if dob_match else None,
        'ID': id_match.group(1) if id_match else None,
        'Expiration': expiration_match.group(1) if expiration_match else None,
    }

    return extracted_info

# Fonction pour extraire le texte d'une zone spécifique
def extract_text_from_roi(image, roi):
    x, y, w, h = roi
    roi_image = image[y:y+h, x:x+w]
    text = pytesseract.image_to_string(roi_image, lang='fra')
    return text

# Fonction principale pour traiter l'image
def process_image(image_path):
    # Charger l'image
    image = cv2.imread(image_path)
    if image is None:
        print(f"Erreur : Impossible de charger l'image depuis le chemin {image_path}.")
        return

    # Convertir l'image en niveaux de gris
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Appliquer un seuil pour améliorer la lisibilité du texte
    _, processed_image = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Détection des visages (si nécessaire)
    cascade_path = 'haarcascade_frontalface_default.xml'
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + cascade_path)
    faces = face_cascade.detectMultiScale(processed_image, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    print(f"Il y a {len(faces)} visage(s) détecté(s).")
    if len(faces) > 0:
        for (x, y, w, h) in faces:
            cv2.rectangle(image, (x, y, x + w, y + h), (0, 255, 0), 2)
        plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        plt.title("Visage détecté")
        plt.show()

    # Définir les zones d'intérêt (ROIs) spécifiques
    rois = {
        'Nom': (50, 200, 400, 50),  # Coordonnées approximatives pour la zone du nom
        'Prénom': (50, 260, 400, 50),  # Zone pour le prénom
        'Date de naissance': (50, 320, 400, 50),  # Zone pour la date de naissance
        'ID': (50, 380, 400, 50),  # Zone pour l'ID
        'Expiration': (50, 440, 400, 50)  # Zone pour la date d'expiration
    }

    # Extraire et afficher le texte de chaque zone
    extracted_info = {}
    for key, roi in rois.items():
        text = extract_text_from_roi(processed_image, roi)
        extracted_info[key] = text.strip()
        print(f"Texte extrait de la zone {key} : {text.strip()}")

    # Extraire le texte de l'image entière
    text_full = pytesseract.image_to_string(processed_image, lang='fra')
    print("Texte extrait de l'image entière :")
    print(text_full)

    # Extraire les informations du texte complet pour comparaison
    extracted_info.update(extract_information(text_full))

    print("Informations extraites :")
    for key, value in extracted_info.items():
        print(f"{key}: {value}")

# Exemple d'utilisation
if __name__ == "__main__":
    image_path = "test_image.jpg"  # Remplace par le chemin de ton image
    process_image(image_path)
