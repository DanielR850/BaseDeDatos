import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QWidget, QHeaderView, QLabel, QPushButton, QHBoxLayout
)
from PyQt5.QtGui import QFont, QBrush, QColor
from PyQt5.QtCore import Qt

class DisponibilidadCitas(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Disponibilidad de Citas")
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
            QTableWidget {
                background-color: #ffefe3;
                font-size: 14pt;
                border: 2px solid #d4a5a5;
                gridline-color: #e0cfcf;
            }
            QHeaderView::section {
                background-color: #e5d3c5;
                font-size: 16pt;
                font-weight: bold;
                color: #333333;
            }
            QPushButton#regresar {
                background-color: #231f20;
                color: #fcb3b3;
                font-family: 'Poppins';
                padding: 10px;
                border-radius: 20px;
                font-size: 14pt;
                min-width: 150px;
            }
            QPushButton#regresar:hover {
                background-color: #333333;
            }
        """)
        self.initUI()

    def initUI(self):
        layout_principal = QVBoxLayout()

        # Botón de regresar
        btn_regresar = QPushButton("⤺ Regresar")
        btn_regresar.setObjectName("regresar")
        btn_regresar.clicked.connect(self.close)

        fila_superior = QHBoxLayout()
        fila_superior.addWidget(btn_regresar, alignment=Qt.AlignLeft)

        titulo = QLabel("Disponibilidad de Citas")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-size: 28pt; font-weight: bold; background-color: transparent; margin-top: 10px; margin-bottom: 20px;")
        fila_superior.addStretch()
        fila_superior.addWidget(titulo)
        fila_superior.addStretch()

        layout_principal.addLayout(fila_superior)

        # Contenedor de tabla con márgenes reducidos
        tabla_layout = QVBoxLayout()
        tabla_layout.setContentsMargins(200, 20, 200, 100)  # Espacios laterales y abajo

        self.table_widget = QTableWidget()
        self.table_widget.setRowCount(6)  # Solo 6 filas
        self.table_widget.setColumnCount(4)  # Fecha + Hora + Cliente + Trabajo

        self.table_widget.setHorizontalHeaderLabels(["Fecha", "Hora", "Cliente", "Trabajo Requerido"])
        self.table_widget.setFont(QFont("Poppins", 12))

        # Ajustar columnas
        header = self.table_widget.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        self.table_widget.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

        citas = [
            ("Jueves 27 Marzo", "10:00 AM", "Ana Torres", "Maquillaje"),
            ("Jueves 27 Marzo", "11:30 AM", "Luis Gómez", "Peinado"),
            ("Jueves 27 Marzo", "12:00 PM", "Claudia Reyes", "Uñas"),
            ("Viernes 28 Marzo", "09:00 AM", "Mariana Díaz", "Peinado"),
            ("Viernes 28 Marzo", "10:30 AM", "Carlos Sánchez", "Maquillaje"),
            ("Viernes 28 Marzo", "12:00 PM", "Patricia Velázquez", "Uñas"),
        ]

        for fila, (fecha, hora, cliente, trabajo) in enumerate(citas):
            self.table_widget.setItem(fila, 0, QTableWidgetItem(fecha))
            self.table_widget.setItem(fila, 1, QTableWidgetItem(hora))
            self.table_widget.setItem(fila, 2, QTableWidgetItem(cliente))
            self.table_widget.setItem(fila, 3, QTableWidgetItem(trabajo))

        # Personalizar colores de celdas
        for fila in range(self.table_widget.rowCount()):
            for columna in range(self.table_widget.columnCount()):
                item = self.table_widget.item(fila, columna)
                if item is not None:
                    if columna == 0:
                        item.setBackground(QBrush(QColor("#e5d3c5")))
                    else:
                        item.setBackground(QBrush(QColor("#ffefe3")))

        tabla_layout.addWidget(self.table_widget)
        layout_principal.addLayout(tabla_layout)

        container = QWidget()
        container.setLayout(layout_principal)
        self.setCentralWidget(container)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = DisponibilidadCitas()
    ventana.show()
    sys.exit(app.exec_())
