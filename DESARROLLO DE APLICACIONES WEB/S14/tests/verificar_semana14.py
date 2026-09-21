import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app

app.config.update(TESTING=True, WTF_CSRF_ENABLED=False)
cliente = app.test_client()

respuesta_login = cliente.get('/login')
assert respuesta_login.status_code == 200
assert 'Iniciar sesión' in respuesta_login.get_data(as_text=True)

respuesta_registro = cliente.get('/registro')
assert respuesta_registro.status_code == 200
assert 'Crear usuario' in respuesta_registro.get_data(as_text=True)

for ruta in ('/', '/productos', '/clientes', '/proveedores', '/facturacion'):
    respuesta = cliente.get(ruta)
    assert respuesta.status_code == 302, (ruta, respuesta.status_code)
    assert '/login' in respuesta.headers['Location'], (ruta, respuesta.headers['Location'])

print('OK: login y registro públicos; rutas administrativas protegidas.')
