import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel
from PyQt5.QtGui import QPainter, QBrush, QLinearGradient, QColor, QPixmap
from PyQt5.QtCore import Qt

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Menú Principal")
        self.resize(800, 500)

       
        self.btn_citas = QPushButton("Citas", self)
        self.btn_inventario = QPushButton("Inventario", self)
        self.btn_opciones = QPushButton("Opciones", self)
        self.btn_salir = QPushButton("SALIR  ✕", self)
        self.logo_label = QLabel(self)

      
        for boton in [self.btn_citas, self.btn_inventario, self.btn_opciones]:
            self.estilizar_boton(boton)

        
        self.btn_salir.setStyleSheet("background-color: transparent; color: black; font: 12pt Arial;")
        self.btn_salir.clicked.connect(self.close)

       
        self.logo_label.setAlignment(Qt.AlignCenter)
        self.pixmap = QPixmap("./resources/logo_sinfondo.png")

        self.actualizar_layout()

    def estilizar_boton(self, boton):
        boton.setStyleSheet("""
            QPushButton {
                background-color: #fbeee6;
                border: 2px solid black;
                border-radius: 20px;
                font: bold 14pt Arial;
            }
            QPushButton:hover {
                background-color: #fcd9c7;
            }
        """)

    def paintEvent(self, event):
        painter = QPainter(self)
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0.0, QColor("#e6a0a0"))
        gradient.setColorAt(1.0, QColor("#e0cfcf"))
        painter.setBrush(QBrush(gradient))
        painter.drawRect(self.rect())

    def resizeEvent(self, event):
        self.actualizar_layout()

    def actualizar_layout(self):
        w = self.width()
        h = self.height()

      
        btn_width = int(w * 0.18)
        btn_height = int(h * 0.12)
        margin_top = int(h * 0.08)
        spacing = int((w - 3 * btn_width) / 4)

        
        self.btn_citas.setGeometry(spacing, margin_top, btn_width, btn_height)
        self.btn_inventario.setGeometry(2 * spacing + btn_width, margin_top, btn_width, btn_height)
        self.btn_opciones.setGeometry(3 * spacing + 2 * btn_width, margin_top, btn_width, btn_height)

        
        self.btn_salir.setGeometry(w - 90, 10, 80, 30)

        
        logo_size = min(w, h) // 5
        self.logo_label.setGeometry(w // 2 - logo_size // 2, h // 2 - logo_size // 2, logo_size, logo_size)
        scaled_pixmap = self.pixmap.scaled(logo_size, logo_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.logo_label.setPixmap(scaled_pixmap)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
