from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QTextEdit,
    QComboBox, QVBoxLayout, QHBoxLayout, QMessageBox
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import datetime
from models.promocion import insertar_promocion
from models.servicio_model import obtener_servicios

class AgregarPromocion(QWidget):
    def __init__(self, regresar_callback=None):
        super().__init__()
        self.setWindowTitle("Agregar Promoción")
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
            QLabel {
                background-color: transparent;
                font-size: 16pt;
                color: #000000;
            }
            QLineEdit, QTextEdit, QComboBox {
                background-color: #e5d3c5;
                border: 2px solid #000000;
                border-radius: 10px;
                padding: 10px;
                font-size: 14pt;
                min-height: 40px;
            }
            QPushButton#regresar {
                background-color: transparent;
                color: #101111;
                font-family: 'Open Sans';
                padding: 10px;
                font-size: 14pt;
                font-weight: bold;
                min-width: 100px;
            }
            QPushButton#regresar:hover {
                color: gray;
            }
            QPushButton#agregar {
                background-color: #231f20;
                color: #fcb3b3;
                font-family: 'Poppins';
                padding: 15px;
                border-radius: 20px;
                font-size: 18pt;
                min-width: 250px;
                min-height: 80px;
            }
            QPushButton#agregar:hover {
                background-color: #333333;
            }
        """)

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(50, 30, 50, 30)
        layout.setSpacing(25)

        # --- Botón regresar ---
        fila1 = QHBoxLayout()
        self.btn_regresar = QPushButton("⤺ Regresar")
        self.btn_regresar.setObjectName("regresar")
        self.btn_regresar.clicked.connect(self.volver_a_promociones)
        fila1.addWidget(self.btn_regresar)
        fila1.addStretch()
        layout.addLayout(fila1)

        # --- Logo ---
        logo = QLabel()
        pixmap = QPixmap("resources/logo_sinfondo.png")
        logo.setPixmap(pixmap.scaledToHeight(100))
        logo.setAlignment(Qt.AlignCenter)
        layout.addWidget(logo)

        # --- Título ---
        titulo = QLabel("Agregar Promoción")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-size: 28pt; font-weight: bold; margin-top: 10px; margin-bottom: 30px;")
        layout.addWidget(titulo)

        # --- Campos principales ---
        self.nombre_input = QLineEdit()
        self.servicio_combo = QComboBox()
        self.descripcion_input = QTextEdit()
        self.descuento_input = QLineEdit()
        self.fecha_inicio_input = QLineEdit()
        self.fecha_fin_input = QLineEdit()

        self.servicios = obtener_servicios()
        for servicio in self.servicios:
            self.servicio_combo.addItem(servicio["Nombre"], servicio["ID"])

        layout.addLayout(self.build_field("Nombre de la Promoción", self.nombre_input))
        layout.addLayout(self.build_field("Servicio de la Promoción", self.servicio_combo))
        layout.addLayout(self.build_field("Descripción", self.descripcion_input))

        # --- Fila final: Porcentaje + Fechas ---
        fila_final = QHBoxLayout()
        fila_final.setSpacing(30)
        fila_final.addLayout(self.build_field("Porcentaje de descuento (%)", self.descuento_input))
        fila_final.addLayout(self.build_field("Fecha de Inicio (YYYY-MM-DD)", self.fecha_inicio_input))
        fila_final.addLayout(self.build_field("Fecha de Vencimiento (YYYY-MM-DD)", self.fecha_fin_input))
        layout.addLayout(fila_final)

        # --- Botón Agregar ---
        self.btn_agregar = QPushButton("Agregar Promoción")
        self.btn_agregar.setObjectName("agregar")
        self.btn_agregar.clicked.connect(self.guardar_promocion)
        layout.addSpacing(30)
        layout.addWidget(self.btn_agregar, alignment=Qt.AlignCenter)

        self.setLayout(layout)

    def build_field(self, label_text, widget):
        layout = QVBoxLayout()
        label = QLabel(label_text)
        label.setAlignment(Qt.AlignLeft)
        layout.addWidget(label)
        layout.addWidget(widget)
        return layout

    def guardar_promocion(self):
        descripcion = self.descripcion_input.toPlainText().strip()
        servicio = self.servicio_combo.currentText()
        descuento = self.descuento_input.text().strip()
        fecha_inicio = self.fecha_inicio_input.text().strip()
        fecha_fin = self.fecha_fin_input.text().strip()

        if not all([descripcion, servicio, descuento, fecha_inicio, fecha_fin]):
            QMessageBox.warning(self, "Campos incompletos", "Por favor completa todos los campos.")
            return

        try:
            descuento_float = float(descuento)
            if not (1 <= descuento_float <= 100):
                QMessageBox.warning(self, "Porcentaje inválido", "El porcentaje debe estar entre 1 y 100.")
                return
        except ValueError:
            QMessageBox.critical(self, "Error", "El porcentaje debe ser un número.")
            return

        try:
            datetime.datetime.strptime(fecha_inicio, "%Y-%m-%d")
            datetime.datetime.strptime(fecha_fin, "%Y-%m-%d")
        except ValueError:
            QMessageBox.critical(self, "Error de Fecha", "Usa el formato correcto: YYYY-MM-DD.")
            return

        id_servicio = self.servicio_combo.currentData()
        exito = insertar_promocion(descripcion, descuento_float, fecha_inicio, fecha_fin, id_servicio)

        if exito:
            QMessageBox.information(self, "Éxito", "Promoción agregada correctamente.")
            if self.regresar_callback:
                self.regresar_callback()
            self.close()
        else:
            QMessageBox.critical(self, "Error", "No se pudo agregar la promoción.")

    def volver_a_promociones(self):
        if self.regresar_callback:
            self.close()
            self.regresar_callback()
        else:
            self.close()
