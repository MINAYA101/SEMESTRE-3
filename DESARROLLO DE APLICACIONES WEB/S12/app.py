"""Aplicación Flask demostrativa para FerreNova. Proyecto Integrador U3 - Avance 12/16."""
import os
import sqlite3
from flask import Flask, render_template, redirect, url_for, flash, request
from forms.producto_form import ProductoForm
from forms.cliente_form import ClienteForm
from forms.proveedor_form import ProveedorForm
from forms.facturacion_form import FacturacionForm

app = Flask(__name__)
# Configuración de SECRET_KEY para protección CSRF
app.config["SECRET_KEY"] = "ferre-nova-semana-12-secret-key"

# Ruta de la base de datos SQLite
DATABASE = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data', 'ferreteria.db')

def get_db_connection():
    """Establece una conexión con la base de datos SQLite."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Permite acceder a las columnas por nombre
    return conn

def init_db():
    """Inicializa la base de datos y crea la tabla de productos si no existe."""
    if not os.path.exists(os.path.dirname(DATABASE)):
        os.makedirs(os.path.dirname(DATABASE))
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Crear tabla de productos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo TEXT NOT NULL,
            nombre TEXT NOT NULL,
            categoria TEXT NOT NULL,
            precio REAL NOT NULL,
            stock INTEGER NOT NULL,
            estado TEXT NOT NULL
        )
    ''')
    
    # Insertar datos iniciales si la tabla está vacía
    cursor.execute('SELECT COUNT(*) FROM productos')
    if cursor.fetchone()[0] == 0:
        datos_iniciales = [
            ("PR-001", "Taladro percutor 650 W", "Herramientas eléctricas", 289.90, 12, "Disponible"),
            ("PR-002", "Juego de destornilladores", "Herramientas manuales", 74.50, 25, "Disponible"),
            ("PR-003", "Pintura látex blanca 4 L", "Pinturas", 96.00, 8, "Stock bajo"),
            ("PR-004", "Cinta métrica profesional 5 m", "Medición", 32.90, 0, "Agotado"),
            ("PR-005", "Caja de tornillos 1/2 pulgada", "Fijaciones", 28.75, 43, "Disponible"),
        ]
        cursor.executemany('INSERT INTO productos (codigo, nombre, categoria, precio, stock, estado) VALUES (?, ?, ?, ?, ?, ?)', datos_iniciales)
    
    conn.commit()
    conn.close()

# Inicializar la base de datos al arrancar la aplicación
init_db()

# Mantener datos temporales para otros módulos (Semana 11)
CLIENTES = [
    {"id": "CL-001", "nombre": "Constructora Andina S.A.C.", "documento": "20601234567", "telefono": "987 654 321", "tipo": "Empresa"},
    {"id": "CL-002", "nombre": "María Fernanda Torres", "documento": "74215698", "telefono": "945 221 876", "tipo": "Persona"},
    {"id": "CL-003", "nombre": "Servicios del Pacífico E.I.R.L.", "documento": "20598765431", "telefono": "986 110 245", "tipo": "Empresa"},
]
PROVEEDORES = [
    {"id": "PV-001", "empresa": "Importaciones El Constructor", "contacto": "Jorge Salazar", "rubro": "Herramientas", "telefono": "01 445 7832"},
    {"id": "PV-002", "empresa": "Pinturas Colorama S.A.", "contacto": "Lucía Mendoza", "rubro": "Pinturas", "telefono": "01 377 9210"},
    {"id": "PV-003", "empresa": "Fijaciones Industriales Perú", "contacto": "Carlos Rivas", "rubro": "Fijaciones", "telefono": "01 512 4680"},
]
FACTURAS = [
    {"numero": "F001-000124", "cliente": "Constructora Andina S.A.C.", "fecha": "08/08/2026", "total": 1250.80, "estado": "Pagada"},
    {"numero": "F001-000125", "cliente": "María Fernanda Torres", "fecha": "09/08/2026", "total": 347.40, "estado": "Pendiente"},
    {"numero": "F001-000126", "cliente": "Servicios del Pacífico E.I.R.L.", "fecha": "10/08/2026", "total": 890.00, "estado": "Pagada"},
]
SISTEMA = {
    "version": "12.0",
    "avance": "12/16",
    "descripcion": "Gestión ferretera con persistencia SQLite",
}

@app.context_processor
def inject_globals():
    return {"empresa": "FerreNova", "anio": 2026}

@app.route("/")
def inicio():
    conn = get_db_connection()
    total_productos = conn.execute('SELECT COUNT(*) FROM productos').fetchone()[0]
    productos_recientes = conn.execute('SELECT * FROM productos LIMIT 3').fetchall()
    conn.close()
    
    resumen = {
        "productos": total_productos, 
        "clientes": len(CLIENTES), 
        "proveedores": len(PROVEEDORES), 
        "facturas": len(FACTURAS)
    }
    mensaje = "Bienvenido al panel de FerreNova"
    return render_template(
        "index.html",
        resumen=resumen,
        productos=productos_recientes,
        mensaje=mensaje,
        sistema=SISTEMA,
    )

@app.route("/productos")
def productos():
    conn = get_db_connection()
    productos_db = conn.execute('SELECT * FROM productos').fetchall()
    conn.close()
    return render_template("productos.html", productos=productos_db)

@app.route("/productos/nuevo", methods=["GET", "POST"])
def nuevo_producto():
    form = ProductoForm()
    if form.validate_on_submit():
        codigo = form.codigo.data
        nombre = form.nombre.data
        categoria = form.categoria.data
        precio = form.precio.data
        stock = form.stock.data
        estado = form.estado.data
        
        # Operación INSERT en SQLite
        conn = get_db_connection()
        conn.execute('INSERT INTO productos (codigo, nombre, categoria, precio, stock, estado) VALUES (?, ?, ?, ?, ?, ?)',
                     (codigo, nombre, categoria, precio, stock, estado))
        conn.commit()
        conn.close()
        
        return redirect(url_for('productos'))
    return render_template("formulario_producto.html", form=form)

@app.route("/clientes")
def clientes():
    return render_template("clientes.html", clientes=CLIENTES)

@app.route("/clientes/nuevo", methods=["GET", "POST"])
def nuevo_cliente():
    form = ClienteForm()
    if form.validate_on_submit():
        nuevo = {
            "id": f"CL-00{len(CLIENTES)+1}",
            "nombre": form.nombre.data,
            "documento": form.documento.data,
            "telefono": form.telefono.data,
            "tipo": form.tipo.data
        }
        CLIENTES.append(nuevo)
        return redirect(url_for('clientes'))
    return render_template("formulario_cliente.html", form=form)

@app.route("/proveedores")
def proveedores():
    return render_template("proveedores.html", proveedores=PROVEEDORES)

@app.route("/proveedores/nuevo", methods=["GET", "POST"])
def nuevo_proveedor():
    form = ProveedorForm()
    if form.validate_on_submit():
        nuevo = {
            "id": f"PV-00{len(PROVEEDORES)+1}",
            "empresa": form.empresa.data,
            "contacto": form.contacto.data,
            "rubro": form.rubro.data,
            "telefono": form.telefono.data
        }
        PROVEEDORES.append(nuevo)
        return redirect(url_for('proveedores'))
    return render_template("formulario_proveedor.html", form=form)

@app.route("/facturacion")
def facturacion():
    total_facturado = sum(factura["total"] for factura in FACTURAS)
    return render_template("facturacion.html", facturas=FACTURAS, total_facturado=total_facturado)

@app.route("/facturacion/nuevo", methods=["GET", "POST"])
def nueva_factura():
    form = FacturacionForm()
    if form.validate_on_submit():
        nuevo = {
            "numero": form.numero.data,
            "cliente": form.cliente.data,
            "fecha": form.fecha.data,
            "total": form.total.data,
            "estado": form.estado.data
        }
        FACTURAS.append(nuevo)
        return redirect(url_for('facturacion'))
    return render_template("formulario_facturacion.html", form=form)

@app.errorhandler(404)
def pagina_no_encontrada(error):
    return render_template("404.html"), 404

if __name__ == "__main__":
    app.run(debug=True)
