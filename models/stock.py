from sqlalchemy import Column, Integer, String, Float, ForeignKey
from .base import Base

class Stock(Base):
    __tablename__ = "stock"
    id = Column(Integer, primary_key=True, index=True)
    nom_produit = Column(String, index=True)
    quantite = Column(Integer)
    prix = Column(Float)
    id_fournisseur = Column(Integer, ForeignKey("fournisseurs.id"))
    tva = Column(Float)