# models/tva.py

from sqlalchemy import Column, Integer, Float, String
from .base import Base

class TauxTVA(Base):
    __tablename__ = 'taux_tva'
    id = Column(Integer, primary_key=True, autoincrement=True)
    taux = Column(Float, nullable=False)
    description = Column(String, nullable=False)
    
    def __repr__(self):
        return f"<TauxTVA(id={self.id}, taux={self.taux}, description='{self.description}')>"
