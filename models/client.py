from sqlalchemy import Column, Integer, String
from .base import Base

class Client(Base):
    __tablename__ = "clients"
    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String, index=True)
    adresse = Column(String)
    email = Column(String, unique=True, index=True)
    telephone = Column(String, unique=True)