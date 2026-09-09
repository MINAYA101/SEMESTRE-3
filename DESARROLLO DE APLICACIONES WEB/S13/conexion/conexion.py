import mysql.connector
from mysql.connector import Error

def obtener_conexion():
    """Establece y devuelve una conexión a la base de datos MySQL."""
    try:
        conexion = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='ferreteria_db'
        )
        if conexion.is_connected():
            return conexion
    except Error as e:
        print(f"Error al conectar a MySQL: {e}")
        return None

def cerrar_conexion(conexion, cursor=None):
    """Cierra el cursor y la conexión de forma segura."""
    if cursor:
        cursor.close()
    if conexion and conexion.is_connected():
        conexion.close()
