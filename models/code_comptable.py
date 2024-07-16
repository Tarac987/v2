from sqlalchemy import Column, Integer, String
from .base import Base

class CodeComptable(Base):
    __tablename__ = "codes_comptables"
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, index=True)
    description = Column(String)