# FerreNova · Proyecto Final

Sistema web para la gestión integral de una ferretería. La entrega final consolida los avances del curso en una aplicación Flask con autenticación, persistencia PostgreSQL y una interfaz responsive orientada a la operación diaria.

## Alcance funcional

- **Autenticación:** registro, inicio de sesión, cierre de sesión, contraseñas protegidas con hash y rutas privadas con Flask-Login.
- **CRUD completo:** productos, proveedores, clientes y facturas.
- **Relaciones:** productos–proveedores y facturas–clientes mediante claves foráneas y consultas `JOIN`.
- **Validaciones:** Flask-WTF, CSRF en formularios, restricciones de datos, códigos y documentos únicos.
- **Presentación:** panel con indicadores, navegación consistente, estados visuales, mensajes de operación y diseño responsive.

## Estructura

```text
S16/
├── app.py
├── models.py
├── conexion/
├── forms/
├── sql/esquema.sql
├── templates/
├── static/css/style.css
├── tests/
└── docs/                 # Página estática de presentación para GitHub Pages
```

## Ejecución local

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export PGHOST=localhost
export PGPORT=5432
export PGUSER=postgres
export PGPASSWORD=tu_clave
export PGDATABASE=ferreteria_db
export FERRENOVA_SECRET_KEY=una-clave-segura
psql -f sql/esquema.sql
python app.py
```

Abrir `http://127.0.0.1:5000/registro`, crear el usuario de demostración e iniciar sesión.

## Despliegue

La configuración está preparada para Render mediante `DATABASE_URL`, `PORT`, `Procfile` y `render.yaml`. Ejecuta `sql/esquema.sql` sobre la base PostgreSQL antes de la primera demostración.

## Guion de defensa

1. Registrar usuario e iniciar sesión.
2. Mostrar el panel y sus cuatro indicadores.
3. Crear, editar y eliminar un proveedor.
4. Crear un producto y demostrar el proveedor relacionado.
5. Crear, editar y eliminar un cliente.
6. Crear una factura y demostrar la relación con el cliente.
7. Editar y eliminar la factura.
8. Cerrar sesión y comprobar que las rutas privadas redirigen al login.

## Página de presentación

La carpeta `docs/` contiene una página estática independiente para activar GitHub Pages desde **Settings → Pages → Deploy from branch → `/docs`**. Esta página presenta el proyecto y su alcance sin sustituir el backend Flask.

## Autoría

Proyecto académico desarrollado por **MINAYA101**.
