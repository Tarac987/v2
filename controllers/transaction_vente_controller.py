from sqlalchemy.orm import Session
from models.transaction_vente import TransactionVente

class TransactionVenteController:
    def __init__(self, db: Session):
        self.db = db

    def create_transaction_vente(self, id_client: int, date: datetime, prix_total_ht: float, tva_total: float, prix_total_ttc: float, moyen_paiement: str):
        transaction_vente = TransactionVente(
            id_client=id_client,
            date=date,
            prix_total_ht=prix_total_ht,
            tva_total=tva_total,
            prix_total_ttc=prix_total_ttc,
            moyen_paiement=moyen_paiement
        )
        self.db.add(transaction_vente)
        self.db.commit()
        return transaction_vente

    def get_transaction_vente(self, transaction_id: int):
        return self.db.query(TransactionVente).filter(TransactionVente.id == transaction_id).first()

    def update_transaction_vente(self, transaction_id: int, id_client: int, date: datetime, prix_total_ht: float, tva_total: float, prix_total_ttc: float, moyen_paiement: str):
        transaction_vente = self.get_transaction_vente(transaction_id)
        if transaction_vente:
            transaction_vente.id_client = id_client
            transaction_vente.date = date
            transaction_vente.prix_total_ht = prix_total_ht
            transaction_vente.tva_total = tva_total
            transaction_vente.prix_total_ttc = prix_total_ttc
            transaction_vente.moyen_paiement = moyen_paiement
            self.db.commit()
        return transaction_vente

    def delete_transaction_vente(self, transaction_id: int):
        transaction_vente = self.get_transaction_vente(transaction_id)
        if transaction_vente:
            self.db.delete(transaction_vente)
            self.db.commit()
        return transaction_vente

    def get_all_transactions_vente(self):
        return self.db.query(TransactionVente).all()

    def get_transactions_vente_by_client(self, id_client: int):
        return self.db.query(TransactionVente).filter(TransactionVente.id_client == id_client).all()
