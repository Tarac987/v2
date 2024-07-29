from PyQt5 import QtWidgets

class AdminSetupDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Création Admin")
        self.setGeometry(100, 100, 300, 250)
        
        layout = QtWidgets.QFormLayout()
        
        self.nom_line_edit = QtWidgets.QLineEdit()
        self.nom_line_edit.setPlaceholderText("Entrez le nom de l'administrateur")
        self.code_personnel_line_edit = QtWidgets.QLineEdit()
        self.code_personnel_line_edit.setPlaceholderText("Entrez le code personnel")
        self.mot_de_passe_line_edit = QtWidgets.QLineEdit()
        self.mot_de_passe_line_edit.setPlaceholderText("Entrez le mot de passe")
        self.mot_de_passe_confirm_line_edit = QtWidgets.QLineEdit()
        self.mot_de_passe_confirm_line_edit.setPlaceholderText("Confirmez le mot de passe")
        
        self.mot_de_passe_line_edit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.mot_de_passe_confirm_line_edit.setEchoMode(QtWidgets.QLineEdit.Password)
        
        layout.addRow("Nom de l'administrateur:", self.nom_line_edit)
        layout.addRow("Code Personnel:", self.code_personnel_line_edit)
        layout.addRow("Mot de Passe:", self.mot_de_passe_line_edit)
        layout.addRow("Confirmer le Mot de Passe:", self.mot_de_passe_confirm_line_edit)
        
        self.setLayout(layout)
        
        self.button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        layout.addWidget(self.button_box)
        
    def accept(self):
        if self.mot_de_passe_line_edit.text() != self.mot_de_passe_confirm_line_edit.text():
            QtWidgets.QMessageBox.critical(self, "Erreur", "Les mots de passe ne correspondent pas.")
        else:
            super().accept()

    def get_data(self):
        return {
            "nom": self.nom_line_edit.text(),
            "code_personnel": self.code_personnel_line_edit.text(),
            "mot_de_passe": self.mot_de_passe_line_edit.text()
        }
