# models/reglement.py
from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship
from .base import Base

class Reglement(Base):
    __tablename__ = "reglements"
    id = Column(Integer, primary_key=True, index=True)
    id_facture = Column(Integer, ForeignKey("factures.id"))
    montant = Column(Float)
    date = Column(DateTime)
    moyen_paiement = Column(String)

    # Relation avec Facture
    facture = relationship("Facture", back_populates="reglements")
