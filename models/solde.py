from sqlalchemy import Column, Integer, Float, DateTime, Enum, ForeignKey
from .base import Base

class Solde(Base):
    __tablename__ = "solde"
    id = Column(Integer, primary_key=True, index=True)
    id_facture = Column(Integer, ForeignKey("factures.id"))
    id_avoir = Column(Integer, ForeignKey("avoirs.id"))
    montant = Column(Float)
    type_transaction = Column(Enum('facture', 'avoir', 'acompte'))
    date_transaction = Column(DateTime)
