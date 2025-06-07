import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QPushButton, QLabel,
    QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QHeaderView, QLineEdit
)
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, QSize
from models.pago import obtener_todos_los_pagos

class RegistroPago(QMainWindow):
    def __init__(self, regresar_callback=None):
        super().__init__()
        self.setWindowTitle("Registro de Pagos")
        self.setMinimumSize(1024, 1000)
        self.showMaximized()
        self.regresar_callback = regresar_callback
        self.initUI()

    def initUI(self):
        widget_principal = QWidget()
        self.setCentralWidget(widget_principal)

        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #EBAAAA,
                    stop: 1 #EADAD3
                );
                font-family: 'Poppins';
            }
            QLineEdit {
                background: white;
                border-radius: 15px;
                padding: 8px 35px 8px 15px;
                font: 14px 'Roboto';
                min-width: 250px;
            }
            QTableWidget {
                background: #ffefe3;
                border-radius: 15px;
                padding: 10px;
                font: 16px 'Roboto';
                color: #4E342E;
            }
            QHeaderView::section {
                background: #D7CCC8;
                font: bold 18px;
                padding: 12px;
                border: none;
            }
            QTableWidget::item {
                border-bottom: 2px solid #D7CCC8;
                padding: 15px;
            }
        """)

        layout_principal = QVBoxLayout(widget_principal)
        layout_principal.setContentsMargins(30, 30, 30, 30)
        layout_principal.setSpacing(20)

        # ⬅️ Barra superior
        layout_superior = QHBoxLayout()

        boton_regresar = QPushButton("⤺ Regresar")
        boton_regresar.setObjectName("regresar")
        boton_regresar.clicked.connect(self.volver_a_home)
        boton_regresar.setStyleSheet("""
            QPushButton {
                background-color: #231f20;
                color: #fcb3b3;
                padding: 10px 20px;
                border-radius: 20px;
                font-size: 14pt;
                font-weight: bold;
                min-width: 150px;
            }
            QPushButton:hover {
                background-color: #333333;
            }
        """)

        self.busqueda = QLineEdit()
        self.busqueda.setPlaceholderText("Buscar por cliente...")
        self.busqueda.textChanged.connect(self.filtrar_pagos)

        layout_superior.addWidget(boton_regresar)
        layout_superior.addStretch()
        layout_superior.addWidget(self.busqueda)
        layout_principal.addLayout(layout_superior)

        # 🎯 Contenedor de título transparente
        contenedor_titulo = QWidget()
        contenedor_titulo.setStyleSheet("background-color: transparent;")
        contenedor_layout = QVBoxLayout(contenedor_titulo)
        contenedor_layout.setContentsMargins(0, 0, 0, 0)

        titulo = QLabel("Registro de Pagos")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font: bold 38px 'Roboto'; color: black; padding: 15px; background-color: transparent;")
        contenedor_layout.addWidget(titulo)
        layout_principal.addWidget(contenedor_titulo)

        # 📋 Tabla de pagos
        self.tabla_pagos = QTableWidget(0, 3)
        self.tabla_pagos.setHorizontalHeaderLabels(["Cliente", "Monto", "Método"])
        self.tabla_pagos.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabla_pagos.verticalHeader().setVisible(False)
        self.tabla_pagos.setShowGrid(True)
        layout_principal.addWidget(self.tabla_pagos)

        # 🖼️ Logo
        lbl_logo = QLabel()
        pixmap = QPixmap('resources/logo_sinfondo.png').scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        lbl_logo.setPixmap(pixmap)
        lbl_logo.setAlignment(Qt.AlignRight | Qt.AlignBottom)
        lbl_logo.setStyleSheet("padding: 0 10px 10px 0; background: transparent;")
        layout_principal.addWidget(lbl_logo, alignment=Qt.AlignRight | Qt.AlignBottom)

        self.cargar_datos()

    def cargar_datos(self):
        pagos = obtener_todos_los_pagos()
        self.tabla_pagos.setRowCount(len(pagos))
        for row_index, pago in enumerate(pagos):
            self.tabla_pagos.setItem(row_index, 0, QTableWidgetItem(pago["cliente"]))
            self.tabla_pagos.setItem(row_index, 1, QTableWidgetItem(f"${pago['monto']:.2f}"))
            self.tabla_pagos.setItem(row_index, 2, QTableWidgetItem(pago["metodo"]))

    def filtrar_pagos(self):
        texto = self.busqueda.text().lower()
        for fila in range(self.tabla_pagos.rowCount()):
            item_cliente = self.tabla_pagos.item(fila, 0)
            if item_cliente:
                visible = texto in item_cliente.text().lower()
                self.tabla_pagos.setRowHidden(fila, not visible)

    def volver_a_home(self):
        self.close()
        if self.regresar_callback:
            self.regresar_callback()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = RegistroPago()
    ventana.show()
    sys.exit(app.exec_())
