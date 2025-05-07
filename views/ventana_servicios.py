import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QPushButton,
    QLabel, QVBoxLayout, QHBoxLayout, QTableWidget,
    QTableWidgetItem, QHeaderView, QLineEdit, QMessageBox
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from models.servicio_model import obtener_servicios, eliminar_servicio  # Asegúrate de tener estas funciones implementadas

class VentanaServicios(QMainWindow):
    def __init__(self, regresar_callback=None):
        super().__init__()
        self.setWindowTitle("Servicios")
        self.showFullScreen()
        self.regresar_callback = regresar_callback  
        self.servicio_seleccionado = None


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

        widget_principal = QWidget()
        self.setCentralWidget(widget_principal)

        layout_principal = QVBoxLayout(widget_principal)
        layout_principal.setContentsMargins(30, 30, 30, 30)
        layout_principal.setSpacing(20)

        # --- Barra superior ---
        layout_superior = QHBoxLayout()
        self.btn_regresar = QPushButton("Regresar")
        self.btn_regresar.setObjectName("regresar")
        self.btn_regresar.clicked.connect(self.volver_a_home)
        layout_superior.addWidget(self.btn_regresar)
        layout_superior.addStretch()
        layout_principal.addLayout(layout_superior)

        # --- Barra de búsqueda ---
        layout_busqueda = QHBoxLayout()
        self.busqueda = QLineEdit()
        self.busqueda.setPlaceholderText("Buscar servicio...")
        self.busqueda.setStyleSheet("""
            QLineEdit {
                background: white;
                border-radius: 15px;
                padding: 8px 35px 8px 15px;
                font: 14px 'Roboto';
                min-width: 250px;
            }
        """)
        self.busqueda.textChanged.connect(self.buscar_servicio)
        layout_busqueda.addStretch()
        layout_busqueda.addWidget(self.busqueda)
        self.busqueda.textChanged.connect(self.buscar_servicio)
        layout_busqueda.addStretch()
        layout_principal.addLayout(layout_busqueda)

        # --- Título ---
        titulo = QLabel("Servicios")
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

        btn_agregar = QPushButton("Agregar servicio")
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
        btn_agregar.clicked.connect(self.abrir_agregar_servicio)
        layout_botones.addWidget(btn_agregar)

        self.btn_modificar = QPushButton("Modificar servicio")
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
        self.btn_modificar.clicked.connect(self.abrir_modificar_servicio)
        self.btn_modificar.setEnabled(False)
        layout_botones.addWidget(self.btn_modificar)

        self.btn_eliminar = QPushButton("Eliminar servicio")
        self.btn_eliminar.setEnabled(False)
        self.btn_eliminar.clicked.connect(self.eliminar_servicio)  # ✅ ya existe 
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
        self.btn_eliminar.clicked.connect(self.eliminar_servicio)
        self.btn_eliminar.setEnabled(False)
        layout_botones.addWidget(self.btn_eliminar)

        layout_principal.addLayout(layout_botones)

        # --- Tabla de servicios ---
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(3)
        self.tabla.setHorizontalHeaderLabels(["Nombre del servicio", "Servicio especificado", "Precio"])
        self.tabla.itemSelectionChanged.connect(self.seleccionar_servicio)
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
        self.tabla.itemSelectionChanged.connect(self.seleccionar_fila)
        layout_principal.addWidget(self.tabla)

        # --- Logo ---
        lbl_logo = QLabel()
        pixmap = QPixmap('resources/logo_sinfondo.png').scaled(80, 80, Qt.KeepAspectRatio)
        lbl_logo.setPixmap(pixmap)
        lbl_logo.setAlignment(Qt.AlignRight | Qt.AlignBottom)
        lbl_logo.setStyleSheet("padding: 0 10px 10px 0; background: transparent;")
        layout_principal.addWidget(lbl_logo, alignment=Qt.AlignRight | Qt.AlignBottom)

        self.cargar_servicios()

    def volver_a_home(self):
        from views.home import HomeWindow
        self.home_window = HomeWindow()
        self.home_window.show()
        self.close()

    def abrir_agregar_servicio(self):
        from views.agregar_servicio import AgregarServicio
        self.ventana_agregar = AgregarServicio(regresar_callback=self.mostrar_ventana)
        self.ventana_agregar.show()
        self.hide()

    def abrir_modificar_servicio(self):
        if self.servicio_seleccionado:
            from views.modificar_servicio import ModificarServicio
            self.ventana_modificar = ModificarServicio(
                servicio=self.servicio_seleccionado,
                regresar_callback=self.mostrar_ventana
            )
            self.ventana_modificar.show()
            self.hide()

    def mostrar_ventana(self):
        self.show()
        self.raise_()
        self.activateWindow()
        self.showFullScreen()
        self.cargar_servicios()

    def cargar_servicios(self):
        print("📥 Cargando servicios en tabla...")
        self.tabla.setRowCount(0)
        servicios = obtener_servicios()
        print(f"🔍 Servicios recuperados: {servicios}")

        for servicio in servicios:
            row_pos = self.tabla.rowCount()
            self.tabla.insertRow(row_pos)

            self.tabla.setItem(row_pos, 0, QTableWidgetItem(servicio["Nombre"]))
            self.tabla.setItem(row_pos, 1, QTableWidgetItem(servicio["Variante"]))  # ✅ corregido
            self.tabla.setItem(row_pos, 2, QTableWidgetItem(str(servicio["Precio"])))

            self.tabla.setVerticalHeaderItem(row_pos, QTableWidgetItem(str(servicio["ID"])))



    def seleccionar_fila(self):
        items = self.tabla.selectedItems()
        if items:
            fila = items[0].row()
            self.servicio_seleccionado = {
                "ID": int(self.tabla.verticalHeaderItem(fila).text()),  # 👈 Añadir correctamente la ID
                "Nombre_Servicio": self.tabla.item(fila, 0).text(),
                "Nombre_Variante": self.tabla.item(fila, 1).text(),
                "Precio": self.tabla.item(fila, 2).text(),
            }
            self.btn_modificar.setEnabled(True)
            self.btn_eliminar.setEnabled(True)
        else:
            self.servicio_seleccionado = None
            self.btn_modificar.setEnabled(False)
            self.btn_eliminar.setEnabled(False)

    def eliminar_servicio(self):
        if not self.servicio_seleccionado:
            return

        id_servicio = int(self.servicio_seleccionado)
        confirm = QMessageBox.question(self, "Confirmar eliminación",
                                    "¿Estás seguro de eliminar este servicio?",
                                    QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            if eliminar_servicio(id_servicio):
                QMessageBox.information(self, "Éxito", "Servicio eliminado correctamente.")
                self.cargar_servicios()
            else:
                QMessageBox.critical(self, "Error", "No se pudo eliminar el servicio.")


    def buscar_servicio(self):
        texto = self.busqueda.text().lower()
        for fila in range(self.tabla.rowCount()):
            nombre = self.tabla.item(fila, 0).text().lower()
            self.tabla.setRowHidden(fila, texto not in nombre)



    def seleccionar_servicio(self):
        selected = self.tabla.currentRow()
        if selected >= 0:
            self.servicio_seleccionado = self.tabla.verticalHeaderItem(selected).text()
            self.btn_modificar.setEnabled(True)
            self.btn_eliminar.setEnabled(True)
        else:
            self.servicio_seleccionado = None
            self.btn_modificar.setEnabled(False)
            self.btn_eliminar.setEnabled(False)

    def eliminar_servicio(self):
        if not self.servicio_seleccionado:
            return

        id_servicio = self.servicio_seleccionado.get("ID")
        if not id_servicio:
            QMessageBox.critical(self, "Error", "No se pudo determinar el ID del servicio.")
            return

        confirm = QMessageBox.question(
            self,
            "Confirmar eliminación",
            "¿Estás seguro de que deseas eliminar este servicio?",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirm == QMessageBox.Yes:
            if eliminar_servicio(id_servicio):
                QMessageBox.information(self, "Éxito", "Servicio eliminado correctamente.")
                self.cargar_servicios()
            else:
                QMessageBox.critical(self, "Error", "No se pudo eliminar el servicio.")


    def buscar_servicio(self):
        texto = self.busqueda.text().lower()
        for fila in range(self.tabla.rowCount()):
            nombre = self.tabla.item(fila, 0).text().lower()  # columna 0 = Nombre del servicio
            variante = self.tabla.item(fila, 1).text().lower()  # columna 1 = Variante
            coincide = texto in nombre or texto in variante
            self.tabla.setRowHidden(fila, not coincide)
