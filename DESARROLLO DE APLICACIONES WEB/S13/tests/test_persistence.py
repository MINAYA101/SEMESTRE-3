import os
import sqlite3
import pytest
from app import app, DATABASE

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False  # Deshabilitar CSRF para facilitar la prueba
    with app.test_client() as client:
        yield client

def test_productos_persistence(client):
    # 1. Verificar que la página de productos carga
    response = client.get('/productos')
    assert response.status_code == 200
    
    # 2. Insertar un nuevo producto mediante el formulario
    nuevo_producto = {
        'codigo': 'PR-TEST',
        'nombre': 'Producto de Prueba',
        'categoria': 'Medición',
        'precio': 15.50,
        'stock': 100,
        'estado': 'Disponible'
    }
    response = client.post('/productos/nuevo', data=nuevo_producto, follow_redirects=True)
    assert response.status_code == 200
    
    # 3. Verificar en la base de datos directamente
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos WHERE codigo = 'PR-TEST'")
    row = cursor.fetchone()
    conn.close()
    
    assert row is not None
    assert row[2] == 'Producto de Prueba'
    print("\n[OK] Persistencia verificada: El producto fue insertado en SQLite.")

if __name__ == "__main__":
    pytest.main([__file__])
