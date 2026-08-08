from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QComboBox,
    QVBoxLayout, QHBoxLayout, QMessageBox
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from models.servicio_model import actualizar_servicio, obtener_variantes_servicio


class ModificarServicio(QWidget):
    def __init__(self, servicio, regresar_callback=None):
        super().__init__()
        self.setWindowTitle("Modificar Servicio")
        self.setMinimumSize(1024, 1000)
        self.showMaximized()

        self.servicio = servicio
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
            QLineEdit, QComboBox {
                background-color: #e5d3c5;
                border: 2px solid #000000;
                border-radius: 10px;
                padding: 10px;
                font-size: 14pt;
                min-width: 250px;
                min-height: 41px;
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
                min-width: 300px;
                min-height: 80px;
            }
            QPushButton#guardar:hover {
                background-color: #333333;
            }
        """)

        self.initUI()

    def initUI(self):
        layout_principal = QVBoxLayout()
        layout_principal.setContentsMargins(100, 30, 100, 30)

        # Botones superiores
        fila_top = QHBoxLayout()
        self.btn_regresar = QPushButton("Regresar")
        self.btn_regresar.setObjectName("regresar")
        self.btn_regresar.clicked.connect(self.regresar)
        fila_top.addWidget(self.btn_regresar)
        fila_top.addStretch()
        layout_principal.addLayout(fila_top)

        # Logo
        logo = QLabel()
        pixmap = QPixmap("resources/logo_sinfondo.png").scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        logo.setPixmap(pixmap)
        logo.setAlignment(Qt.AlignCenter)
        layout_principal.addWidget(logo)

        # Título
        titulo = QLabel("Modificar Servicio")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-size: 28pt; font-weight: bold; margin-bottom: 30px;")
        layout_principal.addWidget(titulo)

        # Campos
        fila_campos = QHBoxLayout()
        fila_campos.setSpacing(50)

        self.nombre_servicio = QLineEdit(self.servicio["Nombre_Servicio"])

        self.tipo_servicio = QComboBox()
        variantes = obtener_variantes_servicio()
        for v in variantes:
            self.tipo_servicio.addItem(v["Nombre_Variante"], v["ID_Variante"])
            if v["Nombre_Variante"] == self.servicio["Nombre_Variante"]:
                self.tipo_servicio.setCurrentText(v["Nombre_Variante"])

        self.precio = QLineEdit(str(self.servicio["Precio"]))

        fila_campos.addLayout(self.create_field_group("Nombre del Servicio", self.nombre_servicio))
        fila_campos.addLayout(self.create_field_group("Servicio", self.tipo_servicio))
        fila_campos.addLayout(self.create_field_group("Costo ($)", self.precio))

        layout_principal.addLayout(fila_campos)

        # Botón guardar
        self.btn_guardar = QPushButton("Guardar Cambios")
        self.btn_guardar.setObjectName("guardar")
        self.btn_guardar.clicked.connect(self.guardar_cambios)
        layout_principal.addSpacing(40)
        layout_principal.addWidget(self.btn_guardar, alignment=Qt.AlignCenter)

        self.setLayout(layout_principal)

    def create_field_group(self, label_text, input_widget):
        vbox = QVBoxLayout()
        label = QLabel(label_text)
        label.setAlignment(Qt.AlignCenter)
        vbox.addWidget(label)
        vbox.addWidget(input_widget)
        return vbox

    def regresar(self):
        self.close()
        if self.regresar_callback:
            self.regresar_callback()

    def guardar_cambios(self):
        nuevo_nombre = self.nombre_servicio.text().strip()
        nuevo_precio = self.precio.text().strip()
        nuevo_id_variante = self.tipo_servicio.currentData()

        if not nuevo_nombre or not nuevo_precio:
            QMessageBox.warning(self, "Campos Vacíos", "Por favor, completa todos los campos.")
            return

        try:
            nuevo_precio = float(nuevo_precio)
        except ValueError:
            QMessageBox.critical(self, "Error de Formato", "El precio debe ser un número.")
            return

        id_servicio = self.servicio["ID"]

        if actualizar_servicio(id_servicio, nuevo_nombre, nuevo_precio, nuevo_id_variante):
            QMessageBox.information(self, "Éxito", "Servicio actualizado correctamente.")
            if self.regresar_callback:
                self.regresar_callback()
            self.close()
        else:
            QMessageBox.critical(self, "Error", "No se pudo actualizar el servicio.")
