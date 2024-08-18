from gui.main_window import MainWindow
from PyQt5.QtWidgets import QApplication
import sys
from models.base import init_db

if __name__ == '__main__':
    # Initialisation de la base de données
    init_db()

    # Lancement de l'application
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
