from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SelectField, SubmitField, DateField
from wtforms.validators import DataRequired, Length, NumberRange

class FacturacionForm(FlaskForm):
    numero = StringField('Número de Factura', validators=[DataRequired(message="El número de factura es obligatorio"), Length(min=5, max=20)])
    cliente = StringField('Cliente', validators=[DataRequired(message="El cliente es obligatorio")])
    fecha = StringField('Fecha (DD/MM/AAAA)', validators=[DataRequired(message="La fecha es obligatoria")])
    total = FloatField('Total', validators=[DataRequired(message="El total es obligatorio"), NumberRange(min=0, message="El total no puede ser negativo")])
    estado = SelectField('Estado', choices=[
        ('Pagada', 'Pagada'),
        ('Pendiente', 'Pendiente'),
        ('Anulada', 'Anulada')
    ], validators=[DataRequired()])
    submit = SubmitField('Emitir Factura')
