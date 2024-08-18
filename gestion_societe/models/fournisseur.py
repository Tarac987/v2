from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from models.base import Base

class Fournisseur(Base):
    __tablename__ = 'fournisseurs'

    id = Column(Integer, primary_key=True, index=True)
    societe = Column(String, nullable=False)
    nom = Column(String, nullable=False)
    prenom = Column(String, nullable=False)
    contact = Column(String, nullable=True)
    email = Column(String, nullable=False)
    telephone = Column(String, nullable=False)

    # Relation avec Produit
    produits = relationship("Produit", back_populates="fournisseur")
