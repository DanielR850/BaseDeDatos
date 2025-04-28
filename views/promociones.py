import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QPushButton,
    QLabel, QVBoxLayout, QHBoxLayout, QTableWidget,
    QTableWidgetItem, QHeaderView, QLineEdit
)
from PyQt5.QtGui import QIcon, QColor, QPixmap
from PyQt5.QtCore import Qt, QSize

class VentanaPromociones(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Promociones")
        self.showFullScreen()

        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(
                    x1: 0, y1: 0,
                    x2: 0, y2: 1,
                    stop: 0 #EBAAAA,
                    stop: 1 #EADAD3
                );
                font-family: 'Poppins';
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
        """)

        # Widget principal
        widget_principal = QWidget()
        self.setCentralWidget(widget_principal)

        layout_principal = QVBoxLayout(widget_principal)
        layout_principal.setContentsMargins(30, 30, 30, 30)
        layout_principal.setSpacing(20)

        # --- Barra superior ---
        layout_superior = QHBoxLayout()

        self.btn_regresar = QPushButton("Regresar")
        self.btn_regresar.setObjectName("regresar")
        self.btn_salir = QPushButton("Salir")
        self.btn_salir.setObjectName("salir")
        self.btn_salir.clicked.connect(self.close)

        layout_superior.addWidget(self.btn_regresar)
        layout_superior.addStretch()
        layout_superior.addWidget(self.btn_salir)

        layout_principal.addLayout(layout_superior)

        # --- Barra de búsqueda ---
        layout_busqueda = QHBoxLayout()
        self.busqueda = QLineEdit()
        self.busqueda.setPlaceholderText("Buscar...")
        self.busqueda.setStyleSheet("""
            QLineEdit {
                background: white;
                border-radius: 15px;
                padding: 8px 35px 8px 15px;
                font: 14px 'Roboto';
                min-width: 250px;
            }
        """)
        layout_busqueda.addStretch()
        layout_busqueda.addWidget(self.busqueda)
        layout_busqueda.addStretch()
        layout_principal.addLayout(layout_busqueda)

        # --- Título ---
        titulo = QLabel("Promociones")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("""
            font: bold 38px 'Roboto';
            color: black;
            padding: 15px;
            background: transparent;
        """)
        layout_principal.addWidget(titulo)

        # --- Botones principales ---
        layout_botones = QHBoxLayout()
        layout_botones.setSpacing(25)

        for texto, color in [
            ("Agregar promoción", "#c6fcb3"),
            ("Modificar promoción", "#fcfbb3"),
            ("Eliminar promoción", "#E57979")
        ]:
            boton = QPushButton(texto)
            boton.setStyleSheet(f"""
                QPushButton {{
                    background: {color};
                    border-radius: 25px;
                    padding: 15px 30px;
                    font: bold 18px;
                    color: black;
                    min-width: 200px;
                }}
                QPushButton:hover {{
                    background: {'#689F38' if color == "#c6fcb3" else
                                '#FFB300' if color == "#fcfbb3" else
                                '#C62828'};
                }}
            """)
            layout_botones.addWidget(boton)

        layout_principal.addLayout(layout_botones)

        # --- Tabla de promociones ---
        self.tabla = QTableWidget(6, 4)
        self.tabla.setHorizontalHeaderLabels(["Descripción", "Servicios", "Precio", "Válido hasta"])
        self.tabla.setStyleSheet("""
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
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabla.verticalHeader().setVisible(False)
        self.tabla.setShowGrid(True)

        layout_principal.addWidget(self.tabla)

        # --- Logo ---
        lbl_logo = QLabel()
        pixmap = QPixmap('c:/Users/agnav/OneDrive - Universidad Autonoma de Nuevo León/Desktop/Base de datos proyecto/BaseDeDatos/BaseDeDatosSalonDeBelleza/resources/logo_sinfondo.png').scaled(80, 80, Qt.KeepAspectRatio)
        lbl_logo.setPixmap(pixmap)
        lbl_logo.setAlignment(Qt.AlignRight | Qt.AlignBottom)
        lbl_logo.setStyleSheet("padding: 0 10px 10px 0; background: transparent;")
        layout_principal.addWidget(lbl_logo, alignment=Qt.AlignRight | Qt.AlignBottom)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaPromociones()
    ventana.show()
    sys.exit(app.exec_())
