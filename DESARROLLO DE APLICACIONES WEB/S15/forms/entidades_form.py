from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField
from wtforms.validators import DataRequired, Length


class ClienteForm(FlaskForm):
    nombre = StringField("Nombre", validators=[DataRequired(), Length(min=3, max=100)])
    documento = StringField("Documento", validators=[DataRequired(), Length(min=5, max=20)])
    telefono = StringField("Teléfono", validators=[DataRequired(), Length(min=7, max=15)])
    tipo = SelectField("Tipo", choices=[("Minorista", "Minorista"), ("Mayorista", "Mayorista")], validators=[DataRequired()])
    submit = SubmitField("Guardar cliente")


class ProveedorForm(FlaskForm):
    empresa = StringField("Empresa", validators=[DataRequired(), Length(min=3, max=100)])
    contacto = StringField("Contacto", validators=[DataRequired(), Length(min=3, max=100)])
    rubro = StringField("Rubro", validators=[DataRequired(), Length(min=3, max=50)])
    telefono = StringField("Teléfono", validators=[DataRequired(), Length(min=7, max=15)])
    submit = SubmitField("Guardar proveedor")
