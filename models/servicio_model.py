from database.conexion import get_connection
import pymysql.cursors

def obtener_variantes_servicio():
    print("🛠️ Entrando a obtener_variantes_servicio()")
    try:
        conn = get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT ID_Variante, Nombre_Variante FROM variante_servicio")
        resultados = cursor.fetchall()
        print(f"🔎 Variantes encontradas: {resultados}")
        return resultados
    except Exception as e:
        print(f"❌ Error al obtener variantes de servicio: {e}")
        return []
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals() and conn.open:
            conn.close()


def obtener_detalles_servicio():
    print("🛠️ Entrando a obtener_detalles_servicio()")
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT ID_Detalle, Nombre_Detalle FROM Servicio_Detalle")
        resultados = cursor.fetchall()
        detalles = [{"ID_Detalle": row[0], "Nombre_Detalle": row[1]} for row in resultados]
        print(f"🔎 Detalles encontrados: {detalles}")
        return detalles
    except Exception as e:
        print(f"❌ Error al obtener detalles de servicio: {e}")
        return []
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals() and conn.open:
            conn.close()

def insertar_servicio(nombre, precio, id_variante, detalles_ids):
    print("🛠️ Entrando a insertar_servicio()")
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Verificar datos
        print(f"📥 Insertando servicio: {nombre}, {precio}, Variante ID: {id_variante}")
        print(f"📎 Detalles seleccionados: {detalles_ids}")

        # Insertar servicio
        cursor.execute(
            "INSERT INTO servicio (Nombre_Servicio, Precio, ID_Variante) VALUES (%s, %s, %s)",
            (nombre, precio, id_variante)
        )
        id_servicio = cursor.lastrowid
        print(f"✅ Servicio insertado con ID: {id_servicio}")

        # Insertar detalles asociados
        for id_detalle in detalles_ids:
            cursor.execute(
                "INSERT INTO servicio_detalle_map (ID_Servicio, ID_Detalle) VALUES (%s, %s)",
                (id_servicio, id_detalle)
            )
            print(f"🧩 Mapeo insertado: Servicio {id_servicio} -> Detalle {id_detalle}")

        conn.commit()
        print("✅ Servicio y detalles registrados correctamente.")
        return True

    except Exception as e:
        print(f"❌ Error al insertar servicio: {e}")
        return False

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals() and conn.open:
            conn.close()


def obtener_servicios():
    print("📥 Entrando a obtener_servicios()")
    try:
        conn = get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)  # ✅

        query = """
        SELECT S.ID_Servicio, S.Nombre_Servicio, V.Nombre_Variante, S.Precio
        FROM Servicio S
        JOIN Variante_Servicio V ON S.ID_Variante = V.ID_Variante
        ORDER BY S.ID_Servicio DESC
        """

        cursor.execute(query)
        resultados = cursor.fetchall()

        servicios = []
        for row in resultados:
            print(f"🔹 Fila cruda: {row}")
            servicios.append({
                "ID": row["ID_Servicio"],
                "Nombre": row["Nombre_Servicio"],
                "Variante": row["Nombre_Variante"],
                "Precio": row["Precio"]
            })

        print(f"🔍 Servicios obtenidos: {len(servicios)}")
        return servicios

    except Exception as e:
        print(f"❌ Error en obtener_servicios: {type(e).__name__} - {e}")
        return []

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals() and conn.open:
            conn.close()



def actualizar_servicio(id_servicio, nuevo_nombre, nuevo_precio, nuevo_id_variante):
    print("🛠️ Entrando a actualizar_servicio()")
    try:
        conn = get_connection()
        cursor = conn.cursor()

        print(f"🔄 Actualizando servicio ID: {id_servicio}")
        print(f"📋 Nuevos datos → Nombre: {nuevo_nombre}, Precio: {nuevo_precio}, Variante ID: {nuevo_id_variante}")

        cursor.execute("""
            UPDATE Servicio
            SET Nombre_Servicio = %s, Precio = %s, ID_Variante = %s
            WHERE ID_Servicio = %s
        """, (nuevo_nombre, nuevo_precio, nuevo_id_variante, id_servicio))

        conn.commit()
        print("✅ Servicio actualizado correctamente.")
        return True

    except Exception as e:
        print(f"❌ Error al actualizar servicio: {e}")
        return False

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals() and conn.open:
            conn.close()

def eliminar_servicio(id_servicio):
    print(f"🗑️ Eliminando servicio con ID: {id_servicio}")
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Eliminar directamente de la tabla Servicio
        cursor.execute("DELETE FROM servicio WHERE ID_Servicio = %s", (id_servicio,))

        conn.commit()
        print("✅ Servicio eliminado correctamente.")
        return True

    except Exception as e:
        print(f"❌ Error al eliminar servicio: {e}")
        return False

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals() and conn.open:
            conn.close()
