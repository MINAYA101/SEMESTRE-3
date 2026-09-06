# FerreNova — Proyecto Integrador U3

## Semana 12 · Avance 12/16: Persistencia de datos en un entorno local con SQLite

**FerreNova** es una aplicación web académica desarrollada con Python y Flask. Esta entrega incorpora persistencia de datos en un entorno local utilizando **SQLite**. Se conecta la aplicación Flask con una base de datos local, se crea la tabla de productos y se almacenan los datos provenientes de los formularios validados, permitiendo que la información permanezca disponible después de reiniciar la aplicación.

> **Alcance de esta entrega:** Implementación del flujo completo en el módulo de productos: Formulario -> Validación -> INSERT -> SELECT -> Tabla HTML. La base de datos se almacena en `data/ferreteria.db`.

## 1. Estructura del proyecto

```text
ProyectoFerreteria/
├── app.py
├── requirements.txt
├── README.md
├── data/
│   └── ferreteria.db
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

## 6. Persistencia con SQLite

- **Base de Datos**: Se utiliza `sqlite3` para gestionar `data/ferreteria.db`.
- **Tabla Productos**: Almacena `codigo`, `nombre`, `categoria`, `precio`, `stock` y `estado`.
- **Operaciones**: 
  - `INSERT`: Los productos validados se guardan mediante consultas parametrizadas.
  - `SELECT`: Los registros se recuperan y se muestran dinámicamente con Jinja2.
- **Inicialización**: La base de datos se crea automáticamente al arrancar la aplicación si no existe.

## 7. Verificación realizada

Se ha verificado localmente que:
1. La base de datos se crea correctamente en la carpeta `data/`.
2. El flujo de registro de productos guarda la información de forma permanente.
3. Los datos persisten incluso después de reiniciar el servidor Flask.
4. Las validaciones de Flask-WTF y la protección CSRF siguen funcionando correctamente.
5. Las rutas y componentes previos (navbar, footer, herencia) se mantienen íntegros.
