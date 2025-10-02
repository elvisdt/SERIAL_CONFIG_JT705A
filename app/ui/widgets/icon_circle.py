

from PyQt6 import QtCore
from PyQt6.QtGui import QPainter, QColor
from PyQt6.QtWidgets import  QWidget

# ---------- Helpers UI ----------
class IconCircle(QWidget):
    """Indicador circular (verde/rojo)."""
    def __init__(self, diameter: int = 12, color: str = "#d9534f", parent=None):
        super().__init__(parent)
        self._diam = diameter
        self._color = color
        self.setFixedSize(self._diam, self._diam)

    def setColor(self, color: str):
        self._color = color
        self.update()

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        p.setPen(QtCore.Qt.PenStyle.NoPen)
        p.setBrush(QColor(self._color))
        r = QtCore.QRect(0, 0, self._diam, self._diam)
        p.drawEllipse(r)





from PyQt6.QtWidgets import QApplication, QWidget, QHBoxLayout, QLabel
import sys

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
