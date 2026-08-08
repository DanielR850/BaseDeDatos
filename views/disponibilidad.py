import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QWidget, QHeaderView, QLabel, QPushButton, QHBoxLayout
)
from PyQt5.QtGui import QFont, QBrush, QColor
from PyQt5.QtCore import Qt
from datetime import date
from models.cita import eliminar_cita_por_id  # Asegúrate de importar esto
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QSizePolicy

class DisponibilidadCitas(QMainWindow):
    def __init__(self, regresar_callback=None):
        super().__init__()
        self.setWindowTitle("Disponibilidad de Citas")
        self.setMinimumSize(1024, 1000)
        self.showMaximized()
        self.regresar_callback = regresar_callback
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

        # Botones superiores
        btn_regresar = QPushButton("⤺ Regresar")
        btn_regresar.setObjectName("regresar")
        btn_regresar.clicked.connect(self.regresar)

        fila_superior = QHBoxLayout()
        fila_superior.addWidget(btn_regresar, alignment=Qt.AlignLeft)

        titulo = QLabel("Disponibilidad de Citas")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-size: 28pt; font-weight: bold; background-color: transparent; margin-top: 10px; margin-bottom: 20px;")
        fila_superior.addStretch()
        fila_superior.addWidget(titulo)
        fila_superior.addStretch()

        layout_principal.addLayout(fila_superior)

        # Tabla
        tabla_layout = QVBoxLayout()
        tabla_layout.setContentsMargins(200, 20, 200, 20)

        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(4)
        self.table_widget.setHorizontalHeaderLabels(["Fecha", "Hora", "Cliente", "Servicio Requerido"])
        self.table_widget.setFont(QFont("Poppins", 12))
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.table_widget.verticalHeader().setVisible(False)
        self.table_widget.setSelectionBehavior(QTableWidget.SelectRows)
        self.table_widget.setSelectionMode(QTableWidget.SingleSelection)

        tabla_layout.addWidget(self.table_widget)

        # Botón eliminar
        self.btn_eliminar = QPushButton("Eliminar Cita")
        self.btn_eliminar.setStyleSheet("""
            QPushButton {
                background-color: #E57979;
                border-radius: 25px;
                padding: 12px 25px;
                font-size: 16pt;
                font-weight: bold;
                color: white;
            }
            QPushButton:hover {
                background-color: #C62828;
            }
        """)
        self.btn_eliminar.clicked.connect(self.eliminar_cita_seleccionada)
        tabla_layout.addWidget(self.btn_eliminar, alignment=Qt.AlignCenter)

        layout_principal.addLayout(tabla_layout)

        container = QWidget()
        container.setLayout(layout_principal)
        self.setCentralWidget(container)

        self.cargar_citas()

    def regresar(self):
        self.close()
        if self.regresar_callback:
            self.regresar_callback()



    def cargar_citas(self):
        from models.cita import obtener_citas_hoy

        citas_hoy = obtener_citas_hoy()
        self.table_widget.setRowCount(len(citas_hoy))

        for fila, cita in enumerate(citas_hoy):
            # Convertir fecha y hora a cadena si son objetos datetime
            fecha_str = str(cita["fecha"])
            hora_str = str(cita["hora"])

            self.table_widget.setItem(fila, 0, QTableWidgetItem(fecha_str))
            self.table_widget.setItem(fila, 1, QTableWidgetItem(hora_str))
            self.table_widget.setItem(fila, 2, QTableWidgetItem(cita["cliente"]))
            self.table_widget.setItem(fila, 3, QTableWidgetItem(cita["trabajo"]))

            # Guardar ID de cita como dato oculto en todas las columnas
            for col in range(4):
                item = self.table_widget.item(fila, col)
                if item:
                    item.setData(Qt.UserRole, cita["id"])
                    item.setBackground(QBrush(QColor("#e5d3c5" if col == 0 else "#ffefe3")))



    def eliminar_cita_seleccionada(self):
        fila = self.table_widget.currentRow()
        if fila >= 0:
            item = self.table_widget.item(fila, 0)
            id_cita = item.data(Qt.UserRole)
            if id_cita:
                confirmacion = QMessageBox.question(
                    self, "Confirmar eliminación",
                    "¿Estás seguro de que deseas eliminar esta cita?",
                    QMessageBox.Yes | QMessageBox.No
                )
                if confirmacion == QMessageBox.Yes:
                    if eliminar_cita_por_id(id_cita):
                        QMessageBox.information(self, "Eliminado", "Cita eliminada correctamente.")
                        self.cargar_citas()
                    else:
                        QMessageBox.critical(self, "Error", "No se pudo eliminar la cita.")
