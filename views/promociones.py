import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QPushButton,
    QLabel, QVBoxLayout, QHBoxLayout, QTableWidget,
    QTableWidgetItem, QHeaderView, QLineEdit
)
from PyQt5.QtGui import QIcon, QColor, QPainter, QPen, QPixmap, QIcon 
from PyQt5.QtCore import Qt, QSize

class VentanaPromociones(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Promociones")
        self.setMinimumSize(900, 650)

        # Widget principal
        widget_principal = QWidget()
        widget_principal.setStyleSheet("""
            background: qlineargradient(
                x1: 0, y1: 0,
                x2: 0, y2: 1,
                stop: 0 #EBAAAA,    /* Rosa oscuro */
                stop: 1 #EADAD3
            );
        """)
        self.setCentralWidget(widget_principal)

        layout_principal = QVBoxLayout(widget_principal)
        layout_principal.setContentsMargins(30, 30, 30, 30)
        layout_principal.setSpacing(20)

        # --- Barra superior ---
        layout_superior = QHBoxLayout()
        boton_regresar = QPushButton()
        boton_regresar.setIcon(QIcon('c:/Users/agnav/OneDrive - Universidad Autonoma de Nuevo León/Desktop/Base de datos proyecto/BaseDeDatos/BaseDeDatosSalonDeBelleza/resources/flecha_regresar.png'))
        boton_regresar.setIconSize(QSize(40, 40))
        boton_regresar.setStyleSheet("border: none; background: transparent;")
        boton_regresar.clicked.connect(self.close)
        layout_superior.addWidget(boton_regresar)
        layout_superior.addStretch()
        layout_principal.addLayout(layout_superior)
        

        # Barra de búsqueda
        self.busqueda = QLineEdit()
        self.busqueda.setPlaceholderText("Buscar...")
        self.busqueda.setStyleSheet("""
            QLineEdit {
                background: white;
                border-radius: 15px;
                padding: 8px 35px 8px 15px;
                font: 14px 'Roboto';
                min-width: 250px;
            }
        """)
        

        layout_superior.addWidget(boton_regresar)
        layout_superior.addStretch(30)
        layout_superior.addWidget(self.busqueda)
        layout_principal.addLayout(layout_superior)

        # --- Título ---
        titulo = QLabel("Promociones")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("""
            font: bold 38px 'Roboto';
            color: black;
            padding: 15px;
            background: transparent;                 
        """)
        
        layout_principal.addWidget(titulo)

        
        layout_botones = QHBoxLayout()
        layout_botones.setSpacing(25)
        
        for texto, color in [
            ("Agregar promoción", "#c6fcb3"),
            ("Modificar promoción", "#fcfbb3"),
            ("Eliminar promoción", "#E57979")
        ]:
            boton = QPushButton(texto)
            boton.setStyleSheet(f"""
                QPushButton {{
                    background: {color};
                    border-radius: 25px;
                    padding: 15px 30px;
                    font: bold 18px;
                    color: black;
                    min-width: 200px;
                }}
                QPushButton:hover {{ 
                    background: {'#689F38' if color == "#c6fcb3" else 
                                '#FFB300' if color == "#fcfbb3" else 
                                '#C62828'};
                }}
            """)
            layout_botones.addWidget(boton)
        
        layout_principal.addLayout(layout_botones)

        # --- Tabla con nuevo estilo integrado ---
        self.tabla = QTableWidget(6,4)
        self.tabla.setColumnCount(4)
        self.tabla.setHorizontalHeaderLabels([
            "Descripción", "Servicios", "Precio", "Válido hasta"
        ])
        
        # Configuración de estilo de tabla
        self.tabla.setStyleSheet("""
            QTableWidget {
                background: #ffefe3;
                border-radius: 15px;
                padding: 10px;
                font: 16px 'Roboto';
                color: #4E342E;
            }
            QHeaderView::section {
                background: #D7CCC8;
                font: bold 18px;
                padding: 12px;
                border: none;
            }
            QTableWidget::item {
                border-bottom: 2px solid #D7CCC8;
                padding: 15px;
            }
        """)
        
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabla.verticalHeader().setVisible(False)
        self.tabla.setShowGrid(True) 

        layout_principal.addWidget(self.tabla)

        lbl_logo = QLabel()
        pixmap = QPixmap('c:/Users/agnav/OneDrive - Universidad Autonoma de Nuevo León/Desktop/Base de datos proyecto/BaseDeDatos/BaseDeDatosSalonDeBelleza/resources/logo_sinfondo.png').scaled(80,80, Qt.KeepAspectRatio)
        lbl_logo.setPixmap(pixmap)
        lbl_logo.setAlignment(Qt.AlignRight | Qt.AlignBottom)
        lbl_logo.setStyleSheet("padding: 0 10px 10px 0; background: transparent;")
        container = QWidget()
        layout_container = QVBoxLayout(container)
        layout_container.addWidget(self.tabla)
        layout_container.addWidget(lbl_logo, alignment=Qt.AlignRight | Qt.AlignBottom)
        layout_principal.addWidget(container)
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaPromociones()
    ventana.show()
    sys.exit(app.exec_())