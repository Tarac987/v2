from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base

class LigneVente(Base):
    __tablename__ = 'ligne_vente'

    id = Column(Integer, primary_key=True)
    transaction_id = Column(Integer, ForeignKey('transaction_vente.id'))
    produit_id = Column(Integer, ForeignKey('produit.id'))
    quantite = Column(Integer, nullable=False)
    prix_unitaire = Column(Float, nullable=False)
    tva = Column(Float, nullable=False)  # Taux de TVA appliqué
    montant_tva = Column(Float, nullable=False)  # Montant de TVA calculé
    prix_total = Column(Float, nullable=False)

    transaction_vente = relationship('TransactionVente', back_populates='lignes_vente')
    produit = relationship('Produit')
