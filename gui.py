import sys
import re
from PyQt5 import QtWidgets, QtCore
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.base import Base
from models.utilisateur import Utilisateur
from controllers.utilisateur_controller import UtilisateurController
from utils.security import generate_key, load_key

# Configuration de la base de données
DATABASE_URL = "sqlite:///./hotua_db.sqlite3"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

def setup_initial_admin():
    print("Début de la configuration initiale de l'administrateur...")
    Base.metadata.create_all(bind=engine)
    utilisateur_controller = UtilisateurController(db, load_key())

    if not db.query(Utilisateur).first():
        print("Aucun utilisateur trouvé. Affichage de la boîte de dialogue de configuration.")
        app = QtWidgets.QApplication([])
        dialog = AdminSetupDialog(utilisateur_controller)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            data = dialog.get_data()
            nom = data["nom"]
            code_personnel = data["code_personnel"]
            mot_de_passe = data["mot_de_passe"]
            mot_de_passe_confirm = data["mot_de_passe_confirm"]

            if mot_de_passe != mot_de_passe_confirm:
                QtWidgets.QMessageBox.critical(None, "Erreur", "Les mots de passe ne correspondent pas.")
                print("Les mots de passe ne correspondent pas.")
                return
            
            if not check_password_strength(mot_de_passe):
                QtWidgets.QMessageBox.critical(None, "Erreur", "Le mot de passe doit comporter au moins 8 caractères, une majuscule, un chiffre et un caractère spécial.")
                print("Mot de passe invalide.")
                return
            
            utilisateur_controller.create_utilisateur(nom, code_personnel, mot_de_passe, "admin")
            QtWidgets.QMessageBox.information(None, "Succès", "Administrateur créé avec succès.")
            print("Administrateur créé avec succès.")
        app.quit()
    else:
        print("Un utilisateur existe déjà. Aucun besoin de configuration initiale.")

def check_password_strength(password: str) -> bool:
    return (len(password) >= 8 and
            re.search(r'[A-Z]', password) and
            re.search(r'[0-9]', password) and
            re.search(r'[!@#$%^&*(),.?":{}|<>]', password))

class AdminSetupDialog(QtWidgets.QDialog):
    def __init__(self, utilisateur_controller):
        super().__init__()
        self.utilisateur_controller = utilisateur_controller
        self.setWindowTitle("Création Admin")
        self.setGeometry(100, 100, 300, 300)
        
        layout = QtWidgets.QFormLayout()
        
        self.nom_line_edit = QtWidgets.QLineEdit()
        self.code_personnel_line_edit = QtWidgets.QLineEdit()
        self.mot_de_passe_line_edit = QtWidgets.QLineEdit()
        self.mot_de_passe_confirm_line_edit = QtWidgets.QLineEdit()
        
        # Configuration des placeholders
        self.nom_line_edit.setPlaceholderText("Entrez le nom complet de l'administrateur")
        self.code_personnel_line_edit.setPlaceholderText("Entrez le code personnel (identifiant unique)")
        self.mot_de_passe_line_edit.setPlaceholderText("Entrez un mot de passe (min. 8 caractères, 1 majuscule, 1 chiffre, 1 caractère spécial)")
        self.mot_de_passe_confirm_line_edit.setPlaceholderText("Confirmez le mot de passe")
        
        # Configuration des info-bulles
        self.nom_line_edit.setToolTip("Nom complet de l'administrateur")
        self.code_personnel_line_edit.setToolTip("Code personnel pour la connexion")
        self.mot_de_passe_line_edit.setToolTip("Le mot de passe doit comporter au moins 8 caractères, une majuscule, un chiffre et un caractère spécial")
        self.mot_de_passe_confirm_line_edit.setToolTip("Confirmez le mot de passe en le saisissant à nouveau")
        
        self.mot_de_passe_line_edit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.mot_de_passe_confirm_line_edit.setEchoMode(QtWidgets.QLineEdit.Password)
        
        layout.addRow("Nom de l'administrateur:", self.nom_line_edit)
        layout.addRow("Code Personnel:", self.code_personnel_line_edit)
        layout.addRow("Mot de Passe:", self.mot_de_passe_line_edit)
        layout.addRow("Confirmer le Mot de Passe:", self.mot_de_passe_confirm_line_edit)
        
        self.setLayout(layout)
        
        self.button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.validate_inputs)
        self.button_box.rejected.connect(self.reject)
        layout.addWidget(self.button_box)
        
    def validate_inputs(self):
        mot_de_passe = self.mot_de_passe_line_edit.text()
        mot_de_passe_confirm = self.mot_de_passe_confirm_line_edit.text()

        if mot_de_passe != mot_de_passe_confirm:
            QtWidgets.QMessageBox.critical(self, "Erreur", "Les mots de passe ne correspondent pas.")
            return

        if not check_password_strength(mot_de_passe):
            QtWidgets.QMessageBox.critical(self, "Erreur", "Le mot de passe doit comporter au moins 8 caractères, une majuscule, un chiffre et un caractère spécial.")
            return
        
        self.accept()

    def get_data(self):
        return {
            "nom": self.nom_line_edit.text(),
            "code_personnel": self.code_personnel_line_edit.text(),
            "mot_de_passe": self.mot_de_passe_line_edit.text(),
            "mot_de_passe_confirm": self.mot_de_passe_confirm_line_edit.text()
        }

class LoginDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Connexion")
        self.setGeometry(100, 100, 300, 150)
        
        layout = QtWidgets.QFormLayout()
        
        self.code_personnel_line_edit = QtWidgets.QLineEdit()
        self.mot_de_passe_line_edit = QtWidgets.QLineEdit()
        
        # Configuration des placeholders
        self.code_personnel_line_edit.setPlaceholderText("Entrez votre code personnel")
        self.mot_de_passe_line_edit.setPlaceholderText("Entrez votre mot de passe")
        
        # Configuration des info-bulles
        self.code_personnel_line_edit.setToolTip("Code personnel utilisé pour la connexion")
        self.mot_de_passe_line_edit.setToolTip("Mot de passe associé à votre code personnel")
        
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
        utilisateur_controller = UtilisateurController(db, load_key())
        utilisateur = utilisateur_controller.authenticate_utilisateur(code_personnel, mot_de_passe)
        
        if utilisateur:
            QtWidgets.QMessageBox.information(self, "Succès", f"Bienvenue, {utilisateur.nom}!")
            self.accept()
        else:
            QtWidgets.QMessageBox.critical(self, "Erreur", "Code personnel ou mot de passe incorrect.")

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, utilisateur):
        super().__init__()
        self.utilisateur = utilisateur
        self.setWindowTitle(f"Bienvenue {utilisateur.nom}")
        self.setGeometry(100, 100, 800, 600)

        label = QtWidgets.QLabel(f"Bienvenue {utilisateur.nom}", self)
        label.setAlignment(QtCore.Qt.AlignCenter)
        self.setCentralWidget(label)

def main():
    app = QtWidgets.QApplication(sys.argv)
    
    print("Chargement de la clé de cryptage...")
    try:
        load_key()
    except FileNotFoundError:
        print("Clé non trouvée. Génération de la clé...")
        generate_key()
    
    print("Configuration de l'administrateur...")
    setup_initial_admin()
    
    print("Affichage de la boîte de dialogue de connexion...")
    login_dialog = LoginDialog()
    if login_dialog.exec_() == QtWidgets.QDialog.Accepted:
        utilisateur = UtilisateurController(db, load_key()).get_utilisateur_by_code_personnel(login_dialog.code_personnel_line_edit.text())
        main_window = MainWindow(utilisateur)
        main_window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
