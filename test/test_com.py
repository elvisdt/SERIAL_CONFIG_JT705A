# test_ui.py
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout

# Importa tus paneles
from app.ui.widgets.panels import ComPanel, BasicInfoPanel

class TestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Test UI Panels")
        #self.resize(600, 400)

        central = QWidget()
        layout = QVBoxLayout(central)

        # Agregamos los paneles que quieres probar
        # layout.addWidget(ComPanel())
        layout.addWidget(BasicInfoPanel())

        self.setCentralWidget(central)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = TestWindow()
    win.show()
    sys.exit(app.exec())
