from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class Stock(Base):
    __tablename__ = "stock"
    id = Column(Integer, primary_key=True, index=True)
    nom_produit = Column(String, index=True)
    quantite = Column(Integer)
    prix_achat_unitaire_ht = Column(Float)
    taux_tva_achat = Column(Float)
    montant_tva_achat = Column(Float)
    prix_vente_unitaire_ht = Column(Float)
    taux_tva_vente = Column(Float)
    id_fournisseur = Column(Integer, ForeignKey("fournisseurs.id"))
    
    fournisseur = relationship("Fournisseur", back_populates="stocks")
    
  