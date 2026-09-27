# FerreNova — Evidencias de Semana 15

## Alcance

Esta actualización implementa el Avance 15/16 con PostgreSQL, CRUD y autenticación integrada. Se mantienen las funcionalidades de login, registro, hash de contraseñas y protección de rutas de la Semana 14.

## Evidencias técnicas

| Requisito | Implementación |
|---|---|
| PostgreSQL | `conexion/conexion.py` utiliza `psycopg2` y soporta `DATABASE_URL` de Render. |
| Tres tablas relacionadas | `productos`, `proveedores` y `clientes` usan claves primarias; `productos.id_proveedor` y `facturas.id_cliente` son claves foráneas. |
| Crear | Formularios validados e instrucciones `INSERT` para productos, proveedores y clientes. |
| Leer | Tablas HTML con consultas `SELECT`. |
| Actualizar | Rutas `/editar/<id>` con formularios reutilizables y `UPDATE`. |
| Eliminar | Rutas POST protegidas con `DELETE`. |
| Relaciones | `LEFT JOIN` para mostrar el proveedor del producto y el cliente de la factura. |
| Login | Flask-Login, `@login_required`, `current_user` y logout conservados. |
| Render | `Procfile`, `render.yaml`, `PORT`, `DATABASE_URL` y `gunicorn` incluidos. |

## Secuencia de revisión

1. Ejecutar `sql/esquema.sql` en la base PostgreSQL.
2. Configurar `DATABASE_URL` y `FERRENOVA_SECRET_KEY`.
3. Ejecutar `pip install -r requirements.txt` y `python app.py`.
4. Registrar usuario e iniciar sesión.
5. Crear, listar, editar y eliminar un producto.
6. Consultar la columna **Proveedor**, que demuestra la relación mediante `JOIN`.
7. Repetir el flujo CRUD en clientes y proveedores.
8. Cerrar sesión e intentar abrir `/productos`; el sistema debe devolver al login.

## Validación ejecutada en el entorno

- Compilación Python: correcta.
- Importación de Flask y registro de rutas: correcta, 18 rutas.
- Suite automatizada: `4 passed`.
- Prueba de rutas públicas y protegidas: correcta.

No se incluyen credenciales, contraseñas reales ni valores privados de PostgreSQL.
