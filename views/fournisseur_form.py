# views/fournisseur_form.py

from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QToolButton
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import QSize, Qt
from PyQt5.Qt import QStyle

from views.base_form import BaseForm
from controllers.fournisseur_controller import FournisseurController

class FournisseurForm(BaseForm):
    def __init__(self, db_session):
        super().__init__('Formulaire Fournisseur')
        self.db_session = db_session
        self.fournisseur_controller = FournisseurController(self.db_session)
        
    def init_ui(self):
        # Ajouter la légende avec une police plus petite
        self.legend_label = QLabel('* Champ obligatoire')
        legend_font = QFont()
        legend_font.setPointSize(8)
        self.legend_label.setFont(legend_font)
        
        main_layout = QVBoxLayout()
        
        main_layout.addWidget(self.legend_label, alignment=Qt.AlignTop | Qt.AlignLeft)  # Légende en haut à gauche
        
        # Ligne 1: Nom et Nom de Contact sur la même ligne
        self.nom_edit, self.nom_contact_edit, self.nom_nom_contact_layout = self.add_double_line_edit('* Société :', '* Nom du Contact:')
        
        # Ligne 2: Téléphone et Email sur la même ligne
        self.telephone_edit, self.email_edit, self.telephone_email_layout = self.add_double_line_edit('* Téléphone:', '* Email:')
        
        # Ligne 3: Adresse sur une ligne complète
        self.adresse_edit, self.adresse_layout = self.add_full_line_edit('Adresse:')
        
        # Ligne 4: Boutons Enregistrer et Annuler
        self.btn_enregistrer = self.add_button('Enregistrer')
        self.btn_annuler = self.add_button('Annuler')
        
        self.btn_enregistrer.clicked.connect(self.enregistrer_fournisseur)
        self.btn_annuler.clicked.connect(self.clear_fields)
        
        main_layout.addLayout(self.nom_nom_contact_layout)
        main_layout.addLayout(self.telephone_email_layout)
        main_layout.addLayout(self.adresse_layout)
        
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.btn_enregistrer)
        button_layout.addWidget(self.btn_annuler)
        
        main_layout.addLayout(button_layout)
        
        # Bouton Quitter en bas à droite avec icône de message critique
        footer_layout = QHBoxLayout()
        
        self.btn_quitter = QToolButton()
        style = self.btn_quitter.style()  # Obtenir le style de QToolButton
        icon = style.standardIcon(QStyle.SP_MessageBoxCritical)
        self.btn_quitter.setIcon(QIcon(icon))
        self.btn_quitter.setIconSize(QSize(24, 24))
        self.btn_quitter.setStyleSheet('background-color: red;')
        self.btn_quitter.clicked.connect(self.close)
        
        footer_layout.addStretch(1)  # Ajouter de l'espace élastique pour aligner à gauche
        footer_layout.addWidget(self.btn_quitter)  # Ajouter le bouton "Quitter"
        
        main_layout.addLayout(footer_layout)  # Ajouter le pied de page au layout principal
        
        self.setLayout(main_layout)
        
        self.set_placeholder_texts()
    
    def set_placeholder_texts(self):
        # Augmenter la taille des champs de saisie
        self.nom_edit.setFixedSize(300, 30)
        self.nom_contact_edit.setFixedSize(300, 30)
        self.telephone_edit.setFixedSize(300, 30)
        self.email_edit.setFixedSize(300, 30)
        self.adresse_edit.setFixedSize(620, 30)
        
        self.nom_edit.setPlaceholderText('Entrez le nom')
        self.nom_contact_edit.setPlaceholderText('Entrez le nom de contact')
        self.telephone_edit.setPlaceholderText('Entrez le numéro de téléphone')
        self.email_edit.setPlaceholderText("Entrez l'adresse email")
        self.adresse_edit.setPlaceholderText("Entrez l'adresse")    
    
    def add_double_line_edit(self, label1_text, label2_text):
        label1 = QLabel(label1_text)
        label2 = QLabel(label2_text)
        
        line_edit1 = QLineEdit()
        line_edit2 = QLineEdit()
        
        # Augmenter la taille des champs de saisie
        line_edit1.setFixedSize(300, 30)
        line_edit2.setFixedSize(300, 30)
        
        layout = QHBoxLayout()
        layout.addWidget(label1)
        layout.addWidget(line_edit1)
        layout.addWidget(label2)
        layout.addWidget(line_edit2)
        
        return line_edit1, line_edit2, layout

    def add_full_line_edit(self, label_text):
        label = QLabel(label_text)
        line_edit = QLineEdit()
        
        # Augmenter la taille des champs de saisie pour occuper toute la ligne
        line_edit.setFixedSize(620, 30)
        
        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(line_edit)
        
        return line_edit, layout
    
    def enregistrer_fournisseur(self):
        nom = self.nom_edit.text()
        nom_contact = self.nom_contact_edit.text()
        adresse = self.adresse_edit.text()
        telephone = self.telephone_edit.text()
        email = self.email_edit.text()
        
        if nom and nom_contact and telephone and email:  # Vérifier que tous les champs obligatoires sont remplis
            # Vérifier si le fournisseur existe déjà par email ou téléphone
            existing_fournisseur_telephone = self.fournisseur_controller.get_fournisseur_by_telephone(telephone)
            existing_fournisseur_email = self.fournisseur_controller.get_fournisseur_by_email(email)
            
            if existing_fournisseur_telephone:
                self.show_message('Erreur', 'Un fournisseur avec ce numéro de téléphone existe déjà.', QMessageBox.Warning)
                return
            if existing_fournisseur_email:
                self.show_message('Erreur', 'Un fournisseur avec cet email existe déjà.', QMessageBox.Warning)
                return
            
            # Créer le fournisseur
            fournisseur = self.fournisseur_controller.create_fournisseur(nom, nom_contact, adresse, email, telephone)
            if fournisseur:
                self.show_message('Succès', 'Fournisseur enregistré avec succès.', QMessageBox.Information)
                self.clear_fields()
        else:
            self.show_message('Erreur', 'Veuillez remplir tous les champs obligatoires.', QMessageBox.Warning)
    
    def clear_fields(self):
        self.nom_edit.clear()
        self.nom_contact_edit.clear()
        self.adresse_edit.clear()
        self.telephone_edit.clear()
        self.email_edit.clear()

