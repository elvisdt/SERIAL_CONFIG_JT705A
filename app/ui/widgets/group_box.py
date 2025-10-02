

# group_box.py
from PyQt6 import  QtWidgets
from PyQt6.QtWidgets import QGroupBox


class GroupBox(QGroupBox):
    def __init__(self, title: str):
        super().__init__(title)
        # El QSS principal ya estiliza QGroupBox; aquí van overrides puntuales si necesitas
        self.setSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Maximum)