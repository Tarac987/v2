from sqlalchemy.orm import Session
from cryptography.fernet import Fernet
from models.informations_bancaires import InformationsBancaires
from models.utilisateur import Utilisateur

class InformationsBancairesController:
    def __init__(self, db: Session, encryption_key: str):
        self.db = db
        self.cipher_suite = Fernet(encryption_key.encode())

    def _encrypt(self, data: str) -> str:
        encrypted_data = self.cipher_suite.encrypt(data.encode())
        return encrypted_data.decode()

    def _decrypt(self, data: str) -> str:
        decrypted_data = self.cipher_suite.decrypt(data.encode())
        return decrypted_data.decode()

    def create_informations_bancaires(self, rib: str, numero_cheque: str, banque: str, id_client: int = None, id_fournisseur: int = None, user: Utilisateur = None):
        if not user:
            raise PermissionError("Accès refusé : utilisateur non authentifié.")
        
        encrypted_rib = self._encrypt(rib)
        encrypted_numero_cheque = self._encrypt(numero_cheque)
        informations_bancaires = InformationsBancaires(
            rib=encrypted_rib,
            numero_cheque=encrypted_numero_cheque,
            banque=banque,
            id_client=id_client,
            id_fournisseur=id_fournisseur
        )
        self.db.add(informations_bancaires)
        self.db.commit()
        return informations_bancaires

    def get_informations_bancaires(self, informations_bancaires_id: int, user: Utilisateur):
        if not user or not user.est_admin():
            raise PermissionError("Accès refusé : seuls les administrateurs peuvent accéder aux informations bancaires.")
        
        informations_bancaires = self.db.query(InformationsBancaires).filter(InformationsBancaires.id == informations_bancaires_id).first()
        if informations_bancaires:
            return {
                "id": informations_bancaires.id,
                "rib": self._decrypt(informations_bancaires.rib),
                "numero_cheque": self._decrypt(informations_bancaires.numero_cheque),
                "banque": informations_bancaires.banque,
                "id_client": informations_bancaires.id_client,
                "id_fournisseur": informations_bancaires.id_fournisseur
            }
        else:
            return None

    def update_informations_bancaires(self, informations_bancaires_id: int, rib: str, numero_cheque: str, banque: str, user: Utilisateur):
        if not user or not user.est_admin():
            raise PermissionError("Accès refusé : seuls les administrateurs peuvent modifier des informations bancaires.")
        
        informations_bancaires = self.db.query(InformationsBancaires).filter(InformationsBancaires.id == informations_bancaires_id).first()
        if informations_bancaires:
            encrypted_rib = self._encrypt(rib)
            encrypted_numero_cheque = self._encrypt(numero_cheque)
            informations_bancaires.rib = encrypted_rib
            informations_bancaires.numero_cheque = encrypted_numero_cheque
            informations_bancaires.banque = banque
            self.db.commit()
            return True
        else:
            return False

    def delete_informations_bancaires(self, informations_bancaires_id: int, user: Utilisateur):
        if not user or not user.est_admin():
            raise PermissionError("Accès refusé : seuls les administrateurs peuvent supprimer des informations bancaires.")
        
        informations_bancaires = self.db.query(InformationsBancaires).filter(InformationsBancaires.id == informations_bancaires_id).first()
        if informations_bancaires:
            self.db.delete(informations_bancaires)
            self.db.commit()
            return True
        else:
            return False
