

from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import (QWidget, QLabel,QSpinBox, QHBoxLayout)



class NumberField(QWidget):
    """Etiqueta + QSpinBox (enteros)."""
    def __init__(self, label: str, minimum: int = 0, maximum: int = 10_000_000, suffix: str = "", default: int = 0):
        super().__init__()
        self.label = QLabel(label)
        self.spin = QSpinBox()
        self.spin.setRange(minimum, maximum)
        self.spin.setValue(default)
        if suffix:
            self.spin.setSuffix(f" {suffix}")

        lay = QHBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(8)
        lay.addWidget(self.label)
        lay.addWidget(self.spin, 1)