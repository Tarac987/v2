# gui/seuil_form.py
from PyQt5.QtWidgets import QWidget, QFormLayout, QComboBox, QSpinBox, QPushButton, QVBoxLayout
from controllers.produit_controller import ProduitController
from controllers.seuil_produit_controller import SeuilProduitController

class SeuilForm(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.produit_controller = ProduitController()
        self.seuil_controller = SeuilProduitController()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        form_layout = QFormLayout()

        self.produit_combobox = QComboBox()
        produits = self.produit_controller.get_all_produits()
        for produit in produits:
            self.produit_combobox.addItem(produit.designation, produit.id)

        self.seuil_min_input = QSpinBox()
        self.seuil_min_input.setRange(1, 1000)

        form_layout.addRow("Produit:", self.produit_combobox)
        form_layout.addRow("Seuil de commande:", self.seuil_min_input)

        save_button = QPushButton("Enregistrer")
        back_button = QPushButton("Retour")
        save_button.clicked.connect(self.save_seuil)
        back_button.clicked.connect(self.close_form)

        layout.addLayout(form_layout)
        layout.addWidget(save_button)
        layout.addWidget(back_button)
        self.setLayout(layout)

    def save_seuil(self):
        produit_id = self.produit_combobox.currentData()
        seuil_min = self.seuil_min_input.value()
        self.seuil_controller.set_seuil(produit_id, seuil_min)

    def close_form(self):
        # Ferme la fenêtre du formulaire
        self.parent().close()
