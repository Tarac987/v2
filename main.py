# main.py
import sys
from PyQt5 import QtWidgets
from database import engine, SessionLocal
from config import load_key
from gui.admin_setup_dialog import AdminSetupDialog
from gui.login_dialog import LoginDialog
from gui.main_window import MainWindow
from controllers.utilisateur_controller import UtilisateurController
from models.base import Base
from models.utilisateur import Utilisateur
from models.client import Client
from models.facture import Facture
from models.avoir import Avoir
from models.reglement import Reglement
import re

def setup_initial_admin():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    utilisateur_controller = UtilisateurController(db, load_key())

    if not db.query(Utilisateur).first():
        app = QtWidgets.QApplication([])
        dialog = AdminSetupDialog()
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            data = dialog.get_data()
            nom = data["nom"]
            code_personnel = data["code_personnel"]
            mot_de_passe = data["mot_de_passe"]

            if not check_password_strength(mot_de_passe):
                QtWidgets.QMessageBox.critical(None, "Erreur", "Le mot de passe doit comporter au moins 8 caractères, une majuscule, un chiffre et un caractère spécial.")
                return
            
            utilisateur_controller.create_utilisateur(nom, code_personnel, mot_de_passe, "admin")
            QtWidgets.QMessageBox.information(None, "Succès", "Administrateur créé avec succès.")
        app.quit()

def check_password_strength(password: str) -> bool:
    return (len(password) >= 8 and
            re.search(r'[A-Z]', password) and
            re.search(r'[0-9]', password) and
            re.search(r'[!@#$%^&*(),.?":{}|<>]', password))

def show_login_interface():
    app = QtWidgets.QApplication(sys.argv)
    
    db = SessionLocal()
    login_dialog = LoginDialog(db)
    if login_dialog.exec_() == QtWidgets.QDialog.Accepted:
        session = login_dialog.get_session()
        main_window = MainWindow(session)
        main_window.show()
        sys.exit(app.exec_())

def main():
    setup_initial_admin()
    show_login_interface()

if __name__ == "__main__":
    main()
