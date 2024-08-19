# caisse_widget.py
import os
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
                             QTreeWidget, QTreeWidgetItem, QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox, QComboBox, QRadioButton, QButtonGroup, QDialog)
from PyQt5.QtCore import Qt
from datetime import datetime
from controllers.client_controller import ClientController
from controllers.produit_controller import ProduitController
from controllers.transaction_vente_controller import TransactionVenteController
from controllers.ligne_vente_controller import LigneVenteController
from utils.piece_counter import get_numero_piece, save_numero_piece
from services.pdf_generator import generate_ticket_de_caisse, show_pdf
from gui.client_form import ClientForm

class CaisseWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.client_controller = ClientController()
        self.produit_controller = ProduitController()
        self.transaction_vente_controller = TransactionVenteController()
        self.ligne_vente_controller = LigneVenteController()
        self.numero_piece = get_numero_piece()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)
        
        # Numéro de pièce et date
        layout_ligne1 = QHBoxLayout()
        self.label_num_piece = QLabel(f'Numéro de Ticket de Caisse : {self.numero_piece}')
        self.label_date_heure = QLabel(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        layout_ligne1.addWidget(self.label_num_piece)
        layout_ligne1.addWidget(self.label_date_heure)
        layout.addLayout(layout_ligne1)

        # Sélection client
        layout_client = QHBoxLayout()
        self.label_client = QLabel('Client: ')
        self.combobox_client = QComboBox()
        self.bouton_ajouter_client = QPushButton('Ajouter Client')
        self.bouton_ajouter_client.clicked.connect(self.ajouter_client)
        layout_client.addWidget(self.label_client)
        layout_client.addWidget(self.combobox_client)
        layout_client.addWidget(self.bouton_ajouter_client)
        layout.addLayout(layout_client)

        # TreeWidget pour les articles
        self.treeview_articles = QTreeWidget()
        self.treeview_articles.setHeaderLabels(['Référence', 'Désignation', 'Quantité en stock', 'Prix HT', 'Taux TVA', 'Prix TTC'])

        # Répartition équitable des colonnes
        header = self.treeview_articles.header()
        header.setSectionResizeMode(QHeaderView.Stretch)

        # Centrer les en-têtes
        for i in range(header.count()):
            header.setDefaultAlignment(Qt.AlignCenter)

        self.treeview_articles.itemDoubleClicked.connect(self.selectionner_article)
        layout.addWidget(self.treeview_articles)

        # Recherche d'articles
        self.lineedit_recherche = QLineEdit()
        self.lineedit_recherche.setPlaceholderText('Rechercher un article')
        self.lineedit_recherche.textChanged.connect(self.rechercher_article)
        layout.addWidget(self.lineedit_recherche)

        # Table des articles sélectionnés
        self.table_articles_selectionnes = QTableWidget()
        self.table_articles_selectionnes.setColumnCount(7)
        self.table_articles_selectionnes.setHorizontalHeaderLabels(['Référence', 'Désignation', 'Quantité', 'Prix HT', 'TVA', 'Prix TTC/unité', 'Total'])
        self.table_articles_selectionnes.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table_articles_selectionnes)

        # Totaux et remise
        layout_total = QVBoxLayout()
        self.label_total_ht = QLabel('Total HT: 0 XPF')
        self.label_total_tva = QLabel('Montant TVA: 0 XPF')
        self.label_total_ttc = QLabel('Total TTC: 0 XPF')
        layout_total.addWidget(self.label_total_ht)
        layout_total.addWidget(self.label_total_tva)
        layout_total.addWidget(self.label_total_ttc)
        layout.addLayout(layout_total)

        # Moyen de paiement
        layout_moyen_paiement = QHBoxLayout()
        self.radio_espece = QRadioButton('Espèces')
        self.radio_cb = QRadioButton('Carte Bleue')
        self.radio_cheque = QRadioButton('Chèque')
        self.radio_cheque.toggled.connect(self.toggle_cheque_fields)
        self.button_group = QButtonGroup()
        self.button_group.addButton(self.radio_espece)
        self.button_group.addButton(self.radio_cb)
        self.button_group.addButton(self.radio_cheque)
        layout_moyen_paiement.addWidget(self.radio_espece)
        layout_moyen_paiement.addWidget(self.radio_cb)
        layout_moyen_paiement.addWidget(self.radio_cheque)
        layout.addLayout(layout_moyen_paiement)

        # Champs spécifiques pour le paiement par chèque
        self.layout_cheque = QVBoxLayout()
        self.label_nom = QLabel('Nom:')
        self.lineedit_nom = QLineEdit()
        self.label_prenom = QLabel('Prénom:')
        self.lineedit_prenom = QLineEdit()
        self.label_numero_cheque = QLabel('Numéro de chèque:')
        self.lineedit_numero_cheque = QLineEdit()
        self.label_banque = QLabel('Banque:')
        self.lineedit_banque = QLineEdit()

        self.layout_cheque.addWidget(self.label_nom)
        self.layout_cheque.addWidget(self.lineedit_nom)
        self.layout_cheque.addWidget(self.label_prenom)
        self.layout_cheque.addWidget(self.lineedit_prenom)
        self.layout_cheque.addWidget(self.label_numero_cheque)
        self.layout_cheque.addWidget(self.lineedit_numero_cheque)
        self.layout_cheque.addWidget(self.label_banque)
        self.layout_cheque.addWidget(self.lineedit_banque)
        layout.addLayout(self.layout_cheque)

        self.set_cheque_fields_visible(False)  # Masquer par défaut

        self.bouton_valider = QPushButton('Valider et Imprimer')
        self.bouton_valider.clicked.connect(self.valider_transaction)
        layout.addWidget(self.bouton_valider)

        self.setLayout(layout)

        self.load_clients()
        self.load_articles()

    def ajouter_client(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Ajouter un Client")
        layout = QVBoxLayout(dialog)
        client_form = ClientForm(parent=dialog)
        layout.addWidget(client_form)
        dialog.setLayout(layout)
        dialog.exec_()
        self.load_clients()

    def load_clients(self):
        clients = self.client_controller.get_all_clients()
        self.combobox_client.clear()
        for client in clients:
            self.combobox_client.addItem(f"{client.nom} {client.prenom}", client.id)

    def load_articles(self):
        produits = self.produit_controller.get_all_produits()
        self.treeview_articles.clear()
        for produit in produits:
            item = QTreeWidgetItem([
                str(produit.id),
                produit.designation,
                str(produit.quantite),
                f"{produit.prix_vente_ht:.2f} XPF",
                f"{produit.taux_tva_vente:.2f} %",
                f"{produit.prix_vente_ttc:.2f} XPF"
            ])
            self.treeview_articles.addTopLevelItem(item)

    def rechercher_article(self):
        recherche = self.lineedit_recherche.text().lower()
        for i in range(self.treeview_articles.topLevelItemCount()):
            item = self.treeview_articles.topLevelItem(i)
            item.setHidden(recherche not in item.text(1).lower())

    def selectionner_article(self, item, column):
        reference = item.text(0)
        designation = item.text(1)
        quantite = 1
        prix_ht = float(item.text(3).replace(' XPF', ''))
        taux_tva = float(item.text(4).replace(' %', ''))
        prix_ttc_unite = float(item.text(5).replace(' XPF', ''))

        row_position = self.table_articles_selectionnes.rowCount()
        self.table_articles_selectionnes.insertRow(row_position)
        self.table_articles_selectionnes.setItem(row_position, 0, QTableWidgetItem(reference))
        self.table_articles_selectionnes.setItem(row_position, 1, QTableWidgetItem(designation))
        self.table_articles_selectionnes.setItem(row_position, 2, QTableWidgetItem(str(quantite)))
        self.table_articles_selectionnes.setItem(row_position, 3, QTableWidgetItem(f"{prix_ht:.2f} XPF"))
        self.table_articles_selectionnes.setItem(row_position, 4, QTableWidgetItem(f"{taux_tva:.2f} %"))
        self.table_articles_selectionnes.setItem(row_position, 5, QTableWidgetItem(f"{prix_ttc_unite:.2f} XPF"))
        self.table_articles_selectionnes.setItem(row_position, 6, QTableWidgetItem(f"{prix_ttc_unite:.2f} XPF"))

        self.update_total()

    def update_total(self):
        total_ht = 0
        total_tva = 0
        total_ttc = 0
        for row in range(self.table_articles_selectionnes.rowCount()):
            quantite = int(self.table_articles_selectionnes.item(row, 2).text())
            prix_ht = float(self.table_articles_selectionnes.item(row, 3).text().replace(' XPF', ''))
            taux_tva = float(self.table_articles_selectionnes.item(row, 4).text().replace(' %', ''))
            total_article = quantite * prix_ht * (1 + taux_tva / 100)
            total_ht += prix_ht * quantite
            total_tva += prix_ht * quantite * (taux_tva / 100)
            total_ttc += total_article

        remise = float(self.lineedit_remise.text() or '0')
        total_ttc *= (1 - remise / 100)

        self.label_total_ht.setText(f'Total HT: {total_ht:.2f} XPF')
        self.label_total_tva.setText(f'Montant TVA: {total_tva:.2f} XPF')
        self.label_total_ttc.setText(f'Total TTC: {total_ttc:.2f} XPF')
        self.lineedit_total_ttc.setText(f"{total_ttc:.2f} XPF")

    def valider_transaction(self):
        client_id = self.combobox_client.currentData()
        moyen_paiement = self.get_moyen_paiement()

        cheque_nom = self.lineedit_nom.text() if self.radio_cheque.isChecked() else None
        cheque_prenom = self.lineedit_prenom.text() if self.radio_cheque.isChecked() else None
        cheque_numero = self.lineedit_numero_cheque.text() if self.radio_cheque.isChecked() else None
        cheque_banque = self.lineedit_banque.text() if self.radio_cheque.isChecked() else None

        articles = []
        total_ht = 0
        total_tva = 0
        total_ttc = float(self.lineedit_total_ttc.text().replace(' XPF', '') or "0")

        for row in range(self.table_articles_selectionnes.rowCount()):
            reference = self.table_articles_selectionnes.item(row, 0).text()
            quantite = int(self.table_articles_selectionnes.item(row, 2).text())
            prix_ht = float(self.table_articles_selectionnes.item(row, 3).text().replace(' XPF', ''))
            taux_tva = float(self.table_articles_selectionnes.item(row, 4).text().replace(' %', ''))
            total_article = quantite * prix_ht * (1 + taux_tva / 100)
            articles.append({
                'reference': reference,
                'quantite': quantite,
                'prix_unitaire': prix_ht,
                'tva': taux_tva,
                'prix_total': total_article
            })
            total_ht += prix_ht * quantite
            total_tva += prix_ht * quantite * (taux_tva / 100)

        transaction = self.transaction_vente_controller.create_transaction_vente(
            client_id=client_id,
            total_ht=total_ht,
            tva_total_encaisse=total_tva,
            total_ttc=total_ttc,
            moyen_paiement=moyen_paiement,
            cheque_nom=cheque_nom,
            cheque_prenom=cheque_prenom,
            cheque_numero=cheque_numero,
            cheque_banque=cheque_banque
        )

        for article in articles:
            self.ligne_vente_controller.create_ligne_vente(
                transaction_id=transaction.id,
                produit_id=article['reference'],
                quantite=article['quantite'],
                prix_unitaire=article['prix_unitaire'],
                tva=article['tva'],
                prix_total=article['prix_total']
            )

        date_du_jour = datetime.now().strftime("%Y-%m-%d")
        dossier_archive = os.path.join("archive", "caisse", date_du_jour)
        os.makedirs(dossier_archive, exist_ok=True)

        file_name, error = generate_ticket_de_caisse(
            self.numero_piece, 
            self.combobox_client.currentText(),
            moyen_paiement,
            articles,
            0,
            len(articles),
            total_tva,
            total_ttc
        )
        if not error:
            os.rename(file_name, os.path.join(dossier_archive, os.path.basename(file_name)))
            show_pdf(os.path.join(dossier_archive, os.path.basename(file_name)))
            self.numero_piece += 1
            save_numero_piece(self.numero_piece)
            self.label_num_piece.setText(f'Numéro de Ticket de Caisse : {self.numero_piece}')
            self.reset_fields()

    def reset_fields(self):
        self.combobox_client.setCurrentIndex(-1)
        self.table_articles_selectionnes.setRowCount(0)
        self.lineedit_remise.clear()
        self.lineedit_total_ttc.clear()
        self.set_cheque_fields_visible(False)

    def toggle_cheque_fields(self):
        self.set_cheque_fields_visible(self.radio_cheque.isChecked())

    def set_cheque_fields_visible(self, visible):
        self.label_nom.setVisible(visible)
        self.lineedit_nom.setVisible(visible)
        self.label_prenom.setVisible(visible)
        self.lineedit_prenom.setVisible(visible)
        self.label_numero_cheque.setVisible(visible)
        self.lineedit_numero_cheque.setVisible(visible)
        self.label_banque.setVisible(visible)
        self.lineedit_banque.setVisible(visible)

    def get_moyen_paiement(self):
        if self.radio_espece.isChecked():
            return 'Espèces'
        elif self.radio_cb.isChecked():
            return 'Carte Bleue'
        elif self.radio_cheque.isChecked():
            return 'Chèque'
        return 'Inconnu'
