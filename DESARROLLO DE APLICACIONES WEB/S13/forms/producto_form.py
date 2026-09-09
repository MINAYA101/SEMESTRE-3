from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange

class ProductoForm(FlaskForm):
    codigo = StringField('Código', validators=[DataRequired(message="El código es obligatorio"), Length(min=3, max=10)])
    nombre = StringField('Nombre del Producto', validators=[DataRequired(message="El nombre es obligatorio"), Length(min=3, max=100)])
    categoria = SelectField('Categoría', choices=[
        ('Herramientas eléctricas', 'Herramientas eléctricas'),
        ('Herramientas manuales', 'Herramientas manuales'),
        ('Pinturas', 'Pinturas'),
        ('Medición', 'Medición'),
        ('Fijaciones', 'Fijaciones')
    ], validators=[DataRequired()])
    precio = FloatField('Precio', validators=[DataRequired(message="El precio debe ser un número"), NumberRange(min=0.01, message="El precio debe ser mayor a 0")])
    stock = IntegerField('Stock', validators=[DataRequired(message="El stock es obligatorio"), NumberRange(min=0, message="El stock no puede ser negativo")])
    estado = SelectField('Estado', choices=[
        ('Disponible', 'Disponible'),
        ('Stock bajo', 'Stock bajo'),
        ('Agotado', 'Agotado')
    ], validators=[DataRequired()])
    id_proveedor = SelectField('Proveedor', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Guardar Producto')
