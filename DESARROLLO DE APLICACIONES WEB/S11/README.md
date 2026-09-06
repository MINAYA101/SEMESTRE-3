# FerreNova — Proyecto Integrador U3

## Semana 11 · Avance 11/16: Validación de formularios con Flask-WTF y WTForms

**FerreNova** es una aplicación web académica desarrollada con Python y Flask. Esta entrega incorpora formularios web y mecanismos de validación del lado del servidor utilizando **Flask-WTF** y **WTForms**, manteniendo la estructura y avances de las semanas anteriores.

> **Alcance de esta entrega:** Los formularios permiten ingresar información, validar datos y mostrar mensajes de error. Se incluye protección contra ataques CSRF mediante una `SECRET_KEY`. La persistencia de datos se maneja temporalmente en memoria.

## 1. Estructura del proyecto

```text
ProyectoFerreteria/
├── app.py
├── requirements.txt
├── README.md
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

## 6. Verificación realizada

Se ha verificado localmente que:
1. Las nuevas rutas responden con estado 200.
2. Los formularios no se procesan si faltan campos obligatorios o hay datos inválidos.
3. Se muestran mensajes de error claros al usuario.
4. La protección CSRF está activa.
5. Las rutas y funcionalidades previas continúan operativas.
