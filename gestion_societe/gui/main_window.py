import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QPushButton,
    QLabel, QStackedWidget, QAction, QMenuBar, QDialog
)
from PyQt5.QtCore import Qt
from gui.client_form import ClientForm
from gui.fournisseur_form import FournisseurForm
from gui.produit_form import ProduitForm
from gui.stock_management import StockManagementWindow
from gui.seuil_form import SeuilForm
from gui.sav_management import SavManagementWindow
from gui.caisse_widget import CaisseWidget  # Importer CaisseWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Gestion de Société")
        self.showMaximized()  # Occupe l'intégralité de l'écran

        # Créer un widget central avec un layout
        central_widget = QWidget()
        self.layout = QVBoxLayout(central_widget)

        # Créer un menu
        menu_bar = QMenuBar(self)
        self.setMenuBar(menu_bar)

        # Menu "Gestion"
        gestion_menu = menu_bar.addMenu("Gestion")

        # Actions du menu
        client_action = QAction("Gérer les Clients", self)
        fournisseur_action = QAction("Gérer les Fournisseurs", self)
        produit_action = QAction("Gérer les Produits", self)

        # Ajouter les actions au menu
        gestion_menu.addAction(client_action)
        gestion_menu.addAction(fournisseur_action)
        gestion_menu.addAction(produit_action)

        # Connecter les actions du menu aux méthodes
        client_action.triggered.connect(self.show_client_form)
        fournisseur_action.triggered.connect(self.show_fournisseur_form)
        produit_action.triggered.connect(self.show_produit_form)

        # Menu "Configuration"
        config_menu = menu_bar.addMenu("Configuration")
        seuil_action = QAction("Seuil de Commande", self)
        config_menu.addAction(seuil_action)

        # Connecter l'action du menu "Configuration" à la méthode correspondante
        seuil_action.triggered.connect(self.show_seuil_form)

        # Navigation supérieure
        nav_layout = QHBoxLayout()
        dashboard_button = QPushButton("Tableau de Bord")
        caisse_button = QPushButton("Caisse")
        devis_button = QPushButton("Devis")
        factures_button = QPushButton("Factures")
        recu_button = QPushButton("Reçus")
        stocks_button = QPushButton("Gestion des Stocks")
        sav_button = QPushButton("SAV")
        location_button = QPushButton("Location")
        bank_button = QPushButton("Mouvements Bancaires")

        nav_layout.addWidget(dashboard_button)
        nav_layout.addWidget(caisse_button)
        nav_layout.addWidget(devis_button)
        nav_layout.addWidget(factures_button)
        nav_layout.addWidget(recu_button)
        nav_layout.addWidget(stocks_button)
        nav_layout.addWidget(sav_button)
        nav_layout.addWidget(location_button)
        nav_layout.addWidget(bank_button)

        # Stacked Widget pour changer de section
        self.stack = QStackedWidget()
        self.stack.addWidget(self.create_dashboard())
        self.stack.addWidget(self.create_caisse())  # Utilise CaisseWidget
        self.stack.addWidget(self.create_devis())
        self.stack.addWidget(self.create_factures())
        self.stack.addWidget(self.create_recu())
        self.stack.addWidget(StockManagementWindow())
        self.stack.addWidget(SavManagementWindow())
        self.stack.addWidget(self.create_location())
        self.stack.addWidget(self.create_bank())

        # Connecter les boutons de navigation aux widgets
        dashboard_button.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        caisse_button.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        devis_button.clicked.connect(lambda: self.stack.setCurrentIndex(2))
        factures_button.clicked.connect(lambda: self.stack.setCurrentIndex(3))
        recu_button.clicked.connect(lambda: self.stack.setCurrentIndex(4))
        stocks_button.clicked.connect(lambda: self.stack.setCurrentIndex(5))
        sav_button.clicked.connect(lambda: self.stack.setCurrentIndex(6))
        location_button.clicked.connect(lambda: self.stack.setCurrentIndex(7))
        bank_button.clicked.connect(lambda: self.stack.setCurrentIndex(8))

        # Ajouter la navigation et le stack au layout principal
        self.layout.addLayout(nav_layout)
        self.layout.addWidget(self.stack)

        self.setCentralWidget(central_widget)

    # Méthodes existantes pour créer les sections
    def create_dashboard(self):
        dashboard_widget = QWidget()
        layout = QVBoxLayout(dashboard_widget)
        layout.addWidget(QLabel("Résumé des Transactions", alignment=Qt.AlignCenter))
        layout.addWidget(QLabel("Statistiques générales", alignment=Qt.AlignCenter))
        return dashboard_widget

    def create_caisse(self):
        return CaisseWidget()  # Utilise le widget de caisse

    def create_devis(self):
        devis_widget = QWidget()
        layout = QVBoxLayout(devis_widget)
        layout.addWidget(QLabel("Gestion des Devis", alignment=Qt.AlignCenter))
        layout.addWidget(QLabel("Création et suivi des devis"))
        return devis_widget

    def create_factures(self):
        factures_widget = QWidget()
        layout = QVBoxLayout(factures_widget)
        layout.addWidget(QLabel("Gestion des Factures", alignment=Qt.AlignCenter))
        layout.addWidget(QLabel("Création et suivi des factures"))
        return factures_widget

    def create_recu(self):
        recu_widget = QWidget()
        layout = QVBoxLayout(recu_widget)
        layout.addWidget(QLabel("Gestion des Reçus", alignment=Qt.AlignCenter))
        layout.addWidget(QLabel("Création et suivi des reçus"))
        return recu_widget

    def create_bank(self):
        bank_widget = QWidget()
        layout = QVBoxLayout(bank_widget)
        layout.addWidget(QLabel("Mouvements Bancaires", alignment=Qt.AlignCenter))
        layout.addWidget(QLabel("Enregistrement des dépôts et retraits"))
        return bank_widget

    def create_location(self):
        location_widget = QWidget()
        layout = QVBoxLayout(location_widget)
        layout.addWidget(QLabel("Gestion des Locations", alignment=Qt.AlignCenter))
        layout.addWidget(QLabel("Fonctionnalités de gestion de location"))
        return location_widget

    # Méthodes pour ouvrir les formulaires dans des fenêtres séparées
    def show_client_form(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Gérer les Clients")
        layout = QVBoxLayout(dialog)
        form = ClientForm(parent=dialog)
        layout.addWidget(form)
        dialog.setLayout(layout)
        dialog.exec_()

    def show_fournisseur_form(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Gérer les Fournisseurs")
        layout = QVBoxLayout(dialog)
        form = FournisseurForm(parent=dialog)
        layout.addWidget(form)
        dialog.setLayout(layout)
        dialog.exec_()

    def show_produit_form(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Gérer les Produits")
        layout = QVBoxLayout(dialog)
        form = ProduitForm(parent=dialog)
        layout.addWidget(form)
        dialog.setLayout(layout)
        dialog.exec_()

    def show_seuil_form(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Configurer les Seuils de Commande")
        layout = QVBoxLayout(dialog)
        form = SeuilForm(parent=dialog)
        layout.addWidget(form)
        dialog.setLayout(layout)
        dialog.exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
