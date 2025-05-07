from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QMessageBox
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import os
from models.producto import insertar_producto

class AgregarProducto(QWidget):
    def __init__(self, regresar_callback=None, salir_callback=None,actualizar_tabla_callback=None):
        super().__init__()
        self.setWindowTitle("Agregar Producto")
        self.showFullScreen()
        self.regresar_callback = regresar_callback
        self.salir_callback = salir_callback
        self.actualizar_tabla_callback = actualizar_tabla_callback

        

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
                qproperty-alignment: 'AlignCenter';
            }
            QLineEdit {
                background-color: #e5d3c5;
                border: 2px solid #000000;
                border-radius: 10px;
                padding: 10px;
                font-size: 14pt;
                min-width: 180px;
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
            QPushButton#agregar {
                background-color: #231f20;
                color: #fcb3b3;
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

        # --- Botones superiores ---
        botones = QHBoxLayout()
        self.btn_regresar = QPushButton("Regresar")
        self.btn_regresar.setObjectName("regresar")
        self.btn_regresar.clicked.connect(self.regresar)

        self.btn_salir = QPushButton("Salir")
        self.btn_salir.setObjectName("salir")
        self.btn_salir.clicked.connect(self.salir)

        botones.addWidget(self.btn_regresar)
        botones.addStretch()
        botones.addWidget(self.btn_salir)
        layout.addLayout(botones)

        # --- Logo ---
        logo = QLabel()
        pixmap = QPixmap("resources/logo_sinfondo.png")
        logo.setPixmap(pixmap.scaledToHeight(100))
        logo.setAlignment(Qt.AlignCenter)
        layout.addWidget(logo)

        # --- Título ---
        titulo = QLabel("Agregar producto")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-size: 28pt; font-weight: bold; margin-bottom: 20px;")
        layout.addWidget(titulo)

        # --- Campos ---
        form_layout = QVBoxLayout()
        fila1 = QHBoxLayout()
        fila1.setSpacing(50)

        self.id_producto = QLineEdit()
        self.id_producto.setEnabled(False)
        self.nombre = QLineEdit()
        self.marca = QLineEdit()

        fila1.addLayout(self.form_group("ID del Producto", self.id_producto))
        fila1.addLayout(self.form_group("Nombre", self.nombre))
        fila1.addLayout(self.form_group("Marca", self.marca))

        fila2 = QHBoxLayout()
        fila2.setSpacing(100)

        self.precio = QLineEdit()
        self.stock = QLineEdit()

        fila2.addLayout(self.form_group("Precio", self.precio))
        fila2.addLayout(self.form_group("Stock", self.stock))

        form_layout.addLayout(fila1)
        form_layout.addSpacing(50)
        form_layout.addLayout(fila2)
        layout.addLayout(form_layout)

        # --- Botón guardar ---
        self.btn_agregar = QPushButton("Agregar Producto")
        self.btn_agregar.setObjectName("agregar")
        self.btn_agregar.clicked.connect(self.guardar_producto)
        layout.addWidget(self.btn_agregar, alignment=Qt.AlignCenter)

        self.setLayout(layout)

    def form_group(self, label_text, line_edit):
        vbox = QVBoxLayout()
        label = QLabel(label_text)
        label.setAlignment(Qt.AlignCenter)
        vbox.addWidget(label)
        vbox.addWidget(line_edit)
        return vbox

    def regresar(self):
        self.hide()
        if self.regresar_callback:
            self.regresar_callback()

    def salir(self):
        self.hide()
        if self.salir_callback:
            self.salir_callback()

    def generar_id(self):
        if not os.path.exists("productos.txt"):
            return 1
        with open("productos.txt", "r", encoding="utf-8") as f:
            lineas = f.readlines()
        ids = [int(l.split(",")[0]) for l in lineas if l.strip() and l.split(",")[0].isdigit()]
        return max(ids) + 1 if ids else 1

    def guardar_producto(self):
        nombre = self.nombre.text().strip()
        marca = self.marca.text().strip()
        precio = self.precio.text().strip()
        stock = self.stock.text().strip()

        if not all([nombre, marca, precio, stock]):
            QMessageBox.warning(self, "Faltan datos", "Por favor, llena todos los campos.")
            return

        try:
            precio_float = float(precio.replace(",", "."))  # por si el usuario usa coma
            stock_int = int(stock)

            if precio_float > 99999.99:
                QMessageBox.warning(self, "Precio inválido", "El precio no puede ser mayor a 99999.99")
                return

            if insertar_producto(nombre, marca, precio_float, stock_int):
                QMessageBox.information(self, "Guardado", "Producto guardado correctamente.")
                self.nombre.clear()
                self.marca.clear()
                self.precio.clear()
                self.stock.clear()
            else:
                QMessageBox.critical(self, "Error", "No se pudo guardar el producto en la base de datos.")

        except ValueError:
            QMessageBox.critical(self, "Error de formato", "Precio debe ser numérico y Stock un número entero.")
        except Exception as e:
            QMessageBox.critical(self, "Error inesperado", str(e))
