###Pantalla de inventario###
import sys
from PyQt5.QtWidgets import (
    QApplication,QWidget,QLabel,
    QLineEdit,QPushButton,QVBoxLayout,QHBoxLayout, QTableWidget, QTableWidgetItem,QSpacerItem, QSizePolicy)
from PyQt5.QtGui import QFont, QPixmap, QIcon
from PyQt5.QtCore import Qt,QSize 
from PyQt5 import QtGui

class InventarioVentana(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Inventario")
        self.setGeometry(470,150,1000,800)
        self.setStyleSheet("""background: qlineargradient(
                                                        x1: 0, y1: 0,
                                                        x2: 0, y2: 1,
                                                        stop: 0 pink,
                                                        stop: 1 white
                                                                    );""")
        self.setWindowIcon(QIcon("resources/logoBD.jpg"))
        
        main_layout = QVBoxLayout()
###Layout del titulo####
        titulo_acciones_layout=QHBoxLayout()
        titulo_label=QLabel("Inventario")
        titulo_label.setStyleSheet("color:black; font-size:30px;font:bold")
        titulo_label.setAlignment(Qt.AlignCenter)
        titulo_acciones_layout.addWidget(titulo_label)
####################################################################
###Layout de los botones y modificacion visual de los botones###
        top_buttons_layout=QHBoxLayout()
        button_add = QPushButton("Agregar Producto")
        button_modificar = QPushButton("Modificar Producto")
        button_delete = QPushButton("Eliminar Producto")
        button_add.setStyleSheet("""
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
        button_modificar.setStyleSheet("""
            QPushButton {
                background-color: #FFF7AE;
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

        button_delete.setStyleSheet("""
            QPushButton {
                background-color: #F18D8D;
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


        top_buttons_layout.addWidget(button_add)
        top_buttons_layout.addWidget(button_modificar)
        top_buttons_layout.addWidget(button_delete)
####################################################################
###Layout de busqueda de items###
        layout_busqueda = QHBoxLayout()
        layout_busqueda.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)) ##PARA EMPUJAR HACIA LA DERECHA
        input_busqueda=QLineEdit()
        input_busqueda.setStyleSheet("background-color:white;font-size:20px;")
        input_busqueda.setFixedWidth(500)
        input_busqueda.setPlaceholderText("Ingrese el id (1,2,3,..) del producto que desea buscar")
        input_busqueda.setAlignment(Qt.AlignLeft)

        boton_buscar=QPushButton("")
        boton_buscar.setIcon(QIcon('C:/Users/Lutec/OneDrive/Documentos/Diego Luna De Labra/6to semestre/Bases de datos/BaseDeDatos/BaseDeDatosSalonDeBelleza/resources/lupa_sinfondo.png'))
        boton_buscar.setIconSize(QSize(50,50))
        boton_buscar.setFixedSize(30, 30)  # Establece el tamaño fijo en 100x100 píxeles
        boton_buscar.setStyleSheet("""
                                    QPushButton {
                                    border: none;
                                    background-color: transparent;
                                    padding: 0px;
                                    }
                                    QPushButton:pressed {
                                    background-color: transparent;
                                    }
                                    """)
        layout_busqueda.addWidget(boton_buscar)

        layout_busqueda.addWidget(input_busqueda)
        


####################################################################
        main_layout.addLayout(titulo_acciones_layout)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        main_layout.addLayout(top_buttons_layout)
        main_layout.addSpacing(10)
        main_layout.addLayout(layout_busqueda)
        main_layout.addStretch(0)
        self.setLayout(main_layout)



if __name__=="__main__":
    from PyQt5.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    ventana= InventarioVentana()
    ventana.show()
    sys.exit(app.exec_())