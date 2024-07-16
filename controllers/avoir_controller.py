from sqlalchemy.orm import Session
from models.avoir import Avoir

class AvoirController:
    def __init__(self, db: Session):
        self.db = db

    def create_avoir(self, id_client: int, date_creation: datetime, montant_total: float, date_validite: datetime, id_facture: int):
        avoir = Avoir(id_client=id_client, date_creation=date_creation, montant_total=montant_total, date_validite=date_validite, id_facture=id_facture)
        self.db.add(avoir)
        self.db.commit()
        return avoir

    def get_avoir(self, avoir_id: int):
        return self.db.query(Avoir).filter(Avoir.id == avoir_id).first()

    def update_avoir(self, avoir_id: int, montant_total: float, date_validite: datetime):
        avoir = self.get_avoir(avoir_id)
        if avoir:
            avoir.montant_total = montant_total
            avoir.date_validite = date_validite
            self.db.commit()
        return avoir

    def delete_avoir(self, avoir_id: int):
        avoir = self.get_avoir(avoir_id)
        if avoir:
            self.db.delete(avoir)
            self.db.commit()
        return avoir

    def get_avoirs_client(self, client_id: int):
        return self.db.query(Avoir).filter(Avoir.id_client == client_id).all()
