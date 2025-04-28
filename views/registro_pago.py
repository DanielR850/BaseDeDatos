import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QPushButton,
    QLabel, QVBoxLayout, QHBoxLayout, QTableWidget,
    QTableWidgetItem, QHeaderView, QLineEdit, QSizePolicy
)
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, QSize

class RegistroPago(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Registro de Pagos")
        self.showFullScreen()

        # Widget principal
        widget_principal = QWidget()
        widget_principal.setStyleSheet("""
            background: qlineargradient(
                x1: 0, y1: 0,
                x2: 0, y2: 1,
                stop: 0 #EBAAAA,
                stop: 1 #EADAD3
            );
            font-family: 'Poppins';
        """)
        self.setCentralWidget(widget_principal)

        layout_principal = QVBoxLayout(widget_principal)
        layout_principal.setContentsMargins(30, 30, 30, 30)
        layout_principal.setSpacing(20)

        # --- Barra superior: Regresar y Salir ---
        barra_superior = QHBoxLayout()

        self.btn_regresar = QPushButton("Regresar")
        self.btn_regresar.setObjectName("regresar")
        self.btn_salir = QPushButton("Salir")
        self.btn_salir.setObjectName("salir")
        self.btn_salir.clicked.connect(self.close)

        self.btn_regresar.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #101111;
                font-family: 'Open Sans';
                padding: 10px;
                font-size: 14pt;
                font-weight: bold;
                min-width: 100px;
            }
            QPushButton:hover {
                color: gray;
            }
        """)
        self.btn_salir.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #101111;
                font-family: 'Open Sans';
                padding: 10px;
                font-size: 14pt;
                font-weight: bold;
                min-width: 100px;
            }
            QPushButton:hover {
                color: gray;
            }
        """)

        barra_superior.addWidget(self.btn_regresar)
        barra_superior.addStretch()
        barra_superior.addWidget(self.btn_salir)
        layout_principal.addLayout(barra_superior)

        # --- Título ---
        titulo = QLabel("Registro de Pagos")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("""
            font: bold 38px 'Roboto';
            color: black;
            padding: 15px;
            background: #EBAAAA;
        """)
        layout_principal.addWidget(titulo)

        # --- Barra de búsqueda y eliminar ---
        barra_acciones = QHBoxLayout()

        self.boton_buscar = QPushButton("Buscar Transacción")
        self.boton_eliminar = QPushButton("Eliminar Transacción")
        self.input_buscar = QLineEdit()
        self.input_eliminar = QLineEdit()

        self.input_buscar.setPlaceholderText("Ingrese el ID a buscar")
        self.input_eliminar.setPlaceholderText("Ingrese el ID a eliminar")
        self.input_buscar.setFixedWidth(250)
        self.input_eliminar.setFixedWidth(250)

        self.boton_buscar.setStyleSheet("""
            QPushButton {
                background-color: #D9FFCC;
                color: black;
                border-radius: 20px;
                padding: 12px 20px;
                font-size: 16px;
                font-weight: bold;
                border: none;
            }
            QPushButton:hover {
                background-color: lightblue;
            }
        """)
        self.boton_eliminar.setStyleSheet("""
            QPushButton {
                background-color: #CF6978;
                color: black;
                border-radius: 20px;
                padding: 12px 20px;
                font-size: 16px;
                font-weight: bold;
                border: none;
            }
            QPushButton:hover {
                background-color: lightblue;
            }
        """)

        barra_acciones.addWidget(self.boton_buscar)
        barra_acciones.addWidget(self.input_buscar)
        barra_acciones.addWidget(self.boton_eliminar)
        barra_acciones.addWidget(self.input_eliminar)
        layout_principal.addLayout(barra_acciones)

        # --- Tabla ---
        self.tabla_pagos = QTableWidget(13, 4)
        self.tabla_pagos.setHorizontalHeaderLabels(["Cliente", "Monto", "Método", "Fecha"])
        self.tabla_pagos.setStyleSheet("""
            QTableWidget {
                background-color: #F5F5DC;
                font-size: 15px;
                font: bold;
                font-family: 'sans-serif';
            }
            QHeaderView::section {
                background-color: #CF6978;
                color: black;
                font-weight: bold;
                font-size: 27px;
            }
            QTableCornerButton::section {
                background-color: #CF6978;
                border: 1px solid #999;
            }
        """)
        self.tabla_pagos.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabla_pagos.verticalHeader().setVisible(False)
        self.tabla_pagos.setShowGrid(True)

        layout_principal.addWidget(self.tabla_pagos)

        # --- Logo en esquina inferior ---
        lbl_logo = QLabel()
        pixmap = QPixmap('C:/Users/Lutec/OneDrive/Documentos/Diego Luna De Labra/6to semestre/Bases de datos/BaseDeDatos/BaseDeDatosSalonDeBelleza/resources/logo_sinfondo.png').scaled(80, 80, Qt.KeepAspectRatio)
        lbl_logo.setPixmap(pixmap)
        lbl_logo.setAlignment(Qt.AlignRight | Qt.AlignBottom)
        lbl_logo.setStyleSheet("padding: 10px; background: transparent;")
        layout_principal.addWidget(lbl_logo, alignment=Qt.AlignRight)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = RegistroPago()
    ventana.show()
    sys.exit(app.exec_())
