# models/seuil_produit.py
from sqlalchemy import Column, Integer, ForeignKey
from models.base import Base

class SeuilProduit(Base):
    __tablename__ = 'seuil_produit'
    id = Column(Integer, primary_key=True)
    produit_id = Column(Integer, ForeignKey('produit.id'), nullable=False)
    seuil_min = Column(Integer, nullable=False)
