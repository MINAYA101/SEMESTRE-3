from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Length

class UsuarioForm(FlaskForm):
    usuario = StringField("Usuario", validators=[DataRequired(), Length(min=3, max=50)])
    password = PasswordField("Contraseña", validators=[DataRequired(), Length(min=8, message="Usa al menos 8 caracteres")])
    confirmar_password = PasswordField("Confirmar contraseña", validators=[DataRequired(), EqualTo("password", message="Las contraseñas deben coincidir")])
    submit = SubmitField("Crear usuario")
