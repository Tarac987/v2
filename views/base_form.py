# views/base_form.py

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox

class BaseForm(QWidget):
    def __init__(self, title):
        super().__init__()
        self.setWindowTitle(title)
        
        self.init_ui()
    
    def init_ui(self):
        pass  # Cette méthode sera implémentée par les sous-classes

    def add_line_edit(self, label_text):
        label = QLabel(label_text)
        line_edit = QLineEdit()
        
        layout = QHBoxLayout()
        layout.addWidget(label)
        layout.addWidget(line_edit)
        
        return line_edit, layout
    
    def add_button(self, text):
        return QPushButton(text)
    
    def show_message(self, title, message, icon=QMessageBox.Information):
        msg_box = QMessageBox()
        msg_box.setIcon(icon)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.exec_()
