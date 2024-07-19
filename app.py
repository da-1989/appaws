from flask import Flask, render_template, request, redirect, url_for
import pyodbc
import base64

app = Flask(__name__)

# Configuración de la conexión a la base de datos
server = 'database-1.clgc2ek4shpb.us-east-1.rds.amazonaws.com'
database = 'dbdavidgc'
username = 'davidgc'
password = 'angelajose1989'
connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'

def get_db_connection():
    conn = pyodbc.connect(connection_string)
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Productos')
    productos = cursor.fetchall()
    conn.close()
    return render_template('index.html', productos=productos)

@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        precio = request.form['precio']
        imagen = request.files['imagen'].read()
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO Productos (nombre, descripcion, precio, imagen) VALUES (?, ?, ?, ?)', 
                       (nombre, descripcion, precio, imagen))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('create.html')

@app.route('/<int:id>/update', methods=('GET', 'POST'))
def update(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Productos WHERE id = ?', (id,))
    producto = cursor.fetchone()

    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        precio = request.form['precio']
        imagen = request.files['imagen'].read()
        cursor.execute('UPDATE Productos SET nombre = ?, descripcion = ?, precio = ?, imagen = ? WHERE id = ?', 
                       (nombre, descripcion, precio, imagen, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    conn.close()
    return render_template('update.html', producto=producto)

@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Productos WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/<int:id>')
def detail(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Productos WHERE id = ?', (id,))
    producto = cursor.fetchone()
    conn.close()

    # Convertir la imagen a base64
    producto = list(producto)  # Convertir de tupla a lista
    if producto[4]:
        producto[4] = base64.b64encode(producto[4]).decode('utf-8')

    return render_template('detail.html', producto=producto)

if __name__ == '__main__':
    app.run(debug=True)
