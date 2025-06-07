from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QTextEdit,
    QVBoxLayout, QHBoxLayout, QMessageBox
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import datetime
from models.promocion import actualizar_promocion


class ModificarPromocion(QWidget):
    def __init__(self, promocion, regresar_callback=None):
        super().__init__()
        self.setWindowTitle("Modificar Promoción")
        self.setMinimumSize(1024, 1000)
        self.showMaximized()
        self.regresar_callback = regresar_callback
        self.promocion = promocion

        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #f8c8dc, stop: 1 #fefefe);
                font-family: 'Poppins';
            }
            QLabel {
                background-color: transparent;
                font-size: 16pt;
                color: #000000;
            }
            QLineEdit, QTextEdit {
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
            QPushButton#guardar {
                background-color: #231f20;
                color: #fcb3b3;
                font-family: 'Poppins';
                padding: 15px;
                border-radius: 20px;
                font-size: 18pt;
                min-width: 250px;
                min-height: 80px;
            }
            QPushButton#guardar:hover {
                background-color: #333333;
            }
        """)

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(50, 30, 50, 30)
        layout.setSpacing(25)

        # Botón regresar y logo
        fila_top = QHBoxLayout()
        self.btn_regresar = QPushButton("⤺ Regresar")
        self.btn_regresar.setObjectName("regresar")
        self.btn_regresar.clicked.connect(self.volver_a_promociones)
        fila_top.addWidget(self.btn_regresar)
        fila_top.addStretch()

        logo = QLabel()
        logo.setPixmap(QPixmap("resources/logo_sinfondo.png").scaledToHeight(100))
        logo.setAlignment(Qt.AlignRight)
        fila_top.addWidget(logo)
        layout.addLayout(fila_top)

        # Título
        titulo = QLabel("Modificar Promoción")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-size: 28pt; font-weight: bold; margin-top: 10px; margin-bottom: 30px;")
        layout.addWidget(titulo)

        # Campos
        self.descripcion_input = QTextEdit(self.promocion.get("Descripcion", ""))
        self.descuento_input = QLineEdit(str(self.promocion.get("Descuento", "")))
        self.fecha_inicio_input = QLineEdit(str(self.promocion.get("Fecha_Inicio", "")))
        self.fecha_fin_input = QLineEdit(str(self.promocion.get("Fecha_Fin", "")))

        layout.addLayout(self.form_group("Descripción", self.descripcion_input))
        layout.addLayout(self.form_group("Porcentaje de Descuento", self.descuento_input))
        layout.addLayout(self.form_group("Fecha de Inicio (YYYY-MM-DD)", self.fecha_inicio_input))
        layout.addLayout(self.form_group("Fecha de Vencimiento (YYYY-MM-DD)", self.fecha_fin_input))

        # Botón guardar
        self.btn_guardar = QPushButton("Guardar Cambios")
        self.btn_guardar.setObjectName("guardar")
        self.btn_guardar.clicked.connect(self.guardar_cambios)
        layout.addWidget(self.btn_guardar, alignment=Qt.AlignCenter)

        self.setLayout(layout)

    def form_group(self, texto, widget):
        layout = QVBoxLayout()
        label = QLabel(texto)
        label.setAlignment(Qt.AlignLeft)
        layout.addWidget(label)
        layout.addWidget(widget)
        return layout

    def guardar_cambios(self):
        descripcion = self.descripcion_input.toPlainText().strip()
        descuento = self.descuento_input.text().strip()
        fecha_inicio = self.fecha_inicio_input.text().strip()
        fecha_fin = self.fecha_fin_input.text().strip()

        if not all([descripcion, descuento, fecha_inicio, fecha_fin]):
            QMessageBox.warning(self, "Campos incompletos", "Por favor completa todos los campos.")
            return

        try:
            descuento_float = float(descuento)
            if descuento_float > 100 or descuento_float < 0:
                QMessageBox.warning(self, "Valor inválido", "El descuento debe ser entre 0 y 100.")
                return
        except ValueError:
            QMessageBox.critical(self, "Error", "El descuento debe ser un número.")
            return

        try:
            datetime.datetime.strptime(fecha_inicio, "%Y-%m-%d")
            datetime.datetime.strptime(fecha_fin, "%Y-%m-%d")
        except ValueError:
            QMessageBox.critical(self, "Error de Fecha", "Formato inválido. Usa YYYY-MM-DD.")
            return

        if "ID_Promocion" not in self.promocion:
            QMessageBox.critical(self, "Error interno", "No se encontró el ID de la promoción.")
            return

        exito = actualizar_promocion(
            self.promocion["ID_Promocion"],
            descripcion,
            descuento_float,
            fecha_inicio,
            fecha_fin
        )

        if exito:
            QMessageBox.information(self, "Éxito", "Promoción actualizada correctamente.")
            if self.regresar_callback:
                self.regresar_callback()
            self.close()
        else:
            QMessageBox.critical(self, "Error", "No se pudo actualizar la promoción.")

    def volver_a_promociones(self):
        if self.regresar_callback:
            self.close()
            self.regresar_callback()
        else:
            self.close()
