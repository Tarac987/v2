# models/suivi_sav.py
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base

class SuiviSav(Base):
    __tablename__ = 'suivi_sav'

    id = Column(Integer, primary_key=True, index=True)
    sav_id = Column(Integer, ForeignKey('sav.id'))
    date_suivi = Column(Date, nullable=False)
    operation = Column(String, nullable=False)
    statut = Column(String, nullable=False)

    # Relation avec la table SAV
    sav = relationship("Sav", back_populates="suivi")
