# controllers/stock_controller.py

from sqlalchemy.orm import Session
from models.stock import Stock
from models.tva import TauxTVA

class StockController:
    def __init__(self, db: Session):
        self.db = db

    def create_produit(self, nom_produit: str, quantite: int, prix_achat_unitaire_ht: float, taux_tva_achat: float, prix_vente_unitaire_ht: float, taux_tva_vente: float, id_fournisseur: int):
        #Crée un nouveau produit dans le stock
        # Calcul du montant de TVA
        montant_tva_achat = (prix_achat_unitaire_ht * taux_tva_achat) / 100
        montant_tva_vente = (prix_vente_unitaire_ht * taux_tva_vente) / 100
        
        produit = Stock(
            nom_produit=nom_produit,
            quantite=quantite,
            prix_achat_unitaire_ht=prix_achat_unitaire_ht,
            taux_tva_achat=taux_tva_achat,
            montant_tva_achat=montant_tva_achat,
            prix_vente_unitaire_ht=prix_vente_unitaire_ht,
            taux_tva_vente=taux_tva_vente,
            montant_tva_vente=montant_tva_vente,
            id_fournisseur=id_fournisseur
        )
        self.db.add(produit)
        self.db.commit()
        return produit

    def get_produit(self, produit_id: int):
        # Récupère un produit spécifique par son ID.
        return self.db.query(Stock).filter(Stock.id == produit_id).first()

    def update_produit(self, produit_id: int, nom_produit: str, quantite: int, prix_achat_unitaire_ht: float, taux_tva_achat: float, prix_vente_unitaire_ht: float, taux_tva_vente: float, id_fournisseur: int):
        #Met à jour un produit existant
        produit = self.get_produit(produit_id)
        if produit:
            produit.nom_produit = nom_produit
            produit.quantite = quantite
            produit.prix_achat_unitaire_ht = prix_achat_unitaire_ht
            produit.taux_tva_achat = taux_tva_achat
            produit.montant_tva_achat = (prix_achat_unitaire_ht * taux_tva_achat) / 100
            produit.prix_vente_unitaire_ht = prix_vente_unitaire_ht
            produit.taux_tva_vente = taux_tva_vente
            produit.montant_tva_vente = (prix_vente_unitaire_ht * taux_tva_vente) / 100
            produit.id_fournisseur = id_fournisseur
            self.db.commit()
        return produit

    def delete_produit(self, produit_id: int):
        #Supprime un produit du stock par son ID
        produit = self.get_produit(produit_id)
        if produit:
            self.db.delete(produit)
            self.db.commit()
        return produit

    def get_all_produits(self):
        #Récupère tous les produits du stock
        return self.db.query(Stock).all()

    def get_produits_by_fournisseur(self, id_fournisseur: int):
        # Récupère tous les produits pour un fournisseur spécifique
        return self.db.query(Stock).filter(Stock.id_fournisseur == id_fournisseur).all()
