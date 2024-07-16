from sqlalchemy.orm import Session
from models.commande import Commande

class CommandeController:
    def __init__(self, db: Session):
        self.db = db

    def create_commande(self, id_fournisseur: int, id_produit: int, quantite: int, date_commande: datetime, date_arrivee_prevue: datetime, statut: str):
        commande = Commande(id_fournisseur=id_fournisseur, id_produit=id_produit, quantite=quantite, date_commande=date_commande, date_arrivee_prevue=date_arrivee_prevue, statut=statut)
        self.db.add(commande)
        self.db.commit()
        return commande

    def get_commande(self, commande_id: int):
        return self.db.query(Commande).filter(Commande.id == commande_id).first()

    def update_commande(self, commande_id: int, quantite: int, date_arrivee_prevue: datetime, statut: str):
        commande = self.get_commande(commande_id)
        if commande:
            commande.quantite = quantite
            commande.date_arrivee_prevue = date_arrivee_prevue
            commande.statut = statut
            self.db.commit()
        return commande

    def delete_commande(self, commande_id: int):
        commande = self.get_commande(commande_id)
        if commande:
            self.db.delete(commande)
            self.db.commit()
        return commande

    def get_commandes_fournisseur(self, fournisseur_id: int):
        return self.db.query(Commande).filter(Commande.id_fournisseur == fournisseur_id).all()
