from database.conexion import get_connection
import traceback

def obtener_id_metodo(nombre_metodo):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        query = "SELECT ID_Metodo FROM metodopago WHERE Nombre = %s"
        cursor.execute(query, (nombre_metodo,))
        resultado = cursor.fetchone()

        # ✅ Usar clave si estás usando DictCursor
        return resultado['ID_Metodo'] if resultado else None

    except Exception as e:
        print(f"[ERROR] obtener_id_metodo: {e}")
        traceback.print_exc()
        return None

    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals() and conn.open: conn.close()

def insertar_pago(monto, id_metodo, id_cita):
    """
    Inserta el pago en la base de datos.
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO pago (monto, id_metodo, id_cita)
            VALUES (%s, %s, %s)
        """
        cursor.execute(query, (monto, id_metodo, id_cita))
        conn.commit()
        print("✅ Pago registrado exitosamente.")
        return True
    except Exception as e:
        print(f"[ERROR] insertar_pago: {e}")
        traceback.print_exc()
        return False
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals() and conn.open:
            conn.close()


def obtener_metodos_pago():
    from database.conexion import get_connection
    try:
        conn = get_connection()
        cursor = conn.cursor()
        query = "SELECT ID_Metodo, Nombre FROM metodopago"
        cursor.execute(query)
        resultados = cursor.fetchall()
        return [{"id": row["ID_Metodo"], "nombre": row["Nombre"]} for row in resultados]
    except Exception as e:
        print("[ERROR] obtener_metodos_pago:", e)
        import traceback
        traceback.print_exc()
        return []
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals() and conn.open: conn.close()


def obtener_todos_los_pagos():
    print("🛠️ Entrando a obtener_todos_los_pagos()")
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = """
        SELECT c.Nombre AS cliente, p.Monto AS monto, mp.Nombre AS metodo
        FROM pago p
        JOIN cita ci ON p.ID_Cita = ci.ID_Cita
        JOIN cliente c ON ci.ID_Cliente = c.ID_Cliente
        JOIN metodopago mp ON p.ID_Metodo = mp.ID_Metodo
        ORDER BY p.ID_Pago DESC
        """
        cursor.execute(query)
        resultados = cursor.fetchall()
        return resultados

    except Exception as e:
        print(f"[ERROR] obtener_todos_los_pagos: {e}")
        return []

    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals() and conn.open: conn.close()
