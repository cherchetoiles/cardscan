from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Modèle de visiteur
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    id_card_number = db.Column(db.String(50), unique=True)

    def __repr__(self):
        return f'<User {self.first_name} {self.last_name}>'
