# views/entreprise_form.py
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFormLayout, QFileDialog, QHBoxLayout)
from PyQt5.QtCore import pyqtSignal
import os
from views.base_form import BaseForm

class EntrepriseForm(BaseForm):
    entreprise_info_saved = pyqtSignal()

    def __init__(self, session):
        super().__init__('Informations Entreprise')
        self.session = session
        self.initUI()
        
    def initUI(self):
        # Configuration de l'interface utilisateur
        layout = QVBoxLayout(self)

        self.nom_commercial_edit = QLineEdit()
        self.adresse_edit = QLineEdit()
        self.telephone_edit = QLineEdit()
        self.email_edit = QLineEdit()
        self.logo_path_edit = QLineEdit()
        self.capital_edit = QLineEdit()  # Champ Capital

        layout.addWidget(QLabel("Nom commercial"))
        layout.addWidget(self.nom_commercial_edit)
        layout.addWidget(QLabel("Adresse"))
        layout.addWidget(self.adresse_edit)
        layout.addWidget(QLabel("Téléphone"))
        layout.addWidget(self.telephone_edit)
        layout.addWidget(QLabel("Email"))
        layout.addWidget(self.email_edit)

        # Layout pour le champ de texte du logo et le bouton "Parcourir"
        logo_layout = QHBoxLayout()
        logo_layout.addWidget(self.logo_path_edit)
        self.browse_button = QPushButton("Parcourir")
        self.browse_button.clicked.connect(self.browse_logo)
        logo_layout.addWidget(self.browse_button)

        layout.addWidget(QLabel("Logo"))
        layout.addLayout(logo_layout)

        layout.addWidget(QLabel("Capital"))  # Étiquette Capital
        layout.addWidget(self.capital_edit)

        self.save_button = QPushButton("Enregistrer")
        self.save_button.clicked.connect(self.save_info)
        layout.addWidget(self.save_button)

        self.setLayout(layout)

    def browse_logo(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Sélectionner un logo", "", "Images (*.png *.xpm *.jpg *.jpeg *.bmp)", options=options)
        if file_name:
            self.logo_path_edit.setText(file_name)

    def save_info(self):
        # Chemin complet pour enregistrer le fichier dans le répertoire utils
        utils_folder = os.path.join(os.path.dirname(__file__), '..', 'utils')
        os.makedirs(utils_folder, exist_ok=True)
        file_path = os.path.join(utils_folder, "entreprise_info.txt")

        # Sauvegarder les informations dans un fichier texte
        with open(file_path, "w") as f:
            f.write(f"Nom commercial: {self.nom_commercial_edit.text()}\n")
            f.write(f"Adresse: {self.adresse_edit.text()}\n")
            f.write(f"Téléphone: {self.telephone_edit.text()}\n")
            f.write(f"Email: {self.email_edit.text()}\n")
            f.write(f"Logo: {self.logo_path_edit.text()}\n")
            f.write(f"Capital: {self.capital_edit.text()}\n")  # Sauvegarder le Capital
        
        self.entreprise_info_saved.emit()
        self.close()
