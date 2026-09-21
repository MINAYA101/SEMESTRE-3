"""Aplicación Flask de FerreNova: CRUD MySQL y autenticación segura."""
import os

from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from mysql.connector import Error
from werkzeug.security import check_password_hash, generate_password_hash

from conexion.conexion import obtener_conexion, cerrar_conexion
from forms.login_form import LoginForm
from forms.usuario_form import UsuarioForm
from forms.producto_form import ProductoForm
from forms.cliente_form import ClienteForm
from forms.proveedor_form import ProveedorForm
from forms.facturacion_form import FacturacionForm
from models import Usuario

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("FERRENOVA_SECRET_KEY", "cambia-esta-clave-en-produccion")

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message = "Debes iniciar sesión para acceder a esta sección."
login_manager.login_message_category = "warning"

SISTEMA = {"version": "14.0", "avance": "14/16", "descripcion": "Gestión ferretera con MySQL, CRUD y autenticación"}

@login_manager.user_loader
def load_user(user_id):
    return Usuario.obtener_por_id(user_id)

@app.context_processor
def inject_globals():
    return {"empresa": "FerreNova", "anio": 2026}

@app.route("/")
def inicio():
    if not current_user.is_authenticated:
        return redirect(url_for("login"))
    conexion = obtener_conexion()
    if not conexion:
        flash("No fue posible conectar con la base de datos.", "danger")
        return render_template("index.html", resumen={}, productos=[], mensaje="Base de datos no disponible", sistema=SISTEMA)
    cursor = conexion.cursor(dictionary=True)
    try:
        resumen = {}
        for tabla, clave in (("productos", "productos"), ("clientes", "clientes"), ("proveedores", "proveedores"), ("facturas", "facturas")):
            cursor.execute(f"SELECT COUNT(*) AS total FROM {tabla}")
            resumen[clave] = cursor.fetchone()["total"]
        cursor.execute("SELECT p.*, prov.empresa AS proveedor_nombre FROM productos p LEFT JOIN proveedores prov ON p.id_proveedor = prov.id_proveedor LIMIT 3")
        productos_recientes = cursor.fetchall()
    finally:
        cerrar_conexion(conexion, cursor)
    return render_template("index.html", resumen=resumen, productos=productos_recientes, mensaje="Bienvenido al panel de FerreNova", sistema=SISTEMA)

