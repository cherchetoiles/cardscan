import cv2
import numpy as np
from PIL import Image
from io import BytesIO
import base64
import pytesseract
from flask import Flask, render_template, request, jsonify
import sqlite3
import os
import face_recognition


app = Flask(__name__)

# Créer le dossier 'images' si nécessaire
if not os.path.exists('static/images'):
    os.makedirs('static/images')

# Connexion à la base de données SQLite
def get_db():
    conn = sqlite3.connect('database.db')
    return conn

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/scanner')
def scanner():
    return render_template('scanner.html')

@app.route('/process_image', methods=['POST'])
def process_image():
    data = request.get_json()
    image_data = data['image']
    
    # Convertir l'image de la carte d'identité
    img_data = base64.b64decode(image_data.split(',')[1])
    img = Image.open(BytesIO(img_data))
    img = np.array(img)

    # Sauvegarder l'image dans 'static/images'
    image_path = 'static/images/card_image.png'
    cv2.imwrite(image_path, cv2.cvtColor(img, cv2.COLOR_RGB2BGR))

    # Utiliser Tesseract pour extraire le texte
    text = pytesseract.image_to_string(img)

    # Ici on suppose que l'extraction de la carte d'identité retourne un numéro de carte
    card_number = extract_card_number(text)

    # Recherche de l'utilisateur dans la base de données
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE card_number=?", (card_number,))
    user = cursor.fetchone()

    if user:
        message = f"Bonjour {user[1]}, nous sommes heureux de vous revoir !"
        return jsonify({'message': message, 'action': 'welcome'})
    else:
        message = "Vous n'êtes pas connu de nos services, souhaitez-vous vous enregistrer ?"
        return jsonify({'message': message, 'action': 'register'})

def extract_card_number(text):
    # Utilisation d'une méthode basique pour extraire un numéro de carte
    # Tu peux utiliser une expression régulière ici pour extraire le numéro de carte.
    return "123456789"  # Exemple de numéro de carte fictif


@app.route('/register_face', methods=['POST'])
def register_face():
    data = request.get_json()
    face_image_data = data['image']
    
    # Convertir la photo du visage
    img_data = base64.b64decode(face_image_data.split(',')[1])
    img = Image.open(BytesIO(img_data))
    img = np.array(img)

    # Charger la photo de la carte d'identité enregistrée
    card_image_path = 'static/images/card_image.png'
    card_image = face_recognition.load_image_file(card_image_path)
    
    # Extraire les encodages de visage pour la carte d'identité et la photo de l'utilisateur
    card_face_encoding = face_recognition.face_encodings(card_image)[0]
    user_face_encoding = face_recognition.face_encodings(img)[0]

    # Comparer les visages
    results = face_recognition.compare_faces([card_face_encoding], user_face_encoding)

    if results[0]:
        # Enregistrer l'utilisateur dans la base de données
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (card_number, name) VALUES (?, ?)", ("123456789", "Nom Utilisateur"))
        conn.commit()
        return jsonify({'message': 'Enregistrement réussi !', 'action': 'success'})
    else:
        return jsonify({'message': 'Les photos ne correspondent pas, veuillez réessayer.', 'action': 'retry'})
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
