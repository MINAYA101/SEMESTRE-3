# FerreNova — Guía de revisión · Semana 14

## Evidencias implementadas

La aplicación incorpora el sistema de autenticación solicitado: tabla `usuarios` en MySQL, registro con Flask-WTF, hash mediante Werkzeug, login con validación segura, gestión de sesión con Flask-Login, protección de rutas con `@login_required`, identificación de `current_user` y cierre de sesión con `logout_user()`.

## Archivos principales

| Archivo | Evidencia |
|---|---|
| `app.py` | Configuración de `LoginManager`, rutas `/registro`, `/login`, `/logout` y rutas privadas. |
| `models.py` | Clase `Usuario(UserMixin)` y función de carga desde MySQL. |
| `forms/login_form.py` | Formulario validado de inicio de sesión. |
| `forms/usuario_form.py` | Formulario validado de registro y confirmación de contraseña. |
| `sql/esquema.sql` | Tabla `usuarios` con usuario único y contraseña de hasta 255 caracteres. |
| `templates/login.html` / `registro.html` | Interfaz de autenticación con CSRF. |
| `templates/components/navbar.html` | Usuario activo y enlace visible de salida. |

## Comprobación local

1. Configurar las variables `MYSQL_HOST`, `MYSQL_USER`, `MYSQL_PASSWORD`, `MYSQL_DATABASE` y `FERRENOVA_SECRET_KEY`.
2. Ejecutar `sql/esquema.sql` en MySQL.
3. Instalar dependencias con `pip install -r requirements.txt`.
4. Iniciar con `python app.py`.
5. Registrar un usuario, consultar la tabla y confirmar que `password` contiene un hash.
6. Probar credenciales incorrectas y correctas.
7. Acceder a `/productos` autenticado, cerrar sesión y comprobar la redirección al login.



No se incluyen contraseñas reales ni credenciales de base de datos en el proyecto.
