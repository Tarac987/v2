# views/stock_form.py

from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QComboBox, QWidget, QFrame, QToolButton
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import QStyle

from views.base_form import BaseForm
from controllers.stock_controller import StockController
from controllers.fournisseur_controller import FournisseurController
from controllers.tva_controller import TVAController

class StockForm(BaseForm):
    def __init__(self, db_session):
        self.db_session = db_session
        self.stock_controller = StockController(self.db_session)
        self.fournisseur_controller = FournisseurController(self.db_session)
        self.tva_controller = TVAController(self.db_session)
        
        self.fournisseurs = self.fournisseur_controller.get_all_fournisseurs()
        self.produits = self.stock_controller.get_all_produits()
        self.taux_tva = self.tva_controller.get_all_taux()
        
        super().__init__('Formulaire Ajouter / Modifier Produit Stock')
    
    def init_ui(self):
        
        # Ajouter la légende avec une police plus petite
        self.legend_label = QLabel('* Champ obligatoire')
        legend_font = QFont()
        legend_font.setPointSize(8)
        self.legend_label.setFont(legend_font)
        
        main_layout = QVBoxLayout()
        
        main_layout.addWidget(self.legend_label, alignment=Qt.AlignTop | Qt.AlignLeft)  # Légende en haut à gauche
       
        # Ligne de recherche en haut
        recherche_layout = QHBoxLayout()
        self.produit_combobox = QComboBox()
        self.produit_combobox.addItem("Sélectionnez un produit", -1)
        for produit in self.produits:
            self.produit_combobox.addItem(produit.nom_produit, produit.id)
        
        self.btn_rechercher = QPushButton('Rechercher')
        self.btn_rechercher.clicked.connect(self.rechercher_produit)
        
        recherche_layout.addWidget(QLabel('Rechercher Produit:'))
        recherche_layout.addWidget(self.produit_combobox)
        recherche_layout.addWidget(self.btn_rechercher)
        main_layout.addLayout(recherche_layout)
        
        # Séparateur entre la recherche et les détails
        search_separator = QFrame()
        search_separator.setFrameShape(QFrame.HLine)
        search_separator.setFrameShadow(QFrame.Sunken)
        main_layout.addWidget(search_separator)
        
        # Ligne pour Nom du Produit, Taux TVA Achat et Taux TVA Vente
        produit_tva_layout = QHBoxLayout()

        # Nom du Produit
        self.nom_produit_edit, nom_produit_label = self.add_line_edit('* Nom du Produit:', 'Entrez le nom du produit')
        produit_tva_layout.addWidget(nom_produit_label)
        produit_tva_layout.addWidget(self.nom_produit_edit)

        # Taux TVA Achat
        self.taux_tva_achat_combobox = QComboBox()
        self.taux_tva_achat_combobox.addItem("Sélectionnez un taux de TVA", -1)
        for taux in self.taux_tva:
            self.taux_tva_achat_combobox.addItem(f"{taux.taux}% - {taux.description}", taux.id)
        produit_tva_layout.addWidget(QLabel('* Taux TVA Achat:'))
        produit_tva_layout.addWidget(self.taux_tva_achat_combobox)
    
        # Taux TVA Vente
        self.taux_tva_vente_combobox = QComboBox()
        self.taux_tva_vente_combobox.addItem("Sélectionnez un taux de TVA", -1)
        for taux in self.taux_tva:
            self.taux_tva_vente_combobox.addItem(f"{taux.taux}% - {taux.description}", taux.id)
        produit_tva_layout.addWidget(QLabel('* Taux TVA Vente:'))
        produit_tva_layout.addWidget(self.taux_tva_vente_combobox)
    
        main_layout.addLayout(produit_tva_layout)
        
        # Ligne de séparation entre Nom et Détails
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        main_layout.addWidget(separator)
        
        # Tableau pour Quantité, Prix Achat HT, Prix Vente HT, Fournisseur
        details_layout = QVBoxLayout()
        
        # Créer un layout pour les labels
        labels_layout = QHBoxLayout()
        fields_layout = QHBoxLayout()
        
        # Quantité
        labels_layout.addWidget(QLabel('* Quantité:'))
        self.quantite_edit = QLineEdit()
        self.quantite_edit.setPlaceholderText('Entrez la quantité')
        self.quantite_edit.setFixedSize(300, 30)
        fields_layout.addWidget(self.quantite_edit)
        
        # Prix Achat Unitaire HT
        labels_layout.addWidget(QLabel('* Prix Achat Unitaire HT:'))
        self.prix_achat_unitaire_ht_edit = QLineEdit()
        self.prix_achat_unitaire_ht_edit.setPlaceholderText('Entrez le prix d\'achat unitaire HT')
        self.prix_achat_unitaire_ht_edit.setFixedSize(300, 30)
        fields_layout.addWidget(self.prix_achat_unitaire_ht_edit)
        
        # Prix Vente Unitaire HT
        labels_layout.addWidget(QLabel('* Prix Vente Unitaire HT:'))
        self.prix_vente_unitaire_edit = QLineEdit()
        self.prix_vente_unitaire_edit.setPlaceholderText('Entrez le prix de vente unitaire HT')
        self.prix_vente_unitaire_edit.setFixedSize(300, 30)
        fields_layout.addWidget(self.prix_vente_unitaire_edit)
        
        # Fournisseur
        labels_layout.addWidget(QLabel('* Fournisseur:'))
        self.fournisseur_combobox = QComboBox()
        for fournisseur in self.fournisseurs:
            self.fournisseur_combobox.addItem(fournisseur.nom, fournisseur.id)
        self.fournisseur_combobox.setFixedSize(300, 30)
        fields_layout.addWidget(self.fournisseur_combobox)
        
        # Ajouter les labels et les champs de saisie au layout principal
        details_layout.addLayout(labels_layout)
        details_layout.addLayout(fields_layout)
        
        main_layout.addLayout(details_layout)

        # Séparateur entre les détails et les boutons
        details_separator = QFrame()
        details_separator.setFrameShape(QFrame.HLine)
        details_separator.setFrameShadow(QFrame.Sunken)
        main_layout.addWidget(details_separator)
        
        # Boutons Enregistrer, Modifier et Supprimer
        button_layout = QHBoxLayout()
        # Création des boutons
        self.btn_enregistrer = QPushButton('Enregistrer')
        self.btn_modifier = QPushButton('Modifier')
        self.btn_supprimer = QPushButton('Supprimer')
        
        self.btn_enregistrer.clicked.connect(self.enregistrer_produit)
        self.btn_modifier.clicked.connect(self.modifier_produit)
        self.btn_supprimer.clicked.connect(self.supprimer_produit)
        
        self.btn_modifier.setEnabled(False)  # Désactiver le bouton Modifier par défaut
        
        # Création du layout pour les boutons
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.btn_enregistrer)
        button_layout.addWidget(self.btn_modifier)
        button_layout.addWidget(self.btn_supprimer)

        # Ajouter le layout des boutons au layout principal
        main_layout.addLayout(button_layout)
        
        # Bouton Quitter en bas à droite
        footer_layout = QHBoxLayout()
        
        self.btn_quitter = QToolButton()
        style = self.btn_quitter.style()  # Obtenir le style de QToolButton
        icon = style.standardIcon(QStyle.SP_MessageBoxCritical)
        self.btn_quitter.setIcon(QIcon(icon))
        self.btn_quitter.setIconSize(QSize(24, 24))
        self.btn_quitter.setStyleSheet('background-color: red; color: white;')
        self.btn_quitter.clicked.connect(self.close)
        
        footer_layout.addStretch(1)  # Ajouter de l'espace élastique pour aligner à gauche
        footer_layout.addWidget(self.btn_quitter)  # Ajouter le bouton "Quitter"
        
        main_layout.addLayout(footer_layout)  # Ajouter le pied de page au layout principal
        
        self.setLayout(main_layout)
    
    def add_line_edit(self, label_text, placeholder_text):
        label = QLabel(label_text)
        line_edit = QLineEdit()
        line_edit.setPlaceholderText(placeholder_text)
        line_edit.setFixedSize(300, 30)
        return line_edit, label
    
    def rechercher_produit(self):
        produit_id = self.produit_combobox.currentData()
        if produit_id == -1:
            QMessageBox.warning(self, 'Erreur', 'Veuillez sélectionner un produit à rechercher.')
            return
        
        produit = self.stock_controller.get_produit(produit_id)
        if produit:
            self.nom_produit_edit.setText(produit.nom_produit)
            self.quantite_edit.setText(str(produit.quantite))
            self.prix_achat_unitaire_ht_edit.setText(str(produit.prix_achat_unitaire_ht))
            self.taux_tva_achat_combobox.setCurrentIndex(self.taux_tva_achat_combobox.findData(produit.taux_tva_achat))
            self.prix_vente_unitaire_edit.setText(str(produit.prix_vente_unitaire))
            self.taux_tva_vente_combobox.setCurrentIndex(self.taux_tva_vente_combobox.findData(produit.taux_tva_vente))
            
            index = self.fournisseur_combobox.findData(produit.id_fournisseur)
            self.fournisseur_combobox.setCurrentIndex(index)
            
            self.btn_modifier.setEnabled(True)
        else:
            QMessageBox.warning(self, 'Erreur', 'Produit non trouvé.')
    
    def enregistrer_produit(self):
        nom_produit = self.nom_produit_edit.text()
        quantite = int(self.quantite_edit.text())
        prix_achat_unitaire_ht = float(self.prix_achat_unitaire_ht_edit.text())
        taux_tva_achat_id = self.taux_tva_achat_combobox.currentData()
        prix_vente_unitaire = float(self.prix_vente_unitaire_edit.text())
        taux_tva_vente_id = self.taux_tva_vente_combobox.currentData()
        id_fournisseur = self.fournisseur_combobox.currentData()
        
        if nom_produit and quantite and prix_achat_unitaire_ht and taux_tva_achat_id and prix_vente_unitaire and taux_tva_vente_id:
            produit = self.stock_controller.create_produit(
                nom_produit, quantite, prix_achat_unitaire_ht, taux_tva_achat_id,
                prix_vente_unitaire, taux_tva_vente_id, id_fournisseur)
            if produit:
                self.show_message('Succès', 'Produit enregistré avec succès.', QMessageBox.Information)
                self.clear_fields()
        else:
            self.show_message('Erreur', 'Veuillez remplir tous les champs obligatoires.', QMessageBox.Warning)
    
    def modifier_produit(self):
        produit_id = self.produit_combobox.currentData()
        if produit_id == -1:
            QMessageBox.warning(self, 'Erreur', 'Veuillez sélectionner un produit à modifier.')
            return
        
        nom_produit = self.nom_produit_edit.text()
        quantite = int(self.quantite_edit.text())
        prix_achat_unitaire_ht = float(self.prix_achat_unitaire_ht_edit.text())
        taux_tva_achat_id = self.taux_tva_achat_combobox.currentData()
        prix_vente_unitaire = float(self.prix_vente_unitaire_edit.text())
        taux_tva_vente_id = self.taux_tva_vente_combobox.currentData()
        id_fournisseur = self.fournisseur_combobox.currentData()
        
        if nom_produit and quantite and prix_achat_unitaire_ht and taux_tva_achat_id and prix_vente_unitaire and taux_tva_vente_id:
            produit = self.stock_controller.update_produit(
                produit_id, nom_produit, quantite, prix_achat_unitaire_ht, taux_tva_achat_id,
                prix_vente_unitaire, taux_tva_vente_id, id_fournisseur)
            if produit:
                self.show_message('Succès', 'Produit modifié avec succès.', QMessageBox.Information)
                self.clear_fields()
                self.btn_modifier.setEnabled(False)
                self.produit_combobox.setCurrentIndex(0)
        else:
            self.show_message('Erreur', 'Veuillez remplir tous les champs obligatoires.', QMessageBox.Warning)
    
    def supprimer_produit(self):
        produit_id = self.produit_combobox.currentData()
        if produit_id == -1:
            QMessageBox.warning(self, 'Erreur', 'Veuillez sélectionner un produit à supprimer.')
            return
        
        produit = self.stock_controller.delete_produit(produit_id)
        if produit:
            self.show_message('Succès', 'Produit supprimé avec succès.', QMessageBox.Information)
            self.clear_fields()
            self.btn_modifier.setEnabled(False)
            self.produit_combobox.setCurrentIndex(0)
    
    def clear_fields(self):
        self.nom_produit_edit.clear()
        self.quantite_edit.clear()
        self.prix_achat_unitaire_ht_edit.clear()
        self.taux_tva_achat_combobox.setCurrentIndex(0)
        self.prix_vente_unitaire_edit.clear()
        self.taux_tva_vente_combobox.setCurrentIndex(0)
        self.fournisseur_combobox.setCurrentIndex(0)
        self.btn_modifier.setEnabled(False)
        self.produit_combobox.setCurrentIndex(0)
