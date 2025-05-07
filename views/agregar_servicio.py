import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QComboBox, QMessageBox
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from models.servicio_model import obtener_variantes_servicio  # asegúrate de tener esta función en tu backend
from models.servicio_model import insertar_servicio  # asegúrate de importar esto arriba

class AgregarServicio(QWidget):
    def __init__(self, regresar_callback=None):
        super().__init__()
        self.setWindowTitle("Registrar Servicio")
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
                font-family: 'Poppins';
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
            QPushButton#registrar {
                background-color: #231f20;
                color: #fcb3b3;
                font-family: 'Poppins';
                padding: 15px;
                border-radius: 20px;
                font-size: 18pt;
                min-width: 300px;
                min-height: 80px;
            }
            QPushButton#registrar:hover {
                background-color: #333333;
            }
        """)

        self.initUI()

    def initUI(self):
        layout_principal = QVBoxLayout()
        layout_principal.setContentsMargins(100, 30, 100, 30)

        botones_superiores = QHBoxLayout()
        self.btn_regresar = QPushButton("Regresar")
        self.btn_regresar.setObjectName("regresar")
        self.btn_regresar.clicked.connect(self.regresar)
        botones_superiores.addWidget(self.btn_regresar)
        botones_superiores.addStretch()
        layout_principal.addLayout(botones_superiores)

        logo = QLabel()
        pixmap = QPixmap("resources/logo_sinfondo.png").scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        logo.setPixmap(pixmap)
        logo.setAlignment(Qt.AlignCenter)
        layout_principal.addWidget(logo)

        titulo = QLabel("Registrar Servicio")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-size: 28pt; font-weight: bold; margin-bottom: 30px;")
        layout_principal.addWidget(titulo)

        fila_campos = QHBoxLayout()
        fila_campos.setSpacing(50)

        self.nombre_servicio = QLineEdit()
        self.combo_variante = QComboBox()
        self.precio = QLineEdit()

        fila_campos.addLayout(self.create_field_group("Nombre del Servicio", self.nombre_servicio))
        fila_campos.addLayout(self.create_field_group("Variante de Servicio", self.combo_variante))
        fila_campos.addLayout(self.create_field_group("Precio", self.precio))

        layout_principal.addLayout(fila_campos)

        self.btn_registrar = QPushButton("Registrar Servicio")
        self.btn_registrar.setObjectName("registrar")
        self.btn_registrar.clicked.connect(self.registrar_servicio)
        layout_principal.addSpacing(40)
        layout_principal.addWidget(self.btn_registrar, alignment=Qt.AlignCenter)

        self.setLayout(layout_principal)

        self.cargar_variantes()

    def create_field_group(self, label_text, input_widget):
        vbox = QVBoxLayout()
        label = QLabel(label_text)
        label.setAlignment(Qt.AlignCenter)
        vbox.addWidget(label)
        vbox.addWidget(input_widget)
        return vbox

    def cargar_variantes(self):
        print("🛠️ Entrando a cargar_variantes()")
        try:
            variantes = obtener_variantes_servicio()
            print(f"📋 Variantes obtenidas: {variantes}")
            self.combo_variante.clear()
            for v in variantes:
                self.combo_variante.addItem(v["Nombre_Variante"], v["ID_Variante"])
        except Exception as e:
            print(f"❌ Error al cargar variantes: {e}")
            QMessageBox.critical(self, "Error", f"No se pudieron cargar las variantes de servicio:\n{e}")


    def regresar(self):
        self.close()
        if self.regresar_callback:
            self.regresar_callback()


    def registrar_servicio(self):
        nombre = self.nombre_servicio.text().strip()
        precio_texto = self.precio.text().strip()

        if not nombre or not precio_texto:
            QMessageBox.warning(self, "Campos Vacíos", "Por favor, completa todos los campos.")
            return

        try:
            precio = float(precio_texto)
        except ValueError:
            QMessageBox.warning(self, "Formato Inválido", "El precio debe ser un número.")
            return

        id_variante = self.combo_variante.currentData()  # Esto obtiene el ID vinculado

        if insertar_servicio(nombre, precio, id_variante, detalles_ids=[]):  # detalles_ids opcional
            QMessageBox.information(self, "Éxito", "Servicio registrado correctamente.")
            self.nombre_servicio.clear()
            self.precio.clear()
            self.combo_variante.setCurrentIndex(0)
        else:
            QMessageBox.critical(self, "Error", "No se pudo registrar el servicio.")