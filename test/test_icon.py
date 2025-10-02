from PyQt6.QtWidgets import QApplication, QWidget, QHBoxLayout, QLabel
import sys

from app.ui.widgets.icon_circle import IconCircle   # importa tu clase

class TestWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Prueba IconCircle")
        self.resize(200, 100)

        layout = QHBoxLayout(self)

        lbl = QLabel("Estado del puerto:")
        icon = IconCircle(diameter=16, color="#d9534f")  # rojo por defecto
        # Puedes luego cambiar color en runtime:
        # icon.setColor("#5cb85c")  # verde

        layout.addWidget(lbl)
        layout.addWidget(icon)
        layout.addStretch(1)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = TestWindow()
    w.show()
    sys.exit(app.exec())
