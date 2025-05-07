from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QTextEdit,
    QComboBox, QVBoxLayout, QHBoxLayout, QGridLayout, QMessageBox
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import sys
from models.promocion import insertar_promocion
import datetime
from models.servicio_model import obtener_servicios

class AgregarPromocion(QWidget):
    def __init__(self, regresar_callback=None):
        super().__init__()
        self.setWindowTitle("Agregar Promoción")
        self.showFullScreen()
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

        # --- Barra superior ---
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
        titulo = QLabel("Agregar Promoción")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-size: 28pt; font-weight: bold; margin-top: 10px; margin-bottom: 30px;")
        layout_principal.addWidget(titulo)

        # --- Campos ---
        grid = QGridLayout()
        grid.setSpacing(30)

        self.nombre_label = QLabel("Nombre de la Promoción")
        self.nombre_input = QLineEdit()

        self.servicio_label = QLabel("Servicio de la Promoción")
        self.servicio_combo = QComboBox()
        self.servicios = obtener_servicios()  # ← obtiene lista con dicts

        for servicio in self.servicios:
            nombre = servicio["Nombre"]
            id_servicio = servicio["ID"]
            self.servicio_combo.addItem(nombre, id_servicio)

        self.descripcion_label = QLabel("Descripción")
        self.descripcion_input = QTextEdit()

        self.precio_label = QLabel("Precio")
        self.descuento_input = QLineEdit()

        self.fecha_inicio_label = QLabel("Fecha de Inicio (YYYY-MM-DD)")
        self.fecha_inicio_input = QLineEdit()

        self.fecha_fin_label = QLabel("Fecha de Vencimiento (YYYY-MM-DD)")
        self.fecha_fin_input = QLineEdit()

        # Campos básicos
        grid.addWidget(self.nombre_label, 0, 0)
        grid.addWidget(self.nombre_input, 1, 0)
        grid.addWidget(self.servicio_label, 0, 1)
        grid.addWidget(self.servicio_combo, 1, 1)

        grid.addWidget(self.descripcion_label, 2, 0)
        grid.addWidget(self.descripcion_input, 3, 0, 1, 2)

        # Renglón conjunto para Precio + Fecha Inicio + Fecha Fin
        grid.addWidget(self.precio_label, 4, 0)
        grid.addWidget(self.fecha_inicio_label, 4, 1)
        grid.addWidget(self.fecha_fin_label, 4, 2)

        grid.addWidget(self.descuento_input, 5, 0)
        grid.addWidget(self.fecha_inicio_input, 5, 1)
        grid.addWidget(self.fecha_fin_input, 5, 2)

        layout_principal.addLayout(grid)

        # --- Botón guardar ---
        self.btn_agregar = QPushButton("Agregar Promoción")
        self.btn_agregar.setObjectName("agregar")
        self.btn_agregar.clicked.connect(self.guardar_promocion)
        layout_principal.addWidget(self.btn_agregar, alignment=Qt.AlignCenter)

        self.setLayout(layout_principal)



    def guardar_promocion(self):
        descripcion = self.descripcion_input.toPlainText().strip()
        servicio = self.servicio_combo.currentText()
        descuento = self.descuento_input.text().strip()
        fecha_inicio = self.fecha_inicio_input.text().strip()
        fecha_fin = self.fecha_fin_input.text().strip()

        if not descripcion or not servicio or not descuento or not fecha_inicio or not fecha_fin:
            QMessageBox.warning(self, "Campos incompletos", "Por favor completa todos los campos.")
            return

        try:
            descuento_float = float(descuento)
        except ValueError:
            QMessageBox.critical(self, "Error", "El descuento debe ser un número.")
            return

        try:
            datetime.datetime.strptime(fecha_inicio, "%Y-%m-%d")
            datetime.datetime.strptime(fecha_fin, "%Y-%m-%d")
        except ValueError:
            QMessageBox.critical(self, "Error de Fecha", "Usa el formato correcto: YYYY-MM-DD.")
            return

        # Llamar al modelo para insertar la promoción (ajusta según tu función real)
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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = AgregarPromocion()
    ventana.show()
    sys.exit(app.exec_())
