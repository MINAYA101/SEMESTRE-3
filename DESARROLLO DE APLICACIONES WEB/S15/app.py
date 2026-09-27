"""FerreNova - Proyecto Integrador U4, Avance 15/16.
PostgreSQL, CRUD relacionado y autenticación con Flask-Login.
"""
import os
from flask import Flask, flash, redirect, render_template, request, url_for
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from psycopg2 import Error
from werkzeug.security import check_password_hash, generate_password_hash

from conexion.conexion import cerrar_conexion, cursor_diccionario, obtener_conexion
from forms.entidades_form import ClienteForm, ProveedorForm
from forms.facturacion_form import FacturacionForm
from forms.login_form import LoginForm
from forms.producto_form import ProductoForm
from forms.usuario_form import UsuarioForm
from models import Usuario

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("FERRENOVA_SECRET_KEY", "cambia-esta-clave-en-produccion")
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message = "Debes iniciar sesión para acceder a esta sección."
login_manager.login_message_category = "warning"
SISTEMA = {"version": "15.0", "avance": "15/16", "descripcion": "CRUD relacional con PostgreSQL y autenticación"}

@login_manager.user_loader
def load_user(user_id):
    return Usuario.obtener_por_id(user_id)

@app.context_processor
def inject_globals():
    return {"empresa": "FerreNova", "anio": 2026}

def db_error(mensaje):
    flash(mensaje, "danger")

@app.route("/")
@login_required
def inicio():
    conexion = obtener_conexion()
    if not conexion:
        db_error("No fue posible conectar con PostgreSQL.")
        return render_template("index.html", resumen={}, productos=[], mensaje="Base de datos no disponible", sistema=SISTEMA)
    cursor = cursor_diccionario(conexion)
    try:
        resumen = {}
        for tabla, clave in (("productos", "productos"), ("clientes", "clientes"), ("proveedores", "proveedores"), ("facturas", "facturas")):
            cursor.execute(f"SELECT COUNT(*) AS total FROM {tabla}")
            resumen[clave] = cursor.fetchone()["total"]
        cursor.execute("SELECT p.*, prov.empresa AS proveedor_nombre FROM productos p LEFT JOIN proveedores prov ON p.id_proveedor = prov.id_proveedor ORDER BY p.id_producto DESC LIMIT 3")
        productos = cursor.fetchall()
    finally:
        cerrar_conexion(conexion, cursor)
    return render_template("index.html", resumen=resumen, productos=productos, mensaje="Bienvenido al panel de FerreNova", sistema=SISTEMA)

