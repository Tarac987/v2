from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from .base import Base

class TransactionAchat(Base):
    __tablename__ = "transactions_achats"
    id = Column(Integer, primary_key=True, index=True)
    id_fournisseur = Column(Integer, ForeignKey("fournisseurs.id"))
    date = Column(DateTime)
    prix_total_ht = Column(Float)
    tva_total = Column(Float)
    prix_total_ttc = Column(Float)
    moyen_paiement = Column(String)