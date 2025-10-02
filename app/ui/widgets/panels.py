





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

class ComPanel(GroupBox):
    def __init__(self):
        super().__init__("COM Setting")
        lay = QGridLayout(self)
        self.label_port = QLabel("Com Port")
        self.combo_port = QComboBox()
        self.combo_port.setEditable(True)
        self.combo_port.setToolTip("Escribe p.ej. '10' o 'COM10'")
        self.combo_port.addItems([str(i) for i in range(1, 51)])

        self.label_baud = QLabel("Baud Rate")
        self.combo_baud = QComboBox()
        self.combo_baud.addItems(["9600", "19200", "38400", "57600", "115200"])
        idx = self.combo_baud.findText("9600")
        if idx >= 0:
            self.combo_baud.setCurrentIndex(idx)

        self.btn_open = QPushButton("Open [O]")
        self.btn_open.setCheckable(True)
        self.btn_open.setMinimumWidth(120)
        self.indicator = IconCircle(12, "#d9534f")  # rojo cuando cerrado

        lay.addWidget(self.label_port, 0, 0)
        lay.addWidget(self.combo_port, 0, 1)
        lay.addWidget(self.btn_open, 0, 2)
        lay.addWidget(self.indicator, 0, 3)
        lay.addWidget(self.label_baud, 1, 0)
        lay.addWidget(self.combo_baud, 1, 1)






# ---------- Paneles superiores ----------
class BasicInfoPanel(GroupBox):
    def __init__(self):
        super().__init__("Basic information")
        grid = QGridLayout(self)
        # ID / IMEI / IMSI / CCID / Version
        self.ed_id = LabeledLine("ID:", read_only=True)
        self.ed_imei = LabeledLine("IMEI:", read_only=True)
        self.ed_imsi = LabeledLine("IMSI:", read_only=True)
        self.ed_ccid = LabeledLine("CCID:", read_only=True)
        self.ed_version = LabeledLine("Version:", read_only=True)

        self.btn_refresh = QToolButton()
        self.btn_refresh.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_BrowserReload))
        self.btn_refresh.setToolTip("Refresh basic information")

        grid.addWidget(self.ed_id, 0, 0, 1, 2)
        grid.addWidget(self.ed_imei, 1, 0, 1, 2)
        grid.addWidget(self.ed_imsi, 2, 0, 1, 2)
        grid.addWidget(self.ed_ccid, 0, 2, 1, 2)
        grid.addWidget(self.ed_version, 1, 2, 1, 2)
        grid.addWidget(self.btn_refresh, 2, 3, 1, 1, alignment=Qt.AlignmentFlag.AlignRight)

