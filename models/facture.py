# models/facture.py
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
    encaissement = Column(Float)
    reglements = relationship("Reglement", back_populates="facture")
    avoirs = relationship("Avoir", back_populates="facture")

    # Relation avec Client
    client = relationship("Client", back_populates="factures")
