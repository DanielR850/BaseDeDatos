from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QTextEdit,
    QComboBox, QVBoxLayout, QHBoxLayout, QGridLayout, QMessageBox
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import sys
from models.promocion import actualizar_promocion

class ModificarPromocion(QWidget):
    def __init__(self, promocion, regresar_callback=None):
        super().__init__()
        self.setWindowTitle("Modificar Promoción")
        self.showFullScreen()
        self.regresar_callback = regresar_callback
        self.promocion = promocion  # Diccionario con datos de la promoción

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

        # --- Barra superior con botón regresar y logo ---
        fila_superior = QHBoxLayout()
        self.btn_regresar = QPushButton("⤺ Regresar")
        self.btn_regresar.setObjectName("regresar")
        self.btn_regresar.clicked.connect(self.volver_a_promociones)
        fila_superior.addWidget(self.btn_regresar, alignment=Qt.AlignLeft)
        fila_superior.addStretch()

        self.logo = QLabel()
        pixmap = QPixmap("resources/logo_sinfondo.png")
        self.logo.setPixmap(pixmap.scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        fila_superior.addWidget(self.logo, alignment=Qt.AlignRight)

        layout_principal.addLayout(fila_superior)

        # --- Título ---
        titulo = QLabel("Modificar Promoción")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-size: 28pt; font-weight: bold; margin-top: 10px; margin-bottom: 30px;")
        layout_principal.addWidget(titulo)

        # --- Grid de campos ---
        grid = QGridLayout()
        grid.setSpacing(30)

        # Campo: Nombre de la promoción
        self.nombre_label = QLabel("Nombre de la Promoción")
        self.nombre_input = QLineEdit(self.promocion.get("Descripcion", ""))

        # Campo: Descripción
        self.descripcion_label = QLabel("Descripción")
        self.descripcion_input = QTextEdit(self.promocion.get("Descripcion", ""))

        # Campo: Descuento
        self.descuento_label = QLabel("Descuento")
        descuento = self.promocion.get("Descuento", self.promocion.get("Precio", ""))
        self.descuento_input = QLineEdit(str(descuento))

        # Campo: Fecha de inicio
        self.fecha_inicio_label = QLabel("Fecha de Inicio (YYYY-MM-DD)")
        self.fecha_inicio_input = QLineEdit(str(self.promocion.get("Fecha_Inicio", "")))

        # Campo: Fecha de fin
        self.fecha_fin_label = QLabel("Fecha de Fin (YYYY-MM-DD)")
        self.fecha_fin_input = QLineEdit(str(self.promocion.get("Fecha_Fin", "")))

        # Agregar widgets al grid
        grid.addWidget(self.nombre_label, 0, 0)
        grid.addWidget(self.nombre_input, 1, 0)
        grid.addWidget(self.descripcion_label, 0, 1)
        grid.addWidget(self.descripcion_input, 1, 1)
        grid.addWidget(self.descuento_label, 2, 0)
        grid.addWidget(self.descuento_input, 3, 0)
        grid.addWidget(self.fecha_inicio_label, 2, 1)
        grid.addWidget(self.fecha_inicio_input, 3, 1)
        grid.addWidget(self.fecha_fin_label, 4, 0)
        grid.addWidget(self.fecha_fin_input, 5, 0)

        layout_principal.addLayout(grid)

        # Botón guardar
        self.btn_agregar = QPushButton("Guardar Cambios")
        self.btn_agregar.setObjectName("agregar")
        self.btn_agregar.clicked.connect(self.guardar_cambios)
        layout_principal.addWidget(self.btn_agregar, alignment=Qt.AlignCenter)

        self.setLayout(layout_principal)


    def guardar_cambios(self):
        print("📦 Datos actuales de la promoción:", self.promocion)

        descripcion = self.descripcion_input.toPlainText().strip()
        descuento = self.descuento_input.text().strip()
        fecha_inicio = self.fecha_inicio_input.text().strip()
        fecha_fin = self.fecha_fin_input.text().strip()

        if not descripcion or not descuento or not fecha_inicio or not fecha_fin:
            QMessageBox.warning(self, "Campos incompletos", "Por favor completa todos los campos.")
            return

        try:
            descuento = float(descuento)
        except ValueError:
            QMessageBox.critical(self, "Error", "El descuento debe ser un número.")
            return

        import datetime
        try:
            datetime.datetime.strptime(fecha_inicio, "%Y-%m-%d")
            datetime.datetime.strptime(fecha_fin, "%Y-%m-%d")
        except ValueError:
            QMessageBox.critical(self, "Error de Fecha", "Usa el formato correcto: YYYY-MM-DD.")
            return

        if "ID_Promocion" not in self.promocion:
            QMessageBox.critical(self, "Error interno", "No se encontró el ID de la promoción.")
            return

        exito = actualizar_promocion(
            self.promocion["ID_Promocion"],
            descripcion,
            descuento,
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


