from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
import smtplib

app = Flask(__name__)
# MySQL configuracion y conexion
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_DB'] = 'rebecca'
mysql = MySQL(app)

# Agregar un nuevo Cliente
app.secret_key = 'mysecretkey'
@app.route('/')
def Index():
	myCursor = mysql.connection.cursor()
	myCursor.execute('SELECT * FROM clientes')
	listaClientes = myCursor.fetchall()
	return render_template('addClient.html', clientes = listaClientes)

# Proceso de guardado y permitir agregar mas clientes
@app.route('/clientes', methods=['POST'])
def clientes():
	if request.method == 'POST':
		nombre = request.form['nombre']
		telefono = request.form['telefono']
		correo = request.form['correo']
		direccion = request.form['direccion']
		miCursor = mysql.connection.cursor()
		miCursor.execute('INSERT INTO clientes (nombre, telefono, correo, direccion) VALUES (%s, %s, %s, %s)',
		(nombre, telefono, correo, direccion))
		mysql.connection.commit()
		flash('El cliente ha sido registrado')
		return redirect(url_for('Index'))

# Mostrar lista de clientes y permitir editar informacion o agregar orden
@app.route('/clientList')
def showClients():
	myCursor = mysql.connection.cursor()
	myCursor.execute('SELECT * FROM clientes')
	listaClientes = myCursor.fetchall()
	return render_template('index.html', clientes = listaClientes)

# Mostrar el cliente a editar y permitir guardar
@app.route('/editClient/<id>')
def editClient(id):
	myCursor = mysql.connection.cursor()
	myCursor.execute('SELECT * FROM clientes WHERE id = %s', (id))
	clienteSeleccionado = myCursor.fetchall()
	return render_template('editClient.html', cliente = clienteSeleccionado[0])

@app.route('/update/<id>', methods=['POST'])
def updateClient(id):
	if request.method == 'POST':
		nombre = request.form['nombre']
		telefono = request.form['telefono']
		correo = request.form['correo']
		direccion = request.form['direccion']
		miCursor = mysql.connection.cursor()
		miCursor.execute("""
		UPDATE clientes 
		SET nombre = %s,
			telefono = %s,
			correo = %s,
			direccion = %s
		WHERE id = %s
		""", (nombre, telefono, correo, direccion, id))
		mysql.connection.commit()
		flash('Cliente actualizado')
		return redirect(url_for('showClients'))

@app.route('/addOrder/<id>')
def addOrder(id):
	myCursor = mysql.connection.cursor()
	myCursor.execute('SELECT * FROM clientes WHERE id = %s', (id))
	clienteSeleccionado = myCursor.fetchall()
	return render_template('addOrder.html', clientes = clienteSeleccionado)

@app.route('/sendEmail/<id>')
def sendEmail(id):
		mensaje = 'No. Orden: 1 - En Reparacion - 6/12/2019 \n\nPantalla rota de Hp 312'
		subject = 'Status de tu orden'
		cuerpoCorreo = 'Subject:{}\n\n{}'.format(subject,mensaje)
		miCursor = mysql.connection.cursor()
		miCursor.execute('SELECT * FROM clientes WHERE id = %s', id)
		dataCLiente = miCursor.fetchall()
		for correo in dataCLiente:
			correoCliente = correo[3]
		print(correoCliente)
		server = smtplib.SMTP('smtp.gmail.com', 587)
		server.starttls()
		server.login('servicepcqueretaro@gmail.com', 'hola123.')
		server.sendmail('servicepcqueretaro@gmail.com', correoCliente, cuerpoCorreo)
		server.quit()
		flash('Correo enviado')
		return redirect(url_for('showClients'))


if __name__ == '__main__':
	app.run(debug = True)