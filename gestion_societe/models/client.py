# models/client.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from models.base import Base

class Client(Base):
    __tablename__ = 'clients'

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String, nullable=False)
    prenom = Column(String, nullable=False)
    telephone = Column(String, nullable=False)
    email = Column(String, nullable=True)

    # Relation avec le SAV
    sav = relationship("Sav", back_populates="client")
