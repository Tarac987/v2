# client_form.py
from PyQt5.QtWidgets import QWidget, QFormLayout, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox
from controllers.client_controller import ClientController

class ClientForm(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.controller = ClientController()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        form_layout = QFormLayout()

        # Champs de saisie
        self.nom_input = QLineEdit()
        self.prenom_input = QLineEdit()
        self.telephone_input = QLineEdit()
        self.email_input = QLineEdit()

        # Ajout des champs au formulaire
        form_layout.addRow("Nom:", self.nom_input)
        form_layout.addRow("Prénom:", self.prenom_input)
        form_layout.addRow("Téléphone:", self.telephone_input)
        form_layout.addRow("Email:", self.email_input)

        # Boutons
        button_layout = QHBoxLayout()
        submit_button = QPushButton("Ajouter Client")
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
        nom = self.nom_input.text().strip()
        prenom = self.prenom_input.text().strip()
        telephone = self.telephone_input.text().strip()

        if not nom or not prenom or not telephone:
            QMessageBox.warning(self, "Erreur de Validation", "Les champs Nom, Prénom et Téléphone sont obligatoires.")
            return

        email = self.email_input.text().strip()
        self.controller.create_client(nom, prenom, telephone, email)
        QMessageBox.information(self, "Succès", f"Client {nom} {prenom} ajouté avec succès.")

        reply = QMessageBox.question(self, "Continuer ?", "Voulez-vous ajouter un autre client ?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.clear_form()
        else:
            self.close_form()

    def clear_form(self):
        self.nom_input.clear()
        self.prenom_input.clear()
        self.telephone_input.clear()
        self.email_input.clear()

    def close_form(self):
        # Ferme la fenêtre du formulaire
        self.parent().close()
