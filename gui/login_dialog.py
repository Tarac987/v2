from PyQt5 import QtWidgets
from controllers.utilisateur_controller import UtilisateurController
from config import load_key
from session import Session
from database import SessionLocal

class LoginDialog(QtWidgets.QDialog):
    def __init__(self, db: SessionLocal):
        super().__init__()
        self.db = db
        self.session = None
        self.setWindowTitle("Connexion")
        self.setGeometry(100, 100, 300, 150)
        
        layout = QtWidgets.QFormLayout()
        
        self.code_personnel_line_edit = QtWidgets.QLineEdit()
        self.code_personnel_line_edit.setPlaceholderText("Entrez votre code personnel")
        self.mot_de_passe_line_edit = QtWidgets.QLineEdit()
        self.mot_de_passe_line_edit.setPlaceholderText("Entrez votre mot de passe")
        
        self.mot_de_passe_line_edit.setEchoMode(QtWidgets.QLineEdit.Password)
        
        layout.addRow("Code Personnel:", self.code_personnel_line_edit)
        layout.addRow("Mot de Passe:", self.mot_de_passe_line_edit)
        
        self.setLayout(layout)
        
        self.button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.authenticate)
        self.button_box.rejected.connect(self.reject)
        layout.addWidget(self.button_box)
        
    def authenticate(self):
        code_personnel = self.code_personnel_line_edit.text()
        mot_de_passe = self.mot_de_passe_line_edit.text()
        utilisateur_controller = UtilisateurController(self.db, load_key())
        utilisateur = utilisateur_controller.authenticate_utilisateur(code_personnel, mot_de_passe)
        
        if utilisateur:
            QtWidgets.QMessageBox.information(self, "Succès", f"Bienvenue, {utilisateur.nom}!")
            self.session = Session(utilisateur)
            self.accept()
        else:
            QtWidgets.QMessageBox.critical(self, "Erreur", "Code personnel ou mot de passe incorrect.")

    def get_session(self):
        return self.session
