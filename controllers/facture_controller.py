from sqlalchemy.orm import Session
from models.facture import Facture
from models.reglement import Reglement
from datetime import datetime

class FactureController:
    def __init__(self, db: Session):
        self.db = db

    def create_facture(self, id_client: int, date_creation: datetime, montant_total: float, date_echeance: datetime):
        facture = Facture(id_client=id_client, date_creation=date_creation, montant_total=montant_total, date_echeance=date_echeance)
        self.db.add(facture)
        self.db.commit()
        return facture

    def get_facture(self, facture_id: int):
        return self.db.query(Facture).filter(Facture.id == facture_id).first()

    def update_facture(self, facture_id: int, montant_total: float, date_echeance: datetime):
        facture = self.get_facture(facture_id)
        if facture:
            facture.montant_total = montant_total
            facture.date_echeance = date_echeance
            self.db.commit()
        return facture

    def delete_facture(self, facture_id: int):
        facture = self.get_facture(facture_id)
        if facture:
            self.db.delete(facture)
            self.db.commit()
        return facture

    def get_reglements_facture(self, facture_id: int):
        facture = self.get_facture(facture_id)
        if facture:
            return facture.reglements
        return []

    def calculer_paiement_final(self, facture_id: int):
        facture = self.get_facture(facture_id)
        if not facture:
            return None
        
        total_reglements = sum(reglement.montant for reglement in facture.reglements)
        
        facture.paiement_final = total_reglements
        self.db.commit()
        
        return facture.paiement_final

    def get_factures_due(self):
        return self.db.query(Facture).filter(Facture.date_echeance < datetime.now()).all()

    def get_factures_unpaid(self):
        return self.db.query(Facture).filter(Facture.paiement_final < Facture.montant_total).all()
