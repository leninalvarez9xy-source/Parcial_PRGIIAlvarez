from flask import Flask, render_template, request, redirect, session, jsonify
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "123456"

CORS(app)


def crear_bd():

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS productos(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        codigo TEXT,
        nombre TEXT,
        descripcion TEXT,
        precio REAL,
        stock INTEGER
    )
    """)

    cursor.execute("SELECT * FROM usuarios")

    if cursor.fetchone() is None:

        cursor.execute("""
        INSERT INTO usuarios
        (username,password)
        VALUES
        ('admin','123')
        """)

        cursor.execute("""
        INSERT INTO productos
        (codigo,nombre,descripcion,precio,stock)
        VALUES
        ('P001','Laptop Lenovo','Core i5',2500,10)
        """)

        cursor.execute("""
        INSERT INTO productos
        (codigo,nombre,descripcion,precio,stock)
        VALUES
        ('P002','Mouse Logitech','Mouse Gamer',80,20)
        """)

        cursor.execute("""
        INSERT INTO productos
        (codigo,nombre,descripcion,precio,stock)
        VALUES
        ('P003','Monitor Samsung','24 pulgadas',650,15)
        """)

    conn.commit()
    conn.close()


crear_bd()


@app.route('/')
def inicio():
    return redirect('/login')


@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        usuario = request.form['usuario']
        password = request.form['password']

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM usuarios WHERE username=? AND password=?",
            (usuario, password)
        )

        dato = cursor.fetchone()

        conn.close()

        if dato:
            session['usuario'] = usuario
            return redirect('/principal')

    return render_template('login.html')


@app.route('/principal')
def principal():

    if 'usuario' not in session:
        return redirect('/login')

    return render_template('principal.html')


@app.route('/buscador')
def buscador():

    if 'usuario' not in session:
        return redirect('/login')

    return render_template('buscador.html')


@app.route('/api/buscar_producto', methods=['POST'])
def buscar_producto():

    datos = request.get_json()

    codigo = datos['codigo']

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM productos WHERE codigo=?",
        (codigo,)
    )

    producto = cursor.fetchone()

    conn.close()

    if producto:

        return jsonify({

            "codigo": producto[1],
            "nombre": producto[2],
            "descripcion": producto[3],
            "precio": producto[4],
            "stock": producto[5]

        })

    return jsonify({
        "mensaje": "Producto no encontrado"
    })


@app.route('/logout')
def logout():

    session.clear()

    return redirect('/login')




if __name__ == '__main__':

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host='0.0.0.0',
        port=port,
        debug=True
    )