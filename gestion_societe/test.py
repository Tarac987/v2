import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QPushButton,
    QLabel, QFrame, QStackedWidget
)
from PyQt5.QtCore import Qt  # Importer Qt pour les alignements


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Gestion de Société")
        self.setGeometry(100, 100, 1024, 768)

        # Créer un widget central avec un layout
        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)

        # Navigation supérieure
        nav_layout = QHBoxLayout()
        dashboard_button = QPushButton("Tableau de Bord")
        caisse_button = QPushButton("Caisse")
        devis_button = QPushButton("Devis")
        factures_button = QPushButton("Factures")
        recu_button = QPushButton("Reçus")
        stocks_button = QPushButton("Gestion des Stocks")
        bank_button = QPushButton("Mouvements Bancaires")

        nav_layout.addWidget(dashboard_button)
        nav_layout.addWidget(caisse_button)
        nav_layout.addWidget(devis_button)
        nav_layout.addWidget(factures_button)
        nav_layout.addWidget(recu_button)
        nav_layout.addWidget(stocks_button)
        nav_layout.addWidget(bank_button)

        # Stacked Widget pour changer de section
        self.stack = QStackedWidget()
        self.stack.addWidget(self.create_dashboard())
        self.stack.addWidget(self.create_caisse())
        self.stack.addWidget(self.create_devis())
        self.stack.addWidget(self.create_factures())
        self.stack.addWidget(self.create_recu())
        self.stack.addWidget(self.create_stocks())
        self.stack.addWidget(self.create_bank())

        # Connecter les boutons de navigation aux widgets
        dashboard_button.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        caisse_button.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        devis_button.clicked.connect(lambda: self.stack.setCurrentIndex(2))
        factures_button.clicked.connect(lambda: self.stack.setCurrentIndex(3))
        recu_button.clicked.connect(lambda: self.stack.setCurrentIndex(4))
        stocks_button.clicked.connect(lambda: self.stack.setCurrentIndex(5))
        bank_button.clicked.connect(lambda: self.stack.setCurrentIndex(6))

        # Ajouter la navigation et le stack au layout principal
        main_layout.addLayout(nav_layout)
        main_layout.addWidget(self.stack)

        self.setCentralWidget(central_widget)

    def create_dashboard(self):
        # Tableau de bord simple
        dashboard_widget = QWidget()
        layout = QVBoxLayout(dashboard_widget)
        layout.addWidget(QLabel("Résumé des Transactions", alignment=Qt.AlignCenter))
        layout.addWidget(QLabel("Statistiques générales", alignment=Qt.AlignCenter))
        return dashboard_widget

    def create_caisse(self):
        # Gestion de la caisse
        caisse_widget = QWidget()
        layout = QVBoxLayout(caisse_widget)
        layout.addWidget(QLabel("Saisie de caisse", alignment=Qt.AlignCenter))
        layout.addWidget(QLabel("Fonctionnalités de gestion de caisse"))
        return caisse_widget

    def create_devis(self):
        # Gestion des devis
        devis_widget = QWidget()
        layout = QVBoxLayout(devis_widget)
        layout.addWidget(QLabel("Gestion des Devis", alignment=Qt.AlignCenter))
        layout.addWidget(QLabel("Création et suivi des devis"))
        return devis_widget

    def create_factures(self):
        # Gestion des factures
        factures_widget = QWidget()
        layout = QVBoxLayout(factures_widget)
        layout.addWidget(QLabel("Gestion des Factures", alignment=Qt.AlignCenter))
        layout.addWidget(QLabel("Création et suivi des factures"))
        return factures_widget

    def create_recu(self):
        # Gestion des reçus
        recu_widget = QWidget()
        layout = QVBoxLayout(recu_widget)
        layout.addWidget(QLabel("Gestion des Reçus", alignment=Qt.AlignCenter))
        layout.addWidget(QLabel("Création et suivi des reçus"))
        return recu_widget

    def create_stocks(self):
        # Gestion des stocks
        stocks_widget = QWidget()
        layout = QVBoxLayout(stocks_widget)
        layout.addWidget(QLabel("Gestion des Stocks", alignment=Qt.AlignCenter))
        layout.addWidget(QLabel("Suivi des stocks et gestion des produits"))
        return stocks_widget

    def create_bank(self):
        # Mouvements bancaires
        bank_widget = QWidget()
        layout = QVBoxLayout(bank_widget)
        layout.addWidget(QLabel("Mouvements Bancaires", alignment=Qt.AlignCenter))
        layout.addWidget(QLabel("Enregistrement des dépôts et retraits"))
        return bank_widget

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
