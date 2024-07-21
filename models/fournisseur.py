from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class Fournisseur(Base):
    __tablename__ = "fournisseurs"
    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String, index=True)
    nom_contact = Column(String)
    adresse = Column(String)
    email = Column(String, unique=True, index=True)
    telephone = Column(String, unique=True)
    
    # Define relationship to Stock
    stocks = relationship('Stock', back_populates='fournisseur')