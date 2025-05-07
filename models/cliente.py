from database.conexion import get_connection
import traceback


def obtener_id_cliente(nombre, primer_apellido, segundo_apellido, telefono):
    """
    Busca al cliente por teléfono. Si no existe, lo inserta y devuelve su ID.
    """
    try:
        print("🔍 Buscando cliente por teléfono:", telefono)
        conn = get_connection()
        cursor = conn.cursor()

        query_buscar = "SELECT ID_Cliente FROM cliente WHERE Telefono = %s"
        cursor.execute(query_buscar, (telefono,))
        resultado = cursor.fetchone()

        if resultado:
            print("✅ Cliente encontrado:", resultado["ID_Cliente"])
            return resultado["ID_Cliente"]

        print("➕ Cliente no encontrado. Insertando nuevo cliente...")
        query_insertar = """
            INSERT INTO cliente (Nombre, PrimerApellido, SegundoApellido, Telefono)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query_insertar, (nombre, primer_apellido, segundo_apellido, telefono))
        conn.commit()
        nuevo_id = cursor.lastrowid
        print("🆕 ID Cliente insertado:", nuevo_id)
        return nuevo_id

    except Exception as e:
        print(f"[ERROR] al obtener o insertar cliente: {e}")
        traceback.print_exc()
        return None

    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals() and conn.open: conn.close()



def insertar_cliente(nombre, apellido_paterno, apellido_materno, telefono):
    from database.conexion import get_connection
    import traceback
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = """
        INSERT INTO cliente (Nombre, PrimerApellido, SegundoApellido, Telefono)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (nombre, apellido_paterno, apellido_materno, telefono))
        conn.commit()

        id_cliente = cursor.lastrowid
        print(f"✅ Cliente insertado con ID: {id_cliente}")
        return id_cliente
    except Exception as e:
        print(f"❌ Error al insertar cliente: {e}")
        traceback.print_exc()
        return None
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals() and conn.open: conn.close()
