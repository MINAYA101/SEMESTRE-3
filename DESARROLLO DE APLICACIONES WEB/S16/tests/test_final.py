import pytest
from app import app

@pytest.fixture()
def client():
    app.config.update(TESTING=True, WTF_CSRF_ENABLED=False)
    with app.test_client() as test_client:
        yield test_client

def test_rutas_publicas(client):
    assert client.get('/login').status_code == 200
    assert client.get('/registro').status_code == 200

def test_rutas_protegidas(client):
    for ruta in ['/', '/productos', '/productos/nuevo', '/clientes', '/proveedores', '/facturacion', '/facturacion/nueva']:
        respuesta = client.get(ruta)
        assert respuesta.status_code == 302
        assert '/login' in respuesta.headers['Location']

def test_crud_facturacion_expuesto():
    reglas = {rule.rule for rule in app.url_map.iter_rules()}
    assert {'/facturacion','/facturacion/nueva','/facturacion/editar/<int:id>','/facturacion/eliminar/<int:id>'} <= reglas

def test_error_404(client):
    assert client.get('/ruta-inexistente').status_code == 404
