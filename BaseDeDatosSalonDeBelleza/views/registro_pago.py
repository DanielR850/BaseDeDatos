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




if __name__=="__main__":
    from PyQt5.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    ventana= InventarioVentana()
    ventana.show()
    sys.exit(app.exec_())