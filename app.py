from flask import Flask, render_template, request, redirect, url_for
import base64
import cv2
import numpy as np
import sqlite3
import pytesseract
import os

app = Flask(__name__)

# Configurations
DATABASE = 'database.sql'
IMAGE_FOLDER = 'statics/images'

if not os.path.exists(IMAGE_FOLDER):
    os.makedirs(IMAGE_FOLDER)

# Fonction pour décoder une image base64 et la sauvegarder
def decode_image(base64_string, output_path):
    image_data = base64.b64decode(base64_string.split(",")[1])
    with open(output_path, "wb") as f:
        f.write(image_data)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scanner', methods=['GET', 'POST'])
def scanner():
    if request.method == 'POST':
        # Sauvegarde de la photo prise
        image_path = os.path.join(IMAGE_FOLDER, 'captured_id.jpg')
        decode_image(request.form['photo'], image_path)

        # Traitement OCR avec Tesseract
        text = pytesseract.image_to_string(cv2.imread(image_path))

        # Recherche dans la base de données
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE name = ?", (text.strip(),))
            user = cursor.fetchone()

        if user:
            return render_template('scanner.html', message=f"Bienvenue, {text.strip()}!")
        else:
            return redirect(url_for('face_photo'))

    return render_template('scanner.html', message="Prenez une photo de la carte pour commencer.")

@app.route('/face_photo', methods=['GET', 'POST'])
def face_photo():
    if request.method == 'POST':
        # Sauvegarde de la photo du visage
        face_image_path = os.path.join(IMAGE_FOLDER, 'captured_face.jpg')
        decode_image(request.form['face'], face_image_path)

        # Chargement des deux images pour comparaison
        id_image_path = os.path.join(IMAGE_FOLDER, 'captured_id.jpg')

        if os.path.exists(id_image_path):
            id_image = cv2.imread(id_image_path)
            face_image = cv2.imread(face_image_path)

            # Conversion en échelles de gris
            id_image_gray = cv2.cvtColor(id_image, cv2.COLOR_BGR2GRAY)
            face_image_gray = cv2.cvtColor(face_image, cv2.COLOR_BGR2GRAY)

            # Détection et comparaison des features
            sift = cv2.SIFT_create()
            keypoints1, descriptors1 = sift.detectAndCompute(id_image_gray, None)
            keypoints2, descriptors2 = sift.detectAndCompute(face_image_gray, None)

            bf = cv2.BFMatcher()
            matches = bf.knnMatch(descriptors1, descriptors2, k=2)

            # Filtrage des bons matches
            good_matches = []
            for m, n in matches:
                if m.distance < 0.75 * n.distance:
                    good_matches.append(m)

            if len(good_matches) > 10:  # Seuil pour considérer une correspondance
                return render_template('face_photo.html', message="Les photos correspondent. Enregistrement réussi.")
            else:
                return render_template('face_photo.html', message="Erreur : Les photos ne correspondent pas.")

        return render_template('face_photo.html', message="Erreur : Aucune photo de carte ID trouvée.")

    return render_template('face_photo.html', message="Prenez une photo de votre visage pour continuer.")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

