-- FerreNova - PostgreSQL - Avance 15/16
-- Ejecutar dentro de la base de datos configurada en Render o localmente.

CREATE TABLE IF NOT EXISTS usuarios (
    id SERIAL PRIMARY KEY,
    usuario VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS proveedores (
    id_proveedor SERIAL PRIMARY KEY,
    empresa VARCHAR(100) UNIQUE NOT NULL,
    contacto VARCHAR(100) NOT NULL,
    rubro VARCHAR(50) NOT NULL,
    telefono VARCHAR(15) NOT NULL
);

CREATE TABLE IF NOT EXISTS clientes (
    id_cliente SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    documento VARCHAR(20) UNIQUE NOT NULL,
    telefono VARCHAR(15) NOT NULL,
    tipo VARCHAR(20) NOT NULL
);

CREATE TABLE IF NOT EXISTS productos (
    id_producto SERIAL PRIMARY KEY,
    codigo VARCHAR(20) UNIQUE NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    categoria VARCHAR(50) NOT NULL,
    precio NUMERIC(10,2) NOT NULL CHECK (precio >= 0),
    stock INTEGER NOT NULL CHECK (stock >= 0),
    estado VARCHAR(20) NOT NULL,
    id_proveedor INTEGER REFERENCES proveedores(id_proveedor) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS facturas (
    id_factura SERIAL PRIMARY KEY,
    numero VARCHAR(20) UNIQUE NOT NULL,
    id_cliente INTEGER REFERENCES clientes(id_cliente) ON DELETE RESTRICT,
    fecha DATE NOT NULL,
    total NUMERIC(10,2) NOT NULL CHECK (total >= 0),
    estado VARCHAR(20) NOT NULL
);

-- Datos iniciales opcionales. ON CONFLICT permite ejecutar el script más de una vez.
INSERT INTO proveedores (empresa, contacto, rubro, telefono) VALUES
('Importaciones El Constructor', 'Jorge Salazar', 'Herramientas', '01 445 7832'),
('Pinturas Colorama S.A.', 'Lucía Mendoza', 'Pinturas', '01 377 9210')
ON CONFLICT (empresa) DO NOTHING;

INSERT INTO clientes (nombre, documento, telefono, tipo) VALUES
('Cliente demostración', '00000000', '999999999', 'Minorista')
ON CONFLICT (documento) DO NOTHING;

INSERT INTO productos (codigo, nombre, categoria, precio, stock, estado, id_proveedor)
SELECT 'PR-001', 'Taladro percutor 650 W', 'Herramientas eléctricas', 289.90, 12, 'Disponible', MIN(id_proveedor)
FROM proveedores WHERE empresa = 'Importaciones El Constructor'
ON CONFLICT (codigo) DO NOTHING;
