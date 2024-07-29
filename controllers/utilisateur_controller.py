from sqlalchemy.orm import Session
from models.utilisateur import Utilisateur
from utils.security import encrypt_password

class UtilisateurController:
    def __init__(self, db: Session, key: bytes):
        self.db = db
        self.key = key

    def create_utilisateur(self, nom: str, code_personnel: str, mot_de_passe: str, role: str):
        encrypted_password = encrypt_password(mot_de_passe, self.key)
        utilisateur = Utilisateur(nom=nom, code_personnel=code_personnel, mot_de_passe=encrypted_password, role=role)
        self.db.add(utilisateur)
        self.db.commit()
        return utilisateur

    def get_utilisateur(self, utilisateur_id: int):
        return self.db.query(Utilisateur).filter(Utilisateur.id == utilisateur_id).first()

    def get_utilisateur_by_code_personnel(self, code_personnel: str):
        return self.db.query(Utilisateur).filter(Utilisateur.code_personnel == code_personnel).first()

    def update_utilisateur(self, utilisateur_id: int, nom: str, code_personnel: str, mot_de_passe: str, role: str):
        utilisateur = self.get_utilisateur(utilisateur_id)
        if utilisateur:
            utilisateur.nom = nom
            utilisateur.code_personnel = code_personnel
            utilisateur.mot_de_passe = encrypt_password(mot_de_passe, self.key)
            utilisateur.role = role
            self.db.commit()
        return utilisateur

    def delete_utilisateur(self, utilisateur_id: int):
        utilisateur = self.get_utilisateur(utilisateur_id)
        if utilisateur:
            self.db.delete(utilisateur)
            self.db.commit()
        return utilisateur

    def authenticate_utilisateur(self, code_personnel: str, mot_de_passe: str):
        utilisateur = self.get_utilisateur_by_code_personnel(code_personnel)
        if utilisateur and utilisateur.verify_password(mot_de_passe):
            return utilisateur
        return None
