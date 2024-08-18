from models.base import SessionLocal
from models.client import Client

class ClientController:
    def __init__(self):
        self.session = SessionLocal()

    def create_client(self, nom, prenom, telephone, email):
        new_client = Client(nom=nom, prenom=prenom, telephone=telephone, email=email)
        self.session.add(new_client)
        self.session.commit()

    def get_client(self, client_id):
        return self.session.query(Client).filter(Client.id == client_id).first()

    def update_client(self, client_id, **kwargs):
        client = self.get_client(client_id)
        for key, value in kwargs.items():
            setattr(client, key, value)
        self.session.commit()

    def delete_client(self, client_id):
        client = self.get_client(client_id)
        self.session.delete(client)
        self.session.commit()
        
    def get_all_clients(self):
        # Récupère tous les clients de la base de données
        return self.session.query(Client).all()


