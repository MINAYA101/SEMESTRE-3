import pytest

from app import app


@pytest.fixture()
def client():
    app.config.update({"TESTING": True})
    with app.test_client() as test_client:
        yield test_client


def test_rutas_principales(client):
    for ruta in ["/", "/productos", "/clientes", "/proveedores", "/facturacion"]:
        respuesta = client.get(ruta)
        assert respuesta.status_code == 200
        assert b"FerreNova" in respuesta.data


def test_herencia_jinja_en_productos(client):
    respuesta = client.get("/productos")
    assert b"Cat\xc3\xa1logo de inventario" in respuesta.data
    assert b"Sistema activo" in respuesta.data


def test_ruta_no_encontrada(client):
    respuesta = client.get("/ruta-inexistente")
    assert respuesta.status_code == 404
    assert b"P\xc3\xa1gina no encontrada" in respuesta.data
