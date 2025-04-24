from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QComboBox,
    QVBoxLayout, QHBoxLayout, QApplication, QDateEdit
)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont
import sys

class VentanaRegistro(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Registro de Usuario")
        self.setGeometry(100, 100, 650, 400)
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(
                    x1: 0, y1: 0,
                    x2: 0, y2: 1,
                    stop: 0 pink,
                    stop: 1 white
                );
                font-family: Arial;
            }
            QLineEdit, QComboBox, QDateEdit {
                border: 2px solid #b88c8c;
                border-radius: 15px;
                padding: 5px 10px;
                background-color: #f4e3d7;
            }
            QLabel {
                font-weight: bold;
                font-size: 12pt;
            }
            QPushButton {
                background-color: #f3b6c4;
                border-radius: 15px;
                padding: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #f27a9d;
            }
        """)
        self.inicializar_ui()

    def inicializar_ui(self):
        layout_principal = QVBoxLayout()
        layout_principal.setAlignment(Qt.AlignTop)
        layout_principal.setContentsMargins(40, 20, 40, 20)
        layout_principal.setSpacing(15)


        titulo = QLabel("Registro de Usuario")
        titulo.setFont(QFont("Arial", 16, QFont.Bold))
        titulo.setAlignment(Qt.AlignCenter)
        layout_principal.addWidget(titulo)


        fila1 = QHBoxLayout()
        self.nombre = QLineEdit()
        self.nombre.setPlaceholderText("Nombre")

        self.apellido_p = QLineEdit()
        self.apellido_p.setPlaceholderText("Apellido Paterno")

        self.apellido_m = QLineEdit()
        self.apellido_m.setPlaceholderText("Apellido Materno")

        fila1.addWidget(self.nombre)
        fila1.addWidget(self.apellido_p)
        fila1.addWidget(self.apellido_m)
        layout_principal.addLayout(fila1)


        fila2 = QHBoxLayout()
        self.tipo_usuario = QComboBox()
        self.tipo_usuario.addItems(["Administrador", "Empleado"])

        self.fecha_nac = QDateEdit()
        self.fecha_nac.setCalendarPopup(True)
        self.fecha_nac.setDate(QDate.currentDate())

        self.contrasena = QLineEdit()
        self.contrasena.setPlaceholderText("Contraseña de Usuario")
        self.contrasena.setEchoMode(QLineEdit.Password)

        fila2.addWidget(self.tipo_usuario)
        fila2.addWidget(self.fecha_nac)
        fila2.addWidget(self.contrasena)
        layout_principal.addLayout(fila2)

    
        botones_layout = QHBoxLayout()
        self.boton_registrar = QPushButton("Registrar")
        self.boton_regresar = QPushButton("Regresar")

        self.boton_registrar.clicked.connect(self.registrar_usuario)
        self.boton_regresar.clicked.connect(self.close)  

        botones_layout.addWidget(self.boton_registrar)
        botones_layout.addWidget(self.boton_regresar)

        layout_principal.addLayout(botones_layout)

        self.setLayout(layout_principal)

    def registrar_usuario(self):
        print("Usuario registrado:")
        print("Nombre:", self.nombre.text())
        print("Apellido Paterno:", self.apellido_p.text())
        print("Apellido Materno:", self.apellido_m.text())
        print("Tipo de usuario:", self.tipo_usuario.currentText())
        print("Fecha de nacimiento:", self.fecha_nac.date().toString())
        print("Contraseña:", self.contrasena.text())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaRegistro()
    ventana.show()
    sys.exit(app.exec_())

