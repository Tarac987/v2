from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QWidget, QMessageBox
from PyQt5.QtCore import Qt
from controllers.code_comptable_controller import CodeComptableController

class CodeComptableForm(QWidget):
    def __init__(self, db_session, code_comptable_id=None):
        super().__init__()
        self.db_session = db_session
        self.code_comptable_controller = CodeComptableController(self.db_session)
        self.code_comptable_id = code_comptable_id
        self.init_ui()
        if self.code_comptable_id:
            self.load_code_comptable()

    def init_ui(self):
        main_layout = QVBoxLayout()

        # Code
        code_layout = QHBoxLayout()
        self.code_edit, code_label = self.add_line_edit('Code:', 'Entrez le code comptable')
        code_layout.addWidget(code_label)
        code_layout.addWidget(self.code_edit)
        main_layout.addLayout(code_layout)

        # Description
        description_layout = QHBoxLayout()
        self.description_edit, description_label = self.add_line_edit('Description:', 'Entrez la description')
        description_layout.addWidget(description_label)
        description_layout.addWidget(self.description_edit)
        main_layout.addLayout(description_layout)

        # Save/Update Button
        button_layout = QHBoxLayout()
        self.btn_save = QPushButton('Enregistrer')
        self.btn_save.clicked.connect(self.save_code_comptable)
        button_layout.addWidget(self.btn_save)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)
        self.setWindowTitle('Code Comptable')
        self.setGeometry(300, 300, 400, 200)

    def add_line_edit(self, label_text, placeholder_text):
        label = QLabel(label_text)
        line_edit = QLineEdit()
        line_edit.setPlaceholderText(placeholder_text)
        line_edit.setFixedSize(300, 30)
        return line_edit, label

    def load_code_comptable(self):
        code_comptable = self.code_comptable_controller.get_code_comptable(self.code_comptable_id)
        if code_comptable:
            self.code_edit.setText(code_comptable.code)
            self.description_edit.setText(code_comptable.description)
        else:
            QMessageBox.warning(self, 'Erreur', 'Code comptable non trouvé.')

    def save_code_comptable(self):
        code = self.code_edit.text().strip()
        description = self.description_edit.text().strip()

        if not code or not description:
            QMessageBox.warning(self, 'Erreur', 'Veuillez remplir tous les champs.')
            return

        try:
            if self.code_comptable_id:
                self.code_comptable_controller.update_code_comptable(self.code_comptable_id, code, description)
                QMessageBox.information(self, 'Succès', 'Code comptable mis à jour avec succès.')
            else:
                existing_code = self.code_comptable_controller.get_code_comptable_by_code(code)
                if existing_code:
                    QMessageBox.warning(self, 'Erreur', 'Ce code comptable existe déjà.')
                    return
                self.code_comptable_controller.create_code_comptable(code, description)
                QMessageBox.information(self, 'Succès', 'Code comptable créé avec succès.')
        except Exception as e:
            QMessageBox.warning(self, 'Erreur', f'Une erreur est survenue : {e}')

        self.clear_fields()

    def clear_fields(self):
        self.code_edit.clear()
        self.description_edit.clear()
