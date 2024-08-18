# controllers/suivi_sav_controller.py
from models.base import SessionLocal
from models.suivi_sav import SuiviSav

class SuiviSavController:
    def __init__(self):
        self.session = SessionLocal()

    def create_suivi(self, sav_id, date_suivi, operation, statut):
        suivi = SuiviSav(
            sav_id=sav_id,
            date_suivi=date_suivi,
            operation=operation,
            statut=statut
        )
        self.session.add(suivi)
        self.session.commit()

    def get_suivi_by_sav(self, sav_id):
        return self.session.query(SuiviSav).filter_by(sav_id=sav_id).all()

    def update_suivi(self, suivi_id, **kwargs):
        suivi = self.session.query(SuiviSav).get(suivi_id)
        for key, value in kwargs.items():
            setattr(suivi, key, value)
        self.session.commit()