@app.route("/registro", methods=["GET", "POST"])
def registro():
    if current_user.is_authenticated:
        return redirect(url_for("inicio"))
    form = UsuarioForm()
    if form.validate_on_submit():
        conexion = obtener_conexion()
        if not conexion:
            flash("No fue posible conectar con la base de datos.", "danger")
            return render_template("registro.html", form=form)
        cursor = conexion.cursor()
        try:
            password_hash = generate_password_hash(form.password.data)
            cursor.execute("INSERT INTO usuarios (usuario, password) VALUES (%s, %s)", (form.usuario.data.strip(), password_hash))
            conexion.commit()
            flash("Usuario registrado correctamente. Ya puedes iniciar sesión.", "success")
            return redirect(url_for("login"))
        except Error:
            conexion.rollback()
            flash("El nombre de usuario ya existe o no pudo registrarse.", "danger")
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
            login_user(usuario)
            flash(f"Bienvenido, {usuario.usuario}.", "success")
            siguiente = request.args.get("next")
            return redirect(siguiente if siguiente and siguiente.startswith("/") else url_for("inicio"))
        flash("Usuario o contraseña incorrectos.", "danger")
    return render_template("login.html", form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("La sesión se cerró correctamente.", "info")
    return redirect(url_for("login"))

@app.route("/productos")
@login_required
def productos():
    conexion = obtener_conexion(); cursor = conexion.cursor(dictionary=True)
    try:
        cursor.execute("SELECT p.*, prov.empresa AS proveedor_nombre FROM productos p LEFT JOIN proveedores prov ON p.id_proveedor = prov.id_proveedor")
        productos_db = cursor.fetchall()
    finally:
        cerrar_conexion(conexion, cursor)
    return render_template("productos.html", productos=productos_db)

@app.route("/productos/nuevo", methods=["GET", "POST"])
@login_required
def nuevo_producto():
    form = ProductoForm(); conexion = obtener_conexion(); cursor = conexion.cursor(dictionary=True)
    try:
        cursor.execute("SELECT id_proveedor, empresa FROM proveedores")
        form.id_proveedor.choices = [(p["id_proveedor"], p["empresa"]) for p in cursor.fetchall()]
        if form.validate_on_submit():
            cursor.execute("INSERT INTO productos (codigo, nombre, categoria, precio, stock, estado, id_proveedor) VALUES (%s, %s, %s, %s, %s, %s, %s)", (form.codigo.data, form.nombre.data, form.categoria.data, form.precio.data, form.stock.data, form.estado.data, form.id_proveedor.data))
            conexion.commit(); flash("Producto agregado correctamente", "success"); return redirect(url_for("productos"))
    except Error:
        conexion.rollback(); flash("No fue posible guardar el producto. Verifica el código.", "danger")
    finally:
        cerrar_conexion(conexion, cursor)
    return render_template("formulario_producto.html", form=form, titulo="Nuevo Producto")

@app.route("/productos/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar_producto(id):
    conexion = obtener_conexion(); cursor = conexion.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM productos WHERE id_producto = %s", (id,)); producto = cursor.fetchone()
        if not producto:
            flash("Producto no encontrado", "danger"); return redirect(url_for("productos"))
        form = ProductoForm(); cursor.execute("SELECT id_proveedor, empresa FROM proveedores")
        form.id_proveedor.choices = [(p["id_proveedor"], p["empresa"]) for p in cursor.fetchall()]
        if request.method == "GET":
            for campo in ("codigo", "nombre", "categoria", "precio", "stock", "estado", "id_proveedor"):
                getattr(form, campo).data = producto[campo]
        if form.validate_on_submit():
            cursor.execute("UPDATE productos SET codigo=%s, nombre=%s, categoria=%s, precio=%s, stock=%s, estado=%s, id_proveedor=%s WHERE id_producto=%s", (form.codigo.data, form.nombre.data, form.categoria.data, form.precio.data, form.stock.data, form.estado.data, form.id_proveedor.data, id))
            conexion.commit(); flash("Producto actualizado correctamente", "success"); return redirect(url_for("productos"))
    except Error:
        conexion.rollback(); flash("No fue posible actualizar el producto.", "danger")
    finally:
        cerrar_conexion(conexion, cursor)
    return render_template("formulario_producto.html", form=form, titulo="Editar Producto")

@app.route("/productos/eliminar/<int:id>", methods=["POST"])
@login_required
def eliminar_producto(id):
    conexion = obtener_conexion(); cursor = conexion.cursor()
    try:
        cursor.execute("DELETE FROM productos WHERE id_producto = %s", (id,)); conexion.commit(); flash("Producto eliminado correctamente", "warning")
    finally:
        cerrar_conexion(conexion, cursor)
    return redirect(url_for("productos"))

@app.route("/clientes")
@login_required
def clientes():
    conexion = obtener_conexion(); cursor = conexion.cursor(dictionary=True)
    try: cursor.execute("SELECT * FROM clientes"); datos = cursor.fetchall()
    finally: cerrar_conexion(conexion, cursor)
    return render_template("clientes.html", clientes=datos)

@app.route("/proveedores")
@login_required
def proveedores():
    conexion = obtener_conexion(); cursor = conexion.cursor(dictionary=True)
    try: cursor.execute("SELECT * FROM proveedores"); datos = cursor.fetchall()
    finally: cerrar_conexion(conexion, cursor)
    return render_template("proveedores.html", proveedores=datos)

@app.route("/facturacion")
@login_required
def facturacion():
    conexion = obtener_conexion(); cursor = conexion.cursor(dictionary=True)
    try:
        cursor.execute("SELECT f.*, c.nombre AS cliente_nombre FROM facturas f LEFT JOIN clientes c ON f.id_cliente = c.id_cliente")
        datos = cursor.fetchall()
    finally: cerrar_conexion(conexion, cursor)
    return render_template("facturacion.html", facturas=datos, total_facturado=sum(float(f["total"]) for f in datos))

@app.errorhandler(404)
def pagina_no_encontrada(error):
    return render_template("404.html"), 404

if __name__ == "__main__":
    app.run(debug=True)
