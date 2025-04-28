import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QComboBox, QDateEdit
)
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt, QDate

class VentanaRegistro(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Registro de Usuario")
        self.showFullScreen()

        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(
                    x1: 0, y1: 0,
                    x2: 0, y2: 1,
                    stop: 0 #f8c8dc,
                    stop: 1 #fefefe
                );
                font-family: 'Poppins';
            }
            QLabel {
                background-color: transparent;
                font-size: 16pt;
                color: #000000;
                font-family: 'Poppins';
            }
            QLineEdit, QComboBox, QDateEdit {
                background-color: #e5d3c5;
                border: 2px solid #000000;
                border-radius: 10px;
                padding: 10px;
                font-size: 14pt;
                min-width: 250px;
                min-height: 41px;
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
            QPushButton#registrar {
                background-color: #231f20;
                color: #fcb3b3;
                font-family: 'Poppins';
                padding: 15px;
                border-radius: 20px;
                font-size: 18pt;
                min-width: 300px;
                min-height: 80px;
            }
            QPushButton#registrar:hover {
                background-color: #333333;
            }
        """)

        self.initUI()

    def initUI(self):
        layout_principal = QVBoxLayout()
        layout_principal.setContentsMargins(100, 20, 100, 20)

        # Botones superiores
        botones_superiores = QHBoxLayout()
        self.btn_regresar = QPushButton("Regresar")
        self.btn_regresar.setObjectName("regresar")
        self.btn_salir = QPushButton("Salir")
        self.btn_salir.setObjectName("salir")
        self.btn_salir.clicked.connect(self.close)

        botones_superiores.addWidget(self.btn_regresar)
        botones_superiores.addStretch()
        botones_superiores.addWidget(self.btn_salir)
        layout_principal.addLayout(botones_superiores)

        # Logo
        logo = QLabel()
        pixmap = QPixmap("C:/Users/makib/Documents/EntornosVirtuales/BaseDeDatosSalonDeBelleza/resources/logo_sinfondo.png")
        logo.setPixmap(pixmap.scaled(120, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        logo.setAlignment(Qt.AlignCenter)
        layout_principal.addWidget(logo)

        # Título
        titulo = QLabel("Registro de Usuario")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-size: 28pt; font-weight: bold; margin-bottom: 30px;")
        layout_principal.addWidget(titulo)

        # Formulario
        campos_centrados = QVBoxLayout()
        campos_centrados.setAlignment(Qt.AlignCenter)

        # Primera fila: 3 campos
        fila1 = QHBoxLayout()
        fila1.setSpacing(50)
        self.nombre = QLineEdit()
        self.apellido_p = QLineEdit()
        self.apellido_m = QLineEdit()

        vbox_nombre = self.create_field_group("Nombre", self.nombre)
        vbox_apellido_p = self.create_field_group("Apellido Paterno", self.apellido_p)
        vbox_apellido_m = self.create_field_group("Apellido Materno", self.apellido_m)

        fila1.addLayout(vbox_nombre)
        fila1.addLayout(vbox_apellido_p)
        fila1.addLayout(vbox_apellido_m)

        # Segunda fila: 3 campos
        fila2 = QHBoxLayout()
        fila2.setSpacing(50)
        self.tipo_usuario = QComboBox()
        self.tipo_usuario.addItems(["Administrador", "Empleado"])
        self.fecha_nac = QDateEdit()
        self.fecha_nac.setCalendarPopup(True)
        self.fecha_nac.setDate(QDate.currentDate())
        self.contrasena = QLineEdit()
        self.contrasena.setPlaceholderText("Contraseña de Usuario")
        self.contrasena.setEchoMode(QLineEdit.Password)

        vbox_tipo = self.create_field_group("Tipo de Usuario", self.tipo_usuario)
        vbox_fecha = self.create_field_group("Contraseña", self.contrasena)
        vbox_contrasena = self.create_field_group("Confirmar Contraseña", self.contrasena)

        fila2.addLayout(vbox_tipo)
        fila2.addLayout(vbox_fecha)
        fila2.addLayout(vbox_contrasena)

        campos_centrados.addLayout(fila1)
        campos_centrados.addSpacing(40)
        campos_centrados.addLayout(fila2)

        layout_principal.addLayout(campos_centrados)

        # Botón registrar
        self.btn_registrar = QPushButton("Registrar")
        self.btn_registrar.setObjectName("registrar")
        self.btn_registrar.clicked.connect(self.registrar_usuario)

        layout_principal.addSpacing(30)
        layout_principal.addWidget(self.btn_registrar, alignment=Qt.AlignCenter)

        self.setLayout(layout_principal)

    def create_field_group(self, label_text, input_widget):
        group = QVBoxLayout()
        label = QLabel(label_text)
        label.setAlignment(Qt.AlignCenter)
        group.addWidget(label)
        group.addWidget(input_widget)
        return group

    def registrar_usuario(self):
        print("Usuario registrado:")
        print("Nombre:", self.nombre.text())
        print("Apellido Paterno:", self.apellido_p.text())
        print("Apellido Materno:", self.apellido_m.text())
        print("Tipo de usuario:", self.tipo_usuario.currentText())
        print("Contraseña:", self.contrasena.text())
        print("Confirmar contraseña:", self.contrasena.text())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaRegistro()
    ventana.show()
    sys.exit(app.exec_())
