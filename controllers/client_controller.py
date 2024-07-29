from sqlalchemy.orm import Session
from models.client import Client

class ClientController:
    def __init__(self, db: Session):
        self.db = db

    def create_client(self, nom: str, prenom: str, email: str, telephone: str):
        client = Client(nom=nom, prenom=prenom, email=email, telephone=telephone)
        self.db.add(client)
        self.db.commit()
        return client

    def get_client(self, client_id: int):
        return self.db.query(Client).filter(Client.id == client_id).first()

    def update_client(self, client_id: int, nom: str, prenom: str, email: str, telephone: str):
        client = self.get_client(client_id)
        if client:
            client.nom = nom
            client.prenom = prenom
            client.email = email
            client.telephone = telephone
            self.db.commit()
        return client

    def delete_client(self, client_id: int):
        client = self.get_client(client_id)
        if client:
            self.db.delete(client)
            self.db.commit()
        return client

    def get_clients(self):
        return self.db.query(Client).all()

    def get_client_by_email(self, email: str):
        return self.db.query(Client).filter(Client.email == email).first()

    def get_client_by_telephone(self, telephone: str):
        return self.db.query(Client).filter(Client.telephone == telephone).first()
