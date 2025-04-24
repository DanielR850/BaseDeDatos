import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QTextEdit,
    QComboBox, QVBoxLayout, QHBoxLayout, QGridLayout
)
from PyQt5.QtGui import QPainter, QBrush, QLinearGradient, QColor, QFont, QPixmap
from PyQt5.QtCore import Qt

class AgregarPromocion(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Agregar Promoción")
        self.resize(800, 500)
        
        
        self.btn_regresar = QPushButton("⤺ Regresar")
        self.btn_regresar.setStyleSheet("background-color: transparent; font: 12pt Arial;")
        self.btn_regresar.setFixedHeight(40)
        self.btn_regresar.clicked.connect(self.close)  # ← Función de regresar

        self.titulo = QLabel("Agregar Promoción")
        self.titulo.setFont(QFont("Arial", 20, QFont.Bold))
        self.titulo.setAlignment(Qt.AlignCenter)

        self.nombre_label = QLabel("Nombre de la Promoción")
        self.nombre_input = QLineEdit()

        self.servicio_label = QLabel("Servicio de la Promoción")
        self.servicio_combo = QComboBox()
        self.servicio_combo.addItems(["Maquillaje", "Peinado", "Uñas"])

        self.descripcion_label = QLabel("Descripción")
        self.descripcion_input = QTextEdit()

        self.descuento_label = QLabel("Descuento")
        self.descuento_input = QLineEdit()

        self.fecha_inicio_label = QLabel("Fecha de Inicio")
        self.fecha_inicio_combo = QComboBox()
        self.fecha_inicio_combo.addItems(["Día", "Mes", "Año"])

        self.fecha_fin_label = QLabel("Fecha de Fin")
        self.fecha_fin_combo = QComboBox()
        self.fecha_fin_combo.addItems(["Día", "Mes", "Año"])

        self.btn_agregar = QPushButton("Agregar Promoción")
        self.btn_agregar.setStyleSheet("background-color: lightgreen; font: 12pt Arial;")

        self.logo = QLabel()
        self.logo.setPixmap(QPixmap("./resources/logo_sinfondo.png").scaled(70, 70, Qt.KeepAspectRatio, Qt.SmoothTransformation))

        self.crear_layout()

    def crear_layout(self):
        layout_principal = QVBoxLayout()

       
        fila_superior = QHBoxLayout()
        fila_superior.addWidget(self.btn_regresar, alignment=Qt.AlignLeft)
        fila_superior.addStretch()
        fila_superior.addWidget(self.titulo, stretch=1)
        fila_superior.addStretch()

        layout_principal.addLayout(fila_superior)

        grid = QGridLayout()

        grid.addWidget(self.nombre_label, 0, 0)
        grid.addWidget(self.nombre_input, 1, 0)

        grid.addWidget(self.servicio_label, 0, 1)
        grid.addWidget(self.servicio_combo, 1, 1)

        grid.addWidget(self.descripcion_label, 0, 2)
        grid.addWidget(self.descripcion_input, 1, 2)

        grid.addWidget(self.descuento_label, 2, 0)
        grid.addWidget(self.descuento_input, 3, 0)

        grid.addWidget(self.fecha_inicio_label, 2, 1)
        grid.addWidget(self.fecha_inicio_combo, 3, 1)

        grid.addWidget(self.fecha_fin_label, 2, 2)
        grid.addWidget(self.fecha_fin_combo, 3, 2)

        grid.addWidget(self.btn_agregar, 4, 1)
        grid.addWidget(self.logo, 4, 2, alignment=Qt.AlignRight)

        layout_principal.addLayout(grid)
        self.setLayout(layout_principal)

    def paintEvent(self, event):
        painter = QPainter(self)
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0.0, QColor("#e6a0a0"))
        gradient.setColorAt(1.0, QColor("#e0cfcf"))
        painter.setBrush(QBrush(gradient))
        painter.drawRect(self.rect())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AgregarPromocion()
    window.show()
    sys.exit(app.exec_())
