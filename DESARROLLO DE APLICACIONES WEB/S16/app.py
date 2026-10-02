"""FerreNova · Proyecto Final — Gestión integral para una ferretería."""
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

app=Flask(__name__)
app.config['SECRET_KEY']=os.getenv('FERRENOVA_SECRET_KEY','cambia-esta-clave-en-produccion')
login_manager=LoginManager(app); login_manager.login_view='login'; login_manager.login_message='Debes iniciar sesión para acceder a esta sección.'; login_manager.login_message_category='warning'
SISTEMA={'version':'16.0','avance':'16/16','descripcion':'Gestión integral de inventario, clientes, proveedores y facturación'}
@login_manager.user_loader
def load_user(user_id): return Usuario.obtener_por_id(user_id)
@app.context_processor
def inject_globals(): return {'empresa':'FerreNova','anio':2026}
def db_error(mensaje): flash(mensaje,'danger')
def con():
    conexion=obtener_conexion()
    if not conexion: db_error('No fue posible conectar con la base de datos. Verifica la configuración.')
    return conexion

@app.route('/')
@login_required
def inicio():
    conexion=con()
    if not conexion: return render_template('index.html',resumen={},productos=[],mensaje='Base de datos no disponible',sistema=SISTEMA)
    cursor=cursor_diccionario(conexion)
    try:
        resumen={}
        for tabla,clave in [('productos','productos'),('clientes','clientes'),('proveedores','proveedores'),('facturas','facturas')]: cursor.execute(f'SELECT COUNT(*) AS total FROM {tabla}'); resumen[clave]=cursor.fetchone()['total']
        cursor.execute('SELECT p.*, prov.empresa AS proveedor_nombre FROM productos p LEFT JOIN proveedores prov ON p.id_proveedor=prov.id_proveedor ORDER BY p.id_producto DESC LIMIT 5'); productos=cursor.fetchall()
    finally: cerrar_conexion(conexion,cursor)
    return render_template('index.html',resumen=resumen,productos=productos,mensaje='Panel operativo de FerreNova',sistema=SISTEMA)

@app.route('/registro',methods=['GET','POST'])
def registro():
    if current_user.is_authenticated:return redirect(url_for('inicio'))
    form=UsuarioForm()
    if form.validate_on_submit():
        conexion=con()
        if not conexion:return render_template('registro.html',form=form)
        cursor=conexion.cursor()
        try: cursor.execute('INSERT INTO usuarios (usuario,password) VALUES (%s,%s)',(form.usuario.data.strip(),generate_password_hash(form.password.data))); conexion.commit(); flash('Usuario registrado correctamente. Ya puedes iniciar sesión.','success'); return redirect(url_for('login'))
        except Error: conexion.rollback(); db_error('El usuario ya existe o no pudo registrarse.')
        finally: cerrar_conexion(conexion,cursor)
    return render_template('registro.html',form=form)
@app.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:return redirect(url_for('inicio'))
    form=LoginForm()
    if form.validate_on_submit():
        usuario=Usuario.obtener_por_nombre(form.usuario.data.strip())
        if usuario and check_password_hash(usuario.password,form.password.data): login_user(usuario); flash(f'Bienvenido, {usuario.usuario}.','success'); return redirect(url_for('inicio'))
        flash('Usuario o contraseña incorrectos.','danger')
    return render_template('login.html',form=form)
@app.route('/logout')
@login_required
def logout(): logout_user(); flash('La sesión se cerró correctamente.','info'); return redirect(url_for('login'))

# El resto de los módulos conserva la implementación CRUD de la Semana 15.
@app.route('/productos')
@login_required
def productos():
    conexion=con();
    if not conexion:return render_template('productos.html',productos=[])
    cursor=cursor_diccionario(conexion)
    try: cursor.execute('SELECT p.*, prov.empresa AS proveedor_nombre FROM productos p LEFT JOIN proveedores prov ON p.id_proveedor=prov.id_proveedor ORDER BY p.id_producto'); datos=cursor.fetchall()
    finally: cerrar_conexion(conexion,cursor)
    return render_template('productos.html',productos=datos)
