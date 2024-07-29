# main_window.py
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QGridLayout, QFrame, QAction, QMenu)
from gui.caisse import CaisseWidget
from views.entreprise_form import EntrepriseForm

class MainWindow(QMainWindow):
    def __init__(self, session):
        super().__init__()
        self.session = session
        self.setWindowTitle("Tableau de Bord et Caisse")

        # Créer le widget central et le layout principal
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.main_layout = QVBoxLayout(central_widget)

        self.create_menu_bar()
        self.create_header()
        self.create_dashboard()
        self.create_caisse_interface()
        self.create_footer()

        # Afficher la fenêtre maximisée
        self.showMaximized()

    def create_menu_bar(self):
        menubar = self.menuBar()

        # Menu Fichier
        file_menu = menubar.addMenu("Fichier")
        exit_action = QAction("Quitter", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Menu Gestion
        gestion_menu = menubar.addMenu("Gestion")
        stock_action = QAction("Gestion du Stock", self)
        stock_action.triggered.connect(self.update_stock)
        gestion_menu.addAction(stock_action)
        
        client_action = QAction("Gestion des Clients", self)
        client_action.triggered.connect(self.manage_clients)
        gestion_menu.addAction(client_action)
        
        invoice_action = QAction("Gestion des Factures", self)
        invoice_action.triggered.connect(self.generate_invoice)
        gestion_menu.addAction(invoice_action)
        
        quote_action = QAction("Gestion des Devis", self)
        quote_action.triggered.connect(self.manage_quotes)
        gestion_menu.addAction(quote_action)

        delivery_note_action = QAction("Gestion des Bons de Commande", self)
        delivery_note_action.triggered.connect(self.manage_delivery_notes)
        gestion_menu.addAction(delivery_note_action)
        
        show_results_action = QAction("Afficher les Resultats", self)
        show_results_action.triggered.connect(self.show_results)
        gestion_menu.addAction(show_results_action)
        
        # Menu Parametres
        parametre_menu = menubar.addMenu("Parametres")
        entreprise_action = QAction("Informations de l'entreprise", self)
        entreprise_action.triggered.connect(self.show_entreprise_form)
        parametre_menu.addAction(entreprise_action)

        tva_action = QAction("Parametre T.V.A", self)
        tva_action.triggered.connect(self.parametre_tva)
        parametre_menu.addAction(tva_action)
        
        # Menu Aide
        help_menu = menubar.addMenu("Aide")
        about_action = QAction("À propos", self)
        about_action.triggered.connect(self.show_about_dialog)
        help_menu.addAction(about_action)

    def create_header(self):
        # Ligne supérieure avec la date/heure actuelle
        date_time_layout = QHBoxLayout()
        self.date_time_label = QLabel()
        self.update_date_time()
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update_date_time)
        timer.start(1000)
        date_time_layout.addWidget(self.date_time_label, alignment=QtCore.Qt.AlignRight)
        self.main_layout.addLayout(date_time_layout)

        # Ajouter une séparation
        self.add_separator()

        # Titre "Tableau de Bord"
        title_layout = QHBoxLayout()
        title_layout.addStretch(1)
        title_label = QLabel("Tableau de Bord")
        title_label.setAlignment(QtCore.Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        title_layout.addWidget(title_label, alignment=QtCore.Qt.AlignCenter)
        title_layout.addStretch(1)
        self.main_layout.addLayout(title_layout)

        # Ajouter une séparation
        self.add_separator()

    def create_dashboard(self):
        # Créer le tableau de bord avec les boutons d'accès
        grid_layout = QGridLayout()
        buttons = [
            ("Devis", self.manage_quotes), ("Factures", self.generate_invoice), ("Avoirs", self.manage_credits),          
            ("Agenda", self.show_agenda), ("Contacts", self.show_contacts), ("Paramètres", self.show_settings)
        ]

        for i, (text, handler) in enumerate(buttons):
            button = QPushButton(text)
            button.clicked.connect(handler)
            grid_layout.addWidget(button, i // 4, i % 4)

        self.main_layout.addLayout(grid_layout)

        # Ajouter une séparation
        self.add_separator()

    def create_caisse_interface(self):
        caisse_widget = CaisseWidget()
        self.main_layout.addWidget(caisse_widget)

    def create_footer(self):
        # Ajouter une séparation
        self.add_separator()

        # Ajouter les boutons Aide et Quitter en bas
        bottom_layout = QHBoxLayout()
        aide_button = QPushButton("Aide")
        bottom_layout.addWidget(aide_button, alignment=QtCore.Qt.AlignLeft)
        quitter_button = QPushButton("Quitter")
        quitter_button.clicked.connect(self.close)
        bottom_layout.addWidget(quitter_button, alignment=QtCore.Qt.AlignRight)
        self.main_layout.addLayout(bottom_layout)

    def add_separator(self):
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        self.main_layout.addWidget(separator)

    def update_date_time(self):
        current_date_time = QtCore.QDateTime.currentDateTime().toString("ddd. dd MMM yyyy HH:mm:ss")
        self.date_time_label.setText(current_date_time)

    def manage_quotes(self):
        QtWidgets.QMessageBox.information(self, "Devis", "Accès à la gestion des devis.")
    
    def generate_invoice(self):
        QtWidgets.QMessageBox.information(self, "Factures", "Accès à la gestion des factures.")
    
    def manage_credits(self):
        QtWidgets.QMessageBox.information(self, "Avoirs", "Accès à la gestion des avoirs.")
    
    def manage_cash(self):
        QtWidgets.QMessageBox.information(self, "Caisse", "Accès à la gestion de la caisse.")
    
    def manage_clients(self):
        QtWidgets.QMessageBox.information(self, "Clients", "Accès à la gestion des clients.")
    
    def manage_suppliers(self):
        QtWidgets.QMessageBox.information(self, "Fournisseurs", "Accès à la gestion des fournisseurs.")
    
    def update_stock(self):
        QtWidgets.QMessageBox.information(self, "Stock", "Accès à la gestion des stocks.")
    
    def show_results(self):
        QtWidgets.QMessageBox.information(self, "Résultats", "Affichage des résultats.")
    
    def show_agenda(self):
        QtWidgets.QMessageBox.information(self, "Agenda", "Affichage de l'agenda.")
    
    def show_contacts(self):
        QtWidgets.QMessageBox.information(self, "Contacts", "Affichage des contacts.")
    
    def show_settings(self):
        QtWidgets.QMessageBox.information(self, "Paramètres", "Accès aux paramètres.")

    def show_about_dialog(self):
        QtWidgets.QMessageBox.information(self, "À propos", "Logiciel de gestion SAS Hotua Services.")

    def manage_delivery_notes(self):
        QtWidgets.QMessageBox.information(self, "Bons de commande", "Accès à la gestion des bons de commande.")
        
    def parametre_tva(self):
        QtWidgets.QMessageBox.information(self, "Parametre TVA")

    def show_entreprise_form(self):
        self.entreprise_form = EntrepriseForm(self.session)
        self.entreprise_form.entreprise_info_saved.connect(self.on_entreprise_info_saved)
        self.entreprise_form.show()
    def on_entreprise_info_saved(self):
        QtWidgets.QMessageBox.information(self, "Informations Entreprise", "Les informations de l'entreprise ont été sauvegardées.")
    
