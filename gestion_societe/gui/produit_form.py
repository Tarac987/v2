from PyQt5.QtWidgets import QWidget, QFormLayout, QLineEdit, QSpinBox, QVBoxLayout, QPushButton, QComboBox
from PyQt5.QtCore import Qt
from controllers.produit_controller import ProduitController
from controllers.seuil_produit_controller import SeuilProduitController
from controllers.fournisseur_controller import FournisseurController
import math

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

        # Connexion des signaux pour déclencher les calculs
        self.prix_achat_ht_input.textChanged.connect(self.calculer_prix_achat_ttc)
        self.taux_tva_achat_input.textChanged.connect(self.calculer_prix_achat_ttc)
        self.prix_achat_ttc_input.textChanged.connect(self.calculer_prix_achat_ht)
        self.taux_tva_vente_input.textChanged.connect(self.calculer_prix_vente_ttc)
        self.prix_vente_ht_input.textChanged.connect(self.calculer_prix_vente_ttc)
        self.prix_vente_ttc_input.textChanged.connect(self.calculer_prix_vente_ht)

        # Boutons
        submit_button = QPushButton("Enregistrer")
        back_button = QPushButton("Retour")
        submit_button.clicked.connect(self.submit_form)
        back_button.clicked.connect(self.close_form)

        form_layout.addRow(submit_button)
        form_layout.addRow(back_button)

        layout.addLayout(form_layout)
        self.setLayout(layout)

    def arrondi_pacifique(self, montant):
        """Arrondit le montant au 0 ou 5 le plus proche."""
        return round(montant * 20) / 20  # 0.05 correspond à 1/20

    def calculer_prix_achat_ttc(self):
        try:
            prix_ht = float(self.prix_achat_ht_input.text())
            taux_tva = float(self.taux_tva_achat_input.text())
            montant_tva = prix_ht * taux_tva / 100
            prix_ttc = prix_ht + montant_tva

            self.montant_tva_achat_input.setText(str(self.arrondi_pacifique(montant_tva)))
            self.prix_achat_ttc_input.setText(str(self.arrondi_pacifique(prix_ttc)))
        except ValueError:
            pass

    def calculer_prix_achat_ht(self):
        try:
            prix_ttc = float(self.prix_achat_ttc_input.text())
            taux_tva = float(self.taux_tva_achat_input.text())
            prix_ht = prix_ttc / (1 + taux_tva / 100)
            montant_tva = prix_ttc - prix_ht

            self.montant_tva_achat_input.setText(str(self.arrondi_pacifique(montant_tva)))
            self.prix_achat_ht_input.setText(str(self.arrondi_pacifique(prix_ht)))
        except ValueError:
            pass

    def calculer_prix_vente_ttc(self):
        try:
            prix_ht = float(self.prix_vente_ht_input.text())
            taux_tva = float(self.taux_tva_vente_input.text())
            montant_tva = prix_ht * taux_tva / 100
            prix_ttc = prix_ht + montant_tva

            self.montant_tva_vente_input.setText(str(self.arrondi_pacifique(montant_tva)))
            self.prix_vente_ttc_input.setText(str(self.arrondi_pacifique(prix_ttc)))
        except ValueError:
            pass

    def calculer_prix_vente_ht(self):
        try:
            prix_ttc = float(self.prix_vente_ttc_input.text())
            taux_tva = float(self.taux_tva_vente_input.text())
            prix_ht = prix_ttc / (1 + taux_tva / 100)
            montant_tva = prix_ttc - prix_ht

            self.montant_tva_vente_input.setText(str(self.arrondi_pacifique(montant_tva)))
            self.prix_vente_ht_input.setText(str(self.arrondi_pacifique(prix_ht)))
        except ValueError:
            pass

    def submit_form(self):
        # Récupérer les données saisies et les envoyer au contrôleur
        # Comme dans le code existant...
        pass

    def close_form(self):
        self.parent().close()
