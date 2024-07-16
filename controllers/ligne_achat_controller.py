from sqlalchemy.orm import Session
from models.ligne_achat import LigneAchat

class LigneAchatController:
    def __init__(self, db: Session):
        self.db = db

    def create_ligne_achat(self, id_transaction: int, id_produit: int, quantite: int, prix_unitaire: float, tva: float, prix_total: float):
        ligne_achat = LigneAchat(id_transaction=id_transaction, id_produit=id_produit, quantite=quantite, prix_unitaire=prix_unitaire, tva=tva, prix_total=prix_total)
        self.db.add(ligne_achat)
        self.db.commit()
        return ligne_achat

    def get_ligne_achat(self, ligne_achat_id: int):
        return self.db.query(LigneAchat).filter(LigneAchat.id == ligne_achat_id).first()

    def update_ligne_achat(self, ligne_achat_id: int, quantite: int, prix_unitaire: float, tva: float, prix_total: float):
        ligne_achat = self.get_ligne_achat(ligne_achat_id)
        if ligne_achat:
            ligne_achat.quantite = quantite
            ligne_achat.prix_unitaire = prix_unitaire
            ligne_achat.tva = tva
            ligne_achat.prix_total = prix_total
            self.db.commit()
        return ligne_achat

    def delete_ligne_achat(self, ligne_achat_id: int):
        ligne_achat = self.get_ligne_achat(ligne_achat_id)
        if ligne_achat:
            self.db.delete(ligne_achat)
            self.db.commit()
        return ligne_achat

    def get_lignes_achat_by_transaction(self, id_transaction: int):
        return self.db.query(LigneAchat).filter(LigneAchat.id_transaction == id_transaction).all()

    def get_all_lignes_achat(self):
        return self.db.query(LigneAchat).all()
