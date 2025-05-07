from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QComboBox, QVBoxLayout, QHBoxLayout, QGraphicsDropShadowEffect,
    QMessageBox, QSpacerItem, QSizePolicy
)
from PyQt5.QtGui import QPixmap, QPainter, QPen
import os
from views.home import HomeWindow

from models.usuario import verificar_credenciales
from views.registro import VentanaRegistro

class IconoOjo(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setCheckable(True)
        self.setFixedSize(40, 40)
        self.setStyleSheet("background: transparent; border: none;")

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        pen = QPen(Qt.black if not self.isChecked() else Qt.gray)
        pen.setWidth(2)
        painter.setPen(pen)

        center = self.rect().center()
        radius = 10

        # Ojo
        painter.drawEllipse(center, radius, radius // 2)
        painter.setBrush(Qt.black if not self.isChecked() else Qt.lightGray)
        painter.drawEllipse(center, 3, 3)

        if self.isChecked():
            painter.drawLine(5, 5, 35, 35)


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Iniciar Sesión")
        self.showFullScreen()  # ← pantalla completa real

        self.setStyleSheet("""
        QWidget {
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #e1938c, stop: 1 #d6c6c2);
        }
        QLineEdit, QComboBox {
            background-color: #ffefe3;
            border: 2px solid black;
            border-radius: 8px;
            padding: 12px;
            font-size: 22px;
            font-weight: bold;
        }
        QPushButton {
            background-color: #e57979;
            border: 2px solid black;
            border-radius: 12px;
            padding: 15px 30px;
            font-weight: bold;
            font-size: 22px;
            color: black;
        }
        QPushButton:hover {
            background-color: #ffe0f0;
        }
        QLabel {
            background: transparent;
            font-size: 22px;
            font-weight: bold;
        }
        """)

        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignCenter)

        # Logo
        logo = QLabel()
        logo_path = os.path.join(os.path.dirname(__file__), "..", "resources", "logo_sinfondo.png")
        pixmap = QPixmap(logo_path)
        if not pixmap.isNull():
            logo.setPixmap(pixmap.scaledToHeight(150))
        logo.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(logo)

        ancho_campo = 500

        form_layout = QVBoxLayout()
        form_layout.setSpacing(25)
        form_layout.setAlignment(Qt.AlignCenter)

        self.roles_dict = {"Administrador": "Admin", "Empleado": "Empleado"}

        # Tipo de Usuario
        self.tipo_usuario = QComboBox()
        self.tipo_usuario.addItems(self.roles_dict.keys())
        self.tipo_usuario.setFixedWidth(ancho_campo)
        form_layout.addWidget(QLabel("Tipo de Usuario"), alignment=Qt.AlignCenter)
        form_layout.addWidget(self.tipo_usuario, alignment=Qt.AlignCenter)

        # Usuario
        self.usuario = QLineEdit()
        self.usuario.setPlaceholderText("Usuario")
        self.usuario.setFixedWidth(ancho_campo)
        form_layout.addWidget(QLabel("Usuario"), alignment=Qt.AlignCenter)
        form_layout.addWidget(self.usuario, alignment=Qt.AlignCenter)

        # Contraseña + botón ojo
        self.contrasena = QLineEdit()
        self.contrasena.setEchoMode(QLineEdit.Password)
        self.contrasena.setPlaceholderText("Contraseña")
        self.contrasena.setFixedHeight(55)
        self.contrasena.setFixedWidth(ancho_campo - 40)
        self.contrasena.setStyleSheet("""
            QLineEdit {
                background-color: #ffefe3;
                border: 2px solid black;
                border-radius: 8px;
                padding-left: 12px;
                font-size: 22px;
                font-weight: bold;
                font-family: 'Roboto', 'Helvetica', monospace;
            }
        """)

        self.boton_ojo = IconoOjo()
        self.boton_ojo.clicked.connect(self.toggle_password_visibility)
        self.boton_ojo.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
                margin-right: 8px;
            }
            QPushButton:hover {
                background-color: rgba(0, 0, 0, 30%);
                border-radius: 20px;
            }
        """)

        pass_layout = QHBoxLayout()
        pass_layout.setContentsMargins(0, 0, 0, 0)
        pass_layout.setSpacing(0)
        pass_layout.addWidget(self.contrasena)
        pass_layout.addWidget(self.boton_ojo)

        pass_widget = QWidget()
        pass_widget.setLayout(pass_layout)
        pass_widget.setStyleSheet("background: transparent;")

        form_layout.addWidget(QLabel("Contraseña"), alignment=Qt.AlignCenter)
        form_layout.addWidget(pass_widget, alignment=Qt.AlignCenter)


        # Botones
        btn_layout = QHBoxLayout()
        btn_login = QPushButton("Iniciar Sesión")
        btn_login.clicked.connect(self.abrir_home)

        btn_registrar = QPushButton("Registrarse")
        btn_registrar.clicked.connect(self.abrir_registro)

        btn_layout.addWidget(btn_login)
        btn_layout.addWidget(btn_registrar)

        form_layout.addLayout(btn_layout)

        main_layout.addLayout(form_layout)

                # Información de contacto (esquina inferior izquierda)
        contacto_label = QLabel(
            "Contacto para mejoras:\n"
            "leo.dav_sg@outlook.com\n"
            "miltonvazquez564@gmail.com\n"
            "denilson_gzzdiaz@hotmail.com\n"
            "d.reyna.burnes@gmail.com"
        )
        contacto_label.setStyleSheet("font-size: 10pt; color: #333; background: transparent;")
        contacto_label.setAlignment(Qt.AlignLeft | Qt.AlignBottom)

        contacto_layout = QHBoxLayout()
        contacto_layout.addWidget(contacto_label, alignment=Qt.AlignLeft | Qt.AlignBottom)

        main_layout.addStretch()
        main_layout.addLayout(contacto_layout)

    def toggle_password_visibility(self):
        if self.boton_ojo.isChecked():
            self.contrasena.setEchoMode(QLineEdit.Normal)
        else:
            self.contrasena.setEchoMode(QLineEdit.Password)

    def abrir_home(self):
        usuario_txt = self.usuario.text().strip()
        contrasena_txt = self.contrasena.text().strip()
        rol_seleccionado = self.tipo_usuario.currentText()
        rol_db = self.roles_dict.get(rol_seleccionado, "")

        if not usuario_txt or not contrasena_txt:
            QMessageBox.warning(self, "Campos vacíos", "Por favor, ingresa usuario y contraseña.")
            return

        try:
            print("🔍 Verificando credenciales...")
            if verificar_credenciales(rol_db, usuario_txt, contrasena_txt):
                print("✅ Credenciales válidas. Intentando abrir HomeWindow...")
                self.home = HomeWindow()
                print("✅ HomeWindow creada exitosamente")
                self.home.show()
                self.close()
            else:
                QMessageBox.warning(self, "Error de autenticación", "Usuario o contraseña incorrectos.")
        except Exception as e:
            print(f"❌ ERROR al crear HomeWindow: {e}")
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self, "Error crítico", f"Hubo un problema al abrir el menú principal:\n{e}")




    def abrir_registro(self):
        self.registro = VentanaRegistro()
        self.registro.show()
        self.close()
