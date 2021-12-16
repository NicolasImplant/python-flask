from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


# Se crea la clase para realizar el formulario login, en este caso se pide al ususario y contraseña, el parametro validators
# genera el caracter oblifatorio de los parametros ingresados a traves de crear instancias de DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username:', validators=[DataRequired()])
    password = PasswordField('Password:', validators=[DataRequired()])
    submit = SubmitField('Submit')