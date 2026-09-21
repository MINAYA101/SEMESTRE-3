# FerreNova — Proyecto Integrador U4 · Avance 14/16

FerreNova es una aplicación web académica desarrollada con Python y Flask para la gestión de una ferretería. Esta entrega integra la conexión centralizada a **MySQL**, el CRUD de productos y un sistema completo de autenticación con **Flask-Login**, Flask-WTF y Werkzeug.

## Funcionalidades implementadas

- Registro de usuarios con validación Flask-WTF y protección CSRF.
- Almacenamiento de contraseñas mediante `generate_password_hash()`; nunca se guardan contraseñas en texto plano.
- Inicio de sesión mediante consulta parametrizada y `check_password_hash()`.
- Sesión persistente administrada por `LoginManager`, `UserMixin` y `load_user()`.
- Rutas administrativas protegidas con `@login_required`.
- Identificación visual del usuario autenticado mediante `current_user`.
- Cierre de sesión con `logout_user()` en `/logout`.
- CRUD completo de productos con consultas parametrizadas y relación con proveedores.
- Consultas de clientes, proveedores y facturación conservadas.

## Estructura principal

```text
ProyectoFerreteria/
├── app.py
├── models.py
├── requirements.txt
├── conexion/
│   ├── __init__.py
│   └── conexion.py
├── forms/
│   ├── login_form.py
│   ├── usuario_form.py
│   └── producto_form.py
├── sql/esquema.sql
├── templates/
│   ├── login.html
│   ├── registro.html
│   ├── base.html
│   └── components/navbar.html
└── static/
```

## Configuración segura

La conexión no contiene credenciales reales en el repositorio. Antes de ejecutar, configure las variables de entorno correspondientes:

```bash
export MYSQL_HOST=localhost
export MYSQL_USER=root
export MYSQL_PASSWORD=su_clave_local
export MYSQL_DATABASE=ferreteria_db
export FERRENOVA_SECRET_KEY=una-clave-secreta-local
```

Ejecute `sql/esquema.sql` en MySQL para crear la base de datos, las tablas y los datos iniciales. La tabla `usuarios` queda lista para recibir registros desde el formulario; no se incluyen contraseñas de ejemplo en el script.

## Instalación y ejecución

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Abra `http://127.0.0.1:5000/registro` para crear el primer usuario. Luego inicie sesión en `/login`.

## Rutas de autenticación

| Ruta | Método | Descripción |
|---|---|---|
| `/registro` | GET / POST | Registra un usuario y almacena el hash de su contraseña. |
| `/login` | GET / POST | Valida usuario y contraseña e inicia la sesión. |
| `/logout` | GET | Cierra la sesión activa. |
| `/`, `/productos`, `/clientes`, `/proveedores`, `/facturacion` | GET | Rutas privadas protegidas con `@login_required`. |

## Prueba obligatoria de la Semana 14

1. Ejecutar el esquema en MySQL y levantar Flask.
2. Registrar un usuario desde `/registro`.
3. Consultar `SELECT id, usuario, password FROM usuarios;` y verificar que `password` sea un hash, no la contraseña escrita.
4. Probar una contraseña incorrecta y confirmar el rechazo.
5. Iniciar sesión con las credenciales correctas y acceder a `/productos`.
6. Verificar que el nombre del usuario aparece en la barra de navegación.
7. Seleccionar **Salir** y volver a abrir `/productos`; Flask-Login debe redirigir a `/login`.

## Seguridad y buenas prácticas

Todas las consultas usan parámetros `%s`; las credenciales se leen mediante variables de entorno; los formularios incluyen `hidden_tag()`; el registro valida los datos antes del `INSERT`; y el acceso a las secciones administrativas requiere una sesión autenticada.
