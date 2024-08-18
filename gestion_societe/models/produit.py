from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base

class Produit(Base):
    __tablename__ = 'produits'

    id = Column(Integer, primary_key=True, index=True)
    reference_fournisseur = Column(String, nullable=False)
    fournisseur_id = Column(Integer, ForeignKey('fournisseurs.id'))
    designation = Column(String, nullable=False)
    prix_achat_ht = Column(Float, nullable=False)
    taux_tva_achat = Column(Float, nullable=False)
    montant_tva_achat = Column(Float, nullable=False)
    prix_achat_ttc = Column(Float, nullable=False)
    prix_vente_ht = Column(Float, nullable=False)
    taux_tva_vente = Column(Float, nullable=False)
    montant_tva_vente = Column(Float, nullable=False)
    prix_vente_ttc = Column(Float, nullable=False)
    duree_garantie = Column(Integer, nullable=False)
    quantite = Column(Integer, nullable=False)

    # Relation avec Fournisseur
    fournisseur = relationship("Fournisseur", back_populates="produits")
