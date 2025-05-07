from database.conexion import get_connection
import traceback
from datetime import date
import pymysql

def crear_cita(id_cliente: int, id_empleado: int, fecha: str, hora: str) -> int:
    """
    Crea una nueva cita en la base de datos y devuelve el ID de la cita creada.
    """
    print("🛠️ Entrando a crear_cita()")
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = """
        INSERT INTO Cita (ID_Cliente, ID_Empleado, Fecha, Hora)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (id_cliente, id_empleado, fecha, hora))
        conn.commit()
        id_cita = cursor.lastrowid

        print(f"✅ Cita creada con ID: {id_cita}")
        return id_cita

    except Exception as e:
        print(f"❌ Error al crear cita: {e}")
        traceback.print_exc()
        return None

    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals() and conn.open: conn.close()


def agregar_servicio_a_cita(id_cita: int, id_servicio: int, cantidad: int = 1):
    """
    Agrega un servicio a una cita específica.
    """
    print("🛠️ Entrando a agregar_servicio_a_cita()")
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = """
        INSERT INTO Detalle_Cita (ID_Cita, ID_Servicio, Cantidad)
        VALUES (%s, %s, %s)
        """
        cursor.execute(query, (id_cita, id_servicio, cantidad))
        conn.commit()

        print("✅ Servicio agregado a cita")

    except Exception as e:
        print(f"❌ Error al agregar servicio a cita: {e}")
        traceback.print_exc()

    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals() and conn.open: conn.close()


def obtener_servicios_por_variante():
    """
    Obtiene los servicios agrupados por su variante (categoría), incluyendo el precio.
    """
    print("🛠️ Entrando a obtener_servicios_por_variante()")
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = """
        SELECT s.id_servicio, s.nombre_servicio, s.precio, v.nombre_variante
        FROM servicio s
        JOIN variante_servicio v ON s.id_variante = v.id_variante
        ORDER BY v.nombre_variante
        """
        cursor.execute(query)
        resultados = cursor.fetchall()

        servicios_por_variante = {}
        for row in resultados:
            variante = row['nombre_variante']
            if variante not in servicios_por_variante:
                servicios_por_variante[variante] = []
            servicios_por_variante[variante].append({
                "id": row['id_servicio'],
                "nombre": row['nombre_servicio'],
                "precio": float(row['precio'])  # ✅ Aquí incluimos el precio
            })

        print(f"🔍 Servicios agrupados: {len(servicios_por_variante)} variantes")
        return servicios_por_variante

    except Exception as e:
        print(f"❌ Error al obtener servicios por variante: {e}")
        traceback.print_exc()
        return {}

    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals() and conn.open: conn.close()


def obtener_citas_hoy():
    try:
        conn = get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        hoy = date.today()
        query = """
            SELECT c.ID_Cita AS id, c.Fecha AS fecha, c.Hora AS hora,
                   cl.Nombre AS cliente,
                   COALESCE(s.nombre_servicio, 'Sin servicio') AS trabajo
            FROM cita c
            JOIN cliente cl ON c.ID_Cliente = cl.ID_Cliente
            LEFT JOIN cita_servicio cs ON c.ID_Cita = cs.ID_Cita
            LEFT JOIN servicio s ON cs.ID_Servicio = s.ID_Servicio
            WHERE c.Fecha = %s
        """
        cursor.execute(query, (hoy,))
        resultados = cursor.fetchall()
        print(f"📅 Citas de hoy ({hoy}): {len(resultados)} encontradas")
        return resultados

    except Exception as e:
        print(f"[ERROR] obtener_citas_hoy(): {e}")
        traceback.print_exc()
        return []

    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals() and conn.open: conn.close()

def eliminar_cita_por_id(id_cita: int) -> bool:
    from database.conexion import get_connection
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Paso 1: Eliminar pagos asociados
        cursor.execute("DELETE FROM pago WHERE ID_Cita = %s", (id_cita,))

        # Paso 2: Eliminar detalles de cita si existen

        # Paso 3: Eliminar la cita
        cursor.execute("DELETE FROM cita WHERE ID_Cita = %s", (id_cita,))
        conn.commit()

        return cursor.rowcount > 0
    except Exception as e:
        print(f"[ERROR] eliminar_cita_por_id(): {e}")
        return False
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals() and conn.open: conn.close()
