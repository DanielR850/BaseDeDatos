###Pantalla de inventario###
import sys
from PyQt5.QtWidgets import (
    QApplication,QWidget,QLabel,
    QLineEdit,QPushButton,QVBoxLayout,
    QHBoxLayout, QTableWidget, QTableWidgetItem,
    QSpacerItem, QSizePolicy,QHeaderView,QMessageBox)
from PyQt5.QtGui import QFont, QPixmap, QIcon,QColor, QBrush
from PyQt5.QtCore import Qt,QSize 
from PyQt5 import QtGui

class InventarioVentana(QWidget):
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

        self.setWindowIcon(QIcon("resources/logoBD.jpg"))
        
        main_layout = QVBoxLayout()
###Layout del titulo####
        titulo_acciones_layout=QHBoxLayout()
        titulo_label=QLabel("Inventario")
        titulo_label.setStyleSheet("color:black; font-size:35px;font:bold; background-color:#EBAAAA; font-family:'roboto';")
        titulo_label.setAlignment(Qt.AlignCenter)
        titulo_acciones_layout.addWidget(titulo_label)
####################################################################
###Layout de los botones y modificacion visual de los botones###
        top_buttons_layout=QHBoxLayout()
        button_add = QPushButton("Agregar Producto")
        button_add.clicked.connect(self.agregar_info_tabla)
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


        top_buttons_layout.addWidget(button_add)
        top_buttons_layout.addWidget(button_modificar)
        top_buttons_layout.addWidget(button_delete)
####################################################################
###Layout de busqueda de items###
        layout_busqueda = QHBoxLayout()
        layout_busqueda.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)) ##PARA EMPUJAR HACIA LA DERECHA
        self.input_busqueda=QLineEdit()
        self.input_busqueda.setStyleSheet("background-color:white;font-size:20px;")
        self.input_busqueda.setFixedWidth(350)
        self.input_busqueda.setPlaceholderText("Buscar por ID")
        self.input_busqueda.setAlignment(Qt.AlignLeft)

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
        boton_buscar.clicked.connect(self.buscar_producto)
        layout_busqueda.addWidget(boton_buscar)

        layout_busqueda.addWidget(self.input_busqueda)
####################################################################
###Layout de la tabla de inventario###

        layout_tabla = QHBoxLayout()

        self.tabla_inventario = QTableWidget()
        self.tabla_inventario.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        self.tabla_inventario.setMinimumWidth(824)
        self.tabla_inventario.setMinimumHeight(500)


        self.tabla_inventario.setColumnCount(4)
        self.tabla_inventario.setHorizontalHeaderLabels(["Nombre","Marca","Precio","Stock"])
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
        self.tabla_inventario.setStyleSheet("font-size:15px; font:bold; font-family:'sans-serif';")
        self.tabla_inventario.setStyleSheet("""
QTableCornerButton::section {
    background-color: #CF6978;
    border: 1px solid #999;
}""")
        self.tabla_inventario.setColumnWidth(0, 200)  # Columna "Nombre"
        self.tabla_inventario.setColumnWidth(1, 200)  # Columna "Marca"
        self.tabla_inventario.setColumnWidth(2, 200)  # Columna "Precio"
        self.tabla_inventario.setColumnWidth(3, 200)  # Columna "Stock"


        layout_tabla.addStretch()
        layout_tabla.addWidget(self.tabla_inventario)
        layout_tabla.addStretch()
###Layout de logo e imagenes de acciones (Regresar, salir, etc.)###

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
        boton_regresar.clicked.connect(self.regresar)
        
    

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
        boton_logo.clicked.connect(self.info)
        
    

        layout_inferior.addWidget(boton_logo)      




####################################################################
###agregar layouts###
        main_layout.addLayout(titulo_acciones_layout)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(10)
        main_layout.addLayout(top_buttons_layout)
        main_layout.addSpacing(15)
        main_layout.addLayout(layout_busqueda)
        main_layout.addStretch(0)
        main_layout.addSpacing(15)
        main_layout.addLayout(layout_tabla)
        main_layout.addStretch(1)
        main_layout.addLayout(layout_inferior)

        self.setLayout(main_layout)
####################################################################
###APARTADO DE FUNCIONES NECESARIAS PARA EL FUNCIONAMIENTO DE LA PANTALLA###
    def buscar_producto(self):
        #########Se pondrá la funcion para realizar busquedas por medio del id#########
        id_busqueda = self.input_busqueda.text()
        print(f"Se realizó una busqueda del articulo con el id {id_busqueda}")
    
    def agregar_info_tabla(self):
        #########Aquí se debe modificar la función, permitiendonos agregar productos a la base de datos y de igual forma a la tabla#########
        fila=self.tabla_inventario.rowCount()
        self.tabla_inventario.insertRow(fila)
        self.tabla_inventario.setItem(fila, 0, QTableWidgetItem(f"Ejemplo"))
        self.tabla_inventario.setItem(fila, 1, QTableWidgetItem(f""))
        self.tabla_inventario.setItem(fila, 2, QTableWidgetItem(f""))
        self.tabla_inventario.setItem(fila, 3, QTableWidgetItem(f""))
            
        datos = ["Ejemplo", " ", "", ""]
        color_beige = QBrush(QColor("#F5F5DC"))  # Beige

        for columna, texto in enumerate(datos):
             item = QTableWidgetItem(texto)
             item.setBackground(color_beige)
             self.tabla_inventario.setItem(fila, columna, item)

    def eliminar_producto(self):
        #########Modificar funcion para que por medio del ID nos permita eliminar un producto#########
        print("Producto eliminado")
    def modificar_producto(self):
        #########Se deberá modificar la función para que nos permita modificar un producto por medio de su ID#########
        print("Producto modificado")
    
    def regresar(self):
        ###En esta función se pondrá la función para regresar a la pantalla principal###
        print("Has regresado a la pantalla anterior")
    
    def info(self):
          ###Modificar mensaje de acerca de...###
          QMessageBox.information(self, "Información", "Este sistema fue hecho por el equipo 1 de bases de datos de la FIME")
    
    def eliminar_producto(self):
        #########Modificar funcion para que por medio del ID nos permita eliminar un producto#########
        print("Producto eliminado")
    def modificar_producto(self):
        #########Se deberá modificar la función para que nos permita modificar un producto por medio de su ID#########
        print("Producto modificado")

####################################################################



if __name__=="__main__":
    from PyQt5.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    ventana= InventarioVentana()
    ventana.show()
    sys.exit(app.exec_())