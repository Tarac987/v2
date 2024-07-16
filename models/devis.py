from sqlalchemy import Column, Integer, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class Devis(Base):
    __tablename__ = "devis"
    id = Column(Integer, primary_key=True, index=True)
    id_client = Column(Integer, ForeignKey("clients.id"))
    date_creation = Column(DateTime)
    montant_total = Column(Float)
    date_validite = Column(DateTime)
    acompte = Column(Float)
    id_facture = Column(Integer, ForeignKey("factures.id"))
    facture = relationship("Facture", back_populates="devis")
