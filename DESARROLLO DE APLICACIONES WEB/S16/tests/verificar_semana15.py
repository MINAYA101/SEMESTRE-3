import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app

app.config.update(TESTING=True, WTF_CSRF_ENABLED=False)
cliente = app.test_client()
assert cliente.get('/login').status_code == 200
assert cliente.get('/registro').status_code == 200
for ruta in ('/', '/productos', '/productos/nuevo', '/proveedores', '/clientes', '/facturacion'):
    respuesta = cliente.get(ruta)
    assert respuesta.status_code == 302
    assert '/login' in respuesta.headers['Location']
print('OK: autenticación y todos los módulos CRUD requieren sesión.')
