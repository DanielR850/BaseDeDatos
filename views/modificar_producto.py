from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QMessageBox
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from models.producto import actualizar_producto


class ModificarProducto(QWidget):
    def __init__(self, regresar_callback=None, salir_callback=None):
        super().__init__()
        self.setWindowTitle("Modificar Producto")
        self.setMinimumSize(1024, 1000)
        self.showMaximized()
        self.regresar_callback = regresar_callback
        self.salir_callback = salir_callback

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
                min-height: 41px;
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

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(50, 30, 50, 30)
        layout.setSpacing(20)

        # --- Barra superior con botones texto ---
        top_bar = QHBoxLayout()
        self.btn_regresar = QPushButton("Regresar")
        self.btn_regresar.setObjectName("regresar")
        self.btn_regresar.clicked.connect(self.regresar)
        top_bar.addWidget(self.btn_regresar)

        top_bar.addStretch()

        self.btn_salir = QPushButton("Salir")
        self.btn_salir.setObjectName("salir")
        self.btn_salir.clicked.connect(self.salir)
        top_bar.addWidget(self.btn_salir)

        layout.addLayout(top_bar)

        # --- Logo ---
        logo = QLabel()
        logo.setPixmap(QPixmap("resources/logo_sinfondo.png").scaledToHeight(100))
        logo.setAlignment(Qt.AlignCenter)
        layout.addWidget(logo)

        # --- Título ---
        titulo = QLabel("Modificar Producto")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-size: 28pt; font-weight: bold; margin-bottom: 20px;")
        layout.addWidget(titulo)

        # --- Formulario de campos ---
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
        form_layout.addSpacing(40)
        form_layout.addLayout(fila2)
        layout.addLayout(form_layout)

        # --- Botón Modificar ---
        self.btn_agregar = QPushButton("Modificar Producto")
        self.btn_agregar.setObjectName("agregar")
        self.btn_agregar.clicked.connect(self.modificar_producto)
        layout.addSpacing(30)
        layout.addWidget(self.btn_agregar, alignment=Qt.AlignCenter)

        self.setLayout(layout)

    def form_group(self, label_text, widget):
        vbox = QVBoxLayout()
        label = QLabel(label_text)
        vbox.addWidget(label)
        vbox.addWidget(widget)
        return vbox

    def modificar_producto(self):
        try:
            id_prod = int(self.id_producto.text())
            nombre = self.nombre.text().strip()
            marca = self.marca.text().strip()
            precio = self.precio.text().strip().replace(",", ".")
            stock = self.stock.text().strip()

            if not all([nombre, marca, precio, stock]):
                QMessageBox.warning(self, "Faltan datos", "Por favor, llena todos los campos.")
                return

            precio_float = float(precio)
            stock_int = int(stock)

            if actualizar_producto(id_prod, nombre, marca, precio_float, stock_int):
                QMessageBox.information(self, "Éxito", "Producto actualizado correctamente.")
                self.regresar()
            else:
                QMessageBox.critical(self, "Error", "No se pudo actualizar el producto.")
        except ValueError:
            QMessageBox.critical(self, "Error de formato", "Asegúrate de que Precio sea decimal y Stock entero.")
        except Exception as e:
            QMessageBox.critical(self, "Error inesperado", str(e))

    def regresar(self):
        self.close()
        if self.regresar_callback:
            self.regresar_callback()

    def salir(self):
        self.close()
        if self.salir_callback:
            self.salir_callback()

    def cargar_datos_producto(self, producto):
        self.id_producto.setText(str(producto.get("ID_Producto", "")))
        self.nombre.setText(producto.get("Nombre_Producto", ""))
        self.marca.setText(producto.get("Marca", ""))
        self.precio.setText(str(producto.get("Precio_Compra", "")))
        self.stock.setText(str(producto.get("Stock", "")))