@app.route('/productos/nuevo',methods=['GET','POST'])
@login_required
def nuevo_producto():
    form=ProductoForm(); conexion=con()
    if not conexion:return render_template('formulario_producto.html',form=form,titulo='Nuevo producto')
    cursor=cursor_diccionario(conexion)
    try:
        cursor.execute('SELECT id_proveedor,empresa FROM proveedores ORDER BY empresa'); form.id_proveedor.choices=[(p['id_proveedor'],p['empresa']) for p in cursor.fetchall()]
        if form.validate_on_submit(): cursor.execute('INSERT INTO productos (codigo,nombre,categoria,precio,stock,estado,id_proveedor) VALUES (%s,%s,%s,%s,%s,%s,%s)',(form.codigo.data,form.nombre.data,form.categoria.data,form.precio.data,form.stock.data,form.estado.data,form.id_proveedor.data)); conexion.commit(); flash('Producto creado correctamente.','success'); return redirect(url_for('productos'))
    except Error: conexion.rollback(); db_error('No fue posible crear el producto. Revisa que el código sea único.')
    finally: cerrar_conexion(conexion,cursor)
    return render_template('formulario_producto.html',form=form,titulo='Nuevo producto')
@app.route('/productos/editar/<int:id>',methods=['GET','POST'])
@login_required
def editar_producto(id):
    conexion=con();
    if not conexion:return redirect(url_for('productos'))
    cursor=cursor_diccionario(conexion)
    try:
        cursor.execute('SELECT * FROM productos WHERE id_producto=%s',(id,)); registro=cursor.fetchone()
        if not registro: flash('Producto no encontrado.','warning'); return redirect(url_for('productos'))
        form=ProductoForm(); cursor.execute('SELECT id_proveedor,empresa FROM proveedores ORDER BY empresa'); form.id_proveedor.choices=[(p['id_proveedor'],p['empresa']) for p in cursor.fetchall()]
        if request.method=='GET':
            for c in ('codigo','nombre','categoria','precio','stock','estado','id_proveedor'):getattr(form,c).data=registro[c]
        if form.validate_on_submit(): cursor.execute('UPDATE productos SET codigo=%s,nombre=%s,categoria=%s,precio=%s,stock=%s,estado=%s,id_proveedor=%s WHERE id_producto=%s',(form.codigo.data,form.nombre.data,form.categoria.data,form.precio.data,form.stock.data,form.estado.data,form.id_proveedor.data,id)); conexion.commit(); flash('Producto actualizado correctamente.','success'); return redirect(url_for('productos'))
    except Error: conexion.rollback(); db_error('No fue posible actualizar el producto.')
    finally: cerrar_conexion(conexion,cursor)
    return render_template('formulario_producto.html',form=form,titulo='Editar producto')
@app.route('/productos/eliminar/<int:id>',methods=['POST'])
@login_required
def eliminar_producto(id):
    conexion=con()
    if conexion:
        cursor=conexion.cursor()
        try: cursor.execute('DELETE FROM productos WHERE id_producto=%s',(id,)); conexion.commit(); flash('Producto eliminado correctamente.','warning')
        except Error: conexion.rollback(); db_error('No fue posible eliminar el producto.')
        finally: cerrar_conexion(conexion,cursor)
    return redirect(url_for('productos'))

# Entidades relacionadas: proveedores y clientes.
def listar(tabla,orden,plantilla,clave):
    conexion=con()
    if not conexion:return render_template(plantilla,**{clave:[]})
    cursor=cursor_diccionario(conexion)
    try: cursor.execute(f'SELECT * FROM {tabla} ORDER BY {orden}'); datos=cursor.fetchall()
    finally: cerrar_conexion(conexion,cursor)
    return render_template(plantilla,**{clave:datos})
