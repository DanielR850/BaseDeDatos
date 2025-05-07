import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QComboBox, QDateEdit, QTimeEdit,
    QDialog
)
from PyQt5.QtCore import Qt, QDate, QTime
from models.cita import obtener_servicios_por_variante
from models.cita import crear_cita  # Asegúrate de importar esto arriba


class AgendarCitaWindow(QWidget):
    def __init__(self, regresar_callback=None):
        super().__init__()
        self.setWindowTitle("Agendar Cita")
        self.showFullScreen()
        self.regresar_callback = regresar_callback
        self.personas_agregadas = []  # ← Lista para guardar info de personas adicionales


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
                color: #000000;
            }
            QLineEdit, QComboBox, QDateEdit, QTimeEdit {
                background-color: #e5d3c5;
                border: 2px solid #000000;
                border-radius: 10px;
                padding: 6px;
                font-size: 14pt;
                min-height: 35px;
            }
            QPushButton {
                background-color: #fbeee6;
                border: 2px solid black;
                border-radius: 20px;
                font: bold 14pt 'Poppins';
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #fcd9c7;
            }
            QPushButton#regresar {
                background-color: transparent;
                border: none;
                color: #101111;
                font: bold 14pt 'Open Sans';
                padding: 10px;
                min-width: 100px;
            }
            QPushButton#regresar:hover {
                color: gray;
            }
        """)

        self.initUI()

    def initUI(self):

        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(50, 30, 50, 30)

        # Fila superior con botón Regresar
        fila_top = QHBoxLayout()
        self.btn_regresar = QPushButton("Regresar")
        self.btn_regresar.setObjectName("regresar")
        self.btn_regresar.clicked.connect(self.volver_a_home)
        fila_top.addWidget(self.btn_regresar, alignment=Qt.AlignLeft)
        fila_top.addStretch()
        layout.addLayout(fila_top)

        # Título
        titulo = QLabel("Agendar Cita")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-size: 20pt; font-weight: bold;")
        layout.addWidget(titulo)

        # Renglón 1: Nombre y apellidos
        fila1 = QHBoxLayout()
        self.nombre = QLineEdit()
        self.apellido_paterno = QLineEdit()
        self.apellido_materno = QLineEdit()
        fila1.addLayout(self.build_widget_group("Nombre", self.nombre))
        fila1.addLayout(self.build_widget_group("Apellido Paterno", self.apellido_paterno))
        fila1.addLayout(self.build_widget_group("Apellido Materno", self.apellido_materno))
        layout.addLayout(fila1)

        # Renglón 2: Teléfono, Servicio, Detalle
        fila2 = QHBoxLayout()
        self.telefono = QLineEdit()
        self.telefono.setFixedWidth(200)

        self.servicio = QComboBox()
        self.detalle = QComboBox()

        # Obtener servicios desde BD
        self.servicios_por_variante = obtener_servicios_por_variante()

        self.servicio.addItem("Seleccionar servicio")
        for categoria in self.servicios_por_variante:
            self.servicio.addItem(categoria)

        self.detalle.addItem("Seleccionar detalle")

        # Conectar el cambio de categoría a la función de actualización
        self.servicio.currentIndexChanged.connect(self.actualizar_detalles_por_categoria)

        fila2.addLayout(self.build_widget_group("Teléfono", self.telefono))
        fila2.addLayout(self.build_widget_group("Servicio", self.servicio))
        fila2.addLayout(self.build_widget_group("Detalle", self.detalle))
        layout.addLayout(fila2)

        # Renglón 3: Fecha, Hora, Botón Agendar
        fila3 = QHBoxLayout()
        self.fecha = QDateEdit()
        self.fecha.setCalendarPopup(True)
        self.fecha.setDate(QDate.currentDate())
        self.hora = QTimeEdit()
        self.hora.setTime(QTime.currentTime())
        self.btn_agendar = QPushButton("Agendar")
        self.btn_agendar.clicked.connect(self.agendar_cita_individual)
        fila3.addLayout(self.build_widget_group("Fecha", self.fecha))
        fila3.addLayout(self.build_widget_group("Hora", self.hora))
        fila3.addWidget(self.btn_agendar)
        layout.addLayout(fila3)

        # Renglón 4: Botón Agregar Persona
        fila4 = QHBoxLayout()
        fila4.addStretch()
        self.btn_agregar_persona = QPushButton("Agregar Persona")
        self.btn_agregar_persona.clicked.connect(self.mostrar_overlay_agregar_persona)
        fila4.addWidget(self.btn_agregar_persona)
        fila4.addStretch()
        layout.addLayout(fila4)

        self.setLayout(layout)


    def build_widget_group(self, label_text, widget):
        group = QVBoxLayout()
        group.setSpacing(1)  # Espaciado aún más reducido
        label = QLabel(label_text)
        label.setAlignment(Qt.AlignCenter)
        group.addWidget(label)
        group.addWidget(widget)
        return group

    def mostrar_overlay_agregar_persona(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Agregar Personas")
        dialog.setFixedSize(800, 300)
        dialog.setStyleSheet("""
            QWidget {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #f8c8dc,
                    stop: 1 #fefefe
                );
                font-family: 'Poppins';
            }
            QLabel {
                font-size: 16pt;
                font-weight: bold;
                color: #000;
                background-color: transparent;
            }
            QLineEdit {
                background-color: #e5d3c5;
                border: 2px solid #000;
                border-radius: 10px;
                font-size: 14pt;
                padding: 10px;
            }
            QPushButton {
                font: bold 14pt 'Poppins';
                padding: 8px 20px;
                border-radius: 15px;
                background-color: #fbeee6;
                border: 2px solid black;
            }
            QPushButton:hover {
                background-color: #fcd9c7;
            }
        """)

        layout = QVBoxLayout(dialog)

        label = QLabel("¿Cuántas personas deseas agendar?")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        cantidad_input = QLineEdit()
        cantidad_input.setPlaceholderText("Ej: 2")
        layout.addWidget(cantidad_input)

        botones = QHBoxLayout()
        btn_regresar = QPushButton("Regresar")
        btn_agendar = QPushButton("Agendar")
        btn_regresar.clicked.connect(dialog.reject)
        btn_agendar.clicked.connect(lambda: self.mostrar_formularios_por_persona(dialog, cantidad_input.text()))

        botones.addWidget(btn_regresar, alignment=Qt.AlignLeft)
        botones.addStretch()
        botones.addWidget(btn_agendar, alignment=Qt.AlignRight)

        layout.addStretch()
        layout.addLayout(botones)
        dialog.exec_()

    def mostrar_formularios_por_persona(self, parent_dialog, cantidad_texto):
        try:
            cantidad = int(cantidad_texto)
            if cantidad <= 0:
                raise ValueError
        except ValueError:
            error = QDialog(self)
            error.setWindowTitle("Error")
            layout = QVBoxLayout(error)
            msg = QLabel("Por favor, introduce un número válido mayor a 0.")
            layout.addWidget(msg)
            ok = QPushButton("OK")
            ok.clicked.connect(error.accept)
            layout.addWidget(ok, alignment=Qt.AlignCenter)
            error.exec_()
            return
        self.total_personas = cantidad           # ← NUEVO
        self.contador_personas = 0   
        parent_dialog.accept()  # Cierra la primera overlay

        for i in range(cantidad):
            self.abrir_formulario_individual(i + 1)
            
    def abrir_formulario_individual(self, numero):
        dialog = QDialog(self)
        dialog.setWindowTitle(f"Persona {numero}")
        dialog.setFixedSize(700, 450)
        dialog.setStyleSheet("""
            QWidget {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #f8c8dc,
                    stop: 1 #fefefe
                );
                font-family: 'Poppins';
            }
            QLabel {
                font-size: 14pt;
                color: #000;
                background-color: transparent;
            }
            QLineEdit, QComboBox {
                background-color: #e5d3c5;
                border: 2px solid #000;
                border-radius: 10px;
                font-size: 13pt;
                padding: 6px;
                min-height: 35px;
            }
            QPushButton {
                font: bold 14pt 'Poppins';
                padding: 8px 20px;
                border-radius: 15px;
                background-color: #fbeee6;
                border: 2px solid black;
            }
            QPushButton:hover {
                background-color: #fcd9c7;
            }
        """)

        layout = QVBoxLayout(dialog)

        titulo = QLabel(f"Ingresar datos de la persona {numero}")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-size: 18pt; font-weight: bold;")
        layout.addWidget(titulo)

        nombre = QLineEdit()
        ap_paterno = QLineEdit()
        ap_materno = QLineEdit()
        servicio = QComboBox()
        servicio.addItems(["Uñas", "Pelo", "Masaje"])
        detalle = QComboBox()
        detalle.addItems(["Uñas verdes", "Uñas rojas", "Corte", "Tinte"])

        fila1 = QHBoxLayout()
        fila1.addLayout(self.formulario_grupo("Nombre", nombre))
        fila1.addLayout(self.formulario_grupo("Apellido Paterno", ap_paterno))
        fila1.addLayout(self.formulario_grupo("Apellido Materno", ap_materno))
        layout.addLayout(fila1)

        fila2 = QHBoxLayout()
        fila2.addLayout(self.formulario_grupo("Servicio", servicio))
        fila2.addLayout(self.formulario_grupo("Detalle", detalle))
        layout.addLayout(fila2)

        layout.addStretch()

        btn_guardar = QPushButton("Guardar Persona")
        btn_guardar.clicked.connect(lambda: self.guardar_persona_y_continuar(
            dialog,
            nombre.text(),
            ap_paterno.text(),
            ap_materno.text(),
            servicio.currentText(),
            detalle.currentText()
        ))

        layout.addWidget(btn_guardar, alignment=Qt.AlignCenter)


        dialog.exec_()


    def formulario_grupo(self, texto, widget):
        vbox = QVBoxLayout()
        label = QLabel(texto)
        label.setAlignment(Qt.AlignLeft)
        vbox.addWidget(label)
        vbox.addWidget(widget)
        return vbox



    def volver_a_home(self):
        self.close()
        if self.regresar_callback:
            self.regresar_callback()

    def guardar_persona_y_continuar(self, dialog, nombre, ap_paterno, ap_materno, servicio, detalle):
        self.personas_agregadas.append({
            "nombre": nombre,
            "apellido_paterno": ap_paterno,
            "apellido_materno": ap_materno,
            "detalle": detalle,
            "precio": self.obtener_precio(servicio, detalle)
        })

        dialog.accept()
        self.contador_personas += 1

        if self.contador_personas >= self.total_personas:
            self.abrir_resumen_cita()
        else:
            self.abrir_formulario_individual(self.contador_personas + 1)






    def abrir_resumen_cita(self):
        from views.resumen_citas import ResumenCitaWindow

        cliente = self.obtener_datos_cliente_principal()

        # ✅ Paso 1: Crear cita real en la base de datos (cliente principal)
        id_cliente = 1  # 🔁 Reemplaza con el ID correcto si ya lo tienes
        id_empleado = 1  # 🔁 Reemplaza si estás manejando empleados por login
        fecha = cliente["fecha"]
        hora = cliente["hora"]
        
        id_cita = crear_cita(id_cliente, id_empleado, fecha, hora)
        cliente["id_cita"] = id_cita  # ✅ Este es el dato importante

        # ✅ También podrías agregar servicios con agregar_servicio_a_cita si quieres

        self.resumen_window = ResumenCitaWindow(
            cliente=cliente,
            servicios=self.personas_agregadas,
            regresar_callback=self.mostrar
        )
        self.resumen_window.show()
        self.hide()



    def actualizar_detalles_por_categoria(self):
        categoria = self.servicio.currentText()
        self.detalle.clear()

        if categoria in self.servicios_por_variante:
            self.detalle.addItem("Seleccionar detalle")
            for servicio in self.servicios_por_variante[categoria]:
                self.detalle.addItem(servicio["nombre"])
        else:
            self.detalle.addItem("Seleccionar detalle")

    def obtener_datos_cliente_principal(self):
        # Buscar el servicio seleccionado para obtener su precio
        categoria = self.servicio.currentText()
        detalle = self.detalle.currentText()
        precio = 0.0

        if categoria in self.servicios_por_variante:
            for servicio in self.servicios_por_variante[categoria]:
                if servicio["nombre"] == detalle:
                    precio = servicio.get("precio", 0.0)
                    break

        return {
            "nombre": self.nombre.text().strip(),
            "apellido_paterno": self.apellido_paterno.text().strip(),
            "apellido_materno": self.apellido_materno.text().strip(),
            "telefono": self.telefono.text().strip(),
            "fecha": self.fecha.date().toString("yyyy-MM-dd"),
            "hora": self.hora.time().toString("HH:mm"),
            "servicio": categoria,
            "detalle": detalle,
            "precio": precio  # ← Aquí se asigna el precio correcto
        }



    def agendar_cita_individual(self):
        cliente = self.obtener_datos_cliente_principal()

        if not all([cliente["nombre"], cliente["apellido_paterno"], cliente["telefono"]]) or cliente["servicio"] == "Seleccionar servicio":
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.warning(self, "Campos incompletos", "Por favor completa todos los campos obligatorios.")
            return

        # 🔥 CORREGIDO: NO agregues el cliente principal a personas_agregadas
        self.abrir_resumen_cita()



    def mostrar(self):
        self.show()
        self.raise_()
        self.activateWindow()
        self.showFullScreen()
