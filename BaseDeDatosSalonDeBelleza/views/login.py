from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QComboBox, QVBoxLayout, QHBoxLayout, QGraphicsDropShadowEffect, QMessageBox 
)
from PyQt5.QtGui import QIcon, QPixmap
import subprocess
import sys

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Iniciar Sesión")
        self.setStyleSheet("""
        QWidget {
            background: qlineargradient(
                x1: 0, y1: 0,
                x2: 0, y2: 1,
                stop: 0 #e1938c,
                stop: 1 #d6c6c2
            );
        }

        QLineEdit, QComboBox {
            background-color: #ffefe3;
            border: 2px solid black;
            border-radius: 8px;
            padding: 12px;
            font-size: 22px;
            font-weight: bold;
            font-family: 'Roboto', 'Helvetica', monospace;

        }

        QPushButton {
            background-color: #e57979;
            border: 2px solid black;
            border-radius: 12px;
            padding: 15px 30px;
            font-weight: bold;
            font-size: 22px;
            font-family: 'Roboto', 'Helvetica', monospace;
            color: black;
            margin: 30px;
        }

        QPushButton:hover {
            background-color: #ffe0f0;
            border: 1px solid black;
        }

        QPushButton:pressed {
            background-color: #f9c5da;
            border: 1px solid #c05383;
        }

        QLabel {
            background: transparent;
            font-size: 22px;
            font-family: Arial;
            font-weight: bold;
            font-family: 'Roboto', 'Helvetica', monospace;

        }
        """)

        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)

        logo = QLabel()
        pixmap = QPixmap("../resources/logo_sinfondo.png")
        logo.setPixmap(pixmap.scaledToHeight(200))
        logo.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(logo)

        form_container = QVBoxLayout()
        form_container.setAlignment(Qt.AlignCenter)
        form_container.setSpacing(30)

        ancho_campo = 600

        # Tipo de Usuario
        label_tipo = QLabel("Tipo de Usuario")
        self.tipo_usuario = QComboBox()
        self.tipo_usuario.addItems(["Administrador", "Empleado"])
        self.tipo_usuario.setFixedWidth(ancho_campo)
        form_container.addWidget(label_tipo, alignment=Qt.AlignCenter)
        form_container.addWidget(self.tipo_usuario, alignment=Qt.AlignCenter)

        # ID de Usuario
        label_usuario = QLabel("ID de Usuario")
        self.usuario = QLineEdit()
        self.usuario.setFixedWidth(ancho_campo)
        self.usuario.setMaxLength(10)
        self.usuario.setPlaceholderText("Ejemplo: admin12345")
        form_container.addWidget(label_usuario, alignment=Qt.AlignCenter)
        form_container.addWidget(self.usuario, alignment=Qt.AlignCenter)

        # Contraseña
        label_contra = QLabel("Contraseña")
        self.contrasena = QLineEdit()
        self.contrasena.setEchoMode(QLineEdit.Password)
        self.contrasena.setFixedWidth(ancho_campo - 40)
        self.contrasena.setMaxLength(8)
        self.contrasena.setPlaceholderText("Mínimo 6 caracteres, máximo 8")
        self.contrasena.setStyleSheet("""
            background-color: #ffefe3;
            border: 2px solid black;
            border-radius: 8px;
            padding: 12px;
            font-size: 20px;
            font-weight: bold;
        """)

        self.boton_ojo = QPushButton()
        self.boton_ojo.setFixedSize(40, 40)
        self.boton_ojo.setIcon(QIcon("../resources/ojo2.png"))
        self.boton_ojo.setIconSize(QSize(40, 40))
        self.boton_ojo.setStyleSheet("""
                    QPushButton {
                    border: none;
                    background: transparent;
                }
                QPushButton:hover {
                    background-color: rgba(255, 255, 255, 60);
                    border-radius: 20px;
                }
            """)
        self.boton_ojo.setCheckable(True)
        self.boton_ojo.clicked.connect(self.toggle_password_visibility)

        sombra = QGraphicsDropShadowEffect()
        sombra.setBlurRadius(15)
        sombra.setXOffset(0)
        sombra.setYOffset(2)
        sombra.setColor(Qt.gray)
        self.boton_ojo.setGraphicsEffect(sombra)

        contrasena_layout = QHBoxLayout()
        contrasena_layout.addWidget(self.contrasena)
        contrasena_layout.addWidget(self.boton_ojo)

        contrasena_widget = QWidget()
        contrasena_widget.setLayout(contrasena_layout)
        contrasena_widget.setStyleSheet("background: transparent;")

        form_container.addWidget(label_contra, alignment=Qt.AlignCenter)
        form_container.addWidget(contrasena_widget, alignment=Qt.AlignCenter)

        main_layout.addLayout(form_container)

        # Botones
        botones = QHBoxLayout()
        btn_login = QPushButton("Iniciar Sesión")
        btn_login.clicked.connect(self.abrir_home)

        btn_registrar = QPushButton("Registrarse")
        btn_registrar.clicked.connect(self.abrir_registro)

        botones.addWidget(btn_login)
        botones.addWidget(btn_registrar)
        main_layout.addLayout(botones)

        self.setLayout(main_layout)

        # Eventos para placeholder dinámico
        self.usuario.focusInEvent = lambda event: self.handle_focus(event, self.usuario, "")
        self.usuario.focusOutEvent = lambda event: self.handle_focus(event, self.usuario, "Ej: admin123")

        self.contrasena.focusInEvent = lambda event: self.handle_focus(event, self.contrasena, "")
        self.contrasena.focusOutEvent = lambda event: self.handle_focus(event, self.contrasena, "Mínimo 6 caracteres, máximo 16")

    def handle_focus(self, event, widget, placeholder_text):
        if event.type() == event.FocusIn:
            widget.setPlaceholderText("")
        elif event.type() == event.FocusOut:
            if not widget.text():
                widget.setPlaceholderText(placeholder_text)

    def toggle_password_visibility(self):
        if self.boton_ojo.isChecked():
            self.contrasena.setEchoMode(QLineEdit.Normal)
        else:
            self.contrasena.setEchoMode(QLineEdit.Password)

    def abrir_home(self):
        usuario = self.usuario.text().strip()
        contrasena = self.contrasena.text().strip()

        if not usuario or usuario == "Ej: admin01":
            QMessageBox.warning(self, "Campo incompleto", "Por favor ingresa tu ID de Usuario.")
            return
        if not contrasena or contrasena == "Ej: 8caract":
            QMessageBox.warning(self, "Campo incompleto", "Por favor ingresa tu contraseña.")
            return

        # Aquí iría la lógica con la base de datos
        if usuario != "admin01" or contrasena != "12345678":
            QMessageBox.critical(self, "Error de autenticación", "Usuario o contraseña incorrectos.")
            return

        self.close()
        subprocess.Popen([sys.executable, "home.py"])

    def abrir_registro(self):
        self.close()
        subprocess.Popen([sys.executable, "registro.py"])

if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    import sys
    app = QApplication(sys.argv)
    ventana = LoginWindow()
    ventana.show()
    sys.exit(app.exec_())
