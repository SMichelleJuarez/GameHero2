import os
from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector
from werkzeug.utils import secure_filename
import conexion as bd
app = Flask(__name__)
CORS(app)

# Configuración de la carpeta para subir imágenes
UPLOAD_FOLDER = 'imagenes/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

class Catalogo:
    def __init__(self, host, user, password, database):
        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.conn.cursor(dictionary=True)
        self._initialize_database()

    def _initialize_database(self):
        self._create_database()
        self._create_tables()

    def _create_database(self):
        self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.conn.database}")
        self.conn.database = self.conn.database

    def _create_tables(self):
        tables = {
            "Pais": '''CREATE TABLE IF NOT EXISTS Pais (
                id_pais INT PRIMARY KEY AUTO_INCREMENT,
                pais VARCHAR(500)
            )''',
            "Provincia": '''CREATE TABLE IF NOT EXISTS Provincia (
                id_provincia INT PRIMARY KEY AUTO_INCREMENT,
                provincia VARCHAR(500),
                id_pais INT,
                FOREIGN KEY (id_pais) REFERENCES Pais(id_pais)
            )''',
            "Ciudad": '''CREATE TABLE IF NOT EXISTS Ciudad (
                id_ciudad INT PRIMARY KEY AUTO_INCREMENT,
                ciudad VARCHAR(500),
                id_provincia INT,
                FOREIGN KEY (id_provincia) REFERENCES Provincia(id_provincia)
            )''',
            "Usuario": '''CREATE TABLE IF NOT EXISTS Usuario (
                id_usuario INT PRIMARY KEY AUTO_INCREMENT,
                nombre VARCHAR(100) NOT NULL,
                apellido VARCHAR(100) NOT NULL,
                fecha_nacimiento DATE,
                fecha_registro DATE,
                id_pais INT,
                id_provincia INT,
                id_ciudad INT,
                email VARCHAR(100) UNIQUE NOT NULL,
                contraseña VARCHAR(100) NOT NULL,
                Privilegios ENUM('Usuario', 'Moderador', 'Administrador') DEFAULT 'Usuario',
                FOREIGN KEY (id_pais) REFERENCES Pais(id_pais),
                FOREIGN KEY (id_provincia) REFERENCES Provincia(id_provincia),
                FOREIGN KEY (id_ciudad) REFERENCES Ciudad(id_ciudad)
            )''',
            "Categoria": '''CREATE TABLE IF NOT EXISTS Categoria (
                id_categoria INT PRIMARY KEY AUTO_INCREMENT,
                nombre ENUM('Acción', 'Estrategia', 'Aventura', 'Simulación', 'Ingenio', 'Arcade', 'Otros', 'Ninguna'),
                padre INT,
                FOREIGN KEY (padre) REFERENCES Categoria(id_categoria)
            )''',
            "Usuario_Categoria": '''CREATE TABLE IF NOT EXISTS Usuario_Categoria (
                id_usuario_categoria INT PRIMARY KEY AUTO_INCREMENT,
                id_usuario INT,
                id_categoria INT,
                FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario),
                FOREIGN KEY (id_categoria) REFERENCES Categoria(id_categoria)
            )''',
            "Reaccion": '''CREATE TABLE IF NOT EXISTS Reaccion (
                id_reaccion INT PRIMARY KEY AUTO_INCREMENT,
                tipo ENUM('Bueno', 'Intermedio', 'Interesante', 'Malo')
            )''',
            "Juego": '''CREATE TABLE IF NOT EXISTS Juego (
                id_juego INT PRIMARY KEY AUTO_INCREMENT,
                titulo VARCHAR(100),
                contenido TEXT,
                contenido_url VARCHAR(255),
                resumen TEXT,
                id_reaccion INT,
                FOREIGN KEY (id_reaccion) REFERENCES Reaccion(id_reaccion)
            )''',
            "Juego_Categoria": '''CREATE TABLE IF NOT EXISTS Juego_Categoria (
                id_juego_categoria INT PRIMARY KEY AUTO_INCREMENT,
                id_juego INT,
                id_categoria INT,
                FOREIGN KEY (id_juego) REFERENCES Juego(id_juego),
                FOREIGN KEY (id_categoria) REFERENCES Categoria(id_categoria)
            )''',
            "Comentario": '''CREATE TABLE IF NOT EXISTS Comentario (
                id_comentario INT PRIMARY KEY AUTO_INCREMENT,
                texto TEXT,
                id_usuario INT,
                id_juego INT,
                id_reaccion INT,
                FOREIGN KEY (id_reaccion) REFERENCES Reaccion(id_reaccion),
                FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario),
                FOREIGN KEY (id_juego) REFERENCES Juego(id_juego)
            )'''
        }
        for table in tables.values():
            self.cursor.execute(table)

    def listar_juegos_categoria(self, id_categoria):
        query = """
            SELECT j.id_juego, j.titulo, j.contenido, j.resumen, j.id_reaccion
            FROM Juego j
            INNER JOIN Juego_Categoria jc ON j.id_juego = jc.id_juego
            WHERE jc.id_categoria = %s
        """
        self.cursor.execute(query, (id_categoria,))
        juegos = self.cursor.fetchall()
        return juegos

    def close(self):
        self.cursor.close()
        self.conn.close()

