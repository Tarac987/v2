from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QTreeView, QDialog, QMessageBox, QSpinBox, QHeaderView
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt
from gui.produit_form import ProduitForm
from controllers.produit_controller import ProduitController
from controllers.seuil_produit_controller import SeuilProduitController

class StockManagementWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.produit_controller = ProduitController()
        self.seuil_controller = SeuilProduitController()

        self.setWindowTitle("Gestion de Stock")
        self.setGeometry(100, 100, 1200, 600)

        main_layout = QVBoxLayout()

        # Vue en arbre pour les produits
        self.tree_view = QTreeView()
        self.tree_view.setSelectionBehavior(QTreeView.SelectRows)
        self.tree_view.setAlternatingRowColors(True)
        self.tree_view.setUniformRowHeights(True)
        self.tree_view.doubleClicked.connect(self.handle_double_click)

        # Modèle de données
        self.model = QStandardItemModel(0, 10)
        self.model.setHorizontalHeaderLabels([
            "Référence", "Produit", "Quantité", "Prix Achat HT", "Taux TVA Achat", "Prix Achat TTC", 
            "Prix Vente HT", "Taux TVA Vente", "Prix Vente TTC", "Seuil de commande"
        ])
        self.tree_view.setModel(self.model)

        # Centrer les en-têtes des colonnes
        header = self.tree_view.header()
        header.setSectionResizeMode(QHeaderView.Stretch)
        header.setDefaultAlignment(Qt.AlignCenter)

        # Boutons d'action
        button_layout = QHBoxLayout()
        add_product_button = QPushButton("Ajouter Produit")
        edit_product_button = QPushButton("Modifier Produit")
        modify_quantity_button = QPushButton("Modifier Quantité")

        button_layout.addWidget(add_product_button)
        button_layout.addWidget(edit_product_button)
        button_layout.addWidget(modify_quantity_button)

        # Connecter les boutons
        add_product_button.clicked.connect(self.open_add_product_form)
        edit_product_button.clicked.connect(self.open_edit_product_form)
        modify_quantity_button.clicked.connect(self.open_modify_quantity_dialog)

        # Ajouter les éléments au layout principal
        main_layout.addWidget(QLabel("Gestion des Stocks", alignment=Qt.AlignCenter))
        main_layout.addWidget(self.tree_view)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

        # Charger les produits existants dans le tableau
        self.load_products()

    def load_products(self):
        self.model.removeRows(0, self.model.rowCount())  # Clear existing data
        produits = self.produit_controller.get_all_produits()

        for produit in produits:
            items = [
                QStandardItem(produit.reference_fournisseur),
                QStandardItem(produit.designation),
                QStandardItem(str(produit.quantite)),
                QStandardItem(f"{produit.prix_achat_ht:.0f}"),
                QStandardItem(f"{produit.taux_tva_achat:.0f}%"),
                QStandardItem(f"{produit.prix_achat_ttc:.0f}"),
                QStandardItem(f"{produit.prix_vente_ht:.0f}"),
                QStandardItem(f"{produit.taux_tva_vente:.0f}%"),
                QStandardItem(f"{produit.prix_vente_ttc:.0f}")
            ]

            # Ajouter le seuil de commande
            seuil = self.seuil_controller.get_seuil_by_produit(produit.id)
            seuil_val = seuil.seuil_min if seuil else "Non défini"
            items.append(QStandardItem(str(seuil_val)))

            self.model.appendRow(items)

    def handle_double_click(self, index):
        row = index.row()
        produit_id = self.produit_controller.get_all_produits()[row].id
        self.open_edit_product_form(produit_id)

    def open_add_product_form(self):
        form = ProduitForm(parent=self)
        dialog = QDialog(self)
        dialog.setWindowTitle("Ajouter un Produit")
        layout = QVBoxLayout(dialog)
        layout.addWidget(form)
        dialog.setLayout(layout)
        if dialog.exec_() == QDialog.Accepted:
            self.load_products()

    def open_edit_product_form(self, produit_id=None):
        if produit_id is None:
            current_index = self.tree_view.currentIndex()
            if not current_index.isValid():
                QMessageBox.warning(self, "Erreur", "Veuillez sélectionner un produit à modifier.")
                return
            row = current_index.row()
            produit_id = self.produit_controller.get_all_produits()[row].id

        form = ProduitForm(parent=self)
        form.load_product(produit_id)
        dialog = QDialog(self)
        dialog.setWindowTitle("Modifier un Produit")
        layout = QVBoxLayout(dialog)
        layout.addWidget(form)
        dialog.setLayout(layout)
        if dialog.exec_() == QDialog.Accepted:
            self.load_products()

    def open_modify_quantity_dialog(self):
        current_index = self.tree_view.currentIndex()
        if not current_index.isValid():
            QMessageBox.warning(self, "Erreur", "Veuillez sélectionner un produit pour modifier la quantité.")
            return

        row = current_index.row()
        product = self.produit_controller.get_all_produits()[row]
        dialog = ModifyQuantityDialog(product, self)
        if dialog.exec_() == QDialog.Accepted:
            self.load_products()
