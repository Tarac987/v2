from PyQt5.QtWidgets import QWidget, QFormLayout, QLineEdit, QSpinBox, QVBoxLayout, QPushButton, QComboBox
from controllers.produit_controller import ProduitController
from controllers.seuil_produit_controller import SeuilProduitController
from controllers.fournisseur_controller import FournisseurController

class ProduitForm(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.controller = ProduitController()
        self.seuil_controller = SeuilProduitController()
        self.fournisseur_controller = FournisseurController()
        self.produit_id = None  # Ajout de cet attribut pour savoir si on modifie un produit existant
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        form_layout = QFormLayout()

        # Champs de saisie
        self.reference_input = QLineEdit()
        self.designation_input = QLineEdit()
        self.prix_achat_ht_input = QLineEdit()
        self.taux_tva_achat_input = QLineEdit()
        self.montant_tva_achat_input = QLineEdit()
        self.prix_achat_ttc_input = QLineEdit()
        self.prix_vente_ht_input = QLineEdit()
        self.taux_tva_vente_input = QLineEdit()
        self.montant_tva_vente_input = QLineEdit()
        self.prix_vente_ttc_input = QLineEdit()
        self.duree_garantie_input = QSpinBox()
        self.duree_garantie_input.setRange(0, 100)
        self.quantite_input = QSpinBox()
        self.quantite_input.setRange(0, 100000)

        # Liste déroulante pour les fournisseurs
        self.fournisseur_combobox = QComboBox()
        fournisseurs = self.fournisseur_controller.get_all_fournisseurs()
        for fournisseur in fournisseurs:
            self.fournisseur_combobox.addItem(fournisseur.nom, fournisseur.id)

        # Ajout des champs au formulaire
        form_layout.addRow("Référence Fournisseur:", self.reference_input)
        form_layout.addRow("Désignation:", self.designation_input)
        form_layout.addRow("Fournisseur:", self.fournisseur_combobox)
        form_layout.addRow("Prix Achat HT:", self.prix_achat_ht_input)
        form_layout.addRow("Taux TVA Achat:", self.taux_tva_achat_input)
        form_layout.addRow("Montant TVA Achat:", self.montant_tva_achat_input)
        form_layout.addRow("Prix Achat TTC:", self.prix_achat_ttc_input)
        form_layout.addRow("Prix Vente HT:", self.prix_vente_ht_input)
        form_layout.addRow("Taux TVA Vente:", self.taux_tva_vente_input)
        form_layout.addRow("Montant TVA Vente:", self.montant_tva_vente_input)
        form_layout.addRow("Prix Vente TTC:", self.prix_vente_ttc_input)
        form_layout.addRow("Durée Garantie:", self.duree_garantie_input)
        form_layout.addRow("Quantité:", self.quantite_input)

        # Boutons
        submit_button = QPushButton("Enregistrer")
        back_button = QPushButton("Retour")
        submit_button.clicked.connect(self.submit_form)
        back_button.clicked.connect(self.close_form)

        form_layout.addRow(submit_button)
        form_layout.addRow(back_button)

        layout.addLayout(form_layout)
        self.setLayout(layout)

    def load_product(self, produit_id):
        produit = self.controller.get_produit(produit_id)
        if produit:
            self.produit_id = produit.id  # Stocke l'ID du produit en cours de modification
            self.reference_input.setText(produit.reference_fournisseur)
            self.designation_input.setText(produit.designation)
            self.fournisseur_combobox.setCurrentText(produit.fournisseur.nom)
            self.prix_achat_ht_input.setText(str(produit.prix_achat_ht))
            self.taux_tva_achat_input.setText(str(produit.taux_tva_achat))
            self.montant_tva_achat_input.setText(str(produit.montant_tva_achat))
            self.prix_achat_ttc_input.setText(str(produit.prix_achat_ttc))
            self.prix_vente_ht_input.setText(str(produit.prix_vente_ht))
            self.taux_tva_vente_input.setText(str(produit.taux_tva_vente))
            self.montant_tva_vente_input.setText(str(produit.montant_tva_vente))
            self.prix_vente_ttc_input.setText(str(produit.prix_vente_ttc))
            self.duree_garantie_input.setValue(produit.duree_garantie)
            self.quantite_input.setValue(produit.quantite)

    def submit_form(self):
        reference = self.reference_input.text()
        designation = self.designation_input.text()
        prix_achat_ht = float(self.prix_achat_ht_input.text())
        taux_tva_achat = float(self.taux_tva_achat_input.text())
        montant_tva_achat = float(self.montant_tva_achat_input.text())
        prix_achat_ttc = float(self.prix_achat_ttc_input.text())
        prix_vente_ht = float(self.prix_vente_ht_input.text())
        taux_tva_vente = float(self.taux_tva_vente_input.text())
        montant_tva_vente = float(self.montant_tva_vente_input.text())
        prix_vente_ttc = float(self.prix_vente_ttc_input.text())
        duree_garantie = self.duree_garantie_input.value()
        quantite = self.quantite_input.value()
        fournisseur_id = self.fournisseur_combobox.currentData()

        if self.produit_id:
            # Mise à jour du produit existant
            self.controller.update_produit(
                self.produit_id,
                reference_fournisseur=reference,
                designation=designation,
                prix_achat_ht=prix_achat_ht,
                taux_tva_achat=taux_tva_achat,
                montant_tva_achat=montant_tva_achat,
                prix_achat_ttc=prix_achat_ttc,
                prix_vente_ht=prix_vente_ht,
                taux_tva_vente=taux_tva_vente,
                montant_tva_vente=montant_tva_vente,
                prix_vente_ttc=prix_vente_ttc,
                duree_garantie=duree_garantie,
                quantite=quantite,
                fournisseur_id=fournisseur_id
            )
        else:
            # Création d'un nouveau produit
            self.controller.create_produit(
                reference_fournisseur=reference,
                designation=designation,
                prix_achat_ht=prix_achat_ht,
                taux_tva_achat=taux_tva_achat,
                montant_tva_achat=montant_tva_achat,
                prix_achat_ttc=prix_achat_ttc,
                prix_vente_ht=prix_vente_ht,
                taux_tva_vente=taux_tva_vente,
                montant_tva_vente=montant_tva_vente,
                prix_vente_ttc=prix_vente_ttc,
                duree_garantie=duree_garantie,
                quantite=quantite,
                fournisseur_id=fournisseur_id
            )

    def close_form(self):
        self.parent().close()
