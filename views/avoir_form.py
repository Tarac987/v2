from PyQt5.QtWidgets import (QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QWidget, QDateEdit, QMessageBox, QTableWidget, QTableWidgetItem, QCheckBox)
from PyQt5.QtCore import Qt, QDate
from controllers.avoir_controller import AvoirController
from controllers.client_controller import ClientController
from controllers.facture_controller import FactureController
from datetime import datetime

class AvoirForm(QWidget):
    def __init__(self, db_session):
        super().__init__()
        self.db_session = db_session
        self.avoir_controller = AvoirController(self.db_session)
        self.client_controller = ClientController(self.db_session)
        self.facture_controller = FactureController(self.db_session)
        self.init_ui()
        
    def init_ui(self):
        main_layout = QVBoxLayout()

        self.legend_label = QLabel('* Champ obligatoire')
        main_layout.addWidget(self.legend_label, alignment=Qt.AlignTop | Qt.AlignLeft)

        # Client selection
        client_layout = QHBoxLayout()
        self.client_combobox = QComboBox()
        self.load_clients_combobox()
        self.client_combobox.currentIndexChanged.connect(self.load_avoirs_table)
        client_layout.addWidget(QLabel('Sélectionnez un client:'))
        client_layout.addWidget(self.client_combobox)
        main_layout.addLayout(client_layout)

        # Avoirs table
        self.avoirs_table = QTableWidget(0, 6)  # Ajout d'une colonne pour l'état soldé
        self.avoirs_table.setHorizontalHeaderLabels(['ID', 'Date Création', 'Montant Total', 'Date Validité', 'Soldé', 'Date Utilisation'])
        self.avoirs_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.avoirs_table.cellDoubleClicked.connect(self.load_selected_avoir)
        main_layout.addWidget(self.avoirs_table)

        # New Avoir fields
        new_avoir_layout = QVBoxLayout()
        self.date_creation_edit = QDateEdit(QDate.currentDate())
        self.date_creation_edit.setCalendarPopup(True)
        new_avoir_layout.addWidget(QLabel('* Date de création:'))
        new_avoir_layout.addWidget(self.date_creation_edit)
        
        self.montant_edit, montant_label = self.add_line_edit('* Montant total:', 'Entrez le montant total')
        new_avoir_layout.addWidget(montant_label)
        new_avoir_layout.addWidget(self.montant_edit)
        
        self.date_validite_edit = QDateEdit(QDate.currentDate())
        self.date_validite_edit.setCalendarPopup(True)
        new_avoir_layout.addWidget(QLabel('* Date de validité:'))
        new_avoir_layout.addWidget(self.date_validite_edit)
        
        self.facture_combobox = QComboBox()
        self.load_factures_combobox()
        new_avoir_layout.addWidget(QLabel('Sélectionnez une facture:'))
        new_avoir_layout.addWidget(self.facture_combobox)

        # Case à cocher pour "Soldé" et date d'utilisation
        self.sold_checkbox = QCheckBox('Soldé')
        self.date_utilisation_edit = QDateEdit(QDate.currentDate())
        self.date_utilisation_edit.setCalendarPopup(True)
        self.date_utilisation_edit.setDisabled(True)  # Désactiver le champ par défaut

        self.sold_checkbox.toggled.connect(self.toggle_date_utilisation)
        
        new_avoir_layout.addWidget(self.sold_checkbox)
        new_avoir_layout.addWidget(QLabel('Date d\'utilisation:'))
        new_avoir_layout.addWidget(self.date_utilisation_edit)

        button_layout = QHBoxLayout()
        self.btn_enregistrer = QPushButton('Enregistrer')
        self.btn_enregistrer.clicked.connect(self.enregistrer_avoir)
        button_layout.addWidget(self.btn_enregistrer)
        
        new_avoir_layout.addLayout(button_layout)
        main_layout.addLayout(new_avoir_layout)
        
        self.setLayout(main_layout)
        self.setWindowTitle('Formulaire Avoir Client')
        self.setGeometry(300, 300, 700, 400)
        
    def add_line_edit(self, label_text, placeholder_text):
        label = QLabel(label_text)
        line_edit = QLineEdit()
        line_edit.setPlaceholderText(placeholder_text)
        line_edit.setFixedSize(300, 30)
        return line_edit, label

    def load_clients_combobox(self):
        """ Charge tous les clients dans le combobox """
        clients = self.client_controller.get_clients()
        for client in clients:
            self.client_combobox.addItem(client.nom, client.id)

    def load_factures_combobox(self):
        """ Charge toutes les factures dans le combobox """
        factures = self.facture_controller.get_all_factures()
        for facture in factures:
            self.facture_combobox.addItem(f"Facture {facture.id} - {facture.montant_total}XPF", facture.id)

    def load_avoirs_table(self):
        """ Charge les avoirs du client sélectionné dans le tableau """
        client_id = self.client_combobox.currentData()
        if client_id:
            avoirs = self.avoir_controller.get_avoirs_client(client_id)
            self.avoirs_table.setRowCount(len(avoirs))
            for row, avoir in enumerate(avoirs):
                self.avoirs_table.setItem(row, 0, QTableWidgetItem(str(avoir.id)))
                self.avoirs_table.setItem(row, 1, QTableWidgetItem(avoir.date_creation.strftime('%Y-%m-%d')))
                self.avoirs_table.setItem(row, 2, QTableWidgetItem(f"{avoir.montant_total} XPF"))
                self.avoirs_table.setItem(row, 3, QTableWidgetItem(avoir.date_validite.strftime('%Y-%m-%d')))
                self.avoirs_table.setItem(row, 4, QTableWidgetItem('Oui' if avoir.solde else 'Non'))
                date_utilisation = avoir.date_utilisation.strftime('%Y-%m-%d') if avoir.date_utilisation else ''
                self.avoirs_table.setItem(row, 5, QTableWidgetItem(date_utilisation))

    def load_selected_avoir(self, row, column):
        """ Charge les détails de l'avoir sélectionné dans les champs de formulaire """
        avoir_id = int(self.avoirs_table.item(row, 0).text())
        avoir = self.avoir_controller.get_avoir(avoir_id)
        if avoir:
            self.date_creation_edit.setDate(QDate.fromString(avoir.date_creation.strftime('%Y-%m-%d'), 'yyyy-MM-dd'))
            self.montant_edit.setText(str(avoir.montant_total))
            self.date_validite_edit.setDate(QDate.fromString(avoir.date_validite.strftime('%Y-%m-%d'), 'yyyy-MM-dd'))
            self.facture_combobox.setCurrentIndex(self.facture_combobox.findData(avoir.id_facture))
            self.sold_checkbox.setChecked(avoir.solde)
            self.date_utilisation_edit.setDate(QDate.fromString(avoir.date_utilisation.strftime('%Y-%m-%d'), 'yyyy-MM-dd')) if avoir.date_utilisation else None
            self.date_utilisation_edit.setDisabled(not avoir.solde)  # Activer/désactiver selon le statut soldé

    def toggle_date_utilisation(self):
        """ Active ou désactive le champ de date d'utilisation en fonction de la case à cocher """
        self.date_utilisation_edit.setDisabled(not self.sold_checkbox.isChecked())

    def enregistrer_avoir(self):
        id_client = self.client_combobox.currentData()
        date_creation = self.date_creation_edit.date().toPyDate()
        montant_total = self.montant_edit.text()
        date_validite = self.date_validite_edit.date().toPyDate()
        id_facture = self.facture_combobox.currentData()
        solde = self.sold_checkbox.isChecked()
        date_utilisation = self.date_utilisation_edit.date().toPyDate() if solde else None

        if not id_client or not montant_total or not id_facture:
            QMessageBox.warning(self, 'Erreur', 'Veuillez remplir tous les champs obligatoires.')
            return

        try:
            montant_total = float(montant_total)
        except ValueError:
            QMessageBox.warning(self, 'Erreur', 'Le montant total doit être un nombre valide.')
            return

        # Vérifier le montant total par rapport à la facture
        facture = self.facture_controller.get_facture(id_facture)
        if not facture:
            QMessageBox.warning(self, 'Erreur', 'Facture non trouvée.')
            return
        
        montant_restant_a_encaisser = facture.montant_total - facture.encaissement

        if montant_total > montant_restant_a_encaisser:
            QMessageBox.warning(self, 'Erreur', 'Le montant total de l\'avoir ne peut pas dépasser le montant restant à encaisser pour la facture.')
            return

        # Créer ou mettre à jour l'avoir
        avoir = self.avoir_controller.get_avoir(self.avoirs_table.currentItem().text()) if self.avoirs_table.currentRow() >= 0 else None

        if avoir:
            # Mettre à jour l'avoir existant
            self.avoir_controller.update_avoir(
                avoir_id=avoir.id,
                montant_total=montant_total,
                date_validite=date_validite,
                solde=solde,
                date_utilisation=date_utilisation
            )
            QMessageBox.information(self, 'Succès', 'Avoir mis à jour avec succès.')
        else:
            # Créer un nouvel avoir
            self.avoir_controller.create_avoir(
                id_client=id_client,
                date_creation=date_creation,
                montant_total=montant_total,
                date_validite=date_validite,
                id_facture=id_facture
            )
            QMessageBox.information(self, 'Succès', 'Avoir enregistré avec succès.')

        self.clear_fields()

    def clear_fields(self):
        self.client_combobox.setCurrentIndex(0)
        self.date_creation_edit.setDate(QDate.currentDate())
        self.montant_edit.clear()
        self.date_validite_edit.setDate(QDate.currentDate())
        self.facture_combobox.setCurrentIndex(0)
        self.sold_checkbox.setChecked(False)
        self.date_utilisation_edit.clear()
        self.date_utilisation_edit.setDisabled(True)
        self.avoirs_table.setRowCount(0)
