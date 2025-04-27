from PyQt5.QtWidgets import QApplication
import sys

# Importa aquí las ventanas que quieras probar
from views.login import LoginVentana
from views.registro import RegistroVentana
from views.home import HomeVentana

# Puedes importar más vistas según necesites

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Cambia el nombre de la ventana que quieras mostrar:
    ventana = LoginVentana()
    # ventana = RegistroVentana()
    # ventana = HomeVentana()

    ventana.show()
    sys.exit(app.exec_())
