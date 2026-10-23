import sys
from PyQt5.QtWidgets import QApplication
from ui_interface import DDoSAcademy


def main():
    """
    Назначение и краткое описание функции `main`.
    """
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = DDoSAcademy()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
