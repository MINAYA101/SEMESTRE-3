"""Aplicación Flask demostrativa para FerreNova. Proyecto Integrador U3 - Avance 9/16."""
from flask import Flask, render_template

app = Flask(__name__)
app.config["SECRET_KEY"] = "ferre-nova-semana9"

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

@app.context_processor
def inject_globals():
    return {"empresa": "FerreNova", "anio": 2026}

@app.route("/")
def inicio():
    resumen = {"productos": len(PRODUCTOS), "clientes": len(CLIENTES), "proveedores": len(PROVEEDORES), "facturas": len(FACTURAS)}
    return render_template("index.html", resumen=resumen, productos=PRODUCTOS[:3])

@app.route("/productos")
def productos():
    return render_template("productos.html", productos=PRODUCTOS)

@app.route("/clientes")
def clientes():
    return render_template("clientes.html", clientes=CLIENTES)

@app.route("/proveedores")
def proveedores():
    return render_template("proveedores.html", proveedores=PROVEEDORES)

@app.route("/facturacion")
def facturacion():
    total_facturado = sum(factura["total"] for factura in FACTURAS)
    return render_template("facturacion.html", facturas=FACTURAS, total_facturado=total_facturado)

@app.errorhandler(404)
def pagina_no_encontrada(error):
    return render_template("404.html"), 404

if __name__ == "__main__":
    app.run(debug=True)
