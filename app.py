from flask import Flask, render_template, request, redirect, url_for, jsonify
import base64
import cv2
import numpy as np
import sqlite3
import pytesseract
import os
import uuid
from image_processing import process_image

# Initialisation de l'application Flask
app = Flask(__name__)

# Configurations
DATABASE = 'database.sql'
IMAGE_FOLDER = 'static/images'

if not os.path.exists(IMAGE_FOLDER):
    os.makedirs(IMAGE_FOLDER)

# Fonction utilitaire pour décoder une image base64 et la sauvegarder
def decode_image(base64_string, output_path):
    image_data = base64.b64decode(base64_string.split(",")[1])
    with open(output_path, "wb") as f:
        f.write(image_data)

# Route principale
@app.route('/')
def index():
    print(app.template_folder)
    return render_template('index.html')

# Route pour scanner une carte
@app.route('/views/scanner', methods=['GET', 'POST'])
def scanner():
    if request.method == 'POST':
        image_path = os.path.join(IMAGE_FOLDER, 'captured_id.jpg')
        decode_image(request.form['photo'], image_path)

        # OCR pour extraire le texte
        text = pytesseract.image_to_string(cv2.imread(image_path)).strip()

        # Recherche dans la base de données
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE name = ?", (text,))
            user = cursor.fetchone()

        if user:
            return render_template('scanner.html', message=f"Bienvenue, {text}!")
        else:
            return redirect(url_for('face_photo'))

    return render_template('scanner.html', message="Prenez une photo de la carte pour commencer.")

# Route pour prendre une photo du visage
@app.route('/face_photo', methods=['GET', 'POST'])
def face_photo():
    if request.method == 'POST':
        face_image_path = os.path.join(IMAGE_FOLDER, 'captured_face.jpg')
        decode_image(request.form['face'], face_image_path)

        id_image_path = os.path.join(IMAGE_FOLDER, 'captured_id.jpg')
        if os.path.exists(id_image_path):
            id_image = cv2.imread(id_image_path)
            face_image = cv2.imread(face_image_path)

            # Comparaison des photos
            if compare_images(id_image, face_image):
                return render_template('face_photo.html', message="Les photos correspondent. Enregistrement réussi.")
            else:
                return render_template('face_photo.html', message="Erreur : Les photos ne correspondent pas.")

        return render_template('face_photo.html', message="Erreur : Aucune photo de carte ID trouvée.")

    return render_template('face_photo.html', message="Prenez une photo de votre visage pour continuer.")

# Fonction utilitaire pour comparer deux images
def compare_images(image1, image2):
    gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

    sift = cv2.SIFT_create()
    kp1, des1 = sift.detectAndCompute(gray1, None)
    kp2, des2 = sift.detectAndCompute(gray2, None)

    bf = cv2.BFMatcher()
    matches = bf.knnMatch(des1, des2, k=2)

    good_matches = [m for m, n in matches if m.distance < 0.75 * n.distance]
    return len(good_matches) > 10

# Route pour sauvegarder une photo
@app.route('/save_photo', methods=['POST'])
def save_photo():
    data = request.get_json()
    photo_data = data.get('photo')

    image_filename = f"{uuid.uuid4()}.png"
    image_path = os.path.join(IMAGE_FOLDER, image_filename)

    decode_image(photo_data, image_path)

    texte_extrait = process_image(image_path)
    return jsonify({"success": True, "texte_extrait": texte_extrait})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
