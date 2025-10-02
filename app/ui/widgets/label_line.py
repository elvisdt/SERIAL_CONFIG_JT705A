
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
                 label_width: int | None = None):
        super().__init__(parent)
        self.label =QLabel(label)
        self.label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        if label_width:
            self.label.setFixedWidth(label_width)

        self.edit = QLineEdit()
        if placeholder: self.edit.setPlaceholderText(placeholder)
        self.edit.setReadOnly(read_only)
        if validator: self.edit.setValidator(validator)

        # políticas de tamaño coherentes
        self.label.setSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        self.edit.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)

        lay = QtWidgets.QHBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(8)
        lay.addWidget(self.label)
        lay.addWidget(self.edit, 1)
