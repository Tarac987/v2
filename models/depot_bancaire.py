from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from .base import Base

class DepotBancaire(Base):
    __tablename__ = "depots_bancaires"
    id = Column(Integer, primary_key=True, index=True)
    montant = Column(Float)
    date = Column(DateTime)
    id_code_comptable = Column(Integer, ForeignKey("codes_comptables.id"))
    type_depot = Column(String)
    numero_piece = Column(String, unique=True, index=True)