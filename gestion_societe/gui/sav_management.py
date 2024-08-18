# gui/sav_management.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTreeView, QDialog, QHeaderView, QLabel
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt
from controllers.sav_controller import SavController
from gui.new_sav_form import NewSavForm  # Assurez-vous que ce fichier existe et est importé correctement
from gui.sav_followup_form import SavFollowUpForm  # Assurez-vous que ce fichier existe et est importé correctement

class SavManagementWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.sav_controller = SavController()

        self.setWindowTitle("Gestion du SAV")
        self.setGeometry(100, 100, 1200, 600)

        layout = QVBoxLayout(self)

        new_sav_button = QPushButton("Créer une nouvelle fiche SAV")
        new_sav_button.clicked.connect(self.open_new_sav_form)
        
        # TreeView pour afficher les fiches SAV existantes
        self.sav_tree_view = QTreeView()
        self.sav_model = QStandardItemModel(0, 7)
        self.sav_model.setHorizontalHeaderLabels(["Nom", "Prénom", "Type", "Marque", "Modèle", "Date d'arrivée", "Statut"])
        self.sav_tree_view.setModel(self.sav_model)
        self.sav_tree_view.header().setSectionResizeMode(QHeaderView.Stretch)
        self.sav_tree_view.doubleClicked.connect(self.open_sav_followup)

        layout.addWidget(new_sav_button)
        layout.addWidget(self.sav_tree_view)
        self.setLayout(layout)

        self.load_sav_data()

    def load_sav_data(self):
        """Charge toutes les fiches SAV dans le tableau."""
        self.sav_model.removeRows(0, self.sav_model.rowCount())
        sav_entries = self.sav_controller.get_all_sav()
        for sav in sav_entries:
            items = [
                QStandardItem(sav.client.nom),
                QStandardItem(sav.client.prenom),
                QStandardItem(sav.type_appareil),
                QStandardItem(sav.marque),
                QStandardItem(sav.modele),
                QStandardItem(sav.date_arrivee.strftime("%d-%m-%Y")),
                QStandardItem(sav.statut)
            ]
            self.sav_model.appendRow(items)

    def open_new_sav_form(self):
        """Ouvre le formulaire pour créer une nouvelle fiche SAV."""
        dialog = QDialog(self)
        dialog.setWindowTitle("Créer une nouvelle fiche SAV")
        layout = QVBoxLayout(dialog)
        form = NewSavForm(parent=dialog)
        layout.addWidget(form)
        dialog.setLayout(layout)
        dialog.exec_()
        self.load_sav_data()  # Recharge les fiches SAV après la création d'une nouvelle fiche

    def open_sav_followup(self, index):
        """Ouvre le formulaire de suivi pour la fiche SAV sélectionnée."""
        row = index.row()
        sav_id = self.sav_controller.get_all_sav()[row].id
        dialog = SavFollowUpForm(sav_id, parent=self)
        dialog.exec_()
        self.load_sav_data()  # Recharge les fiches SAV après le suivi
