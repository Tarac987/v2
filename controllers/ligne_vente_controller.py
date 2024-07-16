from sqlalchemy.orm import Session
from models.ligne_vente import LigneVente

class LigneVenteController:
    def __init__(self, db: Session):
        self.db = db

    def create_ligne_vente(self, id_transaction: int, id_produit: int, quantite: int, prix_unitaire: float, tva: float, prix_total: float):
        ligne_vente = LigneVente(id_transaction=id_transaction, id_produit=id_produit, quantite=quantite, prix_unitaire=prix_unitaire, tva=tva, prix_total=prix_total)
        self.db.add(ligne_vente)
        self.db.commit()
        return ligne_vente

    def get_ligne_vente(self, ligne_vente_id: int):
        return self.db.query(LigneVente).filter(LigneVente.id == ligne_vente_id).first()

    def update_ligne_vente(self, ligne_vente_id: int, quantite: int, prix_unitaire: float, tva: float, prix_total: float):
        ligne_vente = self.get_ligne_vente(ligne_vente_id)
        if ligne_vente:
            ligne_vente.quantite = quantite
            ligne_vente.prix_unitaire = prix_unitaire
            ligne_vente.tva = tva
            ligne_vente.prix_total = prix_total
            self.db.commit()
        return ligne_vente

    def delete_ligne_vente(self, ligne_vente_id: int):
        ligne_vente = self.get_ligne_vente(ligne_vente_id)
        if ligne_vente:
            self.db.delete(ligne_vente)
            self.db.commit()
        return ligne_vente

    def get_lignes_vente_by_transaction(self, id_transaction: int):
        return self.db.query(LigneVente).filter(LigneVente.id_transaction == id_transaction).all()

    def get_all_lignes_vente(self):
        return self.db.query(LigneVente).all()
