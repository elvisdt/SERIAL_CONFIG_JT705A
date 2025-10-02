


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





# ---------- Validadores reutilizables ----------
def ip_validator() -> QRegularExpressionValidator:
    # IPv4 estricta
    rx = QRegularExpression(
        r"^((25[0-5]|2[0-4]\d|[01]?\d?\d)\.){3}"
        r"(25[0-5]|2[0-4]\d|[01]?\d?\d)$"
    )
    return QRegularExpressionValidator(rx)

def phone_validator() -> QRegularExpressionValidator:
    # 5 a 20 dígitos con opcional +
    rx = QRegularExpression(r"^\+?\d{5,20}$")
    return QRegularExpressionValidator(rx)



def normalize_label_width(widgets: list[LabeledLine], extra: int = 16) -> None:
    if not widgets:
        return
    fm = widgets[0].label.fontMetrics()
    max_w = max(fm.horizontalAdvance(w.label.text()) for w in widgets) + extra
    for w in widgets:
        w.label.setFixedWidth(max_w)
        w.label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        w.label.setSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        w.edit.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)


# ---------- Pestañas ----------
class BaseInfoTab(QWidget):
    def __init__(self):
        super().__init__()
        root = QGridLayout(self)
        root.setHorizontalSpacing(14)
        root.setVerticalSpacing(10)

        # Left column - Network / timing
        net_box = GroupBox("BaseInfo Config")
        net_grid = QGridLayout(net_box)

        
        self.main_ip = LabeledLine("Main IP Address:", placeholder="e.g., 52.21.34.100", validator=ip_validator())
        self.main_port = NumberField("Main IP Port:", 0, 65535, default=11000)
        self.sub_ip = LabeledLine("Sub IP Address:", placeholder="e.g., 10.0.0.12", validator=ip_validator())
        self.sub_port = NumberField("Sub IP Port:", 0, 65535, default=11000)
        self.apn = LabeledLine("APN:", placeholder="e.g., claro.pe")
        self.apn_user = LabeledLine("APN User:", placeholder="(opcional)")
        self.apn_pass = LabeledLine("APN Pass:")
        #self.apn_pass.edit.setEchoMode(QLineEdit.EchoMode.Password)

        rows: list[LabeledLine] = [ self.main_ip, self.main_port, self.sub_ip, self.sub_port, self.apn, self.apn_user, self.apn_pass]

        # calcular ancho máximo de etiquetas
        fm = rows[0].label.fontMetrics()
        max_w = max(fm.horizontalAdvance(r.label.text()) for r in rows) + 16  # + padding

        for r in rows:
            r.label.setFixedWidth(max_w)
            net_grid.addWidget(r) 


        num_rows = len(rows)
        # buttons read / write beneath APN fields
        btns_lay = QHBoxLayout()
        self.btn_read_net = QPushButton("Read")
        self.btn_write_net = QPushButton("Write")
        self.btn_write_net.setShortcut("Ctrl+Enter")
        self.btn_write_net.setToolTip("Aplicar configuración de red (UI)")
        btns_lay.addStretch(1)
        btns_lay.addWidget(self.btn_read_net)
        btns_lay.addWidget(self.btn_write_net)
        net_grid.addLayout(btns_lay, num_rows, 0, 1, 2);

        # Timing panel
        time_box = GroupBox("Timing")
        time_grid = QGridLayout(time_box)
        self.time_diff = NumberField("Time Difference:", -10_000, 10_000, "min", 480)
        self.upload_interval = NumberField("Tracking Upload Interval:", 0, 86_400, "sec", 60)
        self.wake_interval = NumberField("Wake up Interval:", 0, 86_400, "min", 30)
        self.btn_read_time = QPushButton("Read")
        self.btn_write_time = QPushButton("Write")
        time_grid.addWidget(self.time_diff, 0, 0, 1, 2)
        time_grid.addWidget(self.upload_interval, 1, 0, 1, 2)
        time_grid.addWidget(self.wake_interval, 2, 0, 1, 2)
        tbtns = QHBoxLayout()
        tbtns.addStretch(1)
        tbtns.addWidget(self.btn_read_time)
        tbtns.addWidget(self.btn_write_time)
        time_grid.addLayout(tbtns, 3, 0, 1, 2)

        # Factory default
        factory_box = GroupBox("Factory Default")
        f_lay = QHBoxLayout(factory_box)
        self.rb_all = QRadioButton("All")
        self.rb_ip = QRadioButton("IP")
        self.rb_common = QRadioButton("Common")
        self.rb_all.setChecked(True)
        self.btn_reset = QPushButton("Reset")
        self.btn_reset.setToolTip("Restaurar parámetros seleccionados")
        f_lay.addWidget(self.rb_all)
        f_lay.addWidget(self.rb_ip)
        f_lay.addWidget(self.rb_common)
        f_lay.addStretch(1)
        f_lay.addWidget(self.btn_reset)

        # Utility row
        util_lay = QHBoxLayout()
        self.btn_syn = QPushButton("SYN")
        self.btn_pa0 = QPushButton("PA0 Sleep Wake up")
        self.chk_tips = QCheckBox("Show Tips")
        self.chk_tips.setChecked(True)
        util_lay.addWidget(self.btn_syn)
        util_lay.addWidget(self.btn_pa0)
        util_lay.addStretch(1)
        util_lay.addWidget(self.chk_tips)

        left_col = QVBoxLayout()
        left_col.addWidget(net_box)
        left_col.addWidget(time_box)
        left_col.addWidget(factory_box)
        left_col.addLayout(util_lay)
        left_col.addStretch(1)
        left_wrap = QWidget()
        left_wrap.setLayout(left_col)

        # Right column - VIP numbers
        vip_box = GroupBox("VIP Numbers")
        vip_grid = QGridLayout(vip_box)
        self.vip_edits = []
        for i in range(5):
            lbl = QLabel(f"VIP Number {i+1}:")
            edit = QLineEdit()
            edit.setPlaceholderText("e.g., +51987654321")
            edit.setValidator(phone_validator())
            vip_grid.addWidget(lbl, i, 0)
            vip_grid.addWidget(edit, i, 1)
            self.vip_edits.append(edit)
        self.btn_vip_read = QPushButton("Read")
        self.btn_vip_write = QPushButton("Write")
        vip_btns = QHBoxLayout()
        vip_btns.addStretch(1)
        vip_btns.addWidget(self.btn_vip_read)
        vip_btns.addWidget(self.btn_vip_write)
        vip_grid.addLayout(vip_btns, 5, 0, 1, 2)

        # Splitter para mejor UX de redimensionado
        self.split = QSplitter(Qt.Orientation.Horizontal)
        self.split.addWidget(left_wrap)
        self.split.addWidget(vip_box)
        self.split.setStretchFactor(0, 1)
        self.split.setStretchFactor(1, 1)

        root.addWidget(self.split, 0, 0, 1, 1)

        
        # rows = [self.main_ip, self.apn, self.apn_user, self.apn_pass, self.sub_ip]
        # normalize_label_width(rows)
