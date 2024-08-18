# controllers/sav_controller.py
from models.base import SessionLocal
from models.sav import Sav

class SavController:
    def __init__(self):
        self.session = SessionLocal()

    def create_sav(self, client_id, date_arrivee, type_appareil, marque, modele, numero_serie, accessoire, probleme, statut="En attente"):
        sav = Sav(
            client_id=client_id,
            date_arrivee=date_arrivee,
            type_appareil=type_appareil,
            marque=marque,
            modele=modele,
            numero_serie=numero_serie,
            accessoire=accessoire,
            probleme=probleme,
            statut=statut
        )
        self.session.add(sav)
        self.session.commit()

    def get_all_sav(self):
        return self.session.query(Sav).all()

    def update_sav(self, sav_id, **kwargs):
        sav = self.session.query(Sav).get(sav_id)
        for key, value in kwargs.items():
            setattr(sav, key, value)
        self.session.commit()

    def get_sav(self, sav_id):
        return self.session.query(Sav).get(sav_id)
