import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QHeaderView
from PyQt5.QtGui import QFont

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Disponibilidad Citas")
        self.setGeometry(100, 100, 800, 600)  
        self.setStyleSheet("""background: qlineargradient(
                                                        x1: 0, y1: 0,
                                                        x2: 0, y2: 1,
                                                        stop: 0 pink,
                                                        stop: 1 white
                                                                    );""")
        self.initUI()

    def initUI(self):
        
        self.table_widget = QTableWidget()
        self.table_widget.setRowCount(6)  
        self.table_widget.setColumnCount(4)  
        self.table_widget.setHorizontalHeaderLabels(["Día", "Hora", "Cliente", "Trabajo Requerido"])
        self.table_widget.setFont(QFont("Arial", 12))  

        
        header = self.table_widget.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        self.table_widget.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

        
        citas = [
            ("", "", "", ""),  
            ("", "", "", ""), 
            ("", "", "", ""),  
            ("", "", "", ""),  
            ("", "", "", ""),  
            ("", "", "", ""),  
        ]

     
        for fila, (dia, hora, cliente, trabajo) in enumerate(citas):
            self.table_widget.setItem(fila, 0, QTableWidgetItem(dia))
            self.table_widget.setItem(fila, 1, QTableWidgetItem(hora))
            self.table_widget.setItem(fila, 2, QTableWidgetItem(cliente))
            self.table_widget.setItem(fila, 3, QTableWidgetItem(trabajo))

       
        layout = QVBoxLayout()
        layout.addWidget(self.table_widget)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())