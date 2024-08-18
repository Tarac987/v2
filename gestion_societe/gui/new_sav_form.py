from PyQt5.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QDateEdit, QComboBox, QDialog, QMessageBox
from PyQt5.QtCore import Qt, QDate
from controllers.client_controller import ClientController
from controllers.sav_controller import SavController
from gui.client_form import ClientForm

class NewSavForm(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.client_controller = ClientController()
        self.sav_controller = SavController()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        form_layout = QFormLayout()

        # Liste des clients existants
        self.client_combobox = QComboBox()
        self.load_clients()

        # Bouton pour ajouter un nouveau client
        add_client_button = QPushButton("Ajouter un nouveau client")
        add_client_button.clicked.connect(self.open_add_client_form)

        self.date_arrivee_input = QDateEdit()
        self.date_arrivee_input.setCalendarPopup(True)
        self.date_arrivee_input.setDate(QDate.currentDate())

        self.type_appareil_input = QLineEdit()
        self.marque_input = QLineEdit()
        self.modele_input = QLineEdit()
        self.numero_serie_input = QLineEdit()
        self.accessoire_input = QLineEdit()
        self.probleme_input = QLineEdit()

        # Champ de sélection du statut
        self.statut_combobox = QComboBox()
        self.statut_combobox.addItems(["En attente", "En diagnostic", "Devis établi", "Devis réglé", 
            "Pièces en commande", "Réparé", "Facture émise", "Sortie"])
        self.statut_combobox.setCurrentText("En attente")  # Définir la valeur par défaut

        form_layout.addRow("Client:", self.client_combobox)
        form_layout.addWidget(add_client_button)
        form_layout.addRow("Date d'arrivée:", self.date_arrivee_input)
        form_layout.addRow("Type d'appareil:", self.type_appareil_input)
        form_layout.addRow("Marque:", self.marque_input)
        form_layout.addRow("Modèle:", self.modele_input)
        form_layout.addRow("Numéro de série:", self.numero_serie_input)
        form_layout.addRow("Accessoires:", self.accessoire_input)
        form_layout.addRow("Problème rencontré:", self.probleme_input)
        form_layout.addRow("Statut:", self.statut_combobox)

        save_button = QPushButton("Enregistrer")
        save_button.clicked.connect(self.save_sav)
        back_button = QPushButton("Retour")
        back_button.clicked.connect(self.close_form)

        layout.addLayout(form_layout)
        layout.addWidget(save_button)
        layout.addWidget(back_button)

    def load_clients(self):
        """Charge les clients existants dans le combo box."""
        self.client_combobox.clear()
        clients = self.client_controller.get_all_clients()
        for client in clients:
            self.client_combobox.addItem(f"{client.nom} {client.prenom}", client.id)

    def open_add_client_form(self):
        """Ouvre un formulaire pour ajouter un nouveau client."""
        dialog = QDialog(self)
        dialog.setWindowTitle("Ajouter un nouveau client")
        layout = QVBoxLayout(dialog)

        client_form = ClientForm(parent=dialog)
        layout.addWidget(client_form)

        dialog.setLayout(layout)
        dialog.exec_()

        # Recharge la liste des clients après la fermeture du formulaire
        self.load_clients()

    def save_sav(self):
        client_id = self.client_combobox.currentData()
        date_arrivee = self.date_arrivee_input.date().toPyDate()
        type_appareil = self.type_appareil_input.text()
        marque = self.marque_input.text()
        modele = self.modele_input.text()
        numero_serie = self.numero_serie_input.text()
        accessoire = self.accessoire_input.text()
        probleme = self.probleme_input.text()
        statut = self.statut_combobox.currentText()  # Récupérer le statut sélectionné

        if not type_appareil or not marque or not modele or not numero_serie or not probleme:
            QMessageBox.warning(self, "Erreur", "Tous les champs sont obligatoires.")
            return

        self.sav_controller.create_sav(
            client_id=client_id,
            date_arrivee=date_arrivee,
            type_appareil=type_appareil,
            marque=marque,
            modele=modele,
            numero_serie=numero_serie,
            accessoire=accessoire,
            probleme=probleme,
            statut=statut  # Enregistrer le statut
        )
        self.parent().close()

    def close_form(self):
        self.parent().close()
