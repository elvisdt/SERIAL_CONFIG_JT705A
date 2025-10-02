





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
        lay.setContentsMargins(8, 8, 8, 8)
        lay.setHorizontalSpacing(16)
        lay.setVerticalSpacing(8)
        
        # --- Widgets ---
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






# basic_info_panel.py
# from PyQt6.QtCore import Qt
# from PyQt6.QtWidgets import QGridLayout, QToolButton, QStyle
# from app.ui.widgets.group_box import GroupBox
# from app.ui.widgets.label_line import LabeledLine

class BasicInfoPanel(GroupBox):
    def __init__(self, label_width: int = 90):
        super().__init__("Basic information")

        # --- Widgets (label_width asegura alineación pareja)
        self.ed_id      = LabeledLine("ID:",      read_only=True, label_width=label_width)
        self.ed_imei    = LabeledLine("IMEI:",    read_only=True, label_width=label_width)
        self.ed_ccid    = LabeledLine("CCID:",    read_only=True, label_width=label_width)
        self.ed_version = LabeledLine("Version:", read_only=True, label_width=label_width)

        self.btn_refresh = QToolButton()
        self.btn_refresh.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_BrowserReload))
        self.btn_refresh.setToolTip("Refresh basic information")

        # Tamaño mínimo (ejemplo: 32x32 px)
        #self.btn_refresh.setMinimumSize(32, 32)

        # También puedes controlar el tamaño del ícono para que llene mejor el botón
        self.btn_refresh.setIconSize(QtCore.QSize(32, 32))

        # --- Layout
        grid = QGridLayout(self)
        grid.setContentsMargins(8, 8, 8, 8)
        #grid.setHorizontalSpacing(16)
        grid.setVerticalSpacing(8)

        # Izquierda: ID, IMEI
        grid.addWidget(self.ed_id,   0, 0)
        grid.addWidget(self.ed_imei, 1, 0)

        # Derecha: CCID, Version
        grid.addWidget(self.ed_ccid,    0, 1)
        grid.addWidget(self.ed_version, 1, 1)

        # Columna separada solo para el botón → ocupa 2 filas centrado
        grid.addWidget(self.btn_refresh, 0, 2, 2, 1, alignment=Qt.AlignmentFlag.AlignCenter)

        # Que columnas 0 y 1 repartan el espacio de los campos
        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 1)
        grid.setColumnStretch(2, 0)  # botón no se estira

    # ---- API cómoda para que el panel sea fácil de usar ----
    def set_values(self, *, id_: str = "", imei: str = "", ccid: str = "", version: str = "") -> None:
        self.ed_id.setText(id_)
        self.ed_imei.setText(imei)
        self.ed_ccid.setText(ccid)
        self.ed_version.setText(version)

    def set_values_from_dict(self, data: dict) -> None:
        self.ed_id.setText(data.get("id_", data.get("id", "")))
        self.ed_imei.setText(data.get("imei", ""))
        self.ed_ccid.setText(data.get("ccid", ""))
        self.ed_version.setText(data.get("version", ""))

    def clear(self) -> None:
        for w in (self.ed_id, self.ed_imei, self.ed_ccid, self.ed_version):
            w.setText("")
