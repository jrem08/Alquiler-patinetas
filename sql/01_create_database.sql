CREATE DATABASE IF NOT EXISTS alquiler_patinetas
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE alquiler_patinetas;

CREATE TABLE IF NOT EXISTS zonas (
    id_zona INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    descripcion VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS puntos_acopio (
    id_punto_acopio INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    id_zona INT UNSIGNED NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    direccion VARCHAR(200) NOT NULL,
    latitud DECIMAL(9, 6) NOT NULL,
    longitud DECIMAL(10, 6) NOT NULL,
    capacidad_maxima INT UNSIGNED NOT NULL,
    CONSTRAINT fk_puntos_acopio_zonas
        FOREIGN KEY (id_zona) REFERENCES zonas (id_zona)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,
    CONSTRAINT chk_punto_latitud CHECK (latitud BETWEEN -90 AND 90),
    CONSTRAINT chk_punto_longitud CHECK (longitud BETWEEN -180 AND 180),
    CONSTRAINT chk_punto_capacidad CHECK (capacidad_maxima > 0),
    INDEX idx_puntos_acopio_zona (id_zona)
);

INSERT INTO zonas (nombre, descripcion)
VALUES ('Zona Centro', 'Zona inicial para pruebas de PAT-0003')
ON DUPLICATE KEY UPDATE nombre = VALUES(nombre);