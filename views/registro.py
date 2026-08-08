import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QComboBox, QMessageBox
)
from PyQt5.QtGui import QPixmap, QPainter, QPen
from PyQt5.QtCore import Qt
from models.usuario import insertar_usuario, obtener_id_rol
import re
import bcrypt

class IconoOjo(QPushButton):
    def __init__(self, input_field):
        super().__init__()
        self.setCheckable(True)
        self.input_field = input_field
        self.setFixedSize(40, 40)
        self.setStyleSheet("background: transparent; border: none;")
        self.clicked.connect(self.toggle_visibility)

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        pen = QPen(Qt.black if not self.isChecked() else Qt.gray)
        pen.setWidth(2)
        painter.setPen(pen)
        center = self.rect().center()
        painter.drawEllipse(center, 10, 5)
        painter.setBrush(Qt.black if not self.isChecked() else Qt.lightGray)
        painter.drawEllipse(center, 3, 3)
        if self.isChecked():
            painter.drawLine(5, 5, 35, 35)

    def toggle_visibility(self):
        mode = QLineEdit.Normal if self.isChecked() else QLineEdit.Password
        self.input_field.setEchoMode(mode)

class VentanaRegistro(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Registro de Usuario")
        self.showMaximized()
        self.initUI()

    def initUI(self):
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #f8c8dc, stop: 1 #fefefe);
                font-family: 'Poppins';
            }
            QLabel {
                font-size: 16pt;
                color: #000;
                background-color: transparent;
            }
            QLineEdit, QComboBox {
                background: #e5d3c5;
                border: 2px solid #000;
                border-radius: 10px;
                padding: 10px;
                font-size: 14pt;
                min-height: 40px;
            }
            QPushButton#regresar, QPushButton#salir {
                background: transparent;
                font-weight: bold;
                font-size: 14pt;
                color: #101111;
            }
            QPushButton#regresar:hover, QPushButton#salir:hover {
                color: gray;
            }
            QPushButton#registrar {
                background-color: #231f20;
                color: #fcb3b3;
                font-size: 18pt;
                padding: 15px;
                border-radius: 20px;
                min-width: 300px;
                min-height: 80px;
            }
            QPushButton#registrar:hover {
                background-color: #333333;
            }
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(100, 30, 100, 30)
        layout.setSpacing(20)

        # Top buttons
        top_row = QHBoxLayout()
        self.btn_regresar = QPushButton("Regresar")
        self.btn_regresar.setObjectName("regresar")
        self.btn_regresar.clicked.connect(self.regresar)
        self.btn_salir = QPushButton("Salir")
        self.btn_salir.setObjectName("salir")
        self.btn_salir.clicked.connect(self.close)
        top_row.addWidget(self.btn_regresar)
        top_row.addStretch()
        top_row.addWidget(self.btn_salir)
        layout.addLayout(top_row)

        # Logo
        logo = QLabel()
        pixmap = QPixmap("resources/logo_sinfondo.png").scaled(120, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        logo.setPixmap(pixmap)
        logo.setAlignment(Qt.AlignCenter)
        layout.addWidget(logo)

        # Título
        titulo = QLabel("Registro de Usuario")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-size: 28pt; font-weight: bold;")
        layout.addWidget(titulo)

        # Formulario
        form_layout = QVBoxLayout()

        # Fila 1: nombre y apellidos
        fila1 = QHBoxLayout()
        self.nombre = QLineEdit()
        self.apellido_p = QLineEdit()
        self.apellido_m = QLineEdit()
        fila1.addLayout(self.build_field("Nombre", self.nombre))
        fila1.addLayout(self.build_field("Apellido Paterno", self.apellido_p))
        fila1.addLayout(self.build_field("Apellido Materno", self.apellido_m))

        # Fila 2: tipo de usuario + nombre de usuario
        fila2 = QHBoxLayout()
        self.tipo_usuario = QComboBox()
        self.tipo_usuario.addItems(["Administrador", "Empleado"])
        self.nombre_usuario = QLineEdit()
        fila2.addLayout(self.build_field("Tipo de Usuario", self.tipo_usuario))
        fila2.addLayout(self.build_field("Usuario", self.nombre_usuario))

        # Fila 3: contraseñas
        fila3 = QHBoxLayout()
        self.contrasena = QLineEdit()
        self.contrasena.setEchoMode(QLineEdit.Password)
        self.confirmar_contrasena = QLineEdit()
        self.confirmar_contrasena.setEchoMode(QLineEdit.Password)
        pass1 = self.build_field("Contraseña", self.contrasena, with_eye=True)
        pass2 = self.build_field("Confirmar Contraseña", self.confirmar_contrasena, with_eye=True)
        fila3.addLayout(pass1)
        fila3.addLayout(pass2)

        # Ensamblar formulario
        form_layout.addLayout(fila1)
        form_layout.addSpacing(15)
        form_layout.addLayout(fila2)
        form_layout.addSpacing(15)
        form_layout.addLayout(fila3)
        layout.addLayout(form_layout)

        # Botón registrar
        self.btn_registrar = QPushButton("Registrar")
        self.btn_registrar.setObjectName("registrar")
        self.btn_registrar.clicked.connect(self.registrar_usuario)
        layout.addSpacing(20)
        layout.addWidget(self.btn_registrar, alignment=Qt.AlignCenter)

        self.setLayout(layout)

    def build_field(self, label_text, widget, with_eye=False):
        layout = QVBoxLayout()
        label = QLabel(label_text)
        label.setAlignment(Qt.AlignLeft)

        if with_eye:
            eye_button = IconoOjo(widget)
            row = QHBoxLayout()
            row.addWidget(widget)
            row.addWidget(eye_button)
            row.setContentsMargins(0, 0, 0, 0)
            row.setSpacing(5)
            field_container = QWidget()
            field_container.setLayout(row)
            field_container.setStyleSheet("background: transparent;")  # 👈 Aquí hacemos el contenedor transparente
            layout.addWidget(label)
            layout.addWidget(field_container)
        else: 
            layout.addWidget(label)
            layout.addWidget(widget)
        return layout


    def registrar_usuario(self):
        try:
            nombre = self.nombre.text().strip()
            ap_paterno = self.apellido_p.text().strip()
            ap_materno = self.apellido_m.text().strip()
            nombre_usuario = self.nombre_usuario.text().strip()
            tipo = self.tipo_usuario.currentText().strip()
            password = self.contrasena.text()
            confirmar = self.confirmar_contrasena.text()

            if not all([nombre, ap_paterno, ap_materno, nombre_usuario, password, confirmar]):
                QMessageBox.warning(self, "Campos incompletos", "Por favor, llena todos los campos.")
                return

            if password != confirmar:
                QMessageBox.critical(self, "Contraseñas no coinciden", "Las contraseñas ingresadas no coinciden.")
                return

            # Validación de contraseña segura
            if len(password) < 10:
                QMessageBox.warning(self, "Contraseña débil", "La contraseña debe tener al menos 10 caracteres.")
                return

            if not re.search(r"[A-Za-z]", password):
                QMessageBox.warning(self, "Contraseña inválida", "Debe contener al menos una letra.")
                return

            if not re.search(r"[0-9]", password):
                QMessageBox.warning(self, "Contraseña inválida", "Debe contener al menos un número.")
                return

            if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
                QMessageBox.warning(self, "Contraseña inválida", "Debe contener al menos un carácter especial.")
                return

            # Encriptar la contraseña
            hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

            # Mapeo de rol
            rol_mapeado = "Admin" if tipo == "Administrador" else "Empleado"

            from models.usuario import obtener_id_rol, insertar_usuario
            id_usuario = obtener_id_rol(rol_mapeado)

            if id_usuario is None:
                QMessageBox.critical(self, "Error", "No se pudo determinar el rol del usuario.")
                return

            exito = insertar_usuario(nombre, ap_paterno, ap_materno, nombre_usuario, hashed_password, id_usuario)

            if exito:
                QMessageBox.information(self, "Éxito", "Usuario registrado correctamente.")
                self.regresar()
            else:
                QMessageBox.critical(self, "Error", "El nombre de usuario ya está en uso. Elige otro.")

        except Exception as e:
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self, "Error", "Ocurrió un error inesperado al registrar.")

    def regresar(self):
        from views.login import LoginWindow
        self.login = LoginWindow()
        self.login.show()
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaRegistro()
    ventana.show()
    sys.exit(app.exec_())
