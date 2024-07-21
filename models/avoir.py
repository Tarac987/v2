# models/avoir.py
from sqlalchemy import Column, Integer, DateTime, Float, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from .base import Base

class Avoir(Base):
    __tablename__ = "avoirs"
    id = Column(Integer, primary_key=True, index=True)
    id_client = Column(Integer, ForeignKey("clients.id"))
    date_creation = Column(DateTime)
    montant_total = Column(Float)
    date_validite = Column(DateTime)
    id_facture = Column(Integer, ForeignKey("factures.id"))
    solde = Column(Boolean, default=False)  # Indique si l'avoir a été soldé
    date_utilisation = Column(DateTime, nullable=True)  # Date à laquelle l'avoir a été utilisé

    # Relation avec Facture
    facture = relationship("Facture", back_populates="avoirs")

    # Relation avec Client
    client = relationship("Client", back_populates="avoirs")
