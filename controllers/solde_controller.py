from sqlalchemy.orm import Session
from models.solde import Solde

class SoldeController:
    def __init__(self, db: Session):
        self.db = db

    def create_solde(self, id_facture: int = None, id_avoir: int = None, montant: float, type_transaction: str, date_transaction: datetime):
        solde = Solde(id_facture=id_facture, id_avoir=id_avoir, montant=montant, type_transaction=type_transaction, date_transaction=date_transaction)
        self.db.add(solde)
        self.db.commit()
        return solde

    def get_solde(self, solde_id: int):
        return self.db.query(Solde).filter(Solde.id == solde_id).first()

    def update_solde(self, solde_id: int, montant: float, type_transaction: str, date_transaction: datetime):
        solde = self.get_solde(solde_id)
        if solde:
            solde.montant = montant
            solde.type_transaction = type_transaction
            solde.date_transaction = date_transaction
            self.db.commit()
        return solde

    def delete_solde(self, solde_id: int):
        solde = self.get_solde(solde_id)
        if solde:
            self.db.delete(solde)
            self.db.commit()
        return solde

    def get_solde_by_type_transaction(self, type_transaction: str):
        return self.db.query(Solde).filter(Solde.type_transaction == type_transaction).all()

    def get_all_solde(self):
        return self.db.query(Solde).all()
