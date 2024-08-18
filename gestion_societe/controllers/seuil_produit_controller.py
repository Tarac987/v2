# controllers/seuil_produit_controller.py
from models.seuil_produit import SeuilProduit
from models.base import SessionLocal

class SeuilProduitController:
    def __init__(self):
        self.session = SessionLocal()

    def get_seuil_by_produit(self, produit_id):
        return self.session.query(SeuilProduit).filter_by(produit_id=produit_id).first()

    def set_seuil(self, produit_id, seuil_min):
        seuil = self.get_seuil_by_produit(produit_id)
        if seuil:
            seuil.seuil_min = seuil_min
        else:
            seuil = SeuilProduit(produit_id=produit_id, seuil_min=seuil_min)
            self.session.add(seuil)
        self.session.commit()

    def get_all_seuils(self):
        return self.session.query(SeuilProduit).all()
