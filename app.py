from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "Bienvenue sur votre API Flask minimale !"})

@app.route('/data', methods=['POST'])
def receive_data():
    data = request.json
    return jsonify({"received": data, "message": "Les données ont été reçues avec succès."})

if __name__ == '__main__':
    # Remplace 0.0.0.0 par l'adresse IP de ton ordinateur pour la rendre accessible
    app.run(host='0.0.0.0', port=5000)
