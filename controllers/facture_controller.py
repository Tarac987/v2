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
        return None

    def delete_facture(self, facture_id: int):
        facture = self.get_facture(facture_id)
        if facture:
            self.db.delete(facture)
            self.db.commit()
            return facture
        return None

    def get_reglements_facture(self, facture_id: int):
        facture = self.get_facture(facture_id)
        if facture:
            return facture.reglements
        return []

    def create_reglement(self, facture_id: int, montant: float, date: datetime, moyen_paiement: str):
        facture = self.get_facture(facture_id)
        if facture:
            reglement = Reglement(id_facture=facture_id, montant=montant, date=date, moyen_paiement=moyen_paiement)
            self.db.add(reglement)
            self.db.commit()
            self.calculer_encaisssement(facture_id)  # Mettre à jour l'encaissement après ajout
            return reglement
        return None

    def update_reglement(self, reglement_id: int, montant: float, date: datetime, moyen_paiement: str):
        reglement = self.db.query(Reglement).filter(Reglement.id == reglement_id).first()
        if reglement:
            facture_id = reglement.id_facture
            reglement.montant = montant
            reglement.date = date
            reglement.moyen_paiement = moyen_paiement
            self.db.commit()
            self.calculer_encaisssement(facture_id)  # Mettre à jour l'encaissement après modification
            return reglement
        return None

    def delete_reglement(self, reglement_id: int):
        reglement = self.db.query(Reglement).filter(Reglement.id == reglement_id).first()
        if reglement:
            facture_id = reglement.id_facture
            self.db.delete(reglement)
            self.db.commit()
            self.calculer_encaisssement(facture_id)  # Mettre à jour l'encaissement après suppression
            return reglement
        return None

    def calculer_encaisssement(self, facture_id: int):
        facture = self.get_facture(facture_id)
        if not facture:
            return None
        
        total_reglements = sum(reglement.montant for reglement in facture.reglements)
        
        facture.encaissement = total_reglements
        self.db.commit()
        
        return facture.encaissement

    def get_factures_due(self):
        return self.db.query(Facture).filter(Facture.date_echeance < datetime.now()).all()

    def get_factures_unpaid(self):
        return self.db.query(Facture).filter(Facture.encaissement < Facture.montant_total).all()
        
    def get_all_factures(self):
        return self.db.query(Facture).all()
