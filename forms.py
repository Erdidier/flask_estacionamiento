from wtforms import Form
from wtforms import StringField, TextField, PasswordField
from wtforms.fields.html5 import EmailField
from wtforms import HiddenField
from wtforms import validators
from models import Parking_lot

def length_honeypot(form, field):
	if len(field.data)>0:
		raise validators.ValidationError('El campo debe estar vacío.')

class Registrar(Form):
	nombre = TextField('Nombre',
		[validators.DataRequired(message='El nombre es requerido!'),
		validators.length(min=4, max=20, message='Ingrese un nombre válido')])
	c_p = TextField('Código Postal',
		[validators.DataRequired(message='El C.P. es requerido!'),
		validators.length(min=5, max=5, message='Ingrese un C.P. válido')])
	teléfono = TextField('Teléfono',
		[validators.DataRequired(message='El password es requerido!'),
		validators.length(min=10, max=10, message='Ingrese un teléfono válido')])
	capacidad = TextField('Capacidad',
		[validators.DataRequired(message='Se necesita colocar la capacidad de automóviles'),
		validators.length(min=1, max=3, message='Ingrese un número no mayor a 3 dígitos')])

class LoginForm(Form):
	username = StringField('Username',
		[validators.DataRequired(message='El username es requerido!'),
		validators.length(min=4, max=25, message='Ingrese un username válido!')])
	password = PasswordField('Password',
		[validators.DataRequired(message='El password es requerido!')])


# class CommentForm(Form):
# 	username = StringField('Username',
# 		[validators.length(min=4, max=25, message='Ingrese un username válido!'),
# 		validators.DataRequired(message='El username es requerido!')])
# 	email = EmailField('Correo electrónico',
# 		[validators.Email(message='Ingrese un email válido!'),
# 		validators.DataRequired(message='El email es requerido!')])
# 	comment = TextField('Comentario')
# 	honeypot = HiddenField('', [length_honeypot])

# class LoginForm(Form):
# 	username = StringField('Username',
# 		[validators.DataRequired(message='El username es requerido!'),
# 		validators.length(min=4, max=25, message='Ingrese un username válido!')])
# 	password = PasswordField('Password',
# 		[validators.DataRequired(message='El password es requerido!')])

# class CreateForm(Form):
# 	username = TextField('Username',
# 		[validators.DataRequired(message='El username es requerido!'),
# 		validators-length(min=4, max=50, message='Ingrese un username válido')])
# 	email = EmailField('Correo electrónico',
# 		[validators.DataRequired(message='El email es requerido!'),
# 		validators.Email(message='Ingrese un email válido'),
# 		validators.length(min=4, max=50, message='Ingrese un email válido')])
# 	password = PasswordField('Password',
# 		[validators.DataRequired(message='El password es requerido!')])

# 	def validate_username(form, field):
# 		username = field.data
# 		user = User.query.filter_by(username = username).first()
# 		if user is not None:
# 			raise validators.ValidationError('El username ya se encuentra registrado!')
