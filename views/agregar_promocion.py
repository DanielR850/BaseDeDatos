from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QTextEdit,
    QComboBox, QVBoxLayout, QHBoxLayout, QGridLayout
)
from PyQt5.QtGui import QPainter, QBrush, QLinearGradient, QColor, QFont, QPixmap
from PyQt5.QtCore import Qt
import sys
import os

class AgregarPromocion(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Agregar Promoción")
        self.showFullScreen()  # Ahora abre en pantalla completa
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #f8c8dc,
                    stop: 1 #fefefe
                );
                font-family: 'Poppins';
            }
            QLabel {
                background-color: transparent;
                font-size: 16pt;
                color: #000000;
            }
            QLineEdit, QTextEdit, QComboBox {
                background-color: #e5d3c5;
                border: 2px solid #000000;
                border-radius: 10px;
                padding: 8px;
                font-size: 14pt;
                min-height: 40px;
            }
            QPushButton#regresar, QPushButton#agregar {
                background-color: #231f20;
                color: #fcb3b3;
                font-family: 'Poppins';
                padding: 10px;
                border-radius: 20px;
                font-size: 16pt;
                min-width: 200px;
            }
            QPushButton#regresar:hover, QPushButton#agregar:hover {
                background-color: #333333;
            }
        """)

        self.initUI()

    def initUI(self):
        layout_principal = QVBoxLayout()

        # Botones y título
        fila_superior = QHBoxLayout()

        self.btn_regresar = QPushButton("⤺ Regresar")
        self.btn_regresar.setObjectName("regresar")
        self.btn_regresar.clicked.connect(self.close)

        fila_superior.addWidget(self.btn_regresar, alignment=Qt.AlignLeft)
        fila_superior.addStretch()

        # Logo
        self.logo = QLabel()
        pixmap = QPixmap("C:/Users/makib/Documents/EntornosVirtuales/BaseDeDatosSalonDeBelleza/resources/logo_sinfondo.png")
        self.logo.setPixmap(pixmap.scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        fila_superior.addWidget(self.logo, alignment=Qt.AlignRight)

        layout_principal.addLayout(fila_superior)

        titulo = QLabel("Agregar Promoción")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-size: 28pt; font-weight: bold; margin-top: 10px; margin-bottom: 30px;")
        layout_principal.addWidget(titulo)

        # Formulario
        grid = QGridLayout()
        grid.setSpacing(30)

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

        layout_principal.addLayout(grid)

        # Botón agregar
        self.btn_agregar = QPushButton("Agregar Promoción")
        self.btn_agregar.setObjectName("agregar")
        layout_principal.addWidget(self.btn_agregar, alignment=Qt.AlignCenter)

        self.setLayout(layout_principal)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = AgregarPromocion()
    ventana.show()
    sys.exit(app.exec_())
