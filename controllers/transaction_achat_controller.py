from sqlalchemy.orm import Session
from models.transaction_achat import TransactionAchat

class TransactionAchatController:
    def __init__(self, db: Session):
        self.db = db

    def create_transaction_achat(self, id_fournisseur: int, date: datetime, prix_total_ht: float, tva_total: float, prix_total_ttc: float, moyen_paiement: str):
        transaction_achat = TransactionAchat(
            id_fournisseur=id_fournisseur,
            date=date,
            prix_total_ht=prix_total_ht,
            tva_total=tva_total,
            prix_total_ttc=prix_total_ttc,
            moyen_paiement=moyen_paiement
        )
        self.db.add(transaction_achat)
        self.db.commit()
        return transaction_achat

    def get_transaction_achat(self, transaction_id: int):
        return self.db.query(TransactionAchat).filter(TransactionAchat.id == transaction_id).first()

    def update_transaction_achat(self, transaction_id: int, id_fournisseur: int, date: datetime, prix_total_ht: float, tva_total: float, prix_total_ttc: float, moyen_paiement: str):
        transaction_achat = self.get_transaction_achat(transaction_id)
        if transaction_achat:
            transaction_achat.id_fournisseur = id_fournisseur
            transaction_achat.date = date
            transaction_achat.prix_total_ht = prix_total_ht
            transaction_achat.tva_total = tva_total
            transaction_achat.prix_total_ttc = prix_total_ttc
            transaction_achat.moyen_paiement = moyen_paiement
            self.db.commit()
        return transaction_achat

    def delete_transaction_achat(self, transaction_id: int):
        transaction_achat = self.get_transaction_achat(transaction_id)
        if transaction_achat:
            self.db.delete(transaction_achat)
            self.db.commit()
        return transaction_achat

    def get_all_transactions_achat(self):
        return self.db.query(TransactionAchat).all()

    def get_transactions_achat_by_fournisseur(self, id_fournisseur: int):
        return self.db.query(TransactionAchat).filter(TransactionAchat.id_fournisseur == id_fournisseur).all()
