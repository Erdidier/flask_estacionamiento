from flask import Flask
from flask import render_template
from flask import request
from flask import make_response
from flask import session
from flask import flash
from flask import g
from flask import url_for
from flask import redirect

from config import DevelopmentConfig

from models import db
from models import Parking_lot
from models import Records
from models import User

from flask_wtf import CsrfProtect
import forms

from helper import date_format

import random
from datetime import datetime, timedelta

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
csrf = CsrfProtect()

@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404

@app.before_request
def before_request():
	if 'username' not in session and request.endpoint in ['comment']:
		return redirect(url_for('login'))
	elif 'username' in session and request.endpoint in ['login', 'create']:
		return redirect(url_for('registros'))

@app.after_request
def after_request(response):
	return response

@app.route('/', methods = ['GET', 'POST'])
def index():
	estacionamientos = Parking_lot.query.all()
	estacionamiento = forms.Registrar(request.form)
	title = "Index"
	return render_template('index.html', title = title, estacionamientos = estacionamientos, form = estacionamiento)

@app.route('/logout')
def logout():
	if 'username' in session:
		session.pop('username')
	return redirect(url_for('login'))

@app.route('/login', methods = ['GET', 'POST'])
def login():
	login_form = forms.LoginForm(request.form)
	if request.method == 'POST' and login_form.validate():
		username = login_form.username.data
		password = login_form.password.data
		user = User.query.filter_by(username = username).first()
		if user is not None and user.password == password:
			success_message = 'Bienvenido {}'.format(username)
			flash(success_message)
			session['username'] = username
			return redirect(url_for('registros'))
		else:
			error_message = 'Usuario o contraseña no válidos!'
			flash(error_message)
	return render_template('login.html', form = login_form)

@app.route('/registros')
def registros():
	registros = Records.query.all()
	for registro in registros:
		print(registro.codigo_llegada)
	return render_template('reviews.html', registros = registros)

@app.route('/create', methods = ['GET', 'POST'])
def create():
	estacionamiento = forms.Registrar(request.form)
	if request.method == 'POST' and estacionamiento.validate():
		parking = Parking_lot(estacionamiento.nombre.data,
			estacionamiento.c_p.data,
			estacionamiento.teléfono.data,
			estacionamiento.capacidad.data)
		db.session.add(parking)
		db.session.commit()
		success_message = 'Estacionamiento registrado en la base de datos'
		flash(success_message)
	return redirect(url_for('index'))

@app.route('/edit/<int:id>')
def get_contact(id):
	data = Parking_lot.query.filter_by(id = id).first()
	return render_template('edit.html', estacionamiento = data)

@app.route('/update/<int:id>', methods = ['POST'])
def update_contact(id):
	if request.method == 'POST':
		nombre = request.form['nombre']
		c_p = request.form['c_p']
		teléfono = request.form['teléfono']
		capacidad = request.form['capacidad']
		update = Parking_lot.query.filter_by(id = id).update(dict(nombre = nombre, c_p = c_p, teléfono = teléfono, capacidad = capacidad))
		db.session.commit()
		flash('Información actualizada con éxito')
		return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete_contact(id):
	update = Parking_lot.query.filter_by(id = id).delete()
	db.session.commit()
	flash('Estacionamiento eliminado satisfactoriamente')
	return redirect(url_for('index'))

@app.route('/llegada', methods = ['GET', 'POST'])
def llegada():
	t = 5
	l = ""
	while t > 0:
		num = random.randint(97,122)
		l+=chr(num)
		print(chr(num))
		print(l)
		t-=1
	if request.method == 'POST':
		nombre = request.form['nombre']
		entrada = request.form['entrada']
		código = request.form['código']
		estacionamiento = Parking_lot.query.filter_by(nombre = nombre).first()
		if estacionamiento is not None:
			registro = Records(código, entrada, None, None)
			db.session.add(registro)
			db.session.commit()
			flash('Entrada registrada con éxito')
		else:
			flash('El nombre ingresado no se encuentra registrado')
		return redirect(url_for('index'))
	return render_template('Llegada.html', código = l)

@app.route('/salida', methods = ['GET', 'POST'])
def salida():
	if request.method == 'POST':
		código = request.form['código']
		estacionamiento = Records.query.filter_by(codigo_llegada = código).first()
		if estacionamiento is not None:
			salida = request.form['salida']
			código = request.form['código']
			total = request.form['total']
			flash('Entrada registrada con éxito')
			return render_template('Calcular.html', salida = salida, código = código, total = total)
		else:
			flash('El nombre ingresado no se encuentra registrado')
	return render_template('Salida.html')

@app.route('/calcular', methods = ['GET', 'POST'])
def calcular():
	if request.method == 'POST':
		salida = request.form['salida']
		código = request.form['código']
		estacionamiento = Records.query.filter_by(codigo_llegada = código).first()
		tiempo = datetime.strptime(salida, '%Y-%m-%d %H:%M:%S') - estacionamiento.fecha_llegada
		if tiempo <= timedelta(minutes = 45):
			total = 0
		elif tiempo <= timedelta(hours = 2):
			total = 20
		elif tiempo < timedelta(days = 1):
			tiempo = str(tiempo - timedelta(hours = 2))
			tiempo = int(tiempo[:2])
			total = 20 + (tiempo * 20)
		elif tiempo < timedelta(days = 7):
			tiempo = int(str(tiempo)[:1])
			print(tiempo)
			total = 200 * tiempo
		elif tiempo < timedelta(days = 30):
			tiempo = int(str(tiempo)[:2])
			print(tiempo)
			total = (int(tiempo/7) * 1000) + ((tiempo - int(tiempo/7) * 7) * 200)
		elif tiempo >= timedelta(days = 30):
			tiempo = int(str(tiempo)[:2])
			print(tiempo)
			total = (int(tiempo/30) * 4000) + ((int((tiempo) / 7) - 4) * 1000) + ((((tiempo - int(tiempo/30) * 30) - (int((tiempo - int(tiempo/30) * 30) / 7) * 7)) * 200))
		update = Records.query.filter_by(codigo_llegada = código).update(dict(fecha_salida = salida, total_pago = total))
		db.session.commit()
		flash('Salida registrada con éxito')
		return redirect(url_for('index'))
	return render_template('Calcular.html', salida = salida, código = código, total = total)

@app.route('/reviews/', methods = ['GET'])
@app.route('/reviews/<int:page>', methods = ['GET'])
def reviews(page = 1):
	per_page = 3
	comments = Comment.query.join(User).add_columns(User.username, Comment.text, Comment.created_date).paginate(page,per_page,False)
	return render_template('reviews.html', comments = comments, date_format = date_format)

if __name__ == '__main__':
	csrf.init_app(app)
	db.init_app(app)
	with app.app_context():
		db.create_all()
	app.run(host="0.0.0.0", port = 8000)	