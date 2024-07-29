#services/auth.py
from models.utilisateur import Utilisateur
from sqlalchemy.orm import Session

def authenticate_user(db: Session, code_personnel: str, mot_de_passe: str):
    user = db.query(Utilisateur).filter(Utilisateur.code_personnel == code_personnel).first()
    if user and user.verify_password(mot_de_passe):
        return user
    else:
        return None

def check_admin(user: Utilisateur):
    if user.role != 'admin':
        raise PermissionError("Accès refusé : seuls les administrateurs peuvent effectuer cette action.")
