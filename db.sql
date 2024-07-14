CREATE DATABASE IF NOT EXISTS GameHero;
USE GameHero;

-- Crear la tabla de país si no existe
CREATE TABLE IF NOT EXISTS Pais (
    id_pais INT PRIMARY KEY AUTO_INCREMENT,
    pais VARCHAR(500)
);

-- Crear la tabla de provincia si no existe
CREATE TABLE IF NOT EXISTS Provincia (
    id_provincia INT PRIMARY KEY AUTO_INCREMENT,
    provincia VARCHAR(500),
    id_pais INT,
    FOREIGN KEY (id_pais) REFERENCES Pais(id_pais)
);

-- Crear la tabla de localidad si no existe
CREATE TABLE IF NOT EXISTS Ciudad (
    id_ciudad INT PRIMARY KEY AUTO_INCREMENT,
    ciudad VARCHAR(500),
    id_provincia INT,
    FOREIGN KEY (id_provincia) REFERENCES Provincia(id_provincia)
);

-- Tabla de Usuario
CREATE TABLE IF NOT EXISTS Usuario (
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
);

-- Tabla categoria 
CREATE TABLE IF NOT EXISTS Categoria (
    id_categoria INT PRIMARY KEY AUTO_INCREMENT,
    nombre ENUM('Acción', 'Estrategia', 'Aventura', 'Simulación', 'Ingenio', 'Arcade', 'Otros', 'Ninguna'),
    padre INT,
    FOREIGN KEY (Padre) REFERENCES Categoria(id_categoria)
);

-- Tabla de Usuario_Categoria
CREATE TABLE IF NOT EXISTS Usuario_Categoria (
    id_usuario_categoria INT PRIMARY KEY AUTO_INCREMENT,
    id_usuario INT,
    id_categoria INT,
    FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario),
    FOREIGN KEY (id_categoria) REFERENCES Categoria(id_categoria)
);
-- Tabla de Reaccion
CREATE TABLE IF NOT EXISTS Reaccion (
    id_reaccion INT PRIMARY KEY AUTO_INCREMENT,
    tipo ENUM('Bueno', 'Intermedio', 'Interesante', 'Malo')
);

-- Tabla de Juego
CREATE TABLE IF NOT EXISTS Juego (
    id_juego INT PRIMARY KEY AUTO_INCREMENT,
    titulo VARCHAR(100),
    contenido TEXT,
    contenido_url VARCHAR(255),
    resumen TEXT,
    id_reaccion INT,
    FOREIGN KEY (id_reaccion) REFERENCES Reaccion(id_reaccion)
);

-- Tabla intermedia Juego_Categoria
CREATE TABLE IF NOT EXISTS Juego_Categoria (
    id_juego_categoria INT PRIMARY KEY AUTO_INCREMENT,
    id_juego INT,
    id_categoria INT,
    FOREIGN KEY (id_juego) REFERENCES Juego(id_juego),
    FOREIGN KEY (id_categoria) REFERENCES Categoria(id_categoria)
);

-- Tabla de Comentario
CREATE TABLE IF NOT EXISTS Comentario (
    id_comentario INT PRIMARY KEY AUTO_INCREMENT,
    texto TEXT,
    id_usuario INT,
    id_juego INT,
    id_reaccion INT,
    FOREIGN KEY (id_reaccion) REFERENCES Reaccion(id_reaccion),
    FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario),
    FOREIGN KEY (id_juego) REFERENCES Juego(id_juego)
);