class Pais:
    def __init__(self, catalogo):
        self.catalogo = catalogo

    def create(self, pais):
        query = "INSERT INTO Pais (pais) VALUES (%s)"
        self.catalogo.cursor.execute(query, (pais,))
        self.catalogo.conn.commit()

class Provincia:
    def __init__(self, catalogo):
        self.catalogo = catalogo

    def create(self, provincia, id_pais):
        query = "INSERT INTO Provincia (provincia, id_pais) VALUES (%s, %s)"
        self.catalogo.cursor.execute(query, (provincia, id_pais))
        self.catalogo.conn.commit()

class Ciudad:
    def __init__(self, catalogo):
        self.catalogo = catalogo

    def create(self, ciudad, id_provincia):
        query = "INSERT INTO Ciudad (ciudad, id_provincia) VALUES (%s, %s)"
        self.catalogo.cursor.execute(query, (ciudad, id_provincia))
        self.catalogo.conn.commit()

class Usuario:
    def __init__(self, catalogo):
        self.catalogo = catalogo

    def create(self, nombre, apellido, fecha_nacimiento, fecha_registro, id_pais, id_provincia, id_ciudad, email, contraseña, privilegios='Usuario'):
        query = """INSERT INTO Usuario (nombre, apellido, fecha_nacimiento, fecha_registro, id_pais, id_provincia, id_ciudad, email, contraseña, Privilegios)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        self.catalogo.cursor.execute(query, (nombre, apellido, fecha_nacimiento, fecha_registro, id_pais, id_provincia, id_ciudad, email, contraseña, privilegios))
        self.catalogo.conn.commit()

class Categoria:
    def __init__(self, catalogo):
        self.catalogo = catalogo

    def create(self, nombre, padre=None):
        query = "INSERT INTO Categoria (nombre, padre) VALUES (%s, %s)"
        self.catalogo.cursor.execute(query, (nombre, padre))
        self.catalogo.conn.commit()

class UsuarioCategoria:
    def __init__(self, catalogo):
        self.catalogo = catalogo

    def create(self, id_usuario, id_categoria):
        query = "INSERT INTO Usuario_Categoria (id_usuario, id_categoria) VALUES (%s, %s)"
        self.catalogo.cursor.execute(query, (id_usuario, id_categoria))
        self.catalogo.conn.commit()

class Reaccion:
    def __init__(self, catalogo):
        self.catalogo = catalogo

    def create(self, tipo):
        query = "INSERT INTO Reaccion (tipo) VALUES (%s)"
        self.catalogo.cursor.execute(query, (tipo,))
        self.catalogo.conn.commit()

class Juego:
    def __init__(self, catalogo):
        self.catalogo = catalogo

    def create(self, titulo, contenido_url, resumen, id_reaccion):
        query = "INSERT INTO Juego (titulo, contenido_url, resumen, id_reaccion) VALUES (%s, %s, %s, %s)"
        self.catalogo.cursor.execute(query, (titulo, contenido_url, resumen, id_reaccion))
        self.catalogo.conn.commit()

    def listar(self):
        self.catalogo.cursor.execute("SELECT * FROM Juego")
        return self.catalogo.cursor.fetchall()

    def consultar(self, id_juego):
        self.catalogo.cursor.execute("SELECT * FROM Juego WHERE id_juego = %s", (id_juego,))
        return self.catalogo.cursor.fetchone()

    def mostrar(self, id_juego):
        juego = self.consultar(id_juego)
        if juego:
            return {
                "ID": juego['id_juego'],
                "Título": juego['titulo'],
                "Imagen": juego['contenido_url'],
                "Resumen": juego['resumen'],
                "Reacción": juego['id_reaccion']
            }
        else:
            return {"error": "Juego no encontrado"}

    def delete(self, id_juego):
        query = "DELETE FROM Juego WHERE id_juego = %s"
        self.catalogo.cursor.execute(query, (id_juego,))
        self.catalogo.conn.commit()

class JuegoCategoria:
    def __init__(self, catalogo):
        self.catalogo = catalogo

    def create(self, id_juego, id_categoria):
        query = "INSERT INTO Juego_Categoria (id_juego, id_categoria) VALUES (%s, %s)"
        self.catalogo.cursor.execute(query, (id_juego, id_categoria))
        self.catalogo.conn.commit()

class Comentario:
    def __init__(self, catalogo):
        self.catalogo = catalogo

    def create(self, texto, id_juego):
        query = "INSERT INTO Comentario (texto, id_juego) VALUES (%s, %s)"
        self.catalogo.cursor.execute(query, (texto, id_juego))
        self.catalogo.conn.commit()
        return self.catalogo.cursor.lastrowid

    def listar(self, id_juego):
        query = "SELECT * FROM Comentario WHERE id_juego = %s"
        self.catalogo.cursor.execute(query, (id_juego,))
        return self.catalogo.cursor.fetchall()


    def delete(self, id_comentario):
        query = "DELETE FROM Comentario WHERE id_comentario = %s"
        self.catalogo.cursor.execute(query, (id_comentario,))
        self.catalogo.conn.commit()

# Configuración de la base de datos
catalogo = Catalogo(host= bd.host,user=bd.user,password=bd.password,database=bd.database)
contenido_url = 'home/SofiaMJuarez/mysite/imagenes'

@app.route('/api/categorias', methods=['GET'])
def get_categorias():
    catalogo.cursor.execute("SELECT * FROM Categoria")
    categorias = catalogo.cursor.fetchall()
    return jsonify(categorias)

@app.route('/api/categorias/<int:id_categoria>', methods=['GET'])
def get_categoria(id_categoria):
    catalogo.cursor.execute("SELECT * FROM Categoria WHERE id_categoria = %s", (id_categoria,))
    categoria = catalogo.cursor.fetchone()
    return jsonify(categoria)

@app.route('/api/juegos', methods=['GET'])
def get_juegos():
    categoria = request.args.get('categoria')
    if categoria:
        query = """
            SELECT j.id_juego, j.titulo, j.contenido_url, j.resumen, j.id_reaccion
            FROM Juego j
            INNER JOIN Juego_Categoria jc ON j.id_juego = jc.id_juego
            INNER JOIN Categoria c ON jc.id_categoria = c.id_categoria
            WHERE c.nombre = %s
        """
        catalogo.cursor.execute(query, (categoria,))
    else:
        query = "SELECT * FROM Juego"
        catalogo.cursor.execute(query)

    juegos = catalogo.cursor.fetchall()
    juegos_list = [{"id_juego": juego['id_juego'], "titulo": juego['titulo'], "contenido_url": juego['contenido_url'], "resumen": juego['resumen']} for juego in juegos]
    return jsonify(juegos_list)

@app.route('/api/comentarios/<int:id_juego>', methods=['GET'])
def get_comentarios(id_juego):
    query = """
        SELECT c.id_comentario, c.texto
                SELECT c.id_comentario, c.texto, u.nombre, u.apellido
        FROM Comentario c
        INNER JOIN Usuario u ON c.id_usuario = u.id_usuario
        WHERE c.id_juego = %s
    """
    catalogo.cursor.execute(query, (id_juego,))
    comentarios = catalogo.cursor.fetchall()
    comentarios_list = [{"id_comentario": comentario['id_comentario'], "texto": comentario['texto'], "nombre": comentario['nombre'], "apellido": comentario['apellido']} for comentario in comentarios]
    return jsonify(comentarios_list)

@app.route('/api/comentarios', methods=['POST'])
def add_comentario():
    data = request.get_json()
    texto = data.get('texto')
    id_usuario = data.get('id_usuario')
    id_juego = data.get('id_juego')
    id_reaccion = data.get('id_reaccion')

    if not texto or not id_usuario or not id_juego or not id_reaccion:
        return jsonify({"error": "Faltan datos para agregar el comentario"}), 400

    query = """
        INSERT INTO Comentario (texto, id_usuario, id_juego, id_reaccion)
        VALUES (%s, %s, %s, %s)
    """
    catalogo.cursor.execute(query, (texto, id_usuario, id_juego, id_reaccion))
    catalogo.connection.commit()
    return jsonify({"mensaje": "Comentario agregado exitosamente"})

@app.route('/api/comentarios/<int:id_comentario>', methods=['DELETE'])
def delete_comentario(id_comentario):
    query = "DELETE FROM Comentario WHERE id_comentario = %s"
    catalogo.cursor.execute(query, (id_comentario,))
    catalogo.connection.commit()
    return jsonify({"mensaje": "Comentario eliminado exitosamente"})


@app.route('/subir_imagen', methods=['POST'])
def subir_imagen():
    if 'imagen' not in request.files:
        return jsonify({'error': 'No se encontró la imagen en la solicitud'}), 400

    imagen = request.files['imagen']

    if imagen.filename == '':
        return jsonify({'error': 'No se seleccionó ninguna imagen'}), 400

    if imagen:
        filename = secure_filename(imagen.filename)
        imagen.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return jsonify({'mensaje': 'Imagen subida exitosamente', 'url': os.path.join(app.config['UPLOAD_FOLDER'], filename)})

if __name__ == '__main__':
    app.run(debug=True)



