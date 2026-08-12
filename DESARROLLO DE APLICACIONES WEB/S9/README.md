# FerreNova — Proyecto Integrador U3

## Semana 9 · Avance 9/16: Configuración de un proyecto web con Flask y manejo de rutas

**FerreNova** es una aplicación web académica desarrollada desde cero con Python y Flask para representar la gestión básica de una ferretería. Esta entrega implementa la estructura solicitada en la actividad: una aplicación principal `app.py`, plantillas HTML organizadas en `templates`, recursos estáticos organizados en `static`, rutas para los módulos del sistema y herencia de plantillas mediante Jinja2.

> **Alcance de esta entrega:** la aplicación utiliza datos demostrativos en memoria. No incluye conexión a una base de datos porque la actividad de la Semana 9 no la requiere.

## 1. Objetivo de la actividad

El objetivo es transformar un proyecto web informativo en una aplicación basada en Flask, conservando una página principal y agregando módulos independientes para productos, clientes, proveedores y facturación. Para evitar la repetición de código, todas las páginas internas heredan de `templates/base.html`, que contiene el encabezado, el menú, los estilos globales, el pie de página y la carga de JavaScript.

## 2. Estructura del proyecto

```text
proyecto-ferreteria-semana9/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── productos.html
│   ├── clientes.html
│   ├── proveedores.html
│   ├── facturacion.html
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

La carpeta `templates` contiene los documentos HTML procesados por Jinja2. La carpeta `static` contiene CSS, JavaScript e imágenes. La carpeta `img` queda preparada para incorporar las imágenes del proyecto en futuras semanas.

## 3. Rutas implementadas

| Ruta | Función | Plantilla |
|---|---|---|
| `/` | Página principal informativa y resumen del sistema | `index.html` |
| `/productos` | Consulta del catálogo y stock | `productos.html` |
| `/clientes` | Directorio de clientes demostrativos | `clientes.html` |
| `/proveedores` | Red de proveedores y contactos | `proveedores.html` |
| `/facturacion` | Comprobantes y resumen de facturación | `facturacion.html` |
| Cualquier ruta inexistente | Página personalizada de error | `404.html` |

Las rutas se definen con el decorador `@app.route()`, renderizan sus respectivas plantillas con `render_template()` y utilizan `url_for()` en los enlaces de navegación. Los recursos CSS y JavaScript se cargan con `url_for('static', filename='...')`.

## 4. Herencia de plantillas con Jinja2

La plantilla `base.html` define la estructura compartida de la aplicación. Cada página interna comienza con:

```jinja2
{% extends 'base.html' %}
```

Después, cada archivo reemplaza los bloques necesarios, por ejemplo:

```jinja2
{% block title %}Productos{% endblock %}
{% block content %}
<!-- contenido específico del módulo -->
{% endblock %}
```

También se utilizan ciclos y condiciones Jinja2 para imprimir los datos demostrativos, clasificar estados de inventario y calcular visualmente los contenidos de cada módulo.

## 5. Requisitos

Se necesita Python 3.9 o superior y `pip`. Flask se instala a partir del archivo `requirements.txt`.

### Windows

```bash
python -m venv venv
venv\\Scripts\\activate
pip install -r requirements.txt
python app.py
```

### Linux o macOS

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

Después de ejecutar la aplicación, abrir [http://127.0.0.1:5000](http://127.0.0.1:5000) en el navegador.

## 6. Funcionalidad visual

La interfaz conserva un enfoque informativo y responsive. Incluye menú de navegación, tarjetas de resumen, catálogo destacado, tablas de módulos, estados de inventario, buscador de tablas en JavaScript y página 404 personalizada. El diseño se adapta a computadoras, tabletas y dispositivos móviles.

## 7. Verificación realizada

El archivo `tests/test_app.py` comprueba que la aplicación se pueda importar, que las cinco rutas principales respondan correctamente, que la plantilla base se utilice y que una ruta inexistente devuelva el estado 404. Para ejecutar las pruebas:

```bash
pip install pytest
pytest -q
```

