# models/client.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base

class Client(Base):
    __tablename__ = "clients"
    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String, index=True)
    adresse = Column(String)
    email = Column(String, unique=True, index=True)
    telephone = Column(String, unique=True)

    # Relation avec Facture
    factures = relationship("Facture", back_populates="client")

    # Relation avec Avoir
    avoirs = relationship("Avoir", back_populates="client")
