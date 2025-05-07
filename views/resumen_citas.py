import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton,
    QVBoxLayout, QHBoxLayout, QFrame, QSizePolicy
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from views.generar_pago import GenerarPago
from models.pago import insertar_pago, obtener_id_metodo

class ResumenCitaWindow(QWidget):
    def __init__(self, cliente=None, servicios=None, regresar_callback=None):
        super().__init__()
        self.cliente = cliente
        self.servicios = servicios or []
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
                font-size: 14pt;
                color: #000;
            }
            QPushButton#pago {
                background-color: #231f20;
                color: #fcb3b3;
                padding: 10px 25px;
                font-size: 16pt;
                border-radius: 20px;
                font-weight: bold;
            }
            QPushButton#pago:hover {
                background-color: #333333;
            }
            QPushButton#regresar {
                background-color: transparent;
                border: none;
                color: black;
                font: bold 13pt 'Poppins';
                padding: 5px 10px;
            }
            QPushButton#regresar:hover {
                color: gray;
            }
        """)

        self.initUI()

    def initUI(self):
        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(80, 40, 80, 40)

        fila_superior = QHBoxLayout()
        self.btn_regresar = QPushButton("⤺ Regresar")
        self.btn_regresar.setObjectName("regresar")
        self.btn_regresar.clicked.connect(self.volver_a_agendar)
        fila_superior.addWidget(self.btn_regresar, alignment=Qt.AlignLeft)
        layout_principal.addLayout(fila_superior)

        ticket = QFrame()
        ticket.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 20px;
                padding: 30px;
            }
        """)
        ticket.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        ticket_layout = QVBoxLayout(ticket)
        ticket_layout.setSpacing(20)

        top_row = QHBoxLayout()
        logo = QLabel()
        pixmap = QPixmap("resources/logo_sinfondo.png").scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        logo.setPixmap(pixmap)
        logo.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        top_row.addWidget(logo, alignment=Qt.AlignLeft)

        header = QVBoxLayout()
        nombre_salon = QLabel("ATENAS DUARTE SALÓN Y MÁS")
        nombre_salon.setStyleSheet("font-size: 20pt; font-weight: bold;")

        cliente_nombre = f"{self.cliente.get('nombre', '')} {self.cliente.get('apellido_paterno', '')} {self.cliente.get('apellido_materno', '')}"
        cliente_telefono = self.cliente.get("telefono", "")
        num_cliente = QLabel(f"Cliente: {cliente_nombre}     Tel: {cliente_telefono}")
        header.addWidget(nombre_salon)
        header.addWidget(num_cliente)
        top_row.addLayout(header)
        ticket_layout.addLayout(top_row)

        def agregar_cliente(nombre, costo, servicio):
            fila1 = QHBoxLayout()
            cliente_lbl = QLabel("Cliente:")
            cliente_nombre = QLabel(nombre)
            fila1.addWidget(cliente_lbl)
            fila1.addWidget(cliente_nombre)
            fila1.addStretch()

            costo_lbl = QLabel("Costo:")
            costo_val = QLabel(f"${costo:.2f}")
            fila1.addWidget(costo_lbl)
            fila1.addWidget(costo_val)
            ticket_layout.addLayout(fila1)

            fila2 = QHBoxLayout()
            serv_lbl = QLabel("Servicio requerido:")
            serv_val = QLabel(servicio)
            fila2.addWidget(serv_lbl)
            fila2.addStretch()
            fila2.addWidget(serv_val)
            ticket_layout.addLayout(fila2)

        principal_nombre = f"{self.cliente.get('nombre', '')} {self.cliente.get('apellido_paterno', '')} {self.cliente.get('apellido_materno', '')}"
        principal_servicio = self.cliente.get("detalle", "")
        principal_costo = self.cliente.get("precio", 0.0)
        agregar_cliente(principal_nombre, principal_costo, principal_servicio)

        total = principal_costo
        for persona in self.servicios:
            nombre = f"{persona['nombre']} {persona['apellido_paterno']} {persona['apellido_materno']}"
            servicio = persona['detalle']
            costo = persona.get('precio', 0.0)
            total += costo
            agregar_cliente(nombre, costo, servicio)

        fecha = self.cliente.get("fecha", "N/A")
        hora = self.cliente.get("hora", "N/A")
        fecha_hora = QHBoxLayout()
        fecha_lbl = QLabel(f"Fecha: {fecha}")
        hora_lbl = QLabel(f"Hora: {hora}")
        fecha_hora.addWidget(fecha_lbl)
        fecha_hora.addStretch()
        fecha_hora.addWidget(hora_lbl)
        ticket_layout.addLayout(fecha_hora)

        total_layout = QHBoxLayout()
        total_label = QLabel("Total a pagar:")
        total_label.setStyleSheet("font-weight: bold; font-size: 16pt;")
        total_val = QLabel(f"${total:.2f}")
        total_val.setStyleSheet("font-weight: bold; font-size: 16pt;")
        total_layout.addWidget(total_label)
        total_layout.addStretch()
        total_layout.addWidget(total_val)
        ticket_layout.addLayout(total_layout)

        pago_btn = QPushButton("Realizar Pago")
        pago_btn.setObjectName("pago")
        pago_btn.clicked.connect(lambda: self.abrir_pago(total))
        ticket_layout.addStretch()
        ticket_layout.addWidget(pago_btn, alignment=Qt.AlignRight)

        layout_principal.addWidget(ticket, alignment=Qt.AlignCenter)

    def volver(self):
        self.close()
        if self.regresar_callback:
            self.regresar_callback()

    def abrir_pago(self, total):
        from models.cliente import insertar_cliente
        from models.cita import crear_cita

        # Insertar cliente y obtener ID
        id_cliente = insertar_cliente(
            self.cliente.get("nombre", ""),
            self.cliente.get("apellido_paterno", ""),
            self.cliente.get("apellido_materno", ""),
            self.cliente.get("telefono", "")
        )

        if not id_cliente:
            print("[ERROR] No se pudo insertar el cliente.")
            return

        # Crear cita con cliente recién insertado
        fecha = self.cliente.get("fecha")
        hora = self.cliente.get("hora")
        id_empleado = 1  # Puedes cambiar esto según el contexto

        id_cita = crear_cita(id_cliente, id_empleado, fecha, hora)

        if not id_cita:
            print("[ERROR] No se pudo crear la cita.")
            return

        # Guardar ID de cita en cliente y pasarla
        self.cliente["id_cita"] = id_cita

        self.pago_window = GenerarPago(
            cliente=self.cliente,
            total=total,
            id_cita=id_cita,
            regresar_callback=self.mostrar_resumen
        )
        self.pago_window.show()
        self.hide()






    def mostrar_resumen(self):
        self.show()
        self.raise_()
        self.activateWindow()
        self.showFullScreen()

    def volver_a_agendar(self):
        from views.agendar_cita import AgendarCitaWindow
        self.agendar_cita_window = AgendarCitaWindow()
        self.agendar_cita_window.show()
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = ResumenCitaWindow()
    ventana.show()
    sys.exit(app.exec_())
