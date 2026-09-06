from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class ProveedorForm(FlaskForm):
    empresa = StringField('Nombre de la Empresa', validators=[DataRequired(message="El nombre de la empresa es obligatorio"), Length(min=3, max=100)])
    contacto = StringField('Nombre de Contacto', validators=[DataRequired(message="El contacto es obligatorio"), Length(min=3, max=100)])
    rubro = StringField('Rubro', validators=[DataRequired(message="El rubro es obligatorio"), Length(min=3, max=50)])
    telefono = StringField('Teléfono', validators=[DataRequired(message="El teléfono es obligatorio"), Length(min=7, max=15)])
    submit = SubmitField('Registrar Proveedor')