@app.route('/proveedores')
@login_required
def proveedores(): return listar('proveedores','empresa','proveedores.html','proveedores')
@app.route('/clientes')
@login_required
def clientes(): return listar('clientes','nombre','clientes.html','clientes')

def guardar_entidad(form,tabla,campos,retorno,titulo,entidad):
    if form.validate_on_submit():
        conexion=con()
        if conexion:
            cursor=conexion.cursor()
            try: cursor.execute(f"INSERT INTO {tabla} ({','.join(campos)}) VALUES ({','.join(['%s']*len(campos))})",tuple(getattr(form,c).data for c in campos)); conexion.commit(); flash(f'{entidad.capitalize()} creado correctamente.','success'); return redirect(url_for(retorno))
            except Error: conexion.rollback(); db_error('No fue posible crear el registro.')
            finally: cerrar_conexion(conexion,cursor)
    return render_template('formulario_entidad.html',form=form,titulo=titulo,entidad=entidad)
@app.route('/proveedores/nuevo',methods=['GET','POST'])
@login_required
def nuevo_proveedor(): return guardar_entidad(ProveedorForm(),'proveedores',['empresa','contacto','rubro','telefono'],'proveedores','Nuevo proveedor','proveedor')
@app.route('/clientes/nuevo',methods=['GET','POST'])
@login_required
def nuevo_cliente(): return guardar_entidad(ClienteForm(),'clientes',['nombre','documento','telefono','tipo'],'clientes','Nuevo cliente','cliente')

def editar_entidad(tabla,clave,id,form,campos,retorno,entidad):
    conexion=con();
    if not conexion:return redirect(url_for(retorno))
    cursor=cursor_diccionario(conexion)
    try: cursor.execute(f'SELECT * FROM {tabla} WHERE {clave}=%s',(id,)); registro=cursor.fetchone()
    finally: cerrar_conexion(conexion,cursor)
    if not registro: flash('Registro no encontrado.','warning'); return redirect(url_for(retorno))
    if request.method=='GET':
        for c in campos:getattr(form,c).data=registro[c]
    if form.validate_on_submit():
        conexion=con(); cursor=conexion.cursor()
        try: cursor.execute(f"UPDATE {tabla} SET {','.join(c+'=%s' for c in campos)} WHERE {clave}=%s",tuple(getattr(form,c).data for c in campos)+(id,)); conexion.commit(); flash('Registro actualizado correctamente.','success'); return redirect(url_for(retorno))
        except Error: conexion.rollback(); db_error('No fue posible actualizar el registro.')
        finally: cerrar_conexion(conexion,cursor)
    return render_template('formulario_entidad.html',form=form,titulo=f'Editar {entidad}',entidad=entidad)
@app.route('/proveedores/editar/<int:id>',methods=['GET','POST'])
@login_required
def editar_proveedor(id): return editar_entidad('proveedores','id_proveedor',id,ProveedorForm(),['empresa','contacto','rubro','telefono'],'proveedores','proveedor')
@app.route('/clientes/editar/<int:id>',methods=['GET','POST'])
@login_required
def editar_cliente(id): return editar_entidad('clientes','id_cliente',id,ClienteForm(),['nombre','documento','telefono','tipo'],'clientes','cliente')
def borrar(tabla,clave,id,retorno):
    conexion=con()
    if conexion:
        cursor=conexion.cursor()
        try: cursor.execute(f'DELETE FROM {tabla} WHERE {clave}=%s',(id,)); conexion.commit(); flash('Registro eliminado correctamente.','warning')
        except Error: conexion.rollback(); db_error('No se puede eliminar un registro relacionado.')
        finally: cerrar_conexion(conexion,cursor)
    return redirect(url_for(retorno))
