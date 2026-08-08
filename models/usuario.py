from database.conexion import get_connection
import traceback
import bcrypt
from pymysql.cursors import DictCursor


def verificar_credenciales(tipo_usuario: str, nombre_usuario: str, contrasena: str) -> int | None:
    """
    Verifica si las credenciales son válidas.
    Si son correctas, devuelve el ID_Usuario. Si no, devuelve None.
    """
    try:
        conn = get_connection()
        cursor = conn.cursor(DictCursor)

        query = """
            SELECT e.ID_Usuario, e.Contraseña
            FROM Empleado e
            JOIN Rol r ON e.ID_Usuario = r.ID_Usuario
            WHERE e.NombreUsuario = %s AND r.NombreRol = %s
        """
        cursor.execute(query, (nombre_usuario, tipo_usuario))
        resultado = cursor.fetchone()

        if resultado:
            contrasena_encriptada = resultado["Contraseña"].encode("utf-8")
            if bcrypt.checkpw(contrasena.encode("utf-8"), contrasena_encriptada):
                return resultado["ID_Usuario"]
        return None

    except Exception as e:
        print(f"[ERROR] verificar_credenciales: {e}")
        traceback.print_exc()
        return None

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals() and conn.open:
            conn.close()


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



def insertar_usuario(nombre, apellido_p, apellido_m, nombre_usuario, contrasena, id_usuario):
    try:
        print("🛠️ Entrando a insertar_usuario()")

        conn = get_connection()
        cursor = conn.cursor()

        # Validar que el nombre de usuario no exista ya
        cursor.execute("SELECT COUNT(*) as total FROM Empleado WHERE NombreUsuario = %s", (nombre_usuario,))
        resultado = cursor.fetchone()
        existe = resultado["total"] if resultado else 0


        if existe:
            print(f"⚠️ Usuario '{nombre_usuario}' ya existe.")
            return False  # Usuario duplicado

        # Insertar nuevo empleado con el campo NombreUsuario
        query = """
            INSERT INTO Empleado (
                NombreEmpleado, PrimerApellido, SegundoApellido, Contraseña, ID_Usuario, NombreUsuario
            ) VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (nombre, apellido_p, apellido_m, contrasena, id_usuario, nombre_usuario))
        conn.commit()
        print("✅ Usuario registrado correctamente.")
        return True

    except Exception as e:
        print(f"[ERROR] al insertar usuario: {e}")
        traceback.print_exc()
        return False

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals() and conn.open:
            conn.close()

def obtener_nombre_usuario_por_id(id_usuario):
    try:
        print(f"🛠️ Buscando nombre de usuario para ID_Usuario: {id_usuario}")
        conn = get_connection()
        cursor = conn.cursor(DictCursor)  # ⚠️ Usa DictCursor para acceder por nombre

        query = "SELECT NombreUsuario FROM Empleado WHERE ID_Usuario = %s"
        cursor.execute(query, (id_usuario,))
        resultado = cursor.fetchone()

        if resultado:
            nombre = resultado["NombreUsuario"]
            print(f"✅ Nombre de usuario encontrado: {nombre}")
            return nombre

        print("⚠️ No se encontró el usuario.")
        return None

    except Exception as e:
        print(f"❌ Error al obtener nombre de usuario: {e}")
        return None

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals() and conn.open:
            conn.close()