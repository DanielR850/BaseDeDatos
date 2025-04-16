###Pantalla de registro de pagos realizados###
import sys
from PyQt5.QtWidgets import (
    QApplication,QWidget,QLabel,
    QLineEdit,QPushButton,QVBoxLayout,
    QHBoxLayout, QTableWidget, QTableWidgetItem,
    QSpacerItem, QSizePolicy,QHeaderView,QMessageBox)
from PyQt5.QtGui import QFont, QPixmap, QIcon,QColor, QBrush
from PyQt5.QtCore import Qt,QSize 
from PyQt5 import QtGui

class RegistroPago(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Inventario")
        self.setGeometry(470,150,1000,800)
        self.setFixedSize(1000,800)
        self.setStyleSheet("""
                        background: qlineargradient(
                        x1: 0, y1: 0,
                        x2: 0, y2: 1,
                        stop: 0 #EBAAAA,    /* Rosa oscuro */
                        stop: 1 #EADAD3
                        );
                        """)
        main_layout = QVBoxLayout()
###Layout del titulo####
        titulo_layout=QHBoxLayout()
        titulo_label=QLabel("Registro de pagos")
        titulo_label.setStyleSheet("color:black; font-size:35px;font:bold; font-family:'roboto'; background-color:#EBAAAA;")
        titulo_label.setAlignment(Qt.AlignCenter)
        titulo_layout.addWidget(titulo_label)
####################################################################
###Layout de botones de Acción (Buscar y eliminar transacción por ID)###
        layout_botones = QHBoxLayout()
        boton_buscar=QPushButton("Buscar transacción")
        boton_buscar.setStyleSheet("""
            QPushButton {
                background-color: #D9FFCC;
                color: black;
                border-radius: 20px;
                padding: 12px 20px;
                font-size: 16px;
                font-weight: bold;
                border: none;
            }
            QPushButton:hover {
                background-color: lightblue;
            }
        """)

        boton_eliminar=QPushButton("Eliminar transacción")
        boton_eliminar.setStyleSheet("""
            QPushButton {
                background-color: #CF6978;
                color: black;
                border-radius: 20px;
                padding: 12px 20px;
                font-size: 16px;
                font-weight: bold;
                border: none;
            }
            QPushButton:hover {
                background-color: lightblue;
            }
        """)
        self.input_buscar = QLineEdit()
        self.input_buscar.setPlaceholderText("Ingrese el ID por buscar")
        self.input_buscar.setStyleSheet("background-color:white;font-size:20px;")
        self.input_buscar.setMaximumWidth(225)

        self.input_eliminar = QLineEdit()
        self.input_eliminar.setPlaceholderText("Ingrese el ID por eliminar")
        self.input_eliminar.setStyleSheet("background-color:white;font-size:20px;")
        self.input_eliminar.setMaximumWidth(240)

        layout_botones.addWidget(boton_buscar)
        layout_botones.addWidget(self.input_buscar)
        layout_botones.addWidget(boton_eliminar)
        layout_botones.addWidget(self.input_eliminar)


###Área de layouts###
        main_layout.addLayout(titulo_layout)        
        main_layout.addStretch(0)
        main_layout.setSpacing(10)
        main_layout.addLayout(layout_botones)
        main_layout.addStretch(32)
        main_layout.setSpacing(10)
        self.setLayout(main_layout)
        
####################################################################




if __name__=="__main__":
    from PyQt5.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    ventana= RegistroPago()
    ventana.show()
    sys.exit(app.exec_())