from sqlalchemy.orm import Session
from models.devis import Devis
from datetime import datetime

class DevisController:
    def __init__(self, db: Session):
        self.db = db

    def create_devis(self, id_client: int, date_creation: datetime, montant_total: float, date_validite: datetime, acompte: float = 0.0):
        devis = Devis(id_client=id_client, date_creation=date_creation, montant_total=montant_total, date_validite=date_validite, acompte=acompte)
        self.db.add(devis)
        self.db.commit()
        return devis

    def get_devis(self, devis_id: int):
        return self.db.query(Devis).filter(Devis.id == devis_id).first()

    def update_devis(self, devis_id: int, montant_total: float, date_validite: datetime, acompte: float):
        devis = self.get_devis(devis_id)
        if devis:
            devis.montant_total = montant_total
            devis.date_validite = date_validite
            devis.acompte = acompte
            self.db.commit()
        return devis

    def delete_devis(self, devis_id: int):
        devis = self.get_devis(devis_id)
        if devis:
            self.db.delete(devis)
            self.db.commit()
        return devis

    def get_devis_by_client(self, client_id: int):
        return self.db.query(Devis).filter(Devis.id_client == client_id).all()

    def get_devis_with_facture(self):
        return self.db.query(Devis).filter(Devis.id_facture.isnot(None)).all()

    def get_devis_overdue(self):
        return self.db.query(Devis).filter(Devis.date_validite < datetime.now()).all()
