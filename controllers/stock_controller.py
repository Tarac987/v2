from sqlalchemy.orm import Session
from models.stock import Stock

class StockController:
    def __init__(self, db: Session):
        self.db = db

    def create_produit(self, nom_produit: str, quantite: int, prix: float, id_fournisseur: int, tva: float):
        produit = Stock(nom_produit=nom_produit, quantite=quantite, prix=prix, id_fournisseur=id_fournisseur, tva=tva)
        self.db.add(produit)
        self.db.commit()
        return produit

    def get_produit(self, produit_id: int):
        return self.db.query(Stock).filter(Stock.id == produit_id).first()

    def update_produit(self, produit_id: int, nom_produit: str, quantite: int, prix: float, id_fournisseur: int, tva: float):
        produit = self.get_produit(produit_id)
        if produit:
            produit.nom_produit = nom_produit
            produit.quantite = quantite
            produit.prix = prix
            produit.id_fournisseur = id_fournisseur
            produit.tva = tva
            self.db.commit()
        return produit

    def delete_produit(self, produit_id: int):
        produit = self.get_produit(produit_id)
        if produit:
            self.db.delete(produit)
            self.db.commit()
        return produit

    def get_all_produits(self):
        return self.db.query(Stock).all()

    def get_produits_by_fournisseur(self, id_fournisseur: int):
        return self.db.query(Stock).filter(Stock.id_fournisseur == id_fournisseur).all()
