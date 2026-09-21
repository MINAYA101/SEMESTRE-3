import pytest
from app import app

@pytest.fixture()
def client():
    app.config.update(TESTING=True, WTF_CSRF_ENABLED=False)
    with app.test_client() as test_client:
        yield test_client

def test_acceso_a_productos_requiere_autenticacion(client):
    respuesta = client.get('/productos')
    assert respuesta.status_code == 302
    assert '/login' in respuesta.headers['Location']

# La persistencia real se verifica ejecutando sql/esquema.sql en MySQL y siguiendo
# el procedimiento de pruebas documentado en README.md.