@app.route('/proveedores/eliminar/<int:id>',methods=['POST'])
@login_required
def eliminar_proveedor(id): return borrar('proveedores','id_proveedor',id,'proveedores')
@app.route('/clientes/eliminar/<int:id>',methods=['POST'])
@login_required
def eliminar_cliente(id): return borrar('clientes','id_cliente',id,'clientes')

# Facturación: CRUD completo y relación con clientes.
def opciones_clientes(form,cursor):
    cursor.execute('SELECT id_cliente,nombre,documento FROM clientes ORDER BY nombre'); form.id_cliente.choices=[(c['id_cliente'],f"{c['nombre']} · {c['documento']}") for c in cursor.fetchall()]
@app.route('/facturacion')
@login_required
def facturacion():
    conexion=con()
    if not conexion:return render_template('facturacion.html',facturas=[],total_facturado=0)
    cursor=cursor_diccionario(conexion)
    try: cursor.execute('SELECT f.*,c.nombre AS cliente_nombre FROM facturas f LEFT JOIN clientes c ON f.id_cliente=c.id_cliente ORDER BY f.fecha DESC,f.id_factura DESC'); datos=cursor.fetchall()
    finally: cerrar_conexion(conexion,cursor)
    return render_template('facturacion.html',facturas=datos,total_facturado=sum(float(x['total']) for x in datos))
@app.route('/facturacion/nueva',methods=['GET','POST'])
@login_required
def nueva_factura():
    form=FacturacionForm(); conexion=con()
    if not conexion:return render_template('formulario_factura.html',form=form,titulo='Nueva factura')
    cursor=cursor_diccionario(conexion)
    try:
        opciones_clientes(form,cursor)
        if form.validate_on_submit(): cursor.execute('INSERT INTO facturas (numero,id_cliente,fecha,total,estado) VALUES (%s,%s,%s,%s,%s)',(form.numero.data,form.id_cliente.data,form.fecha.data,form.total.data,form.estado.data)); conexion.commit(); flash('Factura creada correctamente.','success'); return redirect(url_for('facturacion'))
    except Error: conexion.rollback(); db_error('No fue posible crear la factura. Verifica que el número sea único.')
    finally: cerrar_conexion(conexion,cursor)
    return render_template('formulario_factura.html',form=form,titulo='Nueva factura')
@app.route('/facturacion/editar/<int:id>',methods=['GET','POST'])
@login_required
def editar_factura(id):
    conexion=con()
    if not conexion:return redirect(url_for('facturacion'))
    cursor=cursor_diccionario(conexion)
    try:
        cursor.execute('SELECT * FROM facturas WHERE id_factura=%s',(id,)); registro=cursor.fetchone()
        if not registro: flash('Factura no encontrada.','warning'); return redirect(url_for('facturacion'))
        form=FacturacionForm(); opciones_clientes(form,cursor)
        if request.method=='GET':
            for c in ('numero','id_cliente','fecha','total','estado'):getattr(form,c).data=registro[c]
        if form.validate_on_submit(): cursor.execute('UPDATE facturas SET numero=%s,id_cliente=%s,fecha=%s,total=%s,estado=%s WHERE id_factura=%s',(form.numero.data,form.id_cliente.data,form.fecha.data,form.total.data,form.estado.data,id)); conexion.commit(); flash('Factura actualizada correctamente.','success'); return redirect(url_for('facturacion'))
    except Error: conexion.rollback(); db_error('No fue posible actualizar la factura.')
    finally: cerrar_conexion(conexion,cursor)
    return render_template('formulario_factura.html',form=form,titulo='Editar factura')
@app.route('/facturacion/eliminar/<int:id>',methods=['POST'])
@login_required
def eliminar_factura(id): return borrar('facturas','id_factura',id,'facturacion')
@app.errorhandler(404)
def pagina_no_encontrada(error): return render_template('404.html'),404
if __name__=='__main__': app.run(host='0.0.0.0',port=int(os.getenv('PORT','5000')),debug=os.getenv('FLASK_DEBUG','0')=='1')
