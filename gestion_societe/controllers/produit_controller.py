# produit_controller.py
from models.produit import Produit
from models.base import SessionLocal

class ProduitController:
    def __init__(self):
        self.session = SessionLocal()

    def get_all_produits(self):
        return self.session.query(Produit).all()

    def get_produit(self, produit_id):
        return self.session.query(Produit).filter_by(id=produit_id).first()

    def create_produit(self, **kwargs):
        produit = Produit(**kwargs)
        self.session.add(produit)
        self.session.commit()
        return produit

    def update_produit(self, produit_id, **kwargs):
        produit = self.get_produit(produit_id)
        for key, value in kwargs.items():
            setattr(produit, key, value)
        self.session.commit()
        return produit
