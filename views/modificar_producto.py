import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QGridLayout, QMessageBox
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class ModificarProducto(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Modificar Producto")
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
            QLabel {
                background-color: transparent;
                font-size: 16pt;
                color: #000000;
                font-family: 'Poppins';
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
        layout_principal = QVBoxLayout()

        # Botones superiores
        botones_superiores = QHBoxLayout()

        self.btn_regresar = QPushButton("Regresar")
        self.btn_regresar.setObjectName("regresar")
        self.btn_salir = QPushButton("Salir")
        self.btn_salir.setObjectName("salir")
        self.btn_salir.clicked.connect(self.close)

        botones_superiores.addWidget(self.btn_regresar)
        botones_superiores.addStretch()
        botones_superiores.addWidget(self.btn_salir)

        layout_principal.addLayout(botones_superiores)

        # Logo arriba
        logo = QLabel()
        pixmap = QPixmap("C:/Users/makib/Documents/EntornosVirtuales/BaseDeDatosSalonDeBelleza/resources/logo_sinfondo.png")
        logo.setPixmap(pixmap.scaledToHeight(100))
        logo.setAlignment(Qt.AlignCenter)
        layout_principal.addWidget(logo)

        # Título
        titulo = QLabel("Modificar Producto")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-size: 28pt; font-weight: bold; margin-bottom: 20px;")
        layout_principal.addWidget(titulo)

        # Formulario
        campos_centrados = QVBoxLayout()
        campos_centrados.setAlignment(Qt.AlignCenter)

        fila1 = QHBoxLayout()
        fila1.setSpacing(50)
        self.id_producto = QLineEdit()
        self.id_producto.setEnabled(False)
        self.nombre = QLineEdit()
        self.marca = QLineEdit()

        vbox_id = QVBoxLayout()
        vbox_id.addWidget(self.create_label_centered("ID del Producto"))
        vbox_id.addWidget(self.id_producto)

        vbox_nombre = QVBoxLayout()
        vbox_nombre.addWidget(self.create_label_centered("Nombre"))
        vbox_nombre.addWidget(self.nombre)

        vbox_marca = QVBoxLayout()
        vbox_marca.addWidget(self.create_label_centered("Marca"))
        vbox_marca.addWidget(self.marca)

        fila1.addLayout(vbox_id)
        fila1.addLayout(vbox_nombre)
        fila1.addLayout(vbox_marca)

        fila2 = QHBoxLayout()
        fila2.setSpacing(100)
        self.precio = QLineEdit()
        self.stock = QLineEdit()

        vbox_precio = QVBoxLayout()
        vbox_precio.addWidget(self.create_label_centered("Precio"))
        vbox_precio.addWidget(self.precio)

        vbox_stock = QVBoxLayout()
        vbox_stock.addWidget(self.create_label_centered("Stock"))
        vbox_stock.addWidget(self.stock)

        fila2.addLayout(vbox_precio)
        fila2.addLayout(vbox_stock)

        campos_centrados.addLayout(fila1)
        campos_centrados.addSpacing(50)
        campos_centrados.addLayout(fila2)

        layout_principal.addLayout(campos_centrados)

        # Botón modificar producto
        self.btn_agregar = QPushButton("Modificar Producto")
        self.btn_agregar.setObjectName("agregar")
        self.btn_agregar.clicked.connect(self.modificar_producto)
        layout_principal.addWidget(self.btn_agregar, alignment=Qt.AlignCenter)

        self.setLayout(layout_principal)

    def create_label_centered(self, text):
        label = QLabel(text)
        label.setAlignment(Qt.AlignCenter)
        return label

    def modificar_producto(self):
        nombre = self.nombre.text().strip()
        marca = self.marca.text().strip()
        precio = self.precio.text().strip()
        stock = self.stock.text().strip()

        if not all([nombre, marca, precio, stock]):
            QMessageBox.warning(self, "Faltan datos", "Por favor, llena todos los campos.")
            return

        try:
            QMessageBox.information(self, "Guardado", "Producto modificado correctamente.")
            self.nombre.clear()
            self.marca.clear()
            self.precio.clear()
            self.stock.clear()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo modificar el producto:\n{str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = ModificarProducto()
    ventana.show()
    sys.exit(app.exec_())
