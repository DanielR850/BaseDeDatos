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

###Área de layouts###
        main_layout.addLayout(titulo_layout)        
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addStretch(1)
        self.setLayout(main_layout)
        
####################################################################




if __name__=="__main__":
    from PyQt5.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    ventana= RegistroPago()
    ventana.show()
    sys.exit(app.exec_())