import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt

class PaymentScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Generar Pago')
        self.setGeometry(100, 100, 600, 400)
        self.setStyleSheet("""background: qlineargradient(
                                                        x1: 0, y1: 0,
                                                        x2: 0, y2: 1,
                                                        stop: 0 pink,
                                                        stop: 1 white
                                                                    );""")

        
        main_layout = QVBoxLayout()
        header_layout = QHBoxLayout()
        form_layout = QVBoxLayout()
        bottom_layout = QHBoxLayout()

        
        back_button = QPushButton('Regresar')
        back_button.setFont(QFont('Arial', 12))
        back_button.setStyleSheet("background-color: black; color: pink;")

        logo_label = QLabel()
        logo_label.setPixmap(QPixmap('logo.png'))  
        logo_label.setAlignment(Qt.AlignCenter)


        exit_button = QPushButton('Salir')
        exit_button.setFont(QFont('Arial', 12))
        exit_button.setStyleSheet("background-color: black; color: pink;")

    
        header_layout.addWidget(back_button)
        header_layout.addWidget(logo_label)
        header_layout.addWidget(exit_button)

        
        cita_label = QLabel('Cita')
        cita_label.setFont(QFont('Arial', 12))
        cita_input = QLineEdit()

        nombre_label = QLabel('Nombre')
        nombre_label.setFont(QFont('Arial', 12))
        nombre_input = QLineEdit()

        telefono_label = QLabel('Teléfono')
        telefono_label.setFont(QFont('Arial', 12))
        telefono_input = QLineEdit()

        servicio_label = QLabel('Servicio')
        servicio_label.setFont(QFont('Arial', 12))
        servicio_input = QLineEdit()

        empleado_label = QLabel('Empleado')
        empleado_label.setFont(QFont('Arial', 12))
        empleado_input = QLineEdit()

        form_layout.addWidget(cita_label)
        form_layout.addWidget(cita_input)
        form_layout.addWidget(nombre_label)
        form_layout.addWidget(nombre_input)
        form_layout.addWidget(telefono_label)
        form_layout.addWidget(telefono_input)
        form_layout.addWidget(servicio_label)
        form_layout.addWidget(servicio_input)
        form_layout.addWidget(empleado_label)
        form_layout.addWidget(empleado_input)

        
        realizar_pago_button = QPushButton('Realizar Pago')
        realizar_pago_button.setFont(QFont('Arial', 14))
        realizar_pago_button.setStyleSheet("background-color: black; color: pink;")

        bottom_layout.addStretch()
        bottom_layout.addWidget(realizar_pago_button)
        bottom_layout.addStretch()

        
        main_layout.addLayout(header_layout)
        main_layout.addLayout(form_layout)
        main_layout.addLayout(bottom_layout)

        self.setLayout(main_layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    screen = PaymentScreen()
    screen.show()
    sys.exit(app.exec_())