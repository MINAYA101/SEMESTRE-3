import os
import mysql.connector
from mysql.connector import Error

def obtener_conexion():
    """Obtiene una conexión centralizada sin publicar credenciales sensibles."""
    try:
        conexion = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST", "localhost"),
            user=os.getenv("MYSQL_USER", "root"),
            password=os.getenv("MYSQL_PASSWORD", ""),
            database=os.getenv("MYSQL_DATABASE", "ferreteria_db"),
        )
        return conexion if conexion.is_connected() else None
    except Error as error:
        print(f"Error al conectar a MySQL: {error}")
        return None

def cerrar_conexion(conexion, cursor=None):
    if cursor:
        cursor.close()
    if conexion and conexion.is_connected():
        conexion.close()
