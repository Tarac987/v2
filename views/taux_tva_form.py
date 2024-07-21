from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QComboBox, QWidget, QFrame, QToolButton
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import QSize, Qt
from PyQt5.Qt import QStyle
from PyQt5.QtGui import QFont

from controllers.tva_controller import TVAController

class TauxTVAForm(QWidget):
    def __init__(self, db_session):
        super().__init__()
        self.db_session = db_session
        self.tva_controller = TVAController(self.db_session)
        self.init_ui()
        
    def init_ui(self):
        main_layout = QVBoxLayout()

        self.legend_label = QLabel('* Champ obligatoire')
        legend_font = QFont()
        legend_font.setPointSize(8)
        self.legend_label.setFont(legend_font)
        main_layout.addWidget(self.legend_label, alignment=Qt.AlignTop | Qt.AlignLeft)

        recherche_layout = QHBoxLayout()
        self.taux_combobox = QComboBox()
        self.taux_combobox.addItem("taux de TVA", -1)
        self.load_taux_combobox()
        self.taux_combobox.currentIndexChanged.connect(self.remplir_champs)
      
        recherche_layout.addWidget(self.taux_combobox)
        main_layout.addLayout(recherche_layout)

        search_separator = QFrame()
        search_separator.setFrameShape(QFrame.HLine)
        search_separator.setFrameShadow(QFrame.Sunken)
        main_layout.addWidget(search_separator)
        
        taux_layout = QVBoxLayout()
        self.taux_edit, taux_label = self.add_taux_edit_with_percent('* Taux:', 'Entrez le taux')
        taux_layout.addWidget(taux_label)
        taux_layout.addWidget(self.taux_edit)

        self.description_edit, description_label = self.add_line_edit('* Description:', 'Entrez la description')
        taux_layout.addWidget(description_label)
        taux_layout.addWidget(self.description_edit)

        main_layout.addLayout(taux_layout)

        button_layout = QHBoxLayout()
        self.btn_enregistrer = QPushButton('Enregistrer')
        self.btn_supprimer = QPushButton('Supprimer')
        
        self.btn_enregistrer.clicked.connect(self.enregistrer_taux)
        self.btn_supprimer.clicked.connect(self.supprimer_taux)

        button_layout.addWidget(self.btn_enregistrer)
        button_layout.addWidget(self.btn_supprimer)
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
        self.setWindowTitle('Formulaire Taux TVA')
        
        
    def add_line_edit(self, label_text, placeholder_text):
        label = QLabel(label_text)
        line_edit = QLineEdit()
        line_edit.setPlaceholderText(placeholder_text)
        line_edit.setFixedSize(300, 30)
        return line_edit, label

    def add_taux_edit_with_percent(self, label_text, placeholder_text):
        label = QLabel(label_text)
        taux_layout = QHBoxLayout()
        line_edit = QLineEdit()
        line_edit.setPlaceholderText(placeholder_text)
        line_edit.setFixedSize(300, 30)
        percent_label = QLabel('%')
        percent_label.setFixedSize(20, 30)
        taux_layout.addWidget(line_edit)
        taux_layout.addWidget(percent_label)
        container_widget = QWidget()
        container_widget.setLayout(taux_layout)
        return container_widget, label

    def load_taux_combobox(self):
        """ Charge tous les taux de TVA dans le combobox """
        taux_list = self.tva_controller.get_all_taux()
        print(f"Taux chargés: {taux_list}")  # Débogage
        self.taux_combobox.clear()
        self.taux_combobox.addItem("Sélectionnez un taux de TVA", -1)
        for taux in taux_list:
            print(f"Ajouté au combobox: ID={taux.id}, Taux={taux.taux}, Description={taux.description}")  # Débogage
            self.taux_combobox.addItem(f"{taux.taux}% - {taux.description}", taux.id)

    def remplir_champs(self):
        index = self.taux_combobox.currentIndex()
        taux_id = self.taux_combobox.currentData()
        print(f"Index sélectionné: {index}, ID sélectionné: {taux_id}")  # Débogage
        
        if taux_id is not None and taux_id != -1:
            taux = self.tva_controller.get_taux_by_id(taux_id)
            if taux:
                self.taux_edit.children()[1].setText(str(taux.taux))
                self.description_edit.setText(taux.description)
            else:
                QMessageBox.warning(self, 'Erreur', 'Taux de TVA non trouvé.')
        else:
            self.clear_fields()  # Optionnel : Clear fields if no valid selection
            print(f"Aucun taux de TVA sélectionné ou sélection invalide (ID: {taux_id})")  # Débogage

    def enregistrer_taux(self):
        taux_text = self.taux_edit.children()[1].text()
        description_text = self.description_edit.text()

        if not taux_text or not description_text:
            QMessageBox.warning(self, 'Erreur', 'Veuillez remplir tous les champs obligatoires.')
            return

        try:
            taux = float(taux_text)
        except ValueError:
            QMessageBox.warning(self, 'Erreur', 'Le taux doit être un nombre valide.')
            return
        
        description = description_text
        taux_id = self.taux_combobox.currentData()

        if taux_id == -1:
            self.tva_controller.create_taux(taux, description)
            QMessageBox.information(self, 'Succès', 'Taux de TVA enregistré avec succès.')
        else:
            self.tva_controller.update_taux(taux_id, taux, description)
            QMessageBox.information(self, 'Succès', 'Taux de TVA modifié avec succès.')

        self.clear_fields()
        self.load_taux_combobox()
        
    def clear_fields(self):
        self.taux_edit.children()[1].clear()
        self.description_edit.clear()
        self.taux_combobox.setCurrentIndex(0)

    def supprimer_taux(self):
        taux_id = self.taux_combobox.currentData()
        if taux_id == -1:
            QMessageBox.warning(self, 'Erreur', 'Veuillez sélectionner un taux de TVA à supprimer.')
            return
        
        if QMessageBox.question(self, 'Confirmation', 'Êtes-vous sûr de vouloir supprimer ce taux de TVA ?', QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
            self.tva_controller.delete_taux(taux_id)
            QMessageBox.information(self, 'Succès', 'Taux de TVA supprimé avec succès.')
            self.clear_fields()
            self.load_taux_combobox()
