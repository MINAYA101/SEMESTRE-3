"""Aplicación Flask demostrativa para FerreNova. Proyecto Integrador U4 - Avance 13/16."""
from flask import Flask, render_template, redirect, url_for, flash, request
from forms.producto_form import ProductoForm
from forms.cliente_form import ClienteForm
from forms.proveedor_form import ProveedorForm
from forms.facturacion_form import FacturacionForm
from conexion.conexion import obtener_conexion, cerrar_conexion

app = Flask(__name__)
# Configuración de SECRET_KEY para protección CSRF
app.config["SECRET_KEY"] = "ferre-nova-semana-13-mysql-secret"

SISTEMA = {
    "version": "13.0",
    "avance": "13/16",
    "descripcion": "Gestión ferretera con MySQL y CRUD completo",
}

@app.context_processor
def inject_globals():
    return {"empresa": "FerreNova", "anio": 2026}

@app.route("/")
def inicio():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    
    # Resumen para el dashboard
    cursor.execute("SELECT COUNT(*) as total FROM productos")
    total_prod = cursor.fetchone()['total']
    
    cursor.execute("SELECT COUNT(*) as total FROM clientes")
    total_cli = cursor.fetchone()['total']
    
    cursor.execute("SELECT COUNT(*) as total FROM proveedores")
    total_prov = cursor.fetchone()['total']
    
    cursor.execute("SELECT COUNT(*) as total FROM facturas")
    total_fact = cursor.fetchone()['total']
    
    # Productos recientes con JOIN para mostrar el proveedor
    cursor.execute("""
        SELECT p.*, prov.empresa as proveedor_nombre 
        FROM productos p 
        LEFT JOIN proveedores prov ON p.id_proveedor = prov.id_proveedor 
        LIMIT 3
    """)
    productos_recientes = cursor.fetchall()
    
    cerrar_conexion(conexion, cursor)
    
    resumen = {
        "productos": total_prod, 
        "clientes": total_cli, 
        "proveedores": total_prov, 
        "facturas": total_fact
    }
    
    return render_template(
        "index.html",
        resumen=resumen,
        productos=productos_recientes,
        mensaje="Bienvenido al panel de FerreNova (MySQL)",
        sistema=SISTEMA,
    )

# --- MÓDULO PRODUCTOS (CRUD COMPLETO) ---

@app.route("/productos")
def productos():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    # Uso de JOIN para mostrar el nombre del proveedor en lugar del ID
    cursor.execute("""
        SELECT p.*, prov.empresa as proveedor_nombre 
        FROM productos p 
        LEFT JOIN proveedores prov ON p.id_proveedor = prov.id_proveedor
    """)
    productos_db = cursor.fetchall()
    cerrar_conexion(conexion, cursor)
    return render_template("productos.html", productos=productos_db)

@app.route("/productos/nuevo", methods=["GET", "POST"])
def nuevo_producto():
    form = ProductoForm()
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    
    # Cargar proveedores para el SelectField
    cursor.execute("SELECT id_proveedor, empresa FROM proveedores")
    proveedores = cursor.fetchall()
    form.id_proveedor.choices = [(p['id_proveedor'], p['empresa']) for p in proveedores]
    
    if form.validate_on_submit():
        sql = """INSERT INTO productos (codigo, nombre, categoria, precio, stock, estado, id_proveedor) 
                 VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        valores = (form.codigo.data, form.nombre.data, form.categoria.data, 
                   form.precio.data, form.stock.data, form.estado.data, form.id_proveedor.data)
        
        cursor.execute(sql, valores)
        conexion.commit()
        cerrar_conexion(conexion, cursor)
        flash("Producto agregado correctamente", "success")
        return redirect(url_for('productos'))
    
    cerrar_conexion(conexion, cursor)
    return render_template("formulario_producto.html", form=form, titulo="Nuevo Producto")

@app.route("/productos/editar/<int:id>", methods=["GET", "POST"])
def editar_producto(id):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    
    # Obtener el producto a editar
    cursor.execute("SELECT * FROM productos WHERE id_producto = %s", (id,))
    producto = cursor.fetchone()
    
    if not producto:
        cerrar_conexion(conexion, cursor)
        flash("Producto no encontrado", "danger")
        return redirect(url_for('productos'))
    
    form = ProductoForm()
    
    # Cargar proveedores
    cursor.execute("SELECT id_proveedor, empresa FROM proveedores")
    proveedores = cursor.fetchall()
    form.id_proveedor.choices = [(p['id_proveedor'], p['empresa']) for p in proveedores]
    
    if request.method == 'GET':
        # Pre-cargar datos en el formulario
        form.codigo.data = producto['codigo']
        form.nombre.data = producto['nombre']
        form.categoria.data = producto['categoria']
        form.precio.data = producto['precio']
        form.stock.data = producto['stock']
        form.estado.data = producto['estado']
        form.id_proveedor.data = producto['id_proveedor']
    
    if form.validate_on_submit():
        sql = """UPDATE productos SET codigo=%s, nombre=%s, categoria=%s, precio=%s, stock=%s, estado=%s, id_proveedor=%s 
                 WHERE id_producto=%s"""
        valores = (form.codigo.data, form.nombre.data, form.categoria.data, 
                   form.precio.data, form.stock.data, form.estado.data, form.id_proveedor.data, id)
        
        cursor.execute(sql, valores)
        conexion.commit()
        cerrar_conexion(conexion, cursor)
        flash("Producto actualizado correctamente", "success")
        return redirect(url_for('productos'))
    
    cerrar_conexion(conexion, cursor)
    return render_template("formulario_producto.html", form=form, titulo="Editar Producto")

@app.route("/productos/eliminar/<int:id>", methods=["POST"])
def eliminar_producto(id):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    
    cursor.execute("DELETE FROM productos WHERE id_producto = %s", (id,))
    conexion.commit()
    
    cerrar_conexion(conexion, cursor)
    flash("Producto eliminado correctamente", "warning")
    return redirect(url_for('productos'))

# --- OTROS MÓDULOS (SELECT BÁSICO) ---

@app.route("/clientes")
def clientes():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM clientes")
    clientes_db = cursor.fetchall()
    cerrar_conexion(conexion, cursor)
    return render_template("clientes.html", clientes=clientes_db)

@app.route("/proveedores")
def proveedores():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM proveedores")
    proveedores_db = cursor.fetchall()
    cerrar_conexion(conexion, cursor)
    return render_template("proveedores.html", proveedores=proveedores_db)

@app.route("/facturacion")
def facturacion():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("""
        SELECT f.*, c.nombre as cliente_nombre 
        FROM facturas f 
        LEFT JOIN clientes c ON f.id_cliente = c.id_cliente
    """)
    facturas_db = cursor.fetchall()
    total_facturado = sum(float(f["total"]) for f in facturas_db)
    cerrar_conexion(conexion, cursor)
    return render_template("facturacion.html", facturas=facturas_db, total_facturado=total_facturado)

@app.errorhandler(404)
def pagina_no_encontrada(error):
    return render_template("404.html"), 404

if __name__ == "__main__":
    app.run(debug=True)
