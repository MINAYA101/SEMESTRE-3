from flask_wtf import FlaskForm
from wtforms import DateField, FloatField, SelectField, StringField, SubmitField
from wtforms.validators import DataRequired, NumberRange


class FacturacionForm(FlaskForm):
    numero = StringField("Número", validators=[DataRequired()])
    id_cliente = SelectField("Cliente", coerce=int, validators=[DataRequired()])
    fecha = DateField("Fecha", validators=[DataRequired()])
    total = FloatField("Total", validators=[DataRequired(), NumberRange(min=0)])
    estado = SelectField("Estado", choices=[("Pendiente", "Pendiente"), ("Pagada", "Pagada"), ("Anulada", "Anulada")], validators=[DataRequired()])
    submit = SubmitField("Guardar factura")
