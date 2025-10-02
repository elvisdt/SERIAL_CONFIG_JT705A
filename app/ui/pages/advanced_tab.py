


# main.py — UI mejorada (PyQt6) con tema claro/oscuro, QSettings y validadores
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt, QRegularExpression, QSettings
from PyQt6.QtGui import QRegularExpressionValidator, QIcon, QAction
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QPlainTextEdit, QSpinBox,
    QGroupBox, QHBoxLayout, QVBoxLayout, QGridLayout, QTabWidget, QFileDialog,
    QToolButton, QStyle, QCheckBox, QRadioButton, QPushButton, QComboBox, QSplitter,
    QStatusBar, QToolBar
)

from app.ui.widgets.group_box import    GroupBox
from app.ui.widgets.icon_circle import IconCircle
from app.ui.widgets.label_line import LabeledLine
from app.ui.widgets.number_field import NumberField


class AdvancedTab(QWidget):
    def __init__(self):
        super().__init__()
        lay = QVBoxLayout(self)

        # Command input
        cmd_box = GroupBox("Advanced Operations")
        v = QVBoxLayout(cmd_box)
        self.cmd_edit = QPlainTextEdit()
        self.cmd_edit.setPlaceholderText("Enter raw instruction here, e.g.\n(700160818000,1,001,BASE,1)")
        self.btn_send = QPushButton("Send")
        top = QHBoxLayout()
        top.addWidget(self.btn_send)
        top.addStretch(1)
        v.addWidget(self.cmd_edit)
        v.addLayout(top)

        # Response area
        resp_box = GroupBox("Response / Log")
        resp_lay = QVBoxLayout(resp_box)
        self.resp_view = QPlainTextEdit()
        self.resp_view.setReadOnly(True)
        self.btn_clear = QPushButton("Clear")
        self.btn_save = QPushButton("Save…")
        self.btn_clear.setShortcut("Ctrl+L")
        self.btn_save.setShortcut("Ctrl+S")
        hb = QHBoxLayout()
        hb.addStretch(1)
        hb.addWidget(self.btn_clear)
        hb.addWidget(self.btn_save)
        resp_lay.addWidget(self.resp_view)
        resp_lay.addLayout(hb)

        lay.addWidget(cmd_box)
        lay.addWidget(resp_box)