@app.route("/registro", methods=["GET", "POST"])
def registro():
    if current_user.is_authenticated:
        return redirect(url_for("inicio"))
    form = UsuarioForm()
    if form.validate_on_submit():
        conexion = obtener_conexion()
        if not conexion:
            db_error("No fue posible conectar con PostgreSQL.")
            return render_template("registro.html", form=form)
        cursor = conexion.cursor()
        try:
            cursor.execute("INSERT INTO usuarios (usuario, password) VALUES (%s, %s)", (form.usuario.data.strip(), generate_password_hash(form.password.data)))
            conexion.commit(); flash("Usuario registrado correctamente. Ya puedes iniciar sesión.", "success"); return redirect(url_for("login"))
        except Error:
            conexion.rollback(); db_error("El usuario ya existe o no pudo registrarse.")
        finally:
            cerrar_conexion(conexion, cursor)
    return render_template("registro.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("inicio"))
    form = LoginForm()
    if form.validate_on_submit():
        usuario = Usuario.obtener_por_nombre(form.usuario.data.strip())
        if usuario and check_password_hash(usuario.password, form.password.data):
            login_user(usuario); flash(f"Bienvenido, {usuario.usuario}.", "success")
            siguiente = request.args.get("next")
            return redirect(siguiente if siguiente and siguiente.startswith("/") else url_for("inicio"))
        flash("Usuario o contraseña incorrectos.", "danger")
    return render_template("login.html", form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user(); flash("La sesión se cerró correctamente.", "info"); return redirect(url_for("login"))

# -------------------- PRODUCTOS: CRUD --------------------
@app.route("/productos")
@login_required
def productos():
    conexion = obtener_conexion(); cursor = cursor_diccionario(conexion)
    try:
        cursor.execute("SELECT p.*, prov.empresa AS proveedor_nombre FROM productos p LEFT JOIN proveedores prov ON p.id_proveedor = prov.id_proveedor ORDER BY p.id_producto")
        datos = cursor.fetchall()
    finally: cerrar_conexion(conexion, cursor)
    return render_template("productos.html", productos=datos)

@app.route("/productos/nuevo", methods=["GET", "POST"])
@login_required
def nuevo_producto():
    form = ProductoForm(); conexion = obtener_conexion(); cursor = cursor_diccionario(conexion)
    try:
        cursor.execute("SELECT id_proveedor, empresa FROM proveedores ORDER BY empresa")
        form.id_proveedor.choices = [(p["id_proveedor"], p["empresa"]) for p in cursor.fetchall()]
        if form.validate_on_submit():
            cursor.execute("INSERT INTO productos (codigo, nombre, categoria, precio, stock, estado, id_proveedor) VALUES (%s,%s,%s,%s,%s,%s,%s)", (form.codigo.data, form.nombre.data, form.categoria.data, form.precio.data, form.stock.data, form.estado.data, form.id_proveedor.data))
            conexion.commit(); flash("Producto creado correctamente.", "success"); return redirect(url_for("productos"))
    except Error:
        conexion.rollback(); db_error("No fue posible crear el producto. Revisa que el código sea único.")
    finally: cerrar_conexion(conexion, cursor)
    return render_template("formulario_producto.html", form=form, titulo="Nuevo producto")

@app.route("/productos/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar_producto(id):
    conexion = obtener_conexion(); cursor = cursor_diccionario(conexion)
    try:
        cursor.execute("SELECT * FROM productos WHERE id_producto = %s", (id,)); registro = cursor.fetchone()
        if not registro: flash("Producto no encontrado.", "warning"); return redirect(url_for("productos"))
        form = ProductoForm(); cursor.execute("SELECT id_proveedor, empresa FROM proveedores ORDER BY empresa")
        form.id_proveedor.choices = [(p["id_proveedor"], p["empresa"]) for p in cursor.fetchall()]
        if request.method == "GET":
            for campo in ("codigo", "nombre", "categoria", "precio", "stock", "estado", "id_proveedor"): getattr(form, campo).data = registro[campo]
        if form.validate_on_submit():
            cursor.execute("UPDATE productos SET codigo=%s,nombre=%s,categoria=%s,precio=%s,stock=%s,estado=%s,id_proveedor=%s WHERE id_producto=%s", (form.codigo.data, form.nombre.data, form.categoria.data, form.precio.data, form.stock.data, form.estado.data, form.id_proveedor.data, id))
            conexion.commit(); flash("Producto actualizado correctamente.", "success"); return redirect(url_for("productos"))
    except Error:
        conexion.rollback(); db_error("No fue posible actualizar el producto.")
    finally: cerrar_conexion(conexion, cursor)
    return render_template("formulario_producto.html", form=form, titulo="Editar producto")

@app.route("/productos/eliminar/<int:id>", methods=["POST"])
@login_required
def eliminar_producto(id):
    conexion = obtener_conexion(); cursor = conexion.cursor()
    try:
        cursor.execute("DELETE FROM productos WHERE id_producto = %s", (id,)); conexion.commit(); flash("Producto eliminado correctamente.", "warning")
    except Error:
        conexion.rollback(); db_error("No fue posible eliminar el producto.")
    finally: cerrar_conexion(conexion, cursor)
    return redirect(url_for("productos"))

# -------------------- PROVEEDORES: CRUD --------------------
@app.route("/proveedores")
@login_required
def proveedores():
    conexion = obtener_conexion(); cursor = cursor_diccionario(conexion)
    try: cursor.execute("SELECT * FROM proveedores ORDER BY id_proveedor"); datos = cursor.fetchall()
    finally: cerrar_conexion(conexion, cursor)
    return render_template("proveedores.html", proveedores=datos)

@app.route("/proveedores/nuevo", methods=["GET", "POST"])
@login_required
def nuevo_proveedor():
    form = ProveedorForm()
    if form.validate_on_submit():
        conexion = obtener_conexion(); cursor = conexion.cursor()
        try:
            cursor.execute("INSERT INTO proveedores (empresa, contacto, rubro, telefono) VALUES (%s,%s,%s,%s)", (form.empresa.data, form.contacto.data, form.rubro.data, form.telefono.data)); conexion.commit(); flash("Proveedor creado correctamente.", "success"); return redirect(url_for("proveedores"))
        except Error: conexion.rollback(); db_error("No fue posible crear el proveedor.")
        finally: cerrar_conexion(conexion, cursor)
    return render_template("formulario_entidad.html", form=form, titulo="Nuevo proveedor", entidad="proveedor")

@app.route("/proveedores/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar_proveedor(id):
    conexion = obtener_conexion(); cursor = cursor_diccionario(conexion)
    try:
        cursor.execute("SELECT * FROM proveedores WHERE id_proveedor=%s", (id,)); registro = cursor.fetchone()
    finally: cerrar_conexion(conexion, cursor)
    if not registro: flash("Proveedor no encontrado.", "warning"); return redirect(url_for("proveedores"))
    form = ProveedorForm()
    if request.method == "GET":
        for campo in ("empresa", "contacto", "rubro", "telefono"): getattr(form, campo).data = registro[campo]
    if form.validate_on_submit():
        conexion = obtener_conexion(); cursor = conexion.cursor()
        try:
            cursor.execute("UPDATE proveedores SET empresa=%s,contacto=%s,rubro=%s,telefono=%s WHERE id_proveedor=%s", (form.empresa.data, form.contacto.data, form.rubro.data, form.telefono.data, id)); conexion.commit(); flash("Proveedor actualizado correctamente.", "success"); return redirect(url_for("proveedores"))
        except Error: conexion.rollback(); db_error("No fue posible actualizar el proveedor.")
        finally: cerrar_conexion(conexion, cursor)
    return render_template("formulario_entidad.html", form=form, titulo="Editar proveedor", entidad="proveedor")

@app.route("/proveedores/eliminar/<int:id>", methods=["POST"])
@login_required
def eliminar_proveedor(id):
    conexion = obtener_conexion(); cursor = conexion.cursor()
    try: cursor.execute("DELETE FROM proveedores WHERE id_proveedor=%s", (id,)); conexion.commit(); flash("Proveedor eliminado correctamente.", "warning")
    except Error: conexion.rollback(); db_error("No se puede eliminar un proveedor relacionado o inexistente.")
    finally: cerrar_conexion(conexion, cursor)
    return redirect(url_for("proveedores"))

# -------------------- CLIENTES: CRUD --------------------
@app.route("/clientes")
@login_required
def clientes():
    conexion = obtener_conexion(); cursor = cursor_diccionario(conexion)
    try: cursor.execute("SELECT * FROM clientes ORDER BY id_cliente"); datos = cursor.fetchall()
    finally: cerrar_conexion(conexion, cursor)
    return render_template("clientes.html", clientes=datos)

@app.route("/clientes/nuevo", methods=["GET", "POST"])
@login_required
def nuevo_cliente():
    form = ClienteForm()
    if form.validate_on_submit():
        conexion = obtener_conexion(); cursor = conexion.cursor()
        try:
            cursor.execute("INSERT INTO clientes (nombre, documento, telefono, tipo) VALUES (%s,%s,%s,%s)", (form.nombre.data, form.documento.data, form.telefono.data, form.tipo.data)); conexion.commit(); flash("Cliente creado correctamente.", "success"); return redirect(url_for("clientes"))
        except Error: conexion.rollback(); db_error("No fue posible crear el cliente. Revisa que el documento sea único.")
        finally: cerrar_conexion(conexion, cursor)
    return render_template("formulario_entidad.html", form=form, titulo="Nuevo cliente", entidad="cliente")

@app.route("/clientes/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar_cliente(id):
    conexion = obtener_conexion(); cursor = cursor_diccionario(conexion)
    try:
        cursor.execute("SELECT * FROM clientes WHERE id_cliente=%s", (id,)); registro = cursor.fetchone()
    finally: cerrar_conexion(conexion, cursor)
    if not registro: flash("Cliente no encontrado.", "warning"); return redirect(url_for("clientes"))
    form = ClienteForm()
    if request.method == "GET":
        for campo in ("nombre", "documento", "telefono", "tipo"): getattr(form, campo).data = registro[campo]
    if form.validate_on_submit():
        conexion = obtener_conexion(); cursor = conexion.cursor()
        try:
            cursor.execute("UPDATE clientes SET nombre=%s,documento=%s,telefono=%s,tipo=%s WHERE id_cliente=%s", (form.nombre.data, form.documento.data, form.telefono.data, form.tipo.data, id)); conexion.commit(); flash("Cliente actualizado correctamente.", "success"); return redirect(url_for("clientes"))
        except Error: conexion.rollback(); db_error("No fue posible actualizar el cliente.")
        finally: cerrar_conexion(conexion, cursor)
    return render_template("formulario_entidad.html", form=form, titulo="Editar cliente", entidad="cliente")

@app.route("/clientes/eliminar/<int:id>", methods=["POST"])
@login_required
def eliminar_cliente(id):
    conexion = obtener_conexion(); cursor = conexion.cursor()
    try: cursor.execute("DELETE FROM clientes WHERE id_cliente=%s", (id,)); conexion.commit(); flash("Cliente eliminado correctamente.", "warning")
    except Error: conexion.rollback(); db_error("No se puede eliminar un cliente con facturas asociadas.")
    finally: cerrar_conexion(conexion, cursor)
    return redirect(url_for("clientes"))

@app.route("/facturacion")
@login_required
def facturacion():
    conexion = obtener_conexion(); cursor = cursor_diccionario(conexion)
    try: cursor.execute("SELECT f.*, c.nombre AS cliente_nombre FROM facturas f LEFT JOIN clientes c ON f.id_cliente=c.id_cliente ORDER BY f.id_factura DESC"); datos = cursor.fetchall()
    finally: cerrar_conexion(conexion, cursor)
    return render_template("facturacion.html", facturas=datos, total_facturado=sum(float(x["total"]) for x in datos))

@app.errorhandler(404)
def pagina_no_encontrada(error): return render_template("404.html"), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")), debug=os.getenv("FLASK_DEBUG", "0") == "1")
