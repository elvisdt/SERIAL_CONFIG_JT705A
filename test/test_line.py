import sys
from PyQt6 import QtGui, QtWidgets
from PyQt6.QtCore import QRegularExpression
from PyQt6.QtGui import QRegularExpressionValidator

from app.ui.widgets.label_line import LabeledLine  # tu clase


class TestWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Prueba LabeledLine")
        self.resize(400, 120)

        layout = QtWidgets.QVBoxLayout(self)

        # Ejemplo simple
        # line1 = LabeledLine("Nombre:", placeholder="Escribe tu nombre...")
        # layout.addWidget(line1)

        # # Ejemplo read-only
        # line2 = LabeledLine("Solo lectura:", read_only=True)
        # line2.edit.setText("Valor fijo")
        # layout.addWidget(line2)

        # # Ejemplo con validador (solo dígitos)
        # regex = QRegularExpression(r"^\d+$")
        # validator = QRegularExpressionValidator(regex)
        # line3 = LabeledLine("Número:", placeholder="Solo dígitos", validator=validator)
        # layout.addWidget(line3)

        rows: list[LabeledLine] = []
        rows.append(LabeledLine("Nombre:", placeholder="Escribe tu nombre..."))
        rows.append(LabeledLine("Solo lectura:", read_only=True))
        rows.append(LabeledLine("Número:", placeholder="Solo dígitos"))

        # calcular ancho máximo de etiquetas
        fm = rows[0].label.fontMetrics()
        max_w = max(fm.horizontalAdvance(r.label.text()) for r in rows) + 16  # + padding

        for r in rows:
            r.label.setFixedWidth(max_w)
            layout.addWidget(r)  # tu layout vertical


        layout.addStretch(1)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = TestWindow()
    w.show()
    sys.exit(app.exec())
