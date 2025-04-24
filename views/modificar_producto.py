from PyQt5.QtWidgets import (
    QApplication, QWidget, QLineEdit, QTextEdit,
    QPushButton, QFormLayout, QMessageBox
)
import sys
import os

class ModificarProducto(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Modificar Producto")
        self.showFullScreen()  # Inicia en pantalla completa

        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(
                    x1: 0, y1: 0,
                    x2: 0, y2: 1,
                    stop: 0 pink,
                    stop: 1 white
                );
                font-family: 'Segoe UI';
                font-size: 14pt;
            }

            QLineEdit, QTextEdit {
                background-color: white;
                border: 1px solid #ccc;
                padding: 5px;
                border-radius: 5px;
            }

            QPushButton {
                background-color: #f06292;
                color: white;
                padding: 10px;
                border: none;
                border-radius: 10px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #ec407a;
            }
        """)

        self.initUI()

    def initUI(self):
        layout = QFormLayout()

        self.id_input = QLineEdit()
        self.nombre_input = QLineEdit()
        self.precio_input = QLineEdit()
        self.categoria_input = QLineEdit()
        self.descripcion_input = QTextEdit()

        self.buscar_btn = QPushButton("Buscar")
        self.modificar_btn = QPushButton("Modificar")
        self.cancelar_btn = QPushButton("Cancelar")

        self.buscar_btn.clicked.connect(self.buscar_producto)
        self.modificar_btn.clicked.connect(self.modificar_producto)
        self.cancelar_btn.clicked.connect(self.close)

        layout.addRow("ID Producto:", self.id_input)
        layout.addRow(self.buscar_btn)
        layout.addRow("Nombre:", self.nombre_input)
        layout.addRow("Precio:", self.precio_input)
        layout.addRow("Categoría:", self.categoria_input)
        layout.addRow("Descripción:", self.descripcion_input)
        layout.addRow(self.modificar_btn, self.cancelar_btn)

        self.setLayout(layout)

    def buscar_producto(self):
        id_producto = self.id_input.text().strip()
        if not id_producto:
            QMessageBox.warning(self, "Advertencia", "Ingresa un ID de producto para buscar.")
            return

        if not os.path.exists("productos.txt"):
            QMessageBox.warning(self, "Archivo no encontrado", "No se encontró el archivo de productos.")
            return

        encontrado = False
        with open("productos.txt", "r", encoding="utf-8") as f:
            lineas = f.readlines()
            for linea in lineas:
                partes = linea.strip().split(",")
                if partes[0] == id_producto:
                    self.nombre_input.setText(partes[1])
                    self.precio_input.setText(partes[2])
                    self.categoria_input.setText(partes[3])
                    self.descripcion_input.setPlainText(",".join(partes[4:]))
                    encontrado = True
                    break

        if not encontrado:
            QMessageBox.information(self, "No encontrado", "Producto no encontrado con ese ID.")

    def modificar_producto(self):
        id_producto = self.id_input.text().strip()
        nombre = self.nombre_input.text().strip()
        precio = self.precio_input.text().strip()
        categoria = self.categoria_input.text().strip()
        descripcion = self.descripcion_input.toPlainText().strip()

        if not all([id_producto, nombre, precio, categoria]):
            QMessageBox.warning(self, "Faltan datos", "Por favor, llena todos los campos obligatorios.")
            return

        if not os.path.exists("productos.txt"):
            QMessageBox.warning(self, "Archivo no encontrado", "No se encontró el archivo de productos.")
            return

        actualizado = False
        nuevas_lineas = []
        with open("productos.txt", "r", encoding="utf-8") as f:
            for linea in f:
                partes = linea.strip().split(",")
                if partes[0] == id_producto:
                    nuevas_lineas.append(f"{id_producto},{nombre},{precio},{categoria},{descripcion}\n")
                    actualizado = True
                else:
                    nuevas_lineas.append(linea)

        if actualizado:
            with open("productos.txt", "w", encoding="utf-8") as f:
                f.writelines(nuevas_lineas)
            QMessageBox.information(self, "Éxito", "Producto modificado correctamente.")
        else:
            QMessageBox.warning(self, "No encontrado", "No se encontró un producto con ese ID.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = ModificarProducto()
    ventana.show()
    sys.exit(app.exec_())