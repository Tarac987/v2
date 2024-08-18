# gui/sav_followup_form.py
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QDateEdit, QLineEdit, QComboBox, QPushButton, QMessageBox
from PyQt5.QtCore import QDate
from controllers.suivi_sav_controller import SuiviSavController
from controllers.sav_controller import SavController

class SavFollowUpForm(QDialog):
    def __init__(self, sav_id, parent=None):
        super().__init__(parent)
        self.sav_controller = SavController()
        self.suivi_sav_controller = SuiviSavController()
        self.sav_id = sav_id
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Suivi de la réparation SAV")
        layout = QVBoxLayout(self)

        # Charger les informations du SAV existant
        sav = self.sav_controller.get_sav(self.sav_id)
        if not sav:
            QMessageBox.warning(self, "Erreur", "Fiche SAV non trouvée.")
            self.reject()
            return

        # Informations du client et de l'appareil
        layout.addWidget(QLabel(f"Client: {sav.client.nom} {sav.client.prenom}"))
        layout.addWidget(QLabel(f"Appareil: {sav.marque} {sav.modele}"))
        layout.addWidget(QLabel(f"Numéro de série: {sav.numero_serie}"))

        # Formulaire de suivi
        self.date_suivi_input = QDateEdit()
        self.date_suivi_input.setCalendarPopup(True)
        self.date_suivi_input.setDate(QDate.currentDate())

        self.operation_input = QLineEdit()

        self.statut_combobox = QComboBox()
        self.statut_combobox.addItems([
            "En attente", "En diagnostic", "Devis établi", "Devis réglé", 
            "Pièces en commande", "Réparé", "Facture émise", "Sortie"
        ])

        save_button = QPushButton("Enregistrer")
        save_button.clicked.connect(self.save_follow_up)

        layout.addWidget(QLabel("Date de suivi:"))
        layout.addWidget(self.date_suivi_input)
        layout.addWidget(QLabel("Opération effectuée:"))
        layout.addWidget(self.operation_input)
        layout.addWidget(QLabel("Statut:"))
        layout.addWidget(self.statut_combobox)
        layout.addWidget(save_button)

    def save_follow_up(self):
        statut = self.statut_combobox.currentText()
        operation = self.operation_input.text().strip()
        date_suivi = self.date_suivi_input.date().toPyDate()

        if not operation:
            QMessageBox.warning(self, "Erreur", "L'opération effectuée est obligatoire.")
            return

        # Enregistrer le suivi dans la table suivi_sav
        self.suivi_sav_controller.create_suivi(
            sav_id=self.sav_id,
            date_suivi=date_suivi,
            operation=operation,
            statut=statut
        )

        # Mettre à jour le statut dans la table sav
        self.sav_controller.update_sav(self.sav_id, statut=statut)
        
        QMessageBox.information(self, "Succès", "Suivi de la réparation enregistré.")
        self.accept()
