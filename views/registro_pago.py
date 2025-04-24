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
####################################################################
###Layout de tabla de pagos registrados.###
        layout_tabla = QHBoxLayout()

        self.tabla_inventario = QTableWidget()
        self.tabla_inventario.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        self.tabla_inventario.setMinimumWidth(858)
        self.tabla_inventario.setMinimumHeight(500)


        self.tabla_inventario.setColumnCount(4)
        self.tabla_inventario.setRowCount(13)
        self.tabla_inventario.setHorizontalHeaderLabels(["Cliente","Monto","Método","Fecha"])
        self.tabla_inventario.horizontalHeader().setStyleSheet("""
        QHeaderView::section {
        background-color: #CF6978;
        color: black;
        font-weight: bold;
        font-size:27px;
        font:sans-serif;                                                     
        }
        """)
        self.tabla_inventario.verticalHeader().setStyleSheet("""
        QHeaderView::section {
        background-color: #CF6978;
        color: white;
        font-weight: bold;
        font-size: 20px;
        }
        """)
        self.tabla_inventario.setStyleSheet("""
QTableWidget {
    background-color: #F5F5DC;
    font-size: 15px;
    font: bold;
    font-family: 'sans-serif';
}
QHeaderView::section {
    background-color: #CF6978;
    color: black;
    font-weight: bold;
    font-size: 27px;
    font: sans-serif;
}
QTableCornerButton::section {
    background-color: #CF6978;
    border: 1px solid #999;
}
""")

        self.tabla_inventario.setColumnWidth(0, 200)  # Columna "Nombre"
        self.tabla_inventario.setColumnWidth(1, 200)  # Columna "Marca"
        self.tabla_inventario.setColumnWidth(2, 200)  # Columna "Precio"
        self.tabla_inventario.setColumnWidth(3, 200)  # Columna "Stock"


        layout_tabla.addStretch()
        layout_tabla.addWidget(self.tabla_inventario)
        layout_tabla.addStretch()
####################################################################
###Layout de logo y botón de regresar###

        layout_inferior = QHBoxLayout()


        boton_regresar=QPushButton("Regresar")
        boton_regresar.setIcon(QIcon('C:/Users/Lutec/OneDrive/Documentos/Diego Luna De Labra/6to semestre/Bases de datos/BaseDeDatos/BaseDeDatosSalonDeBelleza/resources/flecha_regresar.png'))
        boton_regresar.setIconSize(QSize(50,50))
        boton_regresar.resize(300,300)
        boton_regresar.setFixedSize(120, 70)  # Establece el tamaño fijo en 100x100 píxeles
        boton_regresar.setStyleSheet("""
                                    QPushButton {
                                    border: none;
                                    background-color: transparent;
                                    padding: 0px;
                                    font:bold; 
                                    font-size:15px;
                                    }
                                    QPushButton:pressed {
                                    background-color: transparent;
                                    }
                                    """)

        
    

        layout_inferior.addWidget(boton_regresar)
        layout_inferior.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        boton_logo=QPushButton("")
        boton_logo.setIcon(QIcon('C:/Users/Lutec/OneDrive/Documentos/Diego Luna De Labra/6to semestre/Bases de datos/BaseDeDatos/BaseDeDatosSalonDeBelleza/resources/logo_sinfondo.png'))
        boton_logo.setIconSize(QSize(70,70))
        boton_logo.setFixedSize(100,100)  # Establece el tamaño fijo en 100x100 píxeles
        boton_logo.setStyleSheet("""
                                    QPushButton {
                                    border: none;
                                    background-color: transparent;
                                    padding: 0px;
                                    }
                                    QPushButton:pressed {
                                    background-color: transparent;
                                    }
                                    """)
        
    

        layout_inferior.addWidget(boton_logo) 
####################################################################
###Área de layouts###
        main_layout.addLayout(titulo_layout)        
        main_layout.addStretch(0)
        main_layout.setSpacing(10)
        main_layout.addLayout(layout_botones)
        main_layout.addStretch(32)
        main_layout.setSpacing(10)
        main_layout.addLayout(layout_tabla)
        main_layout.addStretch(60)
        main_layout.addStretch(1)
        main_layout.addLayout(layout_inferior)
        self.setLayout(main_layout)
        
####################################################################




if __name__=="__main__":
    from PyQt5.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    ventana= RegistroPago()
    ventana.show()
    sys.exit(app.exec_())