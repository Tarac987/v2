# controllers/tva_controller.py

from sqlalchemy.orm import Session
from models.tva import TauxTVA

class TVAController:
    def __init__(self, db: Session):
        self.db = db

    def create_taux(self, taux: float, description: str):
        new_taux = TauxTVA(taux=taux, description=description)
        self.db.add(new_taux)
        self.db.commit()
        return new_taux

    def get_all_taux(self):
        return self.db.query(TauxTVA).all()

    def get_taux_by_id(self, taux_id: int):
        return self.db.query(TauxTVA).filter(TauxTVA.id == taux_id).first()

    def update_taux(self, taux_id: int, taux: float, description: str):
        taux_to_update = self.get_taux_by_id(taux_id)
        if taux_to_update:
            taux_to_update.taux = taux
            taux_to_update.description = description
            self.db.commit()
        return taux_to_update

    def delete_taux(self, taux_id: int):
        taux_to_delete = self.get_taux_by_id(taux_id)
        if taux_to_delete:
            self.db.delete(taux_to_delete)
            self.db.commit()
        return taux_to_delete
