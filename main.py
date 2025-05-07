# main.py
import sys
import traceback
import ctypes

def excepthook(exc_type, exc_value, exc_tb):
    error_msg = f"{exc_type.__name__}: {exc_value}"
    tb_str = ''.join(traceback.format_tb(exc_tb))
    full_msg = f"{error_msg}\n\n{tb_str}"
    
    print("💥 Excepción no detectada:")
    print(full_msg)

    # Mostrar en ventana emergente
    ctypes.windll.user32.MessageBoxW(0, full_msg, "Error Crítico", 0)
    sys.exit(1)
    
sys.excepthook = excepthook

print("🟢 Iniciando main.py")

try:
    from views.login import LoginWindow
    print("✅ LoginWindow importado correctamente")
except Exception as e:
    print("❌ Error al importar LoginWindow:", e)
    traceback.print_exc()
    input("Presiona Enter para salir...")
    sys.exit(1)

from PyQt5.QtWidgets import QApplication

if __name__ == "__main__":
    print("🚀 Lanzando QApplication")
    app = QApplication(sys.argv)
    ventana = LoginWindow()
    ventana.show()
    print("🪟 LoginWindow mostrada")
    sys.exit(app.exec_())
