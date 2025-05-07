import pymysql
import traceback

def get_connection():
    print("🛠️ Entrando a get_connection() con PyMySQL")
    try:
        conn = pymysql.connect(
            host="localhost",
            user="root",
            password="daniel0812",
            database="bellezadb",
            cursorclass=pymysql.cursors.DictCursor
        )
        print("🔗 Conexión a MySQL establecida con PyMySQL")
        return conn
    except Exception as e:
        print("💥 EXCEPCIÓN EN get_connection()")
        print(f"❌ Tipo: {type(e).__name__} - {e}")
        traceback.print_exc()
        raise
