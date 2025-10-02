# main.py — entry point de la aplicación
import sys
from PyQt6 import QtCore, QtWidgets, QtGui
from PyQt6.QtCore import QSettings
from PyQt6.QtWidgets import QApplication

from app.ui.main_window import MainWindow      # Tu ventana principal
from app.themes.styles import get_qss          # get_qss("dark"|"light")


def apply_theme(app: QApplication, theme: str) -> None:
    """Aplica Fusion + QSS Hunter a toda la app."""
    app.setStyle("Fusion")               # base neutral
    app.setPalette(QtGui.QPalette())     # reset paleta a la de Fusion (fresco)
    theme = (theme or "dark").lower()
    if theme not in ("dark", "light"):
        theme = "dark"
    app.setStyleSheet(get_qss(theme))


def main():
    # HiDPI seguro
    AA_EnableHighDpiScaling = getattr(QtCore.Qt.ApplicationAttribute, "AA_EnableHighDpiScaling", None)
    AA_UseHighDpiPixmaps    = getattr(QtCore.Qt.ApplicationAttribute, "AA_UseHighDpiPixmaps", None)
    if AA_EnableHighDpiScaling is not None:
        QtWidgets.QApplication.setAttribute(AA_EnableHighDpiScaling, True)
    if AA_UseHighDpiPixmaps is not None:
        QtWidgets.QApplication.setAttribute(AA_UseHighDpiPixmaps, True)

    HDSFRP = getattr(QtCore.Qt, "HighDpiScaleFactorRoundingPolicy", None)
    if HDSFRP is not None:
        setter = getattr(QtGui.QGuiApplication, "setHighDpiScaleFactorRoundingPolicy", None)
        if callable(setter):
            setter(HDSFRP.PassThrough)

    app = QtWidgets.QApplication(sys.argv)

    settings = QSettings("Hunter", "ConfigVer")
    initial_theme = (settings.value("ui/theme", "dark") or "dark").lower()
    if initial_theme not in ("dark", "light"):
        initial_theme = "dark"

    app.setStyle("Fusion")
    app.setPalette(QtGui.QPalette())  # reset limpio
    app.setStyleSheet(get_qss(initial_theme))

    win = MainWindow(settings)
    win.show()
    sys.exit(app.exec())



if __name__ == "__main__":
    main()
