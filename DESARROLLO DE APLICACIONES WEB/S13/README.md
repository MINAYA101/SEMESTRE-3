# FerreNova — Proyecto Integrador U3

## Semana 13 · Avance 13/16: Uso de bases de datos relacionales: configuración, modelos y consultas básicas (MySQL)

**FerreNova** es una aplicación web académica desarrollada con Python y Flask. Esta entrega evoluciona el proyecto hacia el uso de una base de datos relacional **MySQL**. Se centraliza la conexión, se define un esquema relacional con claves primarias y foráneas, y se implementa el flujo CRUD completo (Listar, Agregar, Modificar, Eliminar) en el módulo de Productos.



## 1. Estructura del proyecto

```text
ProyectoFerreteria/
├── app.py
├── requirements.txt
├── README.md
├── conexion/
│   ├── __init__.py
│   └── conexion.py
├── sql/
│   └── esquema.sql
├── forms/
│   ├── __init__.py
│   ├── producto_form.py
│   ├── cliente_form.py
│   ├── proveedor_form.py
│   └── facturacion_form.py
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── productos.html
│   ├── formulario_producto.html
│   ├── clientes.html
│   ├── formulario_cliente.html
│   ├── proveedores.html
│   ├── formulario_proveedor.html
│   ├── facturacion.html
│   ├── formulario_facturacion.html
│   ├── components/
│   │   ├── navbar.html
│   │   └── footer.html
│   └── 404.html
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── script.js
│   └── img/
└── tests/
    └── test_app.py
```

## 2. Formularios y Validación

Se han implementado clases de formularios que heredan de `FlaskForm` en la carpeta `forms/`:
- **ProductoForm**: Validación de código, nombre, categoría, precio, stock y estado.
- **ClienteForm**: Validación de nombre, documento, teléfono y tipo de cliente.
- **ProveedorForm**: Validación de empresa, contacto, rubro y teléfono.
- **FacturacionForm**: Validación de número, cliente, fecha, total y estado.

Se utilizan validadores como `DataRequired()`, `Length()`, `NumberRange()` y tipos de campos específicos (`StringField`, `FloatField`, `SelectField`, etc.).

## 3. Rutas de Formularios

| Ruta | Método | Función |
|---|---|---|
| `/productos/nuevo` | GET / POST | Formulario para registro de productos |
| `/clientes/nuevo` | GET / POST | Formulario para registro de clientes |
| `/proveedores/nuevo` | GET / POST | Formulario para registro de proveedores |
| `/facturacion/nuevo` | GET / POST | Formulario para emisión de facturas |

Las rutas utilizan `form.validate_on_submit()` para procesar la información únicamente cuando las validaciones son correctas.

## 4. Integración con Jinja2 y Bootstrap

Las plantillas de formularios heredan de `base.html` e incluyen:
- `form.hidden_tag()` para protección CSRF.
- Renderizado dinámico de etiquetas y campos.
- Visualización de mensajes de error debajo de cada campo utilizando clases de **Bootstrap 5** (`is-invalid`, `invalid-feedback`).

## 5. Requisitos y Ejecución

Instalar dependencias:
```bash
pip install -r requirements.txt
```

Ejecutar aplicación:
```bash
python app.py
```

## 6. Gestión de Datos con MySQL

- **Conector**: Se utiliza `mysql-connector-python`.
- **Conexión Centralizada**: Gestionada en `conexion/conexion.py`.
- **Modelo Relacional**:
  - `productos`: Incluye `id_proveedor` como **FOREIGN KEY**.
  - `proveedores`, `clientes`, `facturas`: Tablas creadas con claves primarias.
- **Operaciones CRUD en Productos**:
  - **Listar**: `SELECT` con `LEFT JOIN` para obtener nombres de proveedores.
  - **Agregar**: `INSERT` desde formulario Flask-WTF validado.
  - **Modificar**: `UPDATE` con cláusula `WHERE` para registros específicos.
  - **Eliminar**: `DELETE` con confirmación visual.
- **Consultas Parametrizadas**: Se utilizan marcadores `%s` para prevenir inyecciones SQL.

## 7. Verificación realizada

Se ha verificado localmente que:
1. Flask establece conexión exitosa con MySQL.
2. El esquema SQL se ejecuta correctamente creando las relaciones.
3. Las operaciones de Agregar, Editar y Eliminar impactan directamente en la base de datos.
4. La información persiste tras reiniciar el servidor.
5. Se utiliza `commit()` y `close()` adecuadamente en cada transacción.
