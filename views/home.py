import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel, QVBoxLayout,
    QHBoxLayout
)
from PyQt5.QtGui import QPainter, QBrush, QLinearGradient, QColor, QPixmap
from PyQt5.QtCore import Qt
from views.inventario import InventarioVentana
from views.promociones import VentanaPromociones  # ← NUEVO IMPORT
from views.agendar_cita import AgendarCitaWindow
from views.ventana_servicios import VentanaServicios
from views.disponibilidad import DisponibilidadCitas
from views.generar_pago import GenerarPago
from views.registro_pago import RegistroPago
import os


class HomeWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Menú Principal")
        self.setMinimumSize(1024, 1000)
        self.showMaximized()  # 👈 Ahora sí muestra los controles de ventana

        self.setStyleSheet("""
            QPushButton {
                background-color: #fbeee6;
                border: 2px solid black;
                border-radius: 20px;
                font: bold 14pt 'Poppins';
                min-height: 80px;
                min-width: 220px;
                max-width: 220px;
            }
            QPushButton:hover {
                background-color: #fcd9c7;
            }
            QPushButton#salir {
                background-color: transparent;
                border: none;
                color: black;
                font: bold 14pt 'Open Sans';
                min-width: 80px;
                min-height: 30px;
            }
            QPushButton#salir:hover {
                color: gray;
            }
        """)

        self.initUI()

    def initUI(self):
        layout_principal = QVBoxLayout()
        layout_principal.setContentsMargins(50, 30, 50, 30)

        # Botón Salir
        top_buttons = QHBoxLayout()
        self.btn_salir = QPushButton("Salir ✕")
        self.btn_salir.setObjectName("salir")
        self.btn_salir.clicked.connect(self.volver_a_login)
        top_buttons.addStretch()
        top_buttons.addWidget(self.btn_salir)
        layout_principal.addLayout(top_buttons)

        contenedor_layout = QHBoxLayout()
        contenedor_layout.setSpacing(50)
        contenedor_layout.setAlignment(Qt.AlignCenter)

        # Citas
        self.citas_box = self.create_menu("Citas", [
            ("Agendar Cita", self.abrir_agendar_cita),
            ("Servicios", self.abrir_servicios),
            ("Disponibilidad", self.abrir_disponibilidad)
        ])
        contenedor_layout.addLayout(self.citas_box)

        # Inventario
        inventario_layout = QVBoxLayout()
        btn_inventario = QPushButton("Inventario")
        btn_inventario.clicked.connect(self.abrir_inventario)
        inventario_layout.addWidget(btn_inventario)
        inventario_layout.addStretch()
        contenedor_layout.addLayout(inventario_layout)

        # Opciones
        self.opciones_box = self.create_menu("Opciones", [
            ("Registro de Pagos", self.abrir_registro_pago),
            ("Promociones", self.abrir_promociones)
        ])
        contenedor_layout.addLayout(self.opciones_box)

        layout_principal.addLayout(contenedor_layout)

        # Logo
        logo_label = QLabel()
        ruta_logo = os.path.join(os.path.dirname(__file__), "resources", "logo_sinfondo.png")
        pixmap = QPixmap(ruta_logo)
        logo_label.setPixmap(pixmap.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        logo_label.setAlignment(Qt.AlignCenter)
        layout_principal.addWidget(logo_label)

        self.setLayout(layout_principal)

    def create_menu(self, title, actions):
        layout = QVBoxLayout()
        toggle_btn = QPushButton(title)
        layout.addWidget(toggle_btn)

        submenu_widget = QWidget()
        submenu_layout = QVBoxLayout()
        submenu_layout.setSpacing(10)
        submenu_widget.setLayout(submenu_layout)
        submenu_widget.setVisible(False)

        for text, action in actions:
            btn = QPushButton(text)
            btn.setFixedSize(220, 80)
            btn.clicked.connect(action)
            submenu_layout.addWidget(btn)

        layout.addWidget(submenu_widget)
        layout.addStretch()
        toggle_btn.clicked.connect(lambda: self.toggle_visibility(submenu_widget))
        return layout

    def toggle_visibility(self, widget):
        widget.setVisible(not widget.isVisible())

    def paintEvent(self, event):
        painter = QPainter(self)
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0.0, QColor("#e6a0a0"))
        gradient.setColorAt(1.0, QColor("#e0cfcf"))
        painter.setBrush(QBrush(gradient))
        painter.drawRect(self.rect())

    def abrir_agendar_cita(self):
        self.cita_ventana = AgendarCitaWindow(regresar_callback=self.mostrar_home)
        self.cita_ventana.show()
        self.hide()

    def abrir_servicios(self):
        self.servicios_ventana = VentanaServicios()
        self.servicios_ventana.show()
        self.hide()

    def abrir_disponibilidad(self):
        self.disponibilidad_ventana = DisponibilidadCitas(regresar_callback=self.mostrar_home)
        self.disponibilidad_ventana.show()
        self.hide()

    def abrir_inventario(self):
        self.inventario_ventana = InventarioVentana(regresar_callback=self.mostrar_home)
        self.inventario_ventana.show()
        self.hide()

    def abrir_promociones(self):
        self.promociones_ventana = VentanaPromociones()
        self.promociones_ventana.btn_regresar.clicked.connect(self.mostrar_home)
        self.promociones_ventana.show()
        self.hide()

    def abrir_registro_pago(self):
        self.registro_pago_ventana = RegistroPago(regresar_callback=self.mostrar_home)
        self.registro_pago_ventana.show()
        self.hide()

    def abrir_generar_pago(self):
        self.generar_pago_ventana = GenerarPago(regresar_callback=self.mostrar_home)
        self.generar_pago_ventana.show()
        self.hide()

    def mostrar_home(self):
        self.show()
        self.raise_()
        self.activateWindow()
        self.setWindowState(Qt.WindowActive)
        self.showMaximized()

    def volver_a_login(self):
        from views.login import LoginWindow
        self.login_window = LoginWindow()
        self.login_window.show()
        self.hide()
