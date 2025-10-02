
from PyQt6 import QtGui, QtWidgets
from PyQt6.QtCore import Qt

from PyQt6.QtWidgets import (QWidget, QLabel, QLineEdit, QHBoxLayout)


# class LabeledLine(QWidget):
#     """Etiqueta + QLineEdit, con validador opcional."""
#     def __init__(self, label: str, parent=None, placeholder: str | None = None,
#                  read_only: bool = False, validator: QtGui.QValidator | None = None):
#         super().__init__(parent)
#         self.label = QLabel(label)
#         self.edit = QLineEdit()
#         if placeholder:
#             self.edit.setPlaceholderText(placeholder)
#         self.edit.setReadOnly(read_only)
#         if validator:
#             self.edit.setValidator(validator)

#         lay = QHBoxLayout(self)
#         lay.setContentsMargins(0, 0, 0, 0)
#         lay.setSpacing(8)
#         lay.addWidget(self.label)
#         lay.addWidget(self.edit, 1)


class LabeledLine(QWidget):
    def __init__(self, label: str, parent=None, placeholder: str | None = None,
                 read_only: bool = False, validator: QtGui.QValidator | None = None,
                 label_width: int = 50):  # valor por defecto
        super().__init__(parent)

        # Label alineado a la derecha
        self.label = QLabel(label)
        self.label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.label.setMinimumWidth(label_width)   # siempre al menos este ancho
        self.label.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Fixed
        )

        # Campo de texto
        self.edit = QLineEdit()
        if placeholder:
            self.edit.setPlaceholderText(placeholder)
        self.edit.setReadOnly(read_only)
        if validator:
            self.edit.setValidator(validator)

        # el campo se expande horizontalmente
        self.edit.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Fixed
        )

        # Layout limpio
        lay = QtWidgets.QHBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(8)
        lay.addWidget(self.label)
        lay.addWidget(self.edit, 1)

    # Métodos de conveniencia
    def text(self) -> str:
        return self.edit.text()

    def setText(self, value: str):
        self.edit.setText(value)

    def setPlaceholder(self, text: str):
        self.edit.setPlaceholderText(text)

    def setReadOnly(self, state: bool):
        self.edit.setReadOnly(state)
