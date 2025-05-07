import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QPushButton,
    QLabel, QVBoxLayout, QHBoxLayout, QTableWidget,
    QTableWidgetItem, QHeaderView, QLineEdit, QMessageBox
)
from PyQt5.QtGui import QIcon, QColor, QPixmap
from PyQt5.QtCore import Qt, QSize

from views.agregar_promocion import AgregarPromocion
from views.modificar_promocion import ModificarPromocion
from models.promocion import obtener_promociones, eliminar_promocion  # ← DEBES CREAR ESTE MODELO

class VentanaPromociones(QMainWindow):
    def __init__(self, regresar_callback=None):
        super().__init__()
        self.regresar_callback = regresar_callback  
        self.setWindowTitle("Promociones")
        self.showFullScreen()
        self.promocion_seleccionada = None

        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(
                    x1: 0, y1: 0,
                    x2: 0, y2: 1,
                    stop: 0 #EBAAAA,
                    stop: 1 #EADAD3
                );
                font-family: 'Poppins';
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

        widget_principal = QWidget()
        self.setCentralWidget(widget_principal)
        layout_principal = QVBoxLayout(widget_principal)
        layout_principal.setContentsMargins(30, 30, 30, 30)
        layout_principal.setSpacing(20)

        # --- Barra superior ---
        layout_superior = QHBoxLayout()
        self.btn_regresar = QPushButton("Regresar")
        self.btn_regresar.setObjectName("regresar")
        self.btn_regresar.clicked.connect(self.volver_callback)

        self.btn_salir = QPushButton("Salir")
        self.btn_salir.setObjectName("salir")
        self.btn_salir.clicked.connect(self.close)

        layout_superior.addWidget(self.btn_regresar)
        layout_superior.addStretch()
        layout_superior.addWidget(self.btn_salir)
        layout_principal.addLayout(layout_superior)

        # --- Barra de búsqueda ---
        layout_busqueda = QHBoxLayout()
        self.busqueda = QLineEdit()
        self.busqueda.setPlaceholderText("Buscar...")
        self.busqueda.setStyleSheet("""
            QLineEdit {
                background: white;
                border-radius: 15px;
                padding: 8px 35px 8px 15px;
                font: 14px 'Roboto';
                min-width: 250px;
            }
        """)
        self.busqueda.textChanged.connect(self.buscar_promocion)
        layout_busqueda.addStretch()
        layout_busqueda.addWidget(self.busqueda)
        layout_busqueda.addStretch()
        layout_principal.addLayout(layout_busqueda)

        # --- Título ---
        titulo = QLabel("Promociones")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("""
            font: bold 38px 'Roboto';
            color: black;
            padding: 15px;
            background: transparent;
        """)
        layout_principal.addWidget(titulo)

        # --- Botones principales ---
        layout_botones = QHBoxLayout()
        layout_botones.setSpacing(25)

        btn_agregar = QPushButton("Agregar promoción")
        btn_agregar.setStyleSheet("""
            QPushButton {
                background: #c6fcb3;
                border-radius: 25px;
                padding: 15px 30px;
                font: bold 18px;
                color: black;
                min-width: 200px;
            }
            QPushButton:hover {
                background: #689F38;
            }
        """)
        btn_agregar.clicked.connect(self.abrir_agregar_promocion)
        layout_botones.addWidget(btn_agregar)

        self.btn_modificar = QPushButton("Modificar promoción")
        self.btn_modificar.setEnabled(False)
        self.btn_modificar.setStyleSheet("""
            QPushButton {
                background: #fcfbb3;
                border-radius: 25px;
                padding: 15px 30px;
                font: bold 18px;
                color: black;
                min-width: 200px;
            }
            QPushButton:hover {
                background: #FFB300;
            }
        """)
        self.btn_modificar.clicked.connect(self.abrir_modificar_promocion)
        layout_botones.addWidget(self.btn_modificar)

        self.btn_eliminar = QPushButton("Eliminar promoción")
        self.btn_eliminar.setEnabled(False)
        self.btn_eliminar.setStyleSheet("""
            QPushButton {
                background: #E57979;
                border-radius: 25px;
                padding: 15px 30px;
                font: bold 18px;
                color: black;
                min-width: 200px;
            }
            QPushButton:hover {
                background: #C62828;
            }
        """)
        self.btn_eliminar.clicked.connect(self.eliminar_promocion)
        layout_botones.addWidget(self.btn_eliminar)

        layout_principal.addLayout(layout_botones)

        # --- Tabla de promociones ---
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(4)
        self.tabla.setHorizontalHeaderLabels(["Descripción", "Servicios", "Precio", "Válido hasta"])
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
        self.tabla.itemSelectionChanged.connect(self.seleccionar_promocion)
        layout_principal.addWidget(self.tabla)

        # --- Logo ---
        lbl_logo = QLabel()
        pixmap = QPixmap('resources/logo_sinfondo.png').scaled(80, 80, Qt.KeepAspectRatio)
        lbl_logo.setPixmap(pixmap)
        lbl_logo.setAlignment(Qt.AlignRight | Qt.AlignBottom)
        lbl_logo.setStyleSheet("padding: 0 10px 10px 0; background: transparent;")
        layout_principal.addWidget(lbl_logo, alignment=Qt.AlignRight | Qt.AlignBottom)

        self.cargar_promociones()

    # --- Funcionalidad de botones ---
    def abrir_agregar_promocion(self):
        self.ventana_agregar = AgregarPromocion(regresar_callback=self.mostrar)
        self.ventana_agregar.show()
        self.hide()

    def abrir_modificar_promocion(self):
        if self.promocion_seleccionada:
            self.ventana_modificar = ModificarPromocion(
                promocion=self.promocion_seleccionada,
                regresar_callback=self.mostrar
            )
            self.ventana_modificar.show()
            self.hide()

    def eliminar_promocion(self):
        if not self.promocion_seleccionada:
            return

        id_promo = self.promocion_seleccionada["ID_Promocion"]  # ← corregido
        confirm = QMessageBox.question(self, "Confirmar eliminación",
                                       "¿Estás seguro de eliminar esta promoción?",
                                       QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            if eliminar_promocion(id_promo):
                QMessageBox.information(self, "Éxito", "Promoción eliminada correctamente.")
                self.cargar_promociones()
            else:
                QMessageBox.critical(self, "Error", "No se pudo eliminar la promoción.")

    # --- Utilidades ---
    def cargar_promociones(self):
        self.tabla.setRowCount(0)
        promociones = obtener_promociones()
        for promo in promociones:
            row = self.tabla.rowCount()
            self.tabla.insertRow(row)
            self.tabla.setItem(row, 0, QTableWidgetItem(promo["Descripcion"]))
            self.tabla.setItem(row, 1, QTableWidgetItem(promo["Servicios"]))
            self.tabla.setItem(row, 2, QTableWidgetItem(str(promo["Descuento"])))
            self.tabla.setItem(row, 3, QTableWidgetItem(str(promo["Fecha_Fin"])))
            self.tabla.setVerticalHeaderItem(row, QTableWidgetItem(str(promo["ID_Promocion"])))

    def seleccionar_promocion(self):
        selected = self.tabla.currentRow()
        if selected >= 0:
            self.promocion_seleccionada = {
                "ID_Promocion": int(self.tabla.verticalHeaderItem(selected).text()),  # ← CORREGIDO
                "Descripcion": self.tabla.item(selected, 0).text(),
                "Servicios": self.tabla.item(selected, 1).text(),
                "Descuento": self.tabla.item(selected, 2).text(),                      # ← CAMBIADO de "Precio"
                "Fecha_Fin": self.tabla.item(selected, 3).text()                       # ← CAMBIADO de "Valido_Hasta"
            }

            self.btn_modificar.setEnabled(True)
            self.btn_eliminar.setEnabled(True)
        else:
            self.promocion_seleccionada = None
            self.btn_modificar.setEnabled(False)
            self.btn_eliminar.setEnabled(False)

    def buscar_promocion(self):
        texto = self.busqueda.text().lower()
        for fila in range(self.tabla.rowCount()):
            descripcion = self.tabla.item(fila, 0).text().lower()
            self.tabla.setRowHidden(fila, texto not in descripcion)

    def volver_callback(self):
        if self.regresar_callback:
            self.regresar_callback()
        self.close()

    def mostrar(self):
        self.show()
        self.raise_()
        self.activateWindow()
        self.setWindowState(Qt.WindowActive)
        self.showFullScreen()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaPromociones()
    ventana.show()
    sys.exit(app.exec_())
