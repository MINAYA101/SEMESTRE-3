from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length

class ClienteForm(FlaskForm):
    nombre = StringField('Nombre / Razón Social', validators=[DataRequired(message="El nombre es obligatorio"), Length(min=3, max=100)])
    documento = StringField('Documento (DNI/RUC)', validators=[DataRequired(message="El documento es obligatorio"), Length(min=8, max=11)])
    telefono = StringField('Teléfono', validators=[DataRequired(message="El teléfono es obligatorio"), Length(min=7, max=15)])
    tipo = SelectField('Tipo de Cliente', choices=[
        ('Persona', 'Persona'),
        ('Empresa', 'Empresa')
    ], validators=[DataRequired()])
    submit = SubmitField('Registrar Cliente')
