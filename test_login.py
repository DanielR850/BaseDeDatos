import mysql.connector
import traceback

print("🌐 Intentando conectar con MySQL...")

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="daniel0812",
        database="bellezadb"
    )
    if conn.is_connected():
        print("✅ Conexión exitosa.")
        conn.close()
    else:
        print("❌ Conexión fallida sin excepción.")

except Exception as e:
    print("💥 Excepción capturada:")
    print(f"Tipo: {type(e).__name__} - {e}")
    traceback.print_exc()
