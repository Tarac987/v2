from sqlalchemy import Column, Integer, DateTime, Float, ForeignKey
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
    facture = relationship("Facture", back_populates="avoirs")
