import os
import psycopg2
from psycopg2.extras import RealDictCursor


def obtener_conexion():
    """Obtiene PostgreSQL usando DATABASE_URL de Render o variables individuales."""
    try:
        database_url = os.getenv("DATABASE_URL")
        if database_url:
            return psycopg2.connect(database_url, sslmode=os.getenv("PGSSLMODE", "require"))
        return psycopg2.connect(
            host=os.getenv("PGHOST", "localhost"),
            port=os.getenv("PGPORT", "5432"),
            user=os.getenv("PGUSER", "postgres"),
            password=os.getenv("PGPASSWORD", ""),
            dbname=os.getenv("PGDATABASE", "ferreteria_db"),
        )
    except psycopg2.Error as error:
        print(f"Error al conectar a PostgreSQL: {error}")
        return None


def cursor_diccionario(conexion):
    return conexion.cursor(cursor_factory=RealDictCursor)


def cerrar_conexion(conexion, cursor=None):
    if cursor:
        cursor.close()
    if conexion and not conexion.closed:
        conexion.close()
