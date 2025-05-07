from database.conexion import get_connection
import traceback

def verificar_credenciales(tipo_usuario: str, usuario: str, contrasena: str) -> bool:
    print("📥 Entrando a verificar_credenciales")

    try:
        conn = get_connection()
        print("🔗 Conexión establecida")
        cursor = conn.cursor()

        query = """
            SELECT e.Contraseña
            FROM Empleado e
            JOIN Rol r ON e.ID_Usuario = r.ID_Usuario
            WHERE e.NombreEmpleado = %s AND r.NombreRol = %s
        """
        print(f"📤 Ejecutando consulta con: {usuario}, {tipo_usuario}")
        cursor.execute(query, (usuario, tipo_usuario))
        resultado = cursor.fetchone()

        print("🔎 Resultado de consulta:", resultado)
        return resultado is not None and resultado["Contraseña"] == contrasena

    except Exception as e:
        print(f"[ERROR] En verificar_credenciales: {e}")
        traceback.print_exc()
        return False

    finally:
        print("🚪 Cerrando conexión")
        try:
            if cursor:
                cursor.close()
        except Exception as e:
            print(f"⚠️ Error al cerrar cursor: {e}")
        try:
            if conn:
                conn.close()
        except Exception as e:
            print(f"⚠️ Error al cerrar conexión: {e}")


def obtener_id_rol(nombre_rol):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        query = "SELECT ID_Usuario FROM rol WHERE NombreRol = %s"
        cursor.execute(query, (nombre_rol,))
        resultado = cursor.fetchone()
        return resultado["ID_Usuario"] if resultado else None
    except Exception as e:
        print(f"[ERROR] al obtener ID de rol: {e}")
        return None
    finally:
        cursor.close()
        conn.close()



def insertar_usuario(nombre, apellido_p, apellido_m, contrasena, id_usuario):
    try:
        print("🛠️ Entrando a insertar_usuario()")
        conn = get_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO empleado (NombreEmpleado, PrimerApellido, SegundoApellido, Contraseña, ID_Usuario)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (nombre, apellido_p, apellido_m, contrasena, id_usuario))
        conn.commit()
        return True
    except Exception as e:
        print(f"[ERROR] al insertar usuario: {e}")
        return False
    finally:
        cursor.close()
        conn.close()


