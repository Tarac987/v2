from sqlalchemy import Column, Integer, String
from .base import Base

class InformationsBancaires(Base):
    __tablename__ = "informations_bancaires"
    id = Column(Integer, primary_key=True, index=True)
    rib = Column(String, unique=True, index=True)
    numero_cheque = Column(String, unique=True, index=True)
    banque = Column(String)
    id_client = Column(Integer, ForeignKey("clients.id"))
    id_fournisseur = Column(Integer, ForeignKey("fournisseurs.id"))
