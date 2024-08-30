from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_mysqldb import MySQL
from dotenv import load_dotenv
import os

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'futbolpro'

# Configuración de la clave secreta
app.config['SECRET_KEY'] = 'una_clave_secreta_aleatoria'

mysql = MySQL(app)

def obtener_nombre_imagen(nombre_jugador):
    extensiones = ['.png', '.jpg']
    nombre_base = nombre_jugador.replace(' ', '_')
    for ext in extensiones:
        nombre_archivo = nombre_base + ext
        ruta_archivo = os.path.join('static', 'images', nombre_archivo)
        if os.path.isfile(ruta_archivo):
            return nombre_archivo
        
def obtener_equipo_imagen(equipo):
    extensiones = ['.png', '.jpg']
    nombre_base = equipo.replace(' ', '_')
    for ext in extensiones:
        nombre_archivo = nombre_base + ext
        ruta_archivo = os.path.join('static', 'images','selecciones', nombre_archivo)
        if os.path.isfile(ruta_archivo):
            return nombre_archivo

@app.route('/')
def index():
    return render_template ('index.html')

@app.route('/jugadores')
def jugadores():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM jugadores')
    jugadores = cur.fetchall()
    cur.close()
    if not jugadores:
        flash('No se encontraron jugadores')
        return redirect(url_for('index'))
    players_with_images = [(jugador + (obtener_nombre_imagen(jugador[0]),)) for jugador in jugadores]
    return render_template('jugadores.html', jugadores=players_with_images)


@app.route('/equipos')
def equipos():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM equipos')  # Ajusta la consulta según tu base de datos
    equipos = cur.fetchall()
    cur.close()
    return render_template('equipos.html', equipos=equipos)


@app.route('/iniciarsesion', methods=['GET', 'POST'])
def iniciarsesion():
    if request.method == 'POST':
        email = request.form['email']
        contrasena = request.form['contrasena']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO usuarios (email, contrasena) VALUES (%s, %s)',(email, contrasena))
        mysql.connection.commit()
        flash('success')
        return redirect(url_for('index'))
    return render_template('iniciarsesion.html')

@app.route('/estadisticas')
def estadisticas():
    cur = mysql.connection.cursor()
    cur.execute('SELECT nombre, edad, equipo_actual, partidos_jugados, goles, asistencias FROM jugadores')
    estadisticas = cur.fetchall()
    cur.close()
    if not estadisticas:
        flash('No se encontraron estadísticas de jugadores')
        return redirect(url_for('index'))
    return render_template('estadisticas.html', estadisticas=estadisticas)


if __name__ == '__main__':
    app.run(port = 3000, debug = True)