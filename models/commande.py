from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from .base import Base

class Commande(Base):
    __tablename__ = "commandes"
    id = Column(Integer, primary_key=True, index=True)
    id_fournisseur = Column(Integer, ForeignKey("fournisseurs.id"))
    id_produit = Column(Integer, ForeignKey("stock.id"))
    quantite = Column(Integer)
    date_commande = Column(DateTime)
    date_arrivee_prevue = Column(DateTime)
    statut = Column(String)