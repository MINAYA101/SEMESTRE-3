import pytest
from app import app

@pytest.fixture()
def client():
    app.config.update(TESTING=True, WTF_CSRF_ENABLED=False)
    with app.test_client() as test_client:
        yield test_client

def test_rutas_publicas_autenticacion(client):
    assert client.get('/login').status_code == 200
    assert client.get('/registro').status_code == 200

def test_rutas_administrativas_protegidas(client):
    for ruta in ['/', '/productos', '/clientes', '/proveedores', '/facturacion']:
        respuesta = client.get(ruta)
        assert respuesta.status_code == 302
        assert '/login' in respuesta.headers['Location']

def test_ruta_no_encontrada(client):
    respuesta = client.get('/ruta-inexistente')
    assert respuesta.status_code == 404
    assert b'Pagina no encontrada' in respuesta.data or b'P' in respuesta.data
