from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QTextEdit,
    QPushButton, QFormLayout, QMessageBox, QHBoxLayout
)
import sys
import os

class AgregarProducto(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Agregar Producto")
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

        self.nombre_input = QLineEdit()
        self.precio_input = QLineEdit()
        self.categoria_input = QLineEdit()
        self.descripcion_input = QTextEdit()

        self.guardar_btn = QPushButton("Guardar")
        self.cancelar_btn = QPushButton("Cancelar")

        self.guardar_btn.clicked.connect(self.guardar_producto)
        self.cancelar_btn.clicked.connect(self.close)

        botones_layout = QHBoxLayout()
        botones_layout.addWidget(self.guardar_btn)
        botones_layout.addWidget(self.cancelar_btn)

        layout.addRow("Nombre:", self.nombre_input)
        layout.addRow("Precio:", self.precio_input)
        layout.addRow("Categoría:", self.categoria_input)
        layout.addRow("Descripción:", self.descripcion_input)
        layout.addRow(botones_layout)

        self.setLayout(layout)

    def generar_id(self):
        if not os.path.exists("productos.txt"):
            return 1

        with open("productos.txt", "r", encoding="utf-8") as f:
            lineas = f.readlines()

        ids = []
        for linea in lineas:
            if linea.strip():
                try:
                    id_num = int(linea.split(",")[0])
                    ids.append(id_num)
                except ValueError:
                    continue

        return max(ids) + 1 if ids else 1

    def guardar_producto(self):
        nombre = self.nombre_input.text().strip()
        precio = self.precio_input.text().strip()
        categoria = self.categoria_input.text().strip()
        descripcion = self.descripcion_input.toPlainText().strip()

        if not all([nombre, precio, categoria]):
            QMessageBox.warning(self, "Faltan datos", "Por favor, llena todos los campos obligatorios.")
            return

        nuevo_id = self.generar_id()
        nuevo_id_str = str(nuevo_id).zfill(3)

        try:
            with open("productos.txt", "a", encoding="utf-8") as f:
                f.write(f"{nuevo_id_str},{nombre},{precio},{categoria},{descripcion}\n")
            QMessageBox.information(self, "Guardado", f"Producto guardado con ID {nuevo_id_str}.")
            self.nombre_input.clear()
            self.precio_input.clear()
            self.categoria_input.clear()
            self.descripcion_input.clear()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo guardar el producto:\n{str(e)}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = AgregarProducto()
    ventana.show()
    sys.exit(app.exec_())
