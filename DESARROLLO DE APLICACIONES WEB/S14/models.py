from flask_login import UserMixin
from conexion.conexion import obtener_conexion, cerrar_conexion

class Usuario(UserMixin):
    def __init__(self, id_usuario, usuario, password):
        self.id = str(id_usuario)
        self.usuario = usuario
        self.password = password

    @classmethod
    def obtener_por_id(cls, id_usuario):
        conexion = obtener_conexion()
        if not conexion:
            return None
        cursor = conexion.cursor(dictionary=True)
        try:
            cursor.execute("SELECT id, usuario, password FROM usuarios WHERE id = %s", (id_usuario,))
            dato = cursor.fetchone()
            return cls(dato["id"], dato["usuario"], dato["password"]) if dato else None
        finally:
            cerrar_conexion(conexion, cursor)

    @classmethod
    def obtener_por_nombre(cls, nombre):
        conexion = obtener_conexion()
        if not conexion:
            return None
        cursor = conexion.cursor(dictionary=True)
        try:
            cursor.execute("SELECT id, usuario, password FROM usuarios WHERE usuario = %s", (nombre,))
            dato = cursor.fetchone()
            return cls(dato["id"], dato["usuario"], dato["password"]) if dato else None
        finally:
            cerrar_conexion(conexion, cursor)
