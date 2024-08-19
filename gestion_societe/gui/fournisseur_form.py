# fournisseur_form.py
from PyQt5.QtWidgets import QWidget, QFormLayout, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox
from controllers.fournisseur_controller import FournisseurController

class FournisseurForm(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.controller = FournisseurController()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        form_layout = QFormLayout()

        # Champs de saisie
        self.societe_input = QLineEdit()
        self.nom_input = QLineEdit()
        self.prenom_input = QLineEdit()
        self.contact_input = QLineEdit()
        self.email_input = QLineEdit()
        self.telephone_input = QLineEdit()

        # Ajout des champs au formulaire
        form_layout.addRow("Société:", self.societe_input)
        form_layout.addRow("Nom:", self.nom_input)
        form_layout.addRow("Prénom:", self.prenom_input)
        form_layout.addRow("Contact:", self.contact_input)
        form_layout.addRow("Email:", self.email_input)
        form_layout.addRow("Téléphone:", self.telephone_input)

        # Boutons
        button_layout = QHBoxLayout()
        submit_button = QPushButton("Ajouter Fournisseur")
        back_button = QPushButton("Retour")
        
        # Connexion des boutons
        submit_button.clicked.connect(self.submit_form)
        back_button.clicked.connect(self.close_form)

        # Ajout des boutons au layout
        button_layout.addWidget(submit_button)
        button_layout.addWidget(back_button)
        
        layout.addLayout(form_layout)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def submit_form(self):
        nom = self.societe_input.text().strip()
        prenom = self.prenom_input.text().strip()
        telephone = self.telephone_input.text().strip()
        societe = self.societe_input.text().strip()

        if not societe or not telephone:
            QMessageBox.warning(self, "Erreur de Validation", "Les champs Société et Téléphone sont obligatoires.")
            return
      
        contact = self.contact_input.text().strip()
        email = self.email_input.text().strip()
        self.controller.create_fournisseur(societe, nom, prenom, contact, email, telephone)
        QMessageBox.information(self, "Succès", f"Fournisseur {societe} ajouté avec succès.")

        reply = QMessageBox.question(self, "Continuer ?", "Voulez-vous ajouter un autre fournisseur ?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.clear_form()
        else:
            self.close_form()

    def clear_form(self):
        self.societe_input.clear()
        self.nom_input.clear()
        self.prenom_input.clear()
        self.contact_input.clear()
        self.email_input.clear()
        self.telephone_input.clear()

    def close_form(self):
        # Ferme la fenêtre du formulaire
        self.parent().close()
