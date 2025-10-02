# styles.py — esquema de colores Hunter Perú (claro / oscuro)
from PyQt6.QtGui import QColor

# Paleta Hunter Perú
HUNTER_RED     = QColor("#d32f2f")   # rojo corporativo
HUNTER_ACCENT  = QColor("#b71c1c")   # rojo intenso para hover/acción
HUNTER_DARK    = QColor("#212121")   # gris oscuro
HUNTER_LIGHT   = QColor("#f5f5f5")   # fondo claro
HUNTER_CREAM   = QColor("#fdfcf7")   # crema claro para paneles
HUNTER_BORDER  = QColor("#cfcfcf")   # gris suave para bordes
HUNTER_TEXT    = QColor("#2c2c2c")   # texto en fondo claro

# ==============================
# Tema Oscuro
# ==============================
DARK_QSS = f"""
QWidget {{
    background-color: {HUNTER_DARK.name()};
    color: {HUNTER_CREAM.name()};
    font-size: 13px;
}}

QLineEdit, QPlainTextEdit, QSpinBox {{
    background-color: {HUNTER_CREAM.name()};
    color: {HUNTER_DARK.name()};
    padding: 6px;
    border: 1px solid {HUNTER_BORDER.name()};
    border-radius: 6px;
}}

QPushButton {{
    background-color: {HUNTER_RED.name()};
    color: {HUNTER_CREAM.name()};
    border-radius: 6px;
    padding: 6px 12px;
}}
QPushButton:hover {{
    background-color: {HUNTER_ACCENT.name()};
}}
QPushButton:disabled {{
    background-color: {HUNTER_BORDER.name()};
    color: {HUNTER_DARK.name()};
}}

QGroupBox {{
    border: 1px solid {HUNTER_BORDER.name()};
    border-radius: 8px;
    margin-top: 12px;
    padding: 8px 12px;
    font-weight: bold;
}}
QGroupBox::title {{
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 4px;
}}

QTabBar::tab {{
    background: {HUNTER_RED.name()};
    color: {HUNTER_CREAM.name()};
    padding: 8px 12px;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
}}
QTabBar::tab:selected {{
    background: {HUNTER_ACCENT.name()};
}}
QTabWidget::pane {{
    border-top: 2px solid {HUNTER_ACCENT.name()};
}}
"""

# ==============================
# Tema Claro
# ==============================
LIGHT_QSS = f"""
QWidget {{
    background-color: {HUNTER_LIGHT.name()};
    color: {HUNTER_TEXT.name()};
    font-size: 13px;
}}

QLineEdit, QPlainTextEdit, QSpinBox {{
    background-color: {HUNTER_CREAM.name()};
    color: {HUNTER_TEXT.name()};
    padding: 6px;
    border: 1px solid {HUNTER_BORDER.name()};
    border-radius: 6px;
}}

QPushButton {{
    background-color: {HUNTER_RED.name()};
    color: white;
    border-radius: 6px;
    padding: 6px 12px;
}}
QPushButton:hover {{
    background-color: {HUNTER_ACCENT.name()};
}}
QPushButton:disabled {{
    background-color: {HUNTER_BORDER.name()};
    color: gray;
}}

QGroupBox {{
    border: 1px solid {HUNTER_BORDER.name()};
    border-radius: 8px;
    margin-top: 12px;
    padding: 8px 12px;
    font-weight: bold;
}}
QGroupBox::title {{
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 4px;
}}

QTabBar::tab {{
    background: {HUNTER_RED.name()};
    color: white;
    padding: 8px 12px;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
}}
QTabBar::tab:selected {{
    background: {HUNTER_ACCENT.name()};
}}
QTabWidget::pane {{
    border-top: 2px solid {HUNTER_ACCENT.name()};
}}
"""

# ==============================
# Función para elegir estilo
# ==============================
def get_qss(theme: str = "dark") -> str:
    """
    Retorna la hoja de estilo según el tema.
    theme: "dark" o "light"
    """
    return DARK_QSS if theme.lower() == "dark" else LIGHT_QSS
