import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QComboBox
)
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt


class GenerarPago(QWidget):
    def __init__(self, cliente=None, total=0.0, id_cita=None, regresar_callback=None):
        super().__init__()
        self.cliente = cliente or {}
        self.total_valor = total
        self.id_cita = id_cita
        self.regresar_callback = regresar_callback



        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 0, y2: 1,
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
        from models.pago import obtener_metodos_pago  # ⬅️ Importar dentro por claridad

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

        # Primera fila: 3 campos
        fila1 = QHBoxLayout()
        fila1.setSpacing(50)
        self.cita_input = QLineEdit()
        self.nombre_input = QLineEdit()
        self.telefono_input = QLineEdit()

        vbox_cita = self.create_field_group("ID Cita", self.cita_input)
        vbox_nombre = self.create_field_group("Nombre", self.nombre_input)
        vbox_telefono = self.create_field_group("Teléfono", self.telefono_input)

        fila1.addLayout(vbox_cita)
        fila1.addLayout(vbox_nombre)
        fila1.addLayout(vbox_telefono)

        # Segunda fila: 3 campos
        fila2 = QHBoxLayout()
        fila2.setSpacing(50)
        self.servicio_input = QLineEdit()
        self.empleado_input = QLineEdit()
        self.metodo_pago = QComboBox()

        # Obtener métodos de pago desde la base de datos
        self.metodos_pago_data = obtener_metodos_pago()
        for metodo in self.metodos_pago_data:
            self.metodo_pago.addItem(metodo["nombre"], metodo["id"])

        vbox_servicio = self.create_field_group("Servicio", self.servicio_input)
        vbox_empleado = self.create_field_group("Empleado", self.empleado_input)
        vbox_pago = self.create_field_group("Método de Pago", self.metodo_pago)

        fila2.addLayout(vbox_servicio)
        fila2.addLayout(vbox_empleado)
        fila2.addLayout(vbox_pago)

        # Tercera fila: Total
        fila3 = QHBoxLayout()
        fila3.setSpacing(50)
        self.total_input = QLineEdit()
        self.total_input.setReadOnly(True)
        vbox_total = self.create_field_group("Total a Pagar", self.total_input)
        fila3.addStretch()
        fila3.addLayout(vbox_total)
        fila3.addStretch()

        campos_centrados.addLayout(fila1)
        campos_centrados.addSpacing(30)
        campos_centrados.addLayout(fila2)
        campos_centrados.addSpacing(30)
        campos_centrados.addLayout(fila3)

        layout_principal.addLayout(campos_centrados)

        # Botón Pagar
        self.btn_pagar = QPushButton("Realizar Pago")
        self.btn_pagar.setObjectName("pagar")
        self.btn_pagar.clicked.connect(self.realizar_pago)
        layout_principal.addSpacing(30)
        layout_principal.addWidget(self.btn_pagar, alignment=Qt.AlignCenter)

        # Llenar datos si están disponibles
        if self.cliente:
            self.cita_input.setText(str(self.id_cita) if self.id_cita else "")
            self.nombre_input.setText(f"{self.cliente.get('nombre', '')} {self.cliente.get('apellido_paterno', '')} {self.cliente.get('apellido_materno', '')}")
            self.telefono_input.setText(self.cliente.get("telefono", ""))
            self.servicio_input.setText(self.cliente.get("detalle", ""))
            self.empleado_input.setText("Empleado asignado")  # Se puede personalizar si hay sesión
            self.total_input.setText(f"${self.total_valor:.2f}")

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
