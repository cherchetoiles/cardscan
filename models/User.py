class User:
    def __init__(self, first_name, last_name, id_card_number, photo1=None, photo2=None):
        self.first_name = first_name
        self.last_name = last_name
        self.id_card_number = id_card_number
        self.photo1 = photo1
        self.photo2 = photo2

    def to_dict(self):
        """Convertit l'objet User en dictionnaire compatible Firebase."""
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "id_card_number": self.id_card_number,
            "photo1": self.photo1,
            "photo2": self.photo2,
        }

    @classmethod
    def from_dict(cls, data):
        """Crée un objet User à partir d'un dictionnaire."""
        return cls(
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            id_card_number=data.get("id_card_number"),
            photo1=data.get("photo1"),
            photo2=data.get("photo2"),
        )
