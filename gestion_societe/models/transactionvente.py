# transactionvente.py
from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base
from datetime import datetime

class TransactionVente(Base):
    __tablename__ = 'transaction_vente'

    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('client.id'))
    date = Column(DateTime, default=datetime.now)
    total_ht = Column(Float, nullable=False)
    tva_total_encaisse = Column(Float, nullable=False)
    total_ttc = Column(Float, nullable=False)
    moyen_paiement = Column(String, nullable=False)

    # Champs spécifiques pour le paiement par chèque
    cheque_nom = Column(String, nullable=True)
    cheque_prenom = Column(String, nullable=True)
    cheque_numero = Column(String, nullable=True)
    cheque_banque = Column(String, nullable=True)

    client = relationship('Client', back_populates='transactions')
    lignes_vente = relationship('LigneVente', back_populates='transaction_vente')
