from sqlalchemy.orm import Session
from models.utilisateur import Utilisateur

class UtilisateurController:
    def __init__(self, db: Session):
        self.db = db

    def create_utilisateur(self, nom: str, code_personnel: str, mot_de_passe: str, role: str):
        utilisateur = Utilisateur(nom=nom, code_personnel=code_personnel, mot_de_passe=mot_de_passe, role=role)
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
            utilisateur.mot_de_passe = mot_de_passe
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
        if utilisateur and utilisateur.mot_de_passe == mot_de_passe:
            return utilisateur
        return None
