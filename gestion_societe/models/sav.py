# models/sav.py
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base

class Sav(Base):
    __tablename__ = 'sav'

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey('clients.id'))
    date_arrivee = Column(Date, nullable=False)
    type_appareil = Column(String, nullable=False)
    marque = Column(String, nullable=False)
    modele = Column(String, nullable=False)
    numero_serie = Column(String, nullable=False)
    accessoire = Column(String, nullable=True)
    probleme = Column(String, nullable=False)
    statut = Column(String, default="En attente")

    client = relationship("Client", back_populates="sav")
    
     # Relation avec la table SuiviSav
    suivi = relationship("SuiviSav", back_populates="sav")
