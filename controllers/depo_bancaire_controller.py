from sqlalchemy.orm import Session
from models.depot_bancaire import DepotBancaire

class DepotBancaireController:
    def __init__(self, db: Session):
        self.db = db

    def create_depot_bancaire(self, montant: float, date: datetime, id_code_comptable: int, type_depot: str, numero_piece: str):
        depot_bancaire = DepotBancaire(montant=montant, date=date, id_code_comptable=id_code_comptable, type_depot=type_depot, numero_piece=numero_piece)
        self.db.add(depot_bancaire)
        self.db.commit()
        return depot_bancaire

    def get_depot_bancaire(self, depot_bancaire_id: int):
        return self.db.query(DepotBancaire).filter(DepotBancaire.id == depot_bancaire_id).first()

    def update_depot_bancaire(self, depot_bancaire_id: int, montant: float, date: datetime, id_code_comptable: int, type_depot: str, numero_piece: str):
        depot_bancaire = self.get_depot_bancaire(depot_bancaire_id)
        if depot_bancaire:
            depot_bancaire.montant = montant
            depot_bancaire.date = date
            depot_bancaire.id_code_comptable = id_code_comptable
            depot_bancaire.type_depot = type_depot
            depot_bancaire.numero_piece = numero_piece
            self.db.commit()
        return depot_bancaire

    def delete_depot_bancaire(self, depot_bancaire_id: int):
        depot_bancaire = self.get_depot_bancaire(depot_bancaire_id)
        if depot_bancaire:
            self.db.delete(depot_bancaire)
            self.db.commit()
        return depot_bancaire

    def get_depots_bancaires(self):
        return self.db.query(DepotBancaire).all()

    def get_depots_bancaires_by_type(self, type_depot: str):
        return self.db.query(DepotBancaire).filter(DepotBancaire.type_depot == type_depot).all()

    def get_depots_bancaires_by_code_comptable(self, code_comptable_id: int):
        return self.db.query(DepotBancaire).filter(DepotBancaire.id_code_comptable == code_comptable_id).all()
 
    def get_depots_bancaires_by_date(self, date: datetime):
        return self.db.query(DepotBancaire).filter(DepotBancaire.date == date).all()       
