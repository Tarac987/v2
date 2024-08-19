from models.base import SessionLocal  # Ajout de cet import pour la cohérence
# transaction_vente_controller.py
from models.base import SessionLocal
from models.transactionvente import TransactionVente

class TransactionVenteController:
    def __init__(self):
        self.session = SessionLocal()

    def create_transaction_vente(self, client_id, total_ht, tva_total_encaisse, total_ttc, moyen_paiement, cheque_nom=None, cheque_prenom=None, cheque_numero=None, cheque_banque=None):
        transaction = TransactionVente(
            client_id=client_id,
            total_ht=total_ht,
            tva_total_encaisse=tva_total_encaisse,
            total_ttc=total_ttc,
            moyen_paiement=moyen_paiement,
            cheque_nom=cheque_nom,
            cheque_prenom=cheque_prenom,
            cheque_numero=cheque_numero,
            cheque_banque=cheque_banque
        )
        self.session.add(transaction)
        self.session.commit()
        return transaction

    def get_transaction_vente_by_id(self, transaction_id):
        return self.session.query(TransactionVente).filter_by(id=transaction_id).first()

    def get_all_transactions(self):
        return self.session.query(TransactionVente).all()

    def update_transaction_vente(self, transaction_id, **kwargs):
        transaction = self.get_transaction_vente_by_id(transaction_id)
        if transaction:
            for key, value in kwargs.items():
                setattr(transaction, key, value)
            self.session.commit()
        return transaction

    def delete_transaction_vente(self, transaction_id):
        transaction = self.get_transaction_vente_by_id(transaction_id)
        if transaction:
            self.session.delete(transaction)
            self.session.commit()
