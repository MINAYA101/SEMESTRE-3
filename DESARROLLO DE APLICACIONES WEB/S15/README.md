# FerreNova — Proyecto Integrador U4 · Avance 15/16

FerreNova es una aplicación Flask para administrar una ferretería. Esta entrega migra la persistencia a **PostgreSQL**, conserva el sistema de autenticación de la Semana 14 e implementa CRUD completo para **productos, proveedores y clientes**, con consultas relacionadas mediante `JOIN`.

## Funcionalidades

- Registro e inicio de sesión con Flask-Login y contraseñas protegidas con Werkzeug.
- Rutas administrativas protegidas mediante `@login_required`.
- CRUD completo: `INSERT`, `SELECT`, `UPDATE` y `DELETE`.
- Tres tablas relacionadas mediante claves primarias y foráneas: `productos`, `proveedores`, `clientes`; además de `usuarios` y `facturas`.
- Consulta `LEFT JOIN` entre productos y proveedores, y entre facturas y clientes.
- Formularios Flask-WTF con validación y protección CSRF.
- Consultas SQL parametrizadas con `%s`.
- Configuración compatible con Render mediante `DATABASE_URL` y `PORT`.

## Estructura destacada

```text
ProyectoFerreteria/
├── app.py
├── models.py
├── requirements.txt
├── Procfile
├── render.yaml
├── conexion/conexion.py
├── forms/
│   ├── login_form.py
│   ├── usuario_form.py
│   ├── producto_form.py
│   ├── entidades_form.py
│   └── facturacion_form.py
├── sql/esquema.sql
├── templates/
│   ├── login.html
│   ├── registro.html
│   ├── productos.html
│   ├── proveedores.html
│   ├── clientes.html
│   └── formulario_*.html
└── static/css/style.css
```

## Ejecución local

Instalar dependencias:

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
```

Configurar PostgreSQL mediante variables de entorno:

```bash
export PGHOST=localhost
export PGPORT=5432
export PGUSER=postgres
export PGPASSWORD=su_clave_local
export PGDATABASE=ferreteria_db
export FERRENOVA_SECRET_KEY=clave-secreta-local
```

Crear una base de datos llamada `ferreteria_db`, ejecutar el contenido de `sql/esquema.sql` y levantar la aplicación:

```bash
python app.py
```

Abrir `http://127.0.0.1:5000/registro`, registrar un usuario e iniciar sesión.

## Despliegue en Render

1. Subir el proyecto a GitHub.
2. Crear una base de datos **Render PostgreSQL**.
3. Crear un servicio **Render Web Service** conectado al repositorio.
4. Usar `pip install -r requirements.txt` como Build Command y `gunicorn app:app` como Start Command.
5. Definir `DATABASE_URL` con la Internal Database URL de PostgreSQL y `FERRENOVA_SECRET_KEY` como variables privadas.
6. Ejecutar `sql/esquema.sql` sobre la base PostgreSQL de Render antes de probar el servicio.

El archivo `render.yaml` documenta el servicio y el archivo `Procfile` define el proceso web. No se incluyen credenciales en el repositorio.

## Prueba obligatoria

La secuencia solicitada para la revisión es: registrar usuario → iniciar sesión → listar productos → crear producto → editar producto → eliminar producto → consultar proveedor relacionado en la tabla → cerrar sesión. También se pueden repetir las operaciones CRUD desde los módulos de clientes y proveedores.

## Rutas principales

| Ruta | Acceso | Función |
|---|---|---|
| `/registro` | Público | Registrar usuarios con hash de contraseña. |
| `/login` | Público | Autenticar usuarios. |
| `/logout` | Protegido | Cerrar sesión. |
| `/productos` | Protegido | Listar productos y proveedor relacionado. |
| `/productos/nuevo` | Protegido | Crear producto. |
| `/productos/editar/<id>` | Protegido | Actualizar producto. |
| `/productos/eliminar/<id>` | Protegido | Eliminar producto. |
| `/proveedores/*` | Protegido | CRUD de proveedores. |
| `/clientes/*` | Protegido | CRUD de clientes. |
| `/facturacion` | Protegido | Consultar facturas con cliente relacionado. |
