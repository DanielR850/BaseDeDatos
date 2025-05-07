import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QPushButton,
    QLabel, QVBoxLayout, QHBoxLayout, QTableWidget,
    QTableWidgetItem, QHeaderView, QLineEdit, QMessageBox
)
from PyQt5.QtGui import QIcon, QColor, QPixmap
from PyQt5.QtCore import Qt, QSize
from views.agregar_producto import AgregarProducto
from views.modificar_producto import ModificarProducto
from models.producto import obtener_productos, eliminar_producto_por_id

class InventarioVentana(QMainWindow):
    def __init__(self, regresar_callback=None):
        super().__init__()
        self.setWindowTitle("Inventario")
        self.showFullScreen()
        self.regresar_callback = regresar_callback

        self.producto_seleccionado = None

        widget_principal = QWidget()
        widget_principal.setStyleSheet("""
            background: qlineargradient(
                x1: 0, y1: 0,
                x2: 0, y2: 1,
                stop: 0 #EBAAAA,
                stop: 1 #EADAD3
            );
        """)
        self.setCentralWidget(widget_principal)

        layout_principal = QVBoxLayout(widget_principal)
        layout_principal.setContentsMargins(30, 30, 30, 30)
        layout_principal.setSpacing(20)

        layout_superior = QHBoxLayout()
        boton_regresar = QPushButton()
        boton_regresar.setIcon(QIcon('resources/flecha_regresar.png'))
        boton_regresar.setIconSize(QSize(40, 40))
        boton_regresar.setStyleSheet("border: none; background: transparent;")
        boton_regresar.clicked.connect(self.regresar)
        layout_superior.addWidget(boton_regresar)
        layout_superior.addStretch()

        self.busqueda = QLineEdit()
        self.busqueda.setPlaceholderText("Buscar por nombre...")
        self.busqueda.textChanged.connect(self.filtrar_productos)
        self.busqueda.setStyleSheet("""
            QLineEdit {
                background: white;
                border-radius: 15px;
                padding: 8px 35px 8px 15px;
                font: 14px 'Roboto';
                min-width: 250px;
            }
        """)
        layout_superior.addWidget(self.busqueda)
        layout_principal.addLayout(layout_superior)

        titulo = QLabel("Inventario")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("""
            font: bold 38px 'Roboto';
            color: black;
            padding: 15px;
            background: transparent;
        """)
        layout_principal.addWidget(titulo)

        layout_botones = QHBoxLayout()
        layout_botones.setSpacing(25)

        btn_agregar = QPushButton("Agregar Producto")
        btn_agregar.clicked.connect(self.abrir_agregar_producto)

        self.btn_modificar = QPushButton("Modificar Producto")
        self.btn_modificar.clicked.connect(self.abrir_modificar_producto)
        self.btn_modificar.setEnabled(False)

        self.btn_eliminar = QPushButton("Eliminar Producto")
        self.btn_eliminar.clicked.connect(self.eliminar_producto)
        self.btn_eliminar.setEnabled(False)

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
            layout_botones.addWidget(btn)

        layout_principal.addLayout(layout_botones)

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
        layout_principal.addWidget(self.tabla)

        lbl_logo = QLabel()
        pixmap = QPixmap('resources/logo_sinfondo.png').scaled(80, 80, Qt.KeepAspectRatio)
        lbl_logo.setPixmap(pixmap)
        lbl_logo.setAlignment(Qt.AlignRight | Qt.AlignBottom)
        lbl_logo.setStyleSheet("padding: 0 10px 10px 0; background: transparent;")
        layout_principal.addWidget(lbl_logo, alignment=Qt.AlignRight | Qt.AlignBottom)

        self.cargar_datos()

    def cargar_productos(self):
        from models.producto import obtener_productos

        self.tabla.setRowCount(0)  # Limpia la tabla

        try:
            productos = obtener_productos()
            for row_index, producto in enumerate(productos):
                self.tabla.insertRow(row_index)
                self.tabla.setItem(row_index, 0, QTableWidgetItem(str(producto["ID_Producto"])))
                self.tabla.setItem(row_index, 1, QTableWidgetItem(producto["Nombre_Producto"]))
                self.tabla.setItem(row_index, 2, QTableWidgetItem(producto["Marca"]))
                self.tabla.setItem(row_index, 3, QTableWidgetItem(f"{producto['Precio_Compra']:.2f}"))
                self.tabla.setItem(row_index, 4, QTableWidgetItem(str(producto["Stock"])))


        except Exception as e:
            print(f"❌ Error al cargar productos: {e}")


    def cargar_datos(self):
        self.cargar_productos()


    def seleccionar_producto(self, fila, _):
        self.producto_seleccionado = [self.tabla.item(fila, col).text() for col in range(5)]
        self.btn_modificar.setEnabled(True)
        self.btn_eliminar.setEnabled(True)

    def abrir_agregar_producto(self):
        self.hide()
        self.agregar = AgregarProducto(
            regresar_callback=self.mostrar_inventario,
            salir_callback=self.ir_a_home
        )
        self.agregar.show()

    def abrir_modificar_producto(self):
        selected = self.tabla.currentRow()
        if selected == -1:
            QMessageBox.warning(self, "Selecciona un producto", "Primero selecciona una fila de la tabla.")
            return

        producto = {
            "ID_Producto": int(self.tabla.item(selected, 0).text()),
            "Nombre_Producto": self.tabla.item(selected, 1).text(),
            "Marca": self.tabla.item(selected, 2).text(),
            "Precio_Compra": float(self.tabla.item(selected, 3).text()),
            "Stock": int(self.tabla.item(selected, 4).text())
        }

        self.hide()
        self.modificar = ModificarProducto(
            regresar_callback=self.mostrar_inventario,
            salir_callback=self.ir_a_home
        )
        self.modificar.cargar_datos_producto(producto)
        self.modificar.show()


    def eliminar_producto(self):
        if self.producto_seleccionado:
            confirm = QMessageBox.question(self, "Eliminar", "¿Seguro que quieres eliminar este producto?", QMessageBox.Yes | QMessageBox.No)
            if confirm == QMessageBox.Yes:
                id_producto = int(self.producto_seleccionado[0])
                if eliminar_producto_por_id(id_producto):
                    QMessageBox.information(self, "Eliminado", "Producto eliminado exitosamente.")
                    self.producto_seleccionado = None
                    self.btn_modificar.setEnabled(False)
                    self.btn_eliminar.setEnabled(False)
                    self.cargar_datos()
                else:
                    QMessageBox.critical(self, "Error", "No se pudo eliminar el producto.")

    def regresar(self):
        self.hide()
        if self.regresar_callback:
            self.regresar_callback()

    def mostrar_inventario(self):
        self.showFullScreen()
        self.raise_()
        self.activateWindow()
        self.cargar_datos()

    def ir_a_home(self):
        self.close()
        from views.home import HomeWindow
        self.home = HomeWindow()
        self.home.showFullScreen()

    def filtrar_productos(self):
        texto_busqueda = self.busqueda.text().lower()
        for fila in range(self.tabla.rowCount()):
            item_nombre = self.tabla.item(fila, 1)  # Columna "Nombre"
            if item_nombre:
                visible = texto_busqueda in item_nombre.text().lower()
                self.tabla.setRowHidden(fila, not visible)
