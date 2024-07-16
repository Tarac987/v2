from sqlalchemy.orm import Session
from models.fournisseur import Fournisseur

class FournisseurController:
    def __init__(self, db: Session):
        self.db = db

    def create_fournisseur(self, nom: str, nom_contact: str, adresse: str, email: str, telephone: str):
        fournisseur = Fournisseur(nom=nom, nom_contact=nom_contact, adresse=adresse, email=email, telephone=telephone)
        self.db.add(fournisseur)
        self.db.commit()
        return fournisseur

    def get_fournisseur(self, fournisseur_id: int):
        return self.db.query(Fournisseur).filter(Fournisseur.id == fournisseur_id).first()

    def update_fournisseur(self, fournisseur_id: int, nom: str, nom_contact: str, adresse: str, email: str, telephone: str):
        fournisseur = self.get_fournisseur(fournisseur_id)
        if fournisseur:
            fournisseur.nom = nom
            fournisseur.nom_contact = nom_contact
            fournisseur.adresse = adresse
            fournisseur.email = email
            fournisseur.telephone = telephone
            self.db.commit()
        return fournisseur

    def delete_fournisseur(self, fournisseur_id: int):
        fournisseur = self.get_fournisseur(fournisseur_id)
        if fournisseur:
            self.db.delete(fournisseur)
            self.db.commit()
        return fournisseur

    def get_all_fournisseurs(self):
        return self.db.query(Fournisseur).all()
