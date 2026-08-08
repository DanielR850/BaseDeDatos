from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QFrame,
    QSizePolicy, QApplication
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from views.generar_pago import GenerarPago
from models.cliente import insertar_cliente
from models.cita import crear_cita


class ResumenCitaWindow(QWidget):
    def __init__(self, cliente=None, servicios=None, regresar_callback=None):
        super().__init__()
        self.setWindowTitle("Resumen de Cita")
        self.setMinimumSize(1024, 1000)
        self.showMaximized()
        self.cliente = cliente or {}
        self.servicios = servicios or []
        self.regresar_callback = regresar_callback

        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                            stop: 0 #f8c8dc, stop: 1 #fefefe);
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
                padding: 15px 35px;
                font-size: 18pt;
                border-radius: 20px;
                font-weight: bold;
                min-width: 220px;
                min-height: 60px;
            }
            QPushButton#pago:hover {
                background-color: #333333;
            }
            QPushButton#regresar {
                background-color: transparent;
                border: none;
                color: #101111;
                font: bold 15pt 'Poppins';
                padding: 10px;
                min-width: 120px;
            }
            QPushButton#regresar:hover {
                color: gray;
            }
        """)

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(80, 40, 80, 40)
        layout.setSpacing(20)

        # --- Botón regresar totalmente a la izquierda ---
        top_bar = QHBoxLayout()
        self.btn_regresar = QPushButton("⤺ Regresar")
        self.btn_regresar.setObjectName("regresar")
        self.btn_regresar.clicked.connect(self.volver_a_agendar)
        top_bar.addWidget(self.btn_regresar, alignment=Qt.AlignLeft)
        layout.addLayout(top_bar)

        # --- Contenedor principal ---
        ticket = QFrame()
        ticket.setStyleSheet("background-color: white; border-radius: 20px; padding: 30px;")
        ticket.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        ticket_layout = QVBoxLayout(ticket)
        ticket_layout.setSpacing(20)

        # --- Header con logo y nombre del salón ---
        header = QHBoxLayout()
        logo = QLabel()
        pixmap = QPixmap("resources/logo_sinfondo.png")
        if not pixmap.isNull():
            logo.setPixmap(pixmap.scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        header.addWidget(logo)

        salon_label = QLabel("ATENAS DUARTE SALÓN Y MÁS")
        salon_label.setStyleSheet("font-size: 20pt; font-weight: bold;")
        info = QLabel(f"Cliente: {self.cliente.get('nombre', '')} {self.cliente.get('apellido_paterno', '')} {self.cliente.get('apellido_materno', '')}  Tel: {self.cliente.get('telefono', '')}")
        info_layout = QVBoxLayout()
        info_layout.addWidget(salon_label)
        info_layout.addWidget(info)
        header.addLayout(info_layout)
        ticket_layout.addLayout(header)

        # --- Servicios y precios ---
        total = self.cliente.get("precio", 0.0)

        def agregar_cliente(nombre, costo, servicio):
            fila1 = QHBoxLayout()
            fila1.addWidget(QLabel("Cliente:"))
            fila1.addWidget(QLabel(nombre))
            fila1.addStretch()
            fila1.addWidget(QLabel("Costo:"))
            fila1.addWidget(QLabel(f"${costo:.2f}"))
            ticket_layout.addLayout(fila1)

            fila2 = QHBoxLayout()
            fila2.addWidget(QLabel("Servicio requerido:"))
            fila2.addStretch()
            fila2.addWidget(QLabel(servicio))
            ticket_layout.addLayout(fila2)

        agregar_cliente(
            f"{self.cliente.get('nombre', '')} {self.cliente.get('apellido_paterno', '')} {self.cliente.get('apellido_materno', '')}",
            self.cliente.get("precio", 0.0),
            self.cliente.get("detalle", "")
        )

        for persona in self.servicios:
            agregar_cliente(
                f"{persona.get('nombre', '')} {persona.get('apellido_paterno', '')} {persona.get('apellido_materno', '')}",
                persona.get("precio", 0.0),
                persona.get("detalle", "")
            )
            total += persona.get("precio", 0.0)

        # --- Fecha y hora ---
        fecha = self.cliente.get("fecha", "N/A")
        hora = self.cliente.get("hora", "N/A")
        ticket_layout.addLayout(self.build_row("Fecha:", fecha, "Hora:", hora))

        # --- Total ---
        total_row = self.build_row("Total a pagar:", f"${total:.2f}")
        ticket_layout.addLayout(total_row)

        # --- Botón de pago ---
        btn_pago = QPushButton("Realizar Pago")
        btn_pago.setObjectName("pago")
        btn_pago.clicked.connect(lambda: self.abrir_pago(total))
        ticket_layout.addStretch()
        ticket_layout.addWidget(btn_pago, alignment=Qt.AlignRight)

        layout.addWidget(ticket, alignment=Qt.AlignCenter)

    def build_row(self, label1, value1, label2=None, value2=None):
        row = QHBoxLayout()
        row.addWidget(QLabel(label1))
        row.addWidget(QLabel(value1))
        row.addStretch()
        if label2 and value2:
            row.addWidget(QLabel(label2))
            row.addWidget(QLabel(value2))
        return row

    def abrir_pago(self, total):
        from models.session import SesionActual
        from models.empleado import obtener_id_empleado_por_usuario

        # 1. Obtener ID_Cliente
        id_cliente = insertar_cliente(
            self.cliente.get("nombre", ""),
            self.cliente.get("apellido_paterno", ""),
            self.cliente.get("apellido_materno", ""),
            self.cliente.get("telefono", "")
        )

        if not id_cliente:
            print("[ERROR] No se pudo insertar el cliente.")
            return

        # 2. Obtener ID_Empleado desde sesión actual
        id_usuario = SesionActual.id_usuario
        if not id_usuario:
            print("[ERROR] Sesión inválida: no hay usuario activo.")
            return

        id_empleado = obtener_id_empleado_por_usuario(id_usuario)
        if not id_empleado:
            print("[ERROR] No se encontró el empleado correspondiente.")
            return

        # 3. Crear la cita
        id_cita = crear_cita(id_cliente, id_empleado, self.cliente.get("fecha"), self.cliente.get("hora"))
        if not id_cita:
            print("[ERROR] No se pudo crear la cita.")
            return

        self.cliente["id_cita"] = id_cita

        # 4. Abrir ventana de pago
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
