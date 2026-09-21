-- Esquema de base de datos para FerreNova
-- Proyecto Integrador U4 - Avance 14/16
CREATE DATABASE IF NOT EXISTS ferreteria_db;
USE ferreteria_db;

CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS proveedores (
    id_proveedor INT AUTO_INCREMENT PRIMARY KEY,
    empresa VARCHAR(100) NOT NULL,
    contacto VARCHAR(100) NOT NULL,
    rubro VARCHAR(50) NOT NULL,
    telefono VARCHAR(15) NOT NULL
);

CREATE TABLE IF NOT EXISTS productos (
    id_producto INT AUTO_INCREMENT PRIMARY KEY,
    codigo VARCHAR(20) NOT NULL UNIQUE,
    nombre VARCHAR(100) NOT NULL,
    categoria VARCHAR(50) NOT NULL,
    precio DECIMAL(10, 2) NOT NULL,
    stock INT NOT NULL,
    estado VARCHAR(20) NOT NULL,
    id_proveedor INT,
    FOREIGN KEY (id_proveedor) REFERENCES proveedores(id_proveedor) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS clientes (
    id_cliente INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    documento VARCHAR(20) NOT NULL UNIQUE,
    telefono VARCHAR(15) NOT NULL,
    tipo VARCHAR(20) NOT NULL
);

CREATE TABLE IF NOT EXISTS facturas (
    id_factura INT AUTO_INCREMENT PRIMARY KEY,
    numero VARCHAR(20) NOT NULL UNIQUE,
    id_cliente INT,
    fecha VARCHAR(20) NOT NULL,
    total DECIMAL(10, 2) NOT NULL,
    estado VARCHAR(20) NOT NULL,
    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente) ON DELETE CASCADE
);

INSERT INTO proveedores (empresa, contacto, rubro, telefono) VALUES
('Importaciones El Constructor', 'Jorge Salazar', 'Herramientas', '01 445 7832'),
('Pinturas Colorama S.A.', 'Lucía Mendoza', 'Pinturas', '01 377 9210');

INSERT INTO productos (codigo, nombre, categoria, precio, stock, estado, id_proveedor) VALUES
('PR-001', 'Taladro percutor 650 W', 'Herramientas eléctricas', 289.90, 12, 'Disponible', 1),
('PR-002', 'Juego de destornilladores', 'Herramientas manuales', 74.50, 25, 'Disponible', 1),
('PR-003', 'Pintura látex blanca 4 L', 'Pinturas', 96.00, 8, 'Stock bajo', 2);
