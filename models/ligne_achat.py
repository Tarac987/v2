from sqlalchemy import Column, Integer, Float, ForeignKey
from .base import Base

class LigneAchat(Base):
    __tablename__ = "lignes_achats"
    id = Column(Integer, primary_key=True, index=True)
    id_transaction = Column(Integer, ForeignKey("transactions_achats.id"))
    id_produit = Column(Integer, ForeignKey("stock.id"))
    quantite = Column(Integer)
    prix_unitaire = Column(Float)
    tva = Column(Float)
    prix_total = Column(Float)