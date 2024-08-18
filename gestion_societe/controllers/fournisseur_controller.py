from models.base import SessionLocal
from models.fournisseur import Fournisseur

class FournisseurController:
    def __init__(self):
        self.session = SessionLocal()

    def create_fournisseur(self, societe, nom, prenom, contact, email, telephone):
        new_fournisseur = Fournisseur(societe=societe, nom=nom, prenom=prenom, contact=contact, email=email, telephone=telephone)
        self.session.add(new_fournisseur)
        self.session.commit()

    def get_fournisseur(self, fournisseur_id):
        return self.session.query(Fournisseur).filter(Fournisseur.id == fournisseur_id).first()
        
    def get_all_fournisseurs(self):
        return self.session.query(Fournisseur).all()


    def update_fournisseur(self, fournisseur_id, **kwargs):
        fournisseur = self.get_fournisseur(fournisseur_id)
        for key, value in kwargs.items():
            setattr(fournisseur, key, value)
        self.session.commit()

    def delete_fournisseur(self, fournisseur_id):
        fournisseur = self.get_fournisseur(fournisseur_id)
        self.session.delete(fournisseur)
        self.session.commit()
