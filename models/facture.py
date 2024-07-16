from sqlalchemy import Column, Integer, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class Facture(Base):
    __tablename__ = "factures"
    id = Column(Integer, primary_key=True, index=True)
    id_client = Column(Integer, ForeignKey("clients.id"))
    date_creation = Column(DateTime)
    montant_total = Column(Float)
    date_echeance = Column(DateTime)
    paiement_final = Column(Float)
    reglements = relationship("Reglement", back_populates="facture")

class Reglement(Base):
    __tablename__ = "reglements"
    id = Column(Integer, primary_key=True, index=True)
    id_facture = Column(Integer, ForeignKey("factures.id"))
    montant = Column(Float)
    date = Column(DateTime)
    moyen_paiement = Column(String)
