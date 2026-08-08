import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QComboBox
)
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt
from models.pago import obtener_metodos_pago
from models.empleado import obtener_id_empleado_por_usuario
from models.session import SesionActual
from models.usuario import obtener_nombre_usuario_por_id

class GenerarPago(QWidget):

    def __init__(self, cliente=None, total=0.0, id_cita=None, regresar_callback=None):
        super().__init__()
        self.setWindowTitle("Generar Pago")
        self.cliente = cliente or {}
        self.total_valor = total
        self.id_cita = id_cita
        self.regresar_callback = regresar_callback

        self.setMinimumSize(1024, 1000)  # Puedes ajustar si quieres un tamaño mínimo
        self.showMaximized()  # ✅ Se abre maximizada

        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #f8c8dc, stop: 1 #fefefe);
                font-family: 'Poppins';
            }
            QLabel {
                background-color: transparent;
                font-size: 16pt;
                color: #000000;
                font-family: 'Poppins';
            }
            QLineEdit, QComboBox {
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
            QPushButton#pagar {
                background-color: #231f20;
                color: #fcb3b3;
                font-family: 'Poppins';
                padding: 15px;
                border-radius: 20px;
                font-size: 18pt;
                min-width: 300px;
                min-height: 80px;
            }
            QPushButton#pagar:hover {
                background-color: #333333;
            }
        """)

        self.initUI()


    def initUI(self):
        from models.pago import obtener_metodos_pago
        from models.empleado import obtener_id_empleado_por_usuario
        from models.session import SesionActual
        from models.usuario import obtener_nombre_usuario_por_id

        layout_principal = QVBoxLayout()
        layout_principal.setContentsMargins(100, 20, 100, 20)

        # Botones superiores
        botones_superiores = QHBoxLayout()
        self.btn_regresar = QPushButton("Regresar")
        self.btn_regresar.setObjectName("regresar")
        self.btn_regresar.clicked.connect(self.volver_a_resumen)
        botones_superiores.addWidget(self.btn_regresar)
        botones_superiores.addStretch()
        layout_principal.addLayout(botones_superiores)

        # Logo
        logo = QLabel()
        pixmap = QPixmap("C:/Users/makib/Documents/EntornosVirtuales/BaseDeDatosSalonDeBelleza/resources/logo_sinfondo.png")
        logo.setPixmap(pixmap.scaled(120, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        logo.setAlignment(Qt.AlignCenter)
        layout_principal.addWidget(logo)

        # Título
        titulo = QLabel("Generar Pago")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-size: 28pt; font-weight: bold; margin-bottom: 30px;")
        layout_principal.addWidget(titulo)

        # Formulario
        campos_centrados = QVBoxLayout()
        campos_centrados.setAlignment(Qt.AlignCenter)

        # Fila 1: ID Cita, Nombre, Teléfono
        fila1 = QHBoxLayout()
        fila1.setSpacing(50)
        self.cita_input = QLineEdit()
        self.nombre_input = QLineEdit()
        self.telefono_input = QLineEdit()

        fila1.addLayout(self.create_field_group("ID Cita", self.cita_input))
        fila1.addLayout(self.create_field_group("Nombre", self.nombre_input))
        fila1.addLayout(self.create_field_group("Teléfono", self.telefono_input))

        # Fila 2: Servicio, Empleado, Método de Pago
        fila2 = QHBoxLayout()
        fila2.setSpacing(50)
        self.servicio_input = QLineEdit()
        self.empleado_input = QLineEdit()
        self.metodo_pago = QComboBox()

        self.metodos_pago_data = obtener_metodos_pago()
        for metodo in self.metodos_pago_data:
            self.metodo_pago.addItem(metodo["nombre"], metodo["id"])

        fila2.addLayout(self.create_field_group("Servicio", self.servicio_input))
        fila2.addLayout(self.create_field_group("Empleado", self.empleado_input))
        fila2.addLayout(self.create_field_group("Método de Pago", self.metodo_pago))

        # Fila 3: Total
        fila3 = QHBoxLayout()
        fila3.setSpacing(50)
        self.total_input = QLineEdit()
        fila3.addStretch()
        fila3.addLayout(self.create_field_group("Total a Pagar", self.total_input))
        fila3.addStretch()

        # Agregar filas al layout principal
        campos_centrados.addLayout(fila1)
        campos_centrados.addSpacing(30)
        campos_centrados.addLayout(fila2)
        campos_centrados.addSpacing(30)
        campos_centrados.addLayout(fila3)
        layout_principal.addLayout(campos_centrados)

        # Botón de pagar
        self.btn_pagar = QPushButton("Realizar Pago")
        self.btn_pagar.setObjectName("pagar")
        self.btn_pagar.clicked.connect(self.realizar_pago)
        layout_principal.addSpacing(30)
        layout_principal.addWidget(self.btn_pagar, alignment=Qt.AlignCenter)

        # Llenar los campos con datos disponibles
        if self.cliente:
            self.cita_input.setText(str(self.id_cita or ""))
            self.nombre_input.setText(f"{self.cliente.get('nombre', '')} {self.cliente.get('apellido_paterno', '')} {self.cliente.get('apellido_materno', '')}")
            self.telefono_input.setText(self.cliente.get("telefono", ""))
            self.servicio_input.setText(self.cliente.get("detalle", ""))
            self.total_input.setText(f"${self.total_valor:.2f}")

            # Obtener nombre real del empleado desde la sesión
            id_usuario = SesionActual.id_usuario
            nombre_empleado = "Empleado asignado"
            if id_usuario:
                nombre_empleado = obtener_nombre_usuario_por_id(id_usuario) or nombre_empleado
            self.empleado_input.setText(nombre_empleado)

        # Hacer los campos no editables excepto método de pago
        for field in [self.cita_input, self.nombre_input, self.telefono_input, self.servicio_input, self.empleado_input, self.total_input]:
            field.setReadOnly(True)

        self.setLayout(layout_principal)



    def create_field_group(self, label_text, input_widget):
        group = QVBoxLayout()
        label = QLabel(label_text)
        label.setAlignment(Qt.AlignCenter)
        group.addWidget(label)
        group.addWidget(input_widget)
        return group

    def volver_a_home(self):
        from views.home import HomeWindow
        self.home_window = HomeWindow()
        self.home_window.show()
        self.close()


    def volver_a_resumen(self):
        from views.resumen_citas import ResumenCitasWindow
        self.resumen_window = ResumenCitasWindow()
        self.resumen_window.show()
        self.close()




    def calcular_total(self):
        total = self.cliente.get("precio", 0.0)
        for persona in self.servicios:
            total += persona.get("precio", 0.0)
        return total


    def realizar_pago(self):
        from models.pago import insertar_pago
        from PyQt5.QtWidgets import QMessageBox

        try:
            monto = float(self.total_input.text().replace("$", "").strip())
            id_cita_text = self.cita_input.text().strip()

            if not id_cita_text.isdigit():
                QMessageBox.warning(self, "Error", "ID de Cita inválido.")
                return

            id_cita = int(id_cita_text)

            # Obtener el ID real del método de pago desde el combobox
            id_metodo = self.metodo_pago.currentData()

            if id_metodo is None:
                QMessageBox.warning(self, "Error", "Método de pago no válido.")
                return

            exito = insertar_pago(monto, id_metodo, id_cita)

            if exito:
                QMessageBox.information(self, "Éxito", "Pago registrado correctamente.")
                self.volver_a_home()
            else:
                QMessageBox.critical(self, "Error", "No se pudo registrar el pago.")

        except Exception as e:
            print(f"❌ Error en realizar_pago(): {e}")
            QMessageBox.critical(self, "Error", "Ocurrió un error al procesar el pago.")
