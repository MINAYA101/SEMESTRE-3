"""Aplicación Flask demostrativa para FerreNova. Proyecto Integrador U3 - Avance 11/16."""
from flask import Flask, render_template, redirect, url_for, flash, request
from forms.producto_form import ProductoForm
from forms.cliente_form import ClienteForm
from forms.proveedor_form import ProveedorForm
from forms.facturacion_form import FacturacionForm

app = Flask(__name__)
# Configuración de SECRET_KEY para protección CSRF
app.config["SECRET_KEY"] = "ferre-nova-semana-11-secret-key"

PRODUCTOS = [
    {"codigo": "PR-001", "nombre": "Taladro percutor 650 W", "categoria": "Herramientas eléctricas", "precio": 289.90, "stock": 12, "estado": "Disponible"},
    {"codigo": "PR-002", "nombre": "Juego de destornilladores", "categoria": "Herramientas manuales", "precio": 74.50, "stock": 25, "estado": "Disponible"},
    {"codigo": "PR-003", "nombre": "Pintura látex blanca 4 L", "categoria": "Pinturas", "precio": 96.00, "stock": 8, "estado": "Stock bajo"},
    {"codigo": "PR-004", "nombre": "Cinta métrica profesional 5 m", "categoria": "Medición", "precio": 32.90, "stock": 0, "estado": "Agotado"},
    {"codigo": "PR-005", "nombre": "Caja de tornillos 1/2 pulgada", "categoria": "Fijaciones", "precio": 28.75, "stock": 43, "estado": "Disponible"},
]
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
    "version": "11.0",
    "avance": "11/16",
    "descripcion": "Gestión ferretera con validación de formularios",
}

@app.context_processor
def inject_globals():
    return {"empresa": "FerreNova", "anio": 2026}

@app.route("/")
def inicio():
    resumen = {"productos": len(PRODUCTOS), "clientes": len(CLIENTES), "proveedores": len(PROVEEDORES), "facturas": len(FACTURAS)}
    mensaje = "Bienvenido al panel de FerreNova"
    return render_template(
        "index.html",
        resumen=resumen,
        productos=PRODUCTOS[:3],
        mensaje=mensaje,
        sistema=SISTEMA,
    )

@app.route("/productos")
def productos():
    return render_template("productos.html", productos=PRODUCTOS)

@app.route("/productos/nuevo", methods=["GET", "POST"])
def nuevo_producto():
    form = ProductoForm()
    if form.validate_on_submit():
        nuevo = {
            "codigo": form.codigo.data,
            "nombre": form.nombre.data,
            "categoria": form.categoria.data,
            "precio": form.precio.data,
            "stock": form.stock.data,
            "estado": form.estado.data
        }
        PRODUCTOS.append(nuevo)
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
