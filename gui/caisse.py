# caisse.py
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
                             QTreeWidget, QTreeWidgetItem, QTableWidget, QTableWidgetItem, QHeaderView, QInputDialog, QMessageBox, QComboBox, QRadioButton, QButtonGroup)
from PyQt5.QtCore import Qt
from sqlalchemy.orm import sessionmaker
from database import engine
from models.client import Client
from views.client_form import ClientForm
from services.pdf_generator import generate_ticket_de_caisse, show_pdf

class CaisseWidget(QWidget):
    numero_piece = 1  # Variable de classe pour le numéro de pièce comptable

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Layout principal
        caisse_layout = QVBoxLayout(self)

        # Ligne supérieure avec numéro de pièce et date/heure
        layout_ligne1 = QHBoxLayout()

        self.label_num_piece = QLabel(f'Numéro de pièce comptable: 403-{CaisseWidget.numero_piece}')
        self.label_num_piece.setFixedWidth(300)
        layout_ligne1.addWidget(self.label_num_piece, alignment=Qt.AlignLeft)

        self.label_date_heure = QLabel()
        layout_ligne1.addWidget(self.label_date_heure, alignment=Qt.AlignRight)

        caisse_layout.addLayout(layout_ligne1)

        # Champs client et bouton ajouter client
        layout_client = QHBoxLayout()

        self.label_client = QLabel('Client: ')
        self.combobox_client = QComboBox()
        self.bouton_ajouter_client = QPushButton('Ajouter Client')
        self.bouton_ajouter_client.clicked.connect(self.ajouter_client)

        layout_client.addWidget(self.label_client)
        layout_client.addWidget(self.combobox_client)
        layout_client.addWidget(self.bouton_ajouter_client)

        caisse_layout.addLayout(layout_client)

        # TreeWidget pour les articles
        self.treeview_articles = QTreeWidget()
        self.treeview_articles.setHeaderLabels(['Référence', 'Désignation', 'Quantité en stock', 'Prix HT', 'Taux TVA', 'Prix TTC'])
        self.treeview_articles.itemDoubleClicked.connect(self.selectionner_article)

        caisse_layout.addWidget(self.treeview_articles)

        # Champ de recherche pour les articles
        self.lineedit_recherche = QLineEdit()
        self.lineedit_recherche.setPlaceholderText('Rechercher un article')
        self.lineedit_recherche.textChanged.connect(self.rechercher_article)

        caisse_layout.addWidget(self.lineedit_recherche)

        # Table pour les articles sélectionnés
        self.table_articles_selectionnes = QTableWidget()
        self.table_articles_selectionnes.setColumnCount(7)
        self.table_articles_selectionnes.setHorizontalHeaderLabels(['Référence', 'Désignation', 'Quantité', 'Prix HT', 'TVA', 'Prix TTC/unité', 'Total'])
        self.table_articles_selectionnes.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        caisse_layout.addWidget(self.table_articles_selectionnes)

        # Case remise et total
        layout_total = QHBoxLayout()

        self.label_remise = QLabel('Remise (%):')
        self.lineedit_remise = QLineEdit()
        self.lineedit_remise.setFixedWidth(100)
        layout_total.addWidget(self.label_remise)
        layout_total.addWidget(self.lineedit_remise)

        self.label_total_articles = QLabel('Nombre d\'articles:')
        self.lineedit_total_articles = QLineEdit()
        self.lineedit_total_articles.setFixedWidth(100)
        self.lineedit_total_articles.setReadOnly(True)
        layout_total.addWidget(self.label_total_articles)
        layout_total.addWidget(self.lineedit_total_articles)

        self.label_total_ttc = QLabel('Total TTC:')
        self.lineedit_total_ttc = QLineEdit()
        self.lineedit_total_ttc.setFixedWidth(100)
        self.lineedit_total_ttc.setReadOnly(True)
        layout_total.addWidget(self.label_total_ttc)
        layout_total.addWidget(self.lineedit_total_ttc)

        caisse_layout.addLayout(layout_total)

        # Moyen de paiement
        layout_moyen_paiement = QHBoxLayout()
        self.label_moyen_paiement = QLabel('Moyen de paiement:')

        self.radio_espece = QRadioButton('Espèces')
        self.radio_cb = QRadioButton('Carte Bleue')
        self.radio_cheque = QRadioButton('Chèque')
        self.radio_cheque.toggled.connect(self.toggle_cheque_fields)

        self.button_group = QButtonGroup()
        self.button_group.addButton(self.radio_espece)
        self.button_group.addButton(self.radio_cb)
        self.button_group.addButton(self.radio_cheque)

        layout_moyen_paiement.addWidget(self.label_moyen_paiement)
        layout_moyen_paiement.addWidget(self.radio_espece)
        layout_moyen_paiement.addWidget(self.radio_cb)
        layout_moyen_paiement.addWidget(self.radio_cheque)

        caisse_layout.addLayout(layout_moyen_paiement)

        # Champs pour les informations de chèque
        self.layout_cheque = QVBoxLayout()

        layout_nom_prenom = QHBoxLayout()
        self.label_nom = QLabel('Nom:')
        self.lineedit_nom = QLineEdit()
        layout_nom_prenom.addWidget(self.label_nom)
        layout_nom_prenom.addWidget(self.lineedit_nom)

        self.label_prenom = QLabel('Prénom:')
        self.lineedit_prenom = QLineEdit()
        layout_nom_prenom.addWidget(self.label_prenom)
        layout_nom_prenom.addWidget(self.lineedit_prenom)

        self.layout_cheque.addLayout(layout_nom_prenom)

        layout_numero_banque = QHBoxLayout()
        self.label_numero_cheque = QLabel('Numéro de chèque:')
        self.lineedit_numero_cheque = QLineEdit()
        layout_numero_banque.addWidget(self.label_numero_cheque)
        layout_numero_banque.addWidget(self.lineedit_numero_cheque)

        self.label_banque = QLabel('Banque:')
        self.lineedit_banque = QLineEdit()
        layout_numero_banque.addWidget(self.label_banque)
        layout_numero_banque.addWidget(self.lineedit_banque)

        self.layout_cheque.addLayout(layout_numero_banque)

        caisse_layout.addLayout(self.layout_cheque)
        self.set_cheque_fields_visible(False)

        # Bouton Valider
        self.bouton_valider = QPushButton('Valider')
        self.bouton_valider.clicked.connect(self.valider_saisie)
        caisse_layout.addWidget(self.bouton_valider)

        # Bouton Imprimer
        self.bouton_imprimer = QPushButton('Imprimer')
        self.bouton_imprimer.clicked.connect(self.imprimer_saisie)
        caisse_layout.addWidget(self.bouton_imprimer)

        self.load_clients()
        self.load_articles()

    def load_clients(self):
        Session = sessionmaker(bind=engine)
        session = Session()
        clients = session.query(Client).all()
        self.combobox_client.clear()
        for client in clients:
            self.combobox_client.addItem(f"{client.nom} {client.prenom}")

    def ajouter_client(self):
        Session = sessionmaker(bind=engine)
        session = Session()
        self.client_form = ClientForm(session)
        self.client_form.client_added.connect(self.on_client_added)  # Connecter le signal
        self.client_form.show()

    def on_client_added(self):
        self.load_clients()
        self.combobox_client.setCurrentIndex(self.combobox_client.count() - 1)

    def load_articles(self):
        self.articles = [
            {'reference': 'A001', 'designation': 'Article 1', 'quantite': 10, 'prix_ht': 100, 'taux_tva': 16},
            {'reference': 'A002', 'designation': 'Article 2', 'quantite': 5, 'prix_ht': 200, 'taux_tva': 13},
            {'reference': 'A003', 'designation': 'Article 3', 'quantite': 20, 'prix_ht': 50, 'taux_tva': 0},
        ]
        for article in self.articles:
            self.add_article_to_treeview(article)

    def add_article_to_treeview(self, article):
        item = QTreeWidgetItem([
            article['reference'], 
            article['designation'], 
            str(article['quantite']), 
            f"{article['prix_ht']} €", 
            f"{article['taux_tva']} %",
            f"{article['prix_ht'] * (1 + article['taux_tva'] / 100):.2f} €"
        ])
        self.treeview_articles.addTopLevelItem(item)

    def rechercher_article(self):
        recherche = self.lineedit_recherche.text().lower()
        for i in range(self.treeview_articles.topLevelItemCount()):
            item = self.treeview_articles.topLevelItem(i)
            if recherche in item.text(1).lower():
                self.treeview_articles.setCurrentItem(item)
                break

    def selectionner_article(self, item, column):
        reference = item.text(0)
        designation = item.text(1)
        quantite = item.text(2)
        prix_ht = float(item.text(3).replace(' €', ''))
        taux_tva = float(item.text(4).replace(' %', ''))
        prix_ttc_unite = float(item.text(5).replace(' €', ''))

        row_position = self.table_articles_selectionnes.rowCount()

        # Déconnecter le signal pour éviter des boucles infinies
        try:
            self.table_articles_selectionnes.itemChanged.disconnect()
        except TypeError:
            pass

        self.table_articles_selectionnes.insertRow(row_position)

        self.table_articles_selectionnes.setItem(row_position, 0, QTableWidgetItem(reference))
        self.table_articles_selectionnes.setItem(row_position, 1, QTableWidgetItem(designation))
        self.table_articles_selectionnes.setItem(row_position, 2, QTableWidgetItem('0'))
        self.table_articles_selectionnes.setItem(row_position, 3, QTableWidgetItem(f"{prix_ht} €"))
        self.table_articles_selectionnes.setItem(row_position, 4, QTableWidgetItem(f"{taux_tva} %"))
        self.table_articles_selectionnes.setItem(row_position, 5, QTableWidgetItem(f"{prix_ttc_unite:.2f} €"))

        total_item = QTableWidgetItem(f"{prix_ttc_unite:.2f} €")
        total_item.setFlags(total_item.flags() & ~Qt.ItemIsEditable)
        self.table_articles_selectionnes.setItem(row_position, 6, total_item)

        # Reconnecter le signal
        self.table_articles_selectionnes.itemChanged.connect(self.update_total)

    def update_total(self, item):
        row = item.row()
        if item.column() == 2:  # Quantité
            try:
                quantite = int(item.text())
                prix_ttc_unite = float(self.table_articles_selectionnes.item(row, 5).text().replace(' €', ''))
                total = quantite * prix_ttc_unite
                self.table_articles_selectionnes.item(row, 6).setText(f"{total:.2f} €")
                self.calculer_total()
            except ValueError:
                QMessageBox.warning(self, 'Erreur de saisie', 'Veuillez entrer une quantité valide.')

    def calculer_total(self):
        total_ttc = 0
        total_articles = 0
        total_tva = 0
        for row in range(self.table_articles_selectionnes.rowCount()):
            quantite = int(self.table_articles_selectionnes.item(row, 2).text())
            prix_ht = float(self.table_articles_selectionnes.item(row, 3).text().replace(' €', ''))
            taux_tva = float(self.table_articles_selectionnes.item(row, 4).text().replace(' %', ''))
            total = float(self.table_articles_selectionnes.item(row, 6).text().replace(' €', ''))

            total_articles += quantite
            total_ttc += total
            total_tva += prix_ht * quantite * (taux_tva / 100)

        remise = float(self.lineedit_remise.text() or '0')
        total_ttc *= (1 - remise / 100)

        self.lineedit_total_articles.setText(str(total_articles))
        self.lineedit_total_ttc.setText(f"{total_ttc:.2f} €")
        self.total_tva = total_tva

    def valider_saisie(self):
        QMessageBox.information(self, "Validation", "Saisie validée avec succès.")
        # Implémentez ici la logique pour enregistrer les données

        # Incrémenter le numéro de pièce comptable
        CaisseWidget.numero_piece += 1
        self.label_num_piece.setText(f'Numéro de pièce comptable: 403-{CaisseWidget.numero_piece}')
        # Réinitialiser les champs pour la prochaine saisie
        self.reset_fields()

    def reset_fields(self):
        self.combobox_client.setCurrentIndex(-1)
        self.table_articles_selectionnes.setRowCount(0)
        self.lineedit_remise.clear()
        self.lineedit_total_articles.clear()
        self.lineedit_total_ttc.clear()
        self.button_group.setExclusive(False)
        self.radio_espece.setChecked(False)
        self.radio_cb.setChecked(False)
        self.radio_cheque.setChecked(False)
        self.button_group.setExclusive(True)
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
            return f'Chèque (Nom: {self.lineedit_nom.text()}, Prénom: {self.lineedit_prenom.text()}, Numéro: {self.lineedit_numero_cheque.text()}, Banque: {self.lineedit_banque.text()})'
        return 'Inconnu'

    def imprimer_saisie(self):
        client = self.combobox_client.currentText()
        moyen_paiement = self.get_moyen_paiement()
        articles = []
        for row in range(self.table_articles_selectionnes.rowCount()):
            article = {
                'reference': self.table_articles_selectionnes.item(row, 0).text(),
                'designation': self.table_articles_selectionnes.item(row, 1).text(),
                'quantite': self.table_articles_selectionnes.item(row, 2).text(),
                'prix_ht': self.table_articles_selectionnes.item(row, 3).text(),
                'tva': self.table_articles_selectionnes.item(row, 4).text(),
                'prix_ttc_unite': self.table_articles_selectionnes.item(row, 5).text(),
                'total': self.table_articles_selectionnes.item(row, 6).text()
            }
            articles.append(article)

        remise = self.lineedit_remise.text()
        total_articles = self.lineedit_total_articles.text()
        total_tva = self.total_tva
        total_ttc = self.lineedit_total_ttc.text()

        file_name, error = generate_ticket_de_caisse(CaisseWidget.numero_piece, client, moyen_paiement, articles, remise, total_articles, total_tva, total_ttc)
        if error:
            QMessageBox.warning(self, "Erreur", error)
        else:
            QMessageBox.information(self, "Impression", f"Facture générée avec succès: {file_name}")
            show_pdf(file_name)
