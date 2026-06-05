from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)

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

    return jsonify({
        "mensaje": "API funcionando correctamente"
    })




@app.route('/api/login', methods=['POST'])
def api_login():

    datos = request.get_json()

    usuario = datos['usuario']
    password = datos['password']

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM usuarios WHERE username=? AND password=?",
        (usuario, password)
    )

    usuario_bd = cursor.fetchone()

    conn.close()

    if usuario_bd:

        return jsonify({
            "success": True
        })

    return jsonify({
        "success": False
    })


# ==========================
# BUSCAR PRODUCTO API
# ==========================

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


if __name__ == '__main__':

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host='0.0.0.0',
        port=port,
        debug=True
    )