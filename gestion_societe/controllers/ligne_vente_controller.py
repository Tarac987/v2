from models.base import SessionLocal  # Import cohérent avec les autres contrôleurs
from models.lignevente import LigneVente

class LigneVenteController:
    def __init__(self):
        self.session = SessionLocal()  # Utilisation de SessionLocal

    def create_ligne_vente(self, transaction_id, produit_id, quantite, prix_unitaire, tva, prix_total):
        ligne_vente = LigneVente(
            transaction_id=transaction_id,
            produit_id=produit_id,
            quantite=quantite,
            prix_unitaire=prix_unitaire,
            tva=tva,
            prix_total=prix_total
        )
        self.session.add(ligne_vente)
        self.session.commit()
        return ligne_vente

    def get_ligne_vente_by_id(self, ligne_vente_id):
        return self.session.query(LigneVente).filter_by(id=ligne_vente_id).first()

    def get_lignes_by_transaction_id(self, transaction_id):
        return self.session.query(LigneVente).filter_by(transaction_id=transaction_id).all()

    def update_ligne_vente(self, ligne_vente_id, **kwargs):
        ligne_vente = self.get_ligne_vente_by_id(ligne_vente_id)
        if ligne_vente:
            for key, value in kwargs.items():
                setattr(ligne_vente, key, value)
            self.session.commit()
        return ligne_vente

    def delete_ligne_vente(self, ligne_vente_id):
        ligne_vente = self.get_ligne_vente_by_id(ligne_vente_id)
        if ligne_vente:
            self.session.delete(ligne_vente)
            self.session.commit()
