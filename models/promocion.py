from database.conexion import get_connection
import pymysql
from datetime import datetime

def obtener_promociones():
    print("📥 Entrando a obtener_promociones()")
    try:
        conn = get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        query = """
        SELECT 
            P.ID_Promocion,
            P.Descripcion,
            P.Descuento,
            P.Fecha_Inicio,
            P.Fecha_Fin,
            S.Nombre_Servicio AS Servicios
        FROM Promocion P
        JOIN Servicio S ON P.ID_Servicio = S.ID_Servicio
        """
        cursor.execute(query)
        promociones = cursor.fetchall()
        print(f"🔍 Promociones encontradas: {promociones}")
        return promociones

    except Exception as e:
        print(f"❌ Error al obtener promociones: {e}")
        return []

    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals() and conn.open: conn.close()


def insertar_promocion(descripcion, descuento, fecha_inicio, fecha_fin, id_servicio):
    print("🛠️ Entrando a insertar_promocion()")
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = """
        INSERT INTO Promocion (Descripcion, Descuento, Fecha_Inicio, Fecha_Fin, ID_Servicio)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (descripcion, descuento, fecha_inicio, fecha_fin, id_servicio))
        conn.commit()

        print("✅ Promoción insertada correctamente.")
        return True

    except Exception as e:
        print(f"❌ Error al insertar promoción: {e}")
        return False

    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals() and conn.open: conn.close()



def actualizar_promocion(id_promocion, descripcion, descuento, fecha_inicio, fecha_fin):
    print(f"🛠️ Actualizando promoción ID: {id_promocion}")
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = """
        UPDATE Promocion
        SET Descripcion = %s, Descuento = %s, Fecha_Inicio = %s, Fecha_Fin = %s
        WHERE ID_Promocion = %s
        """
        cursor.execute(query, (descripcion, descuento, fecha_inicio, fecha_fin, id_promocion))
        conn.commit()

        print("✅ Promoción actualizada.")
        return True

    except Exception as e:
        print(f"❌ Error al actualizar promoción: {e}")
        return False

    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals() and conn.open: conn.close()


def eliminar_promocion(id_promocion):
    print(f"🗑️ Eliminando promoción ID: {id_promocion}")
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM Promocion WHERE ID_Promocion = %s", (id_promocion,))
        conn.commit()

        print("✅ Promoción eliminada.")
        return True

    except Exception as e:
        print(f"❌ Error al eliminar promoción: {e}")
        return False

    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals() and conn.open: conn.close()
