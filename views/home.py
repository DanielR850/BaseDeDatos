import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel, QVBoxLayout,
    QHBoxLayout, QVBoxLayout
)
from PyQt5.QtGui import QPainter, QBrush, QLinearGradient, QColor, QPixmap
from PyQt5.QtCore import Qt

class HomeWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Menú Principal")
        self.showFullScreen()

        self.setStyleSheet("""
            QPushButton {
                background-color: #fbeee6;
                border: 2px solid black;
                border-radius: 20px;
                font: bold 14pt 'Poppins';
                min-height: 80px;
                min-width: 220px;
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
            QLabel#titulo {
                font-size: 30pt;
                font-weight: bold;
                color: black;
                font-family: 'Poppins';
            }
        """)

        self.initUI()

    def initUI(self):
        layout_principal = QVBoxLayout()
        layout_principal.setContentsMargins(50, 30, 50, 30)

        # Botón superior (solo salir)
        top_buttons = QHBoxLayout()
        self.btn_salir = QPushButton("Salir ✕")
        self.btn_salir.setObjectName("salir")
        self.btn_salir.clicked.connect(self.close)

        top_buttons.addStretch()
        top_buttons.addWidget(self.btn_salir)
        layout_principal.addLayout(top_buttons)

        # Título principal
        titulo = QLabel("Menú Principal")
        titulo.setObjectName("titulo")
        titulo.setAlignment(Qt.AlignCenter)
        layout_principal.addWidget(titulo)

        # Botones principales (horizontal)
        botones_layout = QHBoxLayout()
        botones_layout.setSpacing(40)

        self.btn_citas = QPushButton("Citas")
        self.btn_inventario = QPushButton("Inventario")
        self.btn_opciones = QPushButton("Opciones")

        self.btn_citas.clicked.connect(self.toggle_submenu_citas)
        self.btn_opciones.clicked.connect(self.toggle_submenu_opciones)
        self.btn_inventario.clicked.connect(self.ir_inventario)

        botones_layout.addStretch()
        botones_layout.addWidget(self.btn_citas)
        botones_layout.addWidget(self.btn_inventario)
        botones_layout.addWidget(self.btn_opciones)
        botones_layout.addStretch()

        layout_principal.addLayout(botones_layout)

        # Submenús con estilo de 3 campos horizontales
        self.submenu_citas = QHBoxLayout()
        self.submenu_citas_widgets = []
        for text in ["Agendar Citas", "Resumen de Citas", "Disponibilidad de Citas"]:
            box = QVBoxLayout()
            btn = QPushButton(text)
            btn.setMinimumSize(180, 60)
            btn.hide()
            box.addWidget(btn)
            self.submenu_citas.addLayout(box)
            self.submenu_citas_widgets.append(btn)
        layout_principal.addLayout(self.submenu_citas)

        self.submenu_opciones = QHBoxLayout()
        self.submenu_opciones_widgets = []
        for text in ["Generar Pagos", "Registro de Pagos", "Promociones"]:
            box = QVBoxLayout()
            btn = QPushButton(text)
            btn.setMinimumSize(180, 60)
            btn.hide()
            box.addWidget(btn)
            self.submenu_opciones.addLayout(box)
            self.submenu_opciones_widgets.append(btn)
        layout_principal.addLayout(self.submenu_opciones)

        # Logo centrado
        logo_label = QLabel()
        pixmap = QPixmap("C:/Users/makib/Documents/EntornosVirtuales/BaseDeDatosSalonDeBelleza/resources/logo_sinfondo.png")
        logo_label.setPixmap(pixmap.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        logo_label.setAlignment(Qt.AlignCenter)
        layout_principal.addWidget(logo_label)

        self.setLayout(layout_principal)

    def toggle_submenu_citas(self):
        for btn in self.submenu_citas_widgets:
            btn.setVisible(not btn.isVisible())
        # Ocultar submenu de opciones
        for btn in self.submenu_opciones_widgets:
            btn.hide()

    def toggle_submenu_opciones(self):
        for btn in self.submenu_opciones_widgets:
            btn.setVisible(not btn.isVisible())
        # Ocultar submenu de citas
        for btn in self.submenu_citas_widgets:
            btn.hide()

    def ir_inventario(self):
        # Aquí conectas el inventario
        print("Ir a Inventario")

    def paintEvent(self, event):
        painter = QPainter(self)
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0.0, QColor("#e6a0a0"))
        gradient.setColorAt(1.0, QColor("#e0cfcf"))
        painter.setBrush(QBrush(gradient))
        painter.drawRect(self.rect())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = HomeWindow()
    ventana.show()
    sys.exit(app.exec_())
