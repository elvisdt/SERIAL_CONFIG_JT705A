

# main_window.py — definición de la ventana principal
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt, QSettings
from PyQt6.QtGui import QIcon, QAction, QKeySequence
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QLabel, QFileDialog,
    QHBoxLayout, QVBoxLayout, QTabWidget, QStatusBar, QToolBar
)



# Páginas
from app.ui.pages.basic_tab import BaseInfoTab
from app.ui.pages.advanced_tab import AdvancedTab

# Widgets
from app.ui.widgets.panels import ComPanel, BasicInfoPanel


class MainWindow(QMainWindow):
    def __init__(self, settings: QSettings):
        super().__init__()
        self.settings = settings
        self.setWindowTitle("Config-Ver — PyQt6 (UI only)")
        self.resize(1200, 680)

        # --- Central widget ---
        central = QWidget()
        self.setCentralWidget(central)
        outer = QVBoxLayout(central)
        outer.setContentsMargins(10, 10, 10, 10)
        outer.setSpacing(10)

        # --- Top row: COM + Basic information ---
        top = QHBoxLayout()
        self.com_panel = ComPanel()
        self.basic_panel = BasicInfoPanel()
        top.addWidget(self.com_panel)
        top.addWidget(self.basic_panel, 1)

        # --- Tabs ---
        tabs = QTabWidget()
        tabs.setDocumentMode(True)
        tabs.setTabPosition(QTabWidget.TabPosition.North)
        self.baseinfo_tab = BaseInfoTab()
        self.advanced_tab = AdvancedTab()
        tabs.addTab(self.baseinfo_tab, "BaseInfo Config")
        tabs.addTab(self.advanced_tab, "Advanced Operations")

        outer.addLayout(top)
        outer.addWidget(tabs, 1)

        # --- Status bar ---
        sb = QStatusBar()
        self.setStatusBar(sb)
        self._sb_msg = QLabel("Ready.")
        sb.addPermanentWidget(self._sb_msg)

        # --- Toolbar ---
        self._make_toolbar()

        # --- Conexiones mínimas (UI only) ---
        self.com_panel.btn_open.toggled.connect(self._toggle_port_visual)
        self.advanced_tab.btn_clear.clicked.connect(self.advanced_tab.resp_view.clear)
        self.advanced_tab.btn_save.clicked.connect(self._save_log_placeholder)

        # --- Restaurar geometría/estado ---
        self._restore_window_state()

    # ---- Toolbar / acciones ----
    def _make_toolbar(self):
        tb = QToolBar("Main")
        tb.setObjectName("toolbar_main")   # requerido para saveState/restoreState
        tb.setMovable(False)
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, tb)

        # Toggle tema
        self.act_toggle_theme = QAction("Toggle Theme", self)
        # atajo: usa StandardKey si existe; si no, fallback a string
        try:
            self.act_toggle_theme.setShortcut(QKeySequence(QKeySequence.StandardKey.Preferences))
        except Exception:
            self.act_toggle_theme.setShortcut(QKeySequence("Ctrl+T"))
        self.act_toggle_theme.triggered.connect(self._toggle_theme)
        tb.addAction(self.act_toggle_theme)

        tb.addSeparator()

        # Guardar log (icono con fallback)
        icon = QIcon.fromTheme("document-save")
        if icon.isNull():
            icon = self.style().standardIcon(QtWidgets.QStyle.StandardPixmap.SP_DialogSaveButton)
        self.act_save_log = QAction(icon, "Save Log", self)
        try:
            self.act_save_log.setShortcut(QKeySequence(QKeySequence.StandardKey.Save))
        except Exception:
            self.act_save_log.setShortcut(QKeySequence("Ctrl+S"))
        self.act_save_log.triggered.connect(self._save_log_placeholder)
        tb.addAction(self.act_save_log)

        # Limpiar log
        self.act_clear_log = QAction("Clear Log", self)
        # Puedes usar Delete como estándar o mantener Ctrl+L
        try:
            self.act_clear_log.setShortcut(QKeySequence(QKeySequence.StandardKey.Delete))
        except Exception:
            self.act_clear_log.setShortcut(QKeySequence("Ctrl+L"))
        self.act_clear_log.triggered.connect(self.advanced_tab.resp_view.clear)
        tb.addAction(self.act_clear_log)


    # ---- Persistencia ----
    def _restore_window_state(self):
        geom = self.settings.value("win/geometry", b'', type=QtCore.QByteArray)
        state = self.settings.value("win/state", b'', type=QtCore.QByteArray)
        if geom:
            self.restoreGeometry(geom)
        if state:
            self.restoreState(state)

    def closeEvent(self, e: QtGui.QCloseEvent):
        self.settings.setValue("win/geometry", self.saveGeometry())
        self.settings.setValue("win/state", self.saveState())
        super().closeEvent(e)

    # ---- UI helpers ----
    def _toggle_port_visual(self, checked: bool):
        self.com_panel.btn_open.setText("Close [O]" if checked else "Open [O]")
        self.com_panel.indicator.setColor("#5cb85c" if checked else "#d9534f")
        self._sb_msg.setText("Port: OPEN" if checked else "Port: CLOSED")

    def _save_log_placeholder(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save Log", "log.txt", "Text Files (*.txt)")
        if path:
            with open(path, "w", encoding="utf-8") as f:
                f.write(self.advanced_tab.resp_view.toPlainText())
            self._sb_msg.setText(f"Log saved: {path}")

    def _toggle_theme(self):
        theme = (self.settings.value("ui/theme", "dark") or "dark").lower()
        new_theme = "light" if theme == "dark" else "dark"
        app = QtWidgets.QApplication.instance()
        from app.themes.styles import get_qss
        app.setStyleSheet(get_qss(new_theme))
        self.settings.setValue("ui/theme", new_theme)
        self._sb_msg.setText(f"Theme: {new_theme.capitalize()}")
