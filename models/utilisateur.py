from sqlalchemy import Column, Integer, String
from models.base import Base
from utils.security import check_password

class Utilisateur(Base):
    __tablename__ = "utilisateurs"
    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String, index=True)
    code_personnel = Column(String, unique=True, index=True)
    mot_de_passe = Column(String)
    role = Column(String)

    def est_admin(self):
        return self.role == "admin"

    def verify_password(self, mot_de_passe):
        return check_password(mot_de_passe, self.mot_de_passe)
