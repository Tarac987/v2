from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QToolButton
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import QSize, Qt, pyqtSignal
from PyQt5.Qt import QStyle

from views.base_form import BaseForm
from controllers.client_controller import ClientController

class ClientForm(BaseForm):
    client_added = pyqtSignal()  # Signal personnalisé

    def __init__(self, db_session):
        super().__init__('Formulaire Client')
        self.db_session = db_session
        self.client_controller = ClientController(self.db_session)
        self.init_ui()
        
    def init_ui(self):
        # Ajouter la légende avec une police plus petite
        self.legend_label = QLabel('* Champ obligatoire')
        legend_font = QFont()
        legend_font.setPointSize(8)
        self.legend_label.setFont(legend_font)
        
        main_layout = QVBoxLayout()
        
        main_layout.addWidget(self.legend_label, alignment=Qt.AlignTop | Qt.AlignLeft)  # Légende en haut à gauche
        
        # Ligne 1: Nom et Prénom sur la même ligne
        self.nom_edit, self.prenom_edit, self.nom_prenom_layout = self.add_double_line_edit('* Nom:', '* Prénom:')
        
        # Ligne 2: Téléphone et Email sur la même ligne
        self.telephone_edit, self.email_edit, self.telephone_email_layout = self.add_double_line_edit('* Téléphone:', 'Email:')
        
        # Ligne 3: Boutons Enregistrer et Annuler
        self.btn_enregistrer = self.add_button('Enregistrer')
        self.btn_annuler = self.add_button('Annuler')
        
        self.btn_enregistrer.clicked.connect(self.enregistrer_client)
        self.btn_annuler.clicked.connect(self.clear_fields)
        
        main_layout.addLayout(self.nom_prenom_layout)
        main_layout.addLayout(self.telephone_email_layout)
        
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
        
        # Indication sur les champs obligatoires
        self.set_placeholder_texts()
    
    def set_placeholder_texts(self):
        # Augmenter la taille des champs de saisie
        self.nom_edit.setFixedSize(300, 30)
        self.prenom_edit.setFixedSize(300, 30)
        self.telephone_edit.setFixedSize(300, 30)
        self.email_edit.setFixedSize(300, 30)
        
        self.nom_edit.setPlaceholderText('Entrez le nom')
        self.prenom_edit.setPlaceholderText('Entrez le prénom')
        self.telephone_edit.setPlaceholderText('Entrez le numéro de téléphone')
        self.email_edit.setPlaceholderText("Entrez l'adresse email")    
    
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
    
    def enregistrer_client(self):
        nom = self.nom_edit.text()
        prenom = self.prenom_edit.text()  # Capture le prénom
        telephone = self.telephone_edit.text()
        email = self.email_edit.text()
        
        if nom and prenom and telephone:  # Vérifier que Nom, Prénom et Téléphone sont remplis
            # Vérifier si le client existe déjà par téléphone
            existing_client_telephone = self.client_controller.get_client_by_telephone(telephone)
            
            if existing_client_telephone:
                self.show_message('Erreur', 'Un client avec ce numéro de téléphone existe déjà.', QMessageBox.Warning)
                return
            
            # Créer le client
            client = self.client_controller.create_client(nom, prenom, telephone, email)
            if client:
                self.show_message('Succès', 'Client enregistré avec succès.', QMessageBox.Information)
                self.clear_fields()
                self.client_added.emit()  # Émettre le signal
                self.close()  # Fermer le formulaire
        else:
            self.show_message('Erreur', 'Veuillez remplir tous les champs obligatoires.', QMessageBox.Warning)
    
    def clear_fields(self):
        self.nom_edit.clear()
        self.prenom_edit.clear()
        self.telephone_edit.clear()
        self.email_edit.clear()
