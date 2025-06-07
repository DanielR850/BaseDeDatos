from database.conexion import get_connection
from pymysql.cursors import DictCursor  # Asegúrate de importar esto

def obtener_id_empleado_por_usuario(id_usuario):
    try:
        conn = get_connection()
        cursor = conn.cursor(DictCursor)  # ✅ Usamos DictCursor
        query = "SELECT ID_Empleado FROM Empleado WHERE ID_Usuario = %s"
        cursor.execute(query, (id_usuario,))
        resultado = cursor.fetchone()
        if resultado:
            print(f"🔍 ID_Empleado encontrado: {resultado['ID_Empleado']}")
            return resultado['ID_Empleado']
        else:
            print("⚠️ No se encontró ID_Empleado para el ID_Usuario proporcionado.")
            return None
    except Exception as e:
        print(f"❌ Error en obtener_id_empleado_por_usuario: {e}")
        return None
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals() and conn.open:
            conn.close()