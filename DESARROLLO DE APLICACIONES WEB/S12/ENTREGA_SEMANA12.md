# Entrega Semana 10 — FerreNova

Este archivo contiene el proyecto Flask actualizado para el Avance 10/16 del Proyecto Integrador U3.

## Contenido incorporado

El proyecto conserva las rutas, estilos, JavaScript y plantillas de la Semana 9. Además, incorpora datos de ejemplo definidos en `app.py`, listas de registros, diccionarios estructurados, variables simples, bucles `{% for %}`, condiciones `{% if %}`, filtros Jinja2 como `upper`, herencia mediante `{% extends 'base.html' %}` y componentes reutilizables mediante `{% include %}`.

Los componentes compartidos se encuentran en:

```text
templates/components/navbar.html
templates/components/footer.html
```

## Ejecución local

Desde esta carpeta, ejecutar:

```bash
python -m venv venv
# Windows: venv\Scripts\activate
# Linux/macOS: source venv/bin/activate
pip install -r requirements.txt
python app.py
```

Después, abrir [http://127.0.0.1:5000](http://127.0.0.1:5000).

Las rutas disponibles son `/`, `/productos`, `/clientes`, `/proveedores` y `/facturacion`. También se incluye una página personalizada para rutas inexistentes.

## Pruebas

```bash
python -m pytest -q
```

La verificación local realizada confirmó que las rutas principales responden con estado 200, la ruta inexistente responde con 404 y los archivos CSS y JavaScript se sirven correctamente desde `static`.


