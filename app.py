from flask import Flask, render_template, request, jsonify, redirect, url_for
from controllers.UserController import UserController
from models.User import User

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    user = User(
        first_name=data.get("first_name"),
        last_name=data.get("last_name"),
        id_card_number=data.get("id_card_number"),
        photo1=data.get("photo1"),
        photo2=data.get("photo2"),
    )
    response = UserController.create_user(user)
    return jsonify(response), 201 if response["success"] else 400

@app.route('/users/<id_card_number>', methods=['GET'])
def get_user(id_card_number):
    response = UserController.get_user(id_card_number)
    return jsonify(response), 200 if response["success"] else 404

@app.route('/users/<id_card_number>', methods=['PUT'])
def update_user(id_card_number):
    updated_data = request.json
    response = UserController.update_user(id_card_number, updated_data)
    return jsonify(response), 200 if response["success"] else 400

@app.route('/users/<id_card_number>', methods=['DELETE'])
def delete_user(id_card_number):
    response = UserController.delete_user(id_card_number)
    return jsonify(response), 200 if response["success"] else 400

@app.route('/views/scanner', methods=['GET', 'POST'])
def scanner():
    if request.method == 'POST':
        id_card_number = request.form['id_card_number']
        response = UserController.get_user(id_card_number)
        if response['success']:
            return render_template('scanner.html', message=f"Bienvenue, {response['data']['first_name']} {response['data']['last_name']}!")
        else:
            return redirect(url_for('face_photo'))

    return render_template('scanner.html', message="Scannez la carte d'identité pour commencer.")

@app.route('/face_photo', methods=['GET', 'POST'])
def face_photo():
    if request.method == 'POST':
        # Traitement des photos et logique de comparaison ici
        return render_template('face_photo.html', message="Traitement terminé.")

    return render_template('face_photo.html', message="Prenez une photo de votre visage pour continuer.")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)