import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QComboBox
)
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt

class GenerarPago(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Generar Pago")
        self.showFullScreen()

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
                font-family: 'Poppins';
            }
            QLineEdit, QComboBox {
                background-color: #e5d3c5;
                border: 2px solid #000000;
                border-radius: 10px;
                padding: 10px;
                font-size: 14pt;
                min-width: 250px;
                min-height: 41px;
            }
            QPushButton#regresar, QPushButton#salir {
                background-color: transparent;
                color: #101111;
                font-family: 'Open Sans';
                padding: 10px;
                font-size: 14pt;
                font-weight: bold;
                min-width: 100px;
            }
            QPushButton#regresar:hover, QPushButton#salir:hover {
                color: gray;
            }
            QPushButton#pagar {
                background-color: #231f20;
                color: #fcb3b3;
                font-family: 'Poppins';
                padding: 15px;
                border-radius: 20px;
                font-size: 18pt;
                min-width: 300px;
                min-height: 80px;
            }
            QPushButton#pagar:hover {
                background-color: #333333;
            }
        """)

        self.initUI()

    def initUI(self):
        layout_principal = QVBoxLayout()
        layout_principal.setContentsMargins(100, 20, 100, 20)

        # Botones superiores
        botones_superiores = QHBoxLayout()
        self.btn_regresar = QPushButton("Regresar")
        self.btn_regresar.setObjectName("regresar")
        self.btn_salir = QPushButton("Salir")
        self.btn_salir.setObjectName("salir")
        self.btn_salir.clicked.connect(self.close)

        botones_superiores.addWidget(self.btn_regresar)
        botones_superiores.addStretch()
        botones_superiores.addWidget(self.btn_salir)
        layout_principal.addLayout(botones_superiores)

        # Logo
        logo = QLabel()
        pixmap = QPixmap("C:/Users/makib/Documents/EntornosVirtuales/BaseDeDatosSalonDeBelleza/resources/logo_sinfondo.png")
        logo.setPixmap(pixmap.scaled(120, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        logo.setAlignment(Qt.AlignCenter)
        layout_principal.addWidget(logo)

        # Título
        titulo = QLabel("Generar Pago")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-size: 28pt; font-weight: bold; margin-bottom: 30px;")
        layout_principal.addWidget(titulo)

        # Formulario
        campos_centrados = QVBoxLayout()
        campos_centrados.setAlignment(Qt.AlignCenter)

        # Primera fila: 3 campos
        fila1 = QHBoxLayout()
        fila1.setSpacing(50)
        self.cita = QLineEdit()
        self.nombre = QLineEdit()
        self.telefono = QLineEdit()

        vbox_cita = self.create_field_group("Cita", self.cita)
        vbox_nombre = self.create_field_group("Nombre", self.nombre)
        vbox_telefono = self.create_field_group("Teléfono", self.telefono)

        fila1.addLayout(vbox_cita)
        fila1.addLayout(vbox_nombre)
        fila1.addLayout(vbox_telefono)

        # Segunda fila: 3 campos
        fila2 = QHBoxLayout()
        fila2.setSpacing(50)
        self.servicio = QLineEdit()
        self.empleado = QLineEdit()
        self.metodo_pago = QComboBox()
        self.metodo_pago.addItems(["Efectivo", "Tarjeta", "Transferencia"])

        vbox_servicio = self.create_field_group("Servicio", self.servicio)
        vbox_empleado = self.create_field_group("Empleado", self.empleado)
        vbox_pago = self.create_field_group("Método de Pago", self.metodo_pago)

        fila2.addLayout(vbox_servicio)
        fila2.addLayout(vbox_empleado)
        fila2.addLayout(vbox_pago)

        campos_centrados.addLayout(fila1)
        campos_centrados.addSpacing(40)
        campos_centrados.addLayout(fila2)

        layout_principal.addLayout(campos_centrados)

        # Botón Pagar
        self.btn_pagar = QPushButton("Realizar Pago")
        self.btn_pagar.setObjectName("pagar")
        layout_principal.addSpacing(30)
        layout_principal.addWidget(self.btn_pagar, alignment=Qt.AlignCenter)

        self.setLayout(layout_principal)

    def create_field_group(self, label_text, input_widget):
        group = QVBoxLayout()
        label = QLabel(label_text)
        label.setAlignment(Qt.AlignCenter)
        group.addWidget(label)
        group.addWidget(input_widget)
        return group

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = GenerarPago()
    ventana.show()
    sys.exit(app.exec_())
