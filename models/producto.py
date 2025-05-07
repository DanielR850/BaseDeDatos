from database.conexion import get_connection
import traceback
import pymysql.cursors


def insertar_producto(nombre, marca, precio, stock):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO Inventario (Nombre_Producto, Marca, Precio_Compra, Stock)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (nombre, marca, float(precio), int(stock)))
        conn.commit()
        return True
    except Exception as e:
        print(f"❌ Error al insertar producto: {e}")
        traceback.print_exc()
        return False
    finally:
        if cursor: cursor.close()
        if conn: conn.close()


def obtener_productos():
    print("📥 Entrando a obtener_productos()")
    productos = []
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT ID_Producto, Nombre_Producto, Marca, Precio_Compra, Stock
                FROM Inventario
            """)
            rows = cursor.fetchall()
            print(f"🔎 {len(rows)} productos encontrados")
            for row in rows:
                productos.append({
                    "ID_Producto": row["ID_Producto"],
                    "Nombre_Producto": row["Nombre_Producto"],
                    "Marca": row["Marca"],
                    "Precio_Compra": row["Precio_Compra"],
                    "Stock": row["Stock"],
                })
        return productos
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"❌ Error en obtener_productos: {e}")
        return []
    finally:
        conn.close()



def eliminar_producto_por_id(id_producto):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Inventario WHERE ID_Producto = %s", (id_producto,))
        conn.commit()
        return cursor.rowcount > 0
    except Exception as e:
        print(f"❌ Error al eliminar producto: {e}")
        return False
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals() and conn.open:
            conn.close()


def actualizar_producto(id_producto, nombre, marca, precio, stock):
    print(f"📝 Actualizando producto ID {id_producto}...")
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = """
            UPDATE Inventario
            SET Nombre_Producto = %s,
                Marca = %s,
                Precio_Compra = %s,
                Stock = %s
            WHERE ID_Producto = %s
        """
        cursor.execute(query, (nombre, marca, precio, stock, id_producto))
        conn.commit()

        print("✅ Producto actualizado correctamente")
        return True

    except Exception as e:
        print(f"❌ Error al actualizar producto: {e}")
        return False

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()