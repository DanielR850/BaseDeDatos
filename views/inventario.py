from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QHeaderView, QLineEdit, QMessageBox
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

from views.agregar_producto import AgregarProducto
from views.modificar_producto import ModificarProducto
from models.producto import obtener_productos, eliminar_producto_por_id


class InventarioVentana(QMainWindow):
    def __init__(self, regresar_callback=None):
        super().__init__()
        self.setWindowTitle("Inventario")
        self.setMinimumSize(1024, 1000)
        self.showMaximized()
        self.regresar_callback = regresar_callback
        self.producto_seleccionado = None

        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #EBAAAA, stop: 1 #EADAD3);
                font-family: 'Poppins';
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
        """)

        widget = QWidget()
        self.setCentralWidget(widget)
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        # --- Barra superior ---
        top_bar = QHBoxLayout()
        self.btn_regresar = QPushButton("Regresar")
        self.btn_regresar.setObjectName("regresar")
        self.btn_regresar.clicked.connect(self.regresar)
        top_bar.addWidget(self.btn_regresar)
        top_bar.addStretch()

        self.busqueda = QLineEdit()
        self.busqueda.setPlaceholderText("Buscar por nombre...")
        self.busqueda.setStyleSheet("""
            QLineEdit {
                background: white;
                border-radius: 15px;
                padding: 8px 35px 8px 15px;
                font: 14px 'Roboto';
                min-width: 250px;
            }
        """)
        self.busqueda.textChanged.connect(self.filtrar_productos)
        top_bar.addWidget(self.busqueda)
        layout.addLayout(top_bar)

        # --- Título ---
        titulo = QLabel("Inventario")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("""
            font: bold 38px 'Roboto';
            color: black;
            padding: 15px;
            background: transparent;
        """)
        layout.addWidget(titulo)

        # --- Botones acción ---
        botones = QHBoxLayout()
        botones.setSpacing(25)

        btn_agregar = QPushButton("Agregar Producto")
        btn_agregar.clicked.connect(self.abrir_agregar_producto)

        self.btn_modificar = QPushButton("Modificar Producto")
        self.btn_modificar.setEnabled(False)
        self.btn_modificar.clicked.connect(self.abrir_modificar_producto)

        self.btn_eliminar = QPushButton("Eliminar Producto")
        self.btn_eliminar.setEnabled(False)
        self.btn_eliminar.clicked.connect(self.eliminar_producto)

        for btn, color in zip([btn_agregar, self.btn_modificar, self.btn_eliminar],
                              ["#c6fcb3", "#fcfbb3", "#E57979"]):
            btn.setStyleSheet(f"""
                QPushButton {{
                    background: {color};
                    border-radius: 25px;
                    padding: 15px 30px;
                    font: bold 18px;
                    color: black;
                    min-width: 200px;
                }}
                QPushButton:hover {{
                    background: {'#689F38' if color == "#c6fcb3" else '#FFB300' if color == "#fcfbb3" else '#C62828'};
                }}
            """)
            botones.addWidget(btn)

        layout.addLayout(botones)

        # --- Tabla ---
        self.tabla = QTableWidget(0, 5)
        self.tabla.setHorizontalHeaderLabels(["ID", "Nombre", "Marca", "Precio", "Stock"])
        self.tabla.setStyleSheet("""
            QTableWidget {
                background: #ffefe3;
                border-radius: 15px;
                padding: 10px;
                font: 16px 'Roboto';
                color: #4E342E;
            }
            QHeaderView::section {
                background: #D7CCC8;
                font: bold 18px;
                padding: 12px;
                border: none;
            }
            QTableWidget::item {
                border-bottom: 2px solid #D7CCC8;
                padding: 15px;
            }
        """)
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabla.verticalHeader().setVisible(False)
        self.tabla.setShowGrid(True)
        self.tabla.cellClicked.connect(self.seleccionar_producto)
        layout.addWidget(self.tabla)

        # --- Logo ---
        logo = QLabel()
        logo.setPixmap(QPixmap("resources/logo_sinfondo.png").scaled(80, 80, Qt.KeepAspectRatio))
        logo.setAlignment(Qt.AlignRight)
        logo.setStyleSheet("padding: 0 10px 10px 0; background: transparent;")
        layout.addWidget(logo)

        self.cargar_datos()

    def cargar_datos(self):
        self.tabla.setRowCount(0)
        try:
            productos = obtener_productos()
            for i, p in enumerate(productos):
                self.tabla.insertRow(i)
                self.tabla.setItem(i, 0, QTableWidgetItem(str(p["ID_Producto"])))
                self.tabla.setItem(i, 1, QTableWidgetItem(p["Nombre_Producto"]))
                self.tabla.setItem(i, 2, QTableWidgetItem(p["Marca"]))
                self.tabla.setItem(i, 3, QTableWidgetItem(f"${p['Precio_Compra']:.2f}"))
                self.tabla.setItem(i, 4, QTableWidgetItem(str(p["Stock"])))
        except Exception as e:
            print("❌ Error al cargar productos:", e)

    def seleccionar_producto(self, fila, _):
        try:
            self.producto_seleccionado = {
                "ID_Producto": int(self.tabla.item(fila, 0).text()),
                "Nombre_Producto": self.tabla.item(fila, 1).text(),
                "Marca": self.tabla.item(fila, 2).text(),
                "Precio_Compra": float(self.tabla.item(fila, 3).text().replace("$", "")),
                "Stock": int(self.tabla.item(fila, 4).text())
            }
            self.btn_modificar.setEnabled(True)
            self.btn_eliminar.setEnabled(True)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo seleccionar el producto.\n{e}")

    def abrir_agregar_producto(self):
        self.hide()
        self.agregar = AgregarProducto(
            regresar_callback=self.mostrar_inventario,
            salir_callback=self.ir_a_home
        )
        self.agregar.show()

    def abrir_modificar_producto(self):
        if not self.producto_seleccionado:
            QMessageBox.warning(self, "Selecciona un producto", "Selecciona un producto primero.")
            return

        self.hide()
        self.modificar = ModificarProducto(
            regresar_callback=self.mostrar_inventario,
            salir_callback=self.ir_a_home
        )
        self.modificar.cargar_datos_producto(self.producto_seleccionado)
        self.modificar.show()

    def eliminar_producto(self):
        if not self.producto_seleccionado:
            QMessageBox.warning(self, "Sin selección", "Selecciona un producto primero.")
            return

        confirm = QMessageBox.question(
            self, "Confirmar eliminación",
            "¿Estás seguro de eliminar este producto?",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirm == QMessageBox.Yes:
            id_producto = self.producto_seleccionado["ID_Producto"]
            if eliminar_producto_por_id(id_producto):
                QMessageBox.information(self, "Éxito", "Producto eliminado correctamente.")
                self.producto_seleccionado = None
                self.btn_modificar.setEnabled(False)
                self.btn_eliminar.setEnabled(False)
                self.cargar_datos()
            else:
                QMessageBox.critical(self, "Error", "No se pudo eliminar el producto.")

    def filtrar_productos(self):
        texto = self.busqueda.text().lower()
        for fila in range(self.tabla.rowCount()):
            nombre = self.tabla.item(fila, 1).text().lower()
            self.tabla.setRowHidden(fila, texto not in nombre)

    def mostrar_inventario(self):
        self.showFullScreen()
        self.raise_()
        self.activateWindow()
        self.cargar_datos()

    def regresar(self):
        self.hide()
        if self.regresar_callback:
            self.regresar_callback()

    def ir_a_home(self):
        from views.home import HomeWindow
        self.close()
        self.home = HomeWindow()
        self.home.showFullScreen()
