-- ALTER USER 'root'@'localhost' IDENTIFIED BY 'USAT2026';
-- FLUSH PRIVILEGES;
-- 1. Eliminar la base de datos (esquema) si existe
DROP DATABASE IF EXISTS PREFIX_medical_app_db;

-- 2. Crear la base de datos de nuevo
CREATE DATABASE PREFIX_medical_app_db;

-- 3. (Opcional) Seleccionar la base de datos para usarla
USE PREFIX_medical_app_db;

-- =====================================================
-- TABLAS DE ESTADO
-- =====================================================

CREATE TABLE estado_usuario (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(30) NOT NULL UNIQUE
);

CREATE TABLE estado_medico (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(30) NOT NULL UNIQUE
);

CREATE TABLE estado_cita (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(30) NOT NULL UNIQUE
);

CREATE TABLE estado_horario_disponible (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(30) NOT NULL UNIQUE
);

-- =====================================================
-- TABLA: rol
-- =====================================================

CREATE TABLE rol (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(30) NOT NULL UNIQUE
);

-- =====================================================
-- TABLA: usuario y usuario_fcm
-- =====================================================

CREATE TABLE usuario (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(120) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    rol_id INT NOT NULL,
    estado_usuario_id INT NOT NULL,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (rol_id) REFERENCES rol(id),
    FOREIGN KEY (estado_usuario_id) REFERENCES estado_usuario(id)
);
ALTER TABLE usuario ADD COLUMN foto VARCHAR(20);
ALTER TABLE usuario ADD COLUMN fecha_hora_actualizacion TIMESTAMP;

CREATE TABLE usuario_fcm (
    id INT(11) NOT NULL AUTO_INCREMENT,
    usuario_id INT(11) NOT NULL,
    dispositivo VARCHAR(100) NOT NULL COLLATE 'latin1_swedish_ci',
    token TEXT NOT NULL COLLATE 'latin1_swedish_ci',
    fecha_hora_registro TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    estado_id INT(11) NOT NULL DEFAULT '1',
    PRIMARY KEY (id) USING BTREE,
    INDEX fk_usuario_fcm (usuario_id) USING BTREE,
    INDEX fk_usuario_fcm_estado (estado_id) USING BTREE,
    CONSTRAINT fk_usuario_fcm FOREIGN KEY (usuario_id) REFERENCES usuario (id),
    CONSTRAINT fk_usuario_fcm_estado FOREIGN KEY (estado_id) REFERENCES estado_usuario (id)
);
-- =====================================================
-- TABLA: paciente
-- =====================================================

CREATE TABLE paciente (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL UNIQUE,
    nombres VARCHAR(100) NOT NULL,
    apellidos VARCHAR(100) NOT NULL,
    dni CHAR(8) NOT NULL UNIQUE,
    celular VARCHAR(15),
    fecha_nacimiento DATE,
    genero ENUM('Masculino', 'Femenino', 'Otro') DEFAULT 'Otro',
    FOREIGN KEY (usuario_id) REFERENCES usuario(id)
);

-- =====================================================
-- TABLA: administrativo
-- =====================================================

CREATE TABLE administrativo (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL UNIQUE,
    nombres VARCHAR(100) NOT NULL,
    apellidos VARCHAR(100) NOT NULL,
    dni CHAR(8) NOT NULL UNIQUE,
    celular VARCHAR(15),
    cargo VARCHAR(100) NOT NULL,
    area VARCHAR(100),
    FOREIGN KEY (usuario_id) REFERENCES usuario(id)
);

-- =====================================================
-- TABLA: especialidad
-- =====================================================

CREATE TABLE especialidad (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    descripcion VARCHAR(255),
    imagen_url VARCHAR(255)
);

-- =====================================================
-- TABLA: medico
-- =====================================================

CREATE TABLE medico (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL UNIQUE,
    nombres VARCHAR(100) NOT NULL,
    apellidos VARCHAR(100) NOT NULL,
    dni CHAR(8) NOT NULL UNIQUE,
    cmp VARCHAR(20) NOT NULL UNIQUE,
    telefono VARCHAR(15),
    consultorio VARCHAR(20),
    estado_medico_id INT NOT NULL,
    imagen_url VARCHAR(255) default 'default.png',
    FOREIGN KEY (usuario_id) REFERENCES usuario(id),
    FOREIGN KEY (estado_medico_id) REFERENCES estado_medico(id)
);

-- =====================================================
-- TABLA: medico_especialidad
-- =====================================================

CREATE TABLE medico_especialidad (
    id INT AUTO_INCREMENT PRIMARY KEY,
    medico_id INT NOT NULL,
    especialidad_id INT NOT NULL,
    FOREIGN KEY (medico_id) REFERENCES medico(id),
    FOREIGN KEY (especialidad_id) REFERENCES especialidad(id),
    UNIQUE (medico_id, especialidad_id)
);

-- =====================================================
-- TABLA: horario_disponible
-- Cada registro representa un bloque de atención reservable
-- =====================================================

CREATE TABLE horario_disponible (
    id INT AUTO_INCREMENT PRIMARY KEY,
    medico_id INT NOT NULL,
    especialidad_id INT NOT NULL,
    fecha DATE NOT NULL,
    hora_inicio TIME NOT NULL,
    hora_fin TIME NOT NULL,
    estado_horario_disponible_id INT NOT NULL,
    FOREIGN KEY (medico_id) REFERENCES medico(id),
    FOREIGN KEY (especialidad_id) REFERENCES especialidad(id),
    FOREIGN KEY (estado_horario_disponible_id) REFERENCES estado_horario_disponible(id),
    UNIQUE (medico_id, fecha, hora_inicio, hora_fin)
);

-- =====================================================
-- TABLA: cita
-- La cita queda enlazada al horario disponible seleccionado
-- =====================================================

CREATE TABLE cita (
    id INT AUTO_INCREMENT PRIMARY KEY,
    paciente_id INT NOT NULL,
    horario_disponible_id INT NOT NULL UNIQUE,
    motivo TEXT,
    motivo_cancelacion TEXT,
    paciente_oncologico BOOLEAN DEFAULT FALSE,
    estado_cita_id INT NOT NULL,
    creado_por_usuario_id INT NOT NULL,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (paciente_id) REFERENCES paciente(id),
    FOREIGN KEY (horario_disponible_id) REFERENCES horario_disponible(id),
    FOREIGN KEY (estado_cita_id) REFERENCES estado_cita(id),
    FOREIGN KEY (creado_por_usuario_id) REFERENCES usuario(id)
);

CREATE INDEX idx_medico_especialidad_especialidad ON medico_especialidad(especialidad_id);
CREATE INDEX idx_horario_especialidad_fecha_estado ON horario_disponible(especialidad_id, fecha, estado_horario_disponible_id);
CREATE INDEX idx_cita_paciente ON cita(paciente_id);

-- =====================================================
-- DATOS MAESTROS
-- =====================================================

INSERT INTO estado_usuario (nombre) VALUES
('ACTIVO'),
('INACTIVO');

INSERT INTO estado_medico (nombre) VALUES
('ACTIVO'),
('INACTIVO');

INSERT INTO estado_cita (nombre) VALUES
('PENDIENTE'),
('CONFIRMADA'),
('CANCELADA'),
('ATENDIDA'),
('REPROGRAMADA');

INSERT INTO estado_horario_disponible (nombre) VALUES
('DISPONIBLE'),
('RESERVADO'),
('NO_DISPONIBLE');

INSERT INTO rol (nombre) VALUES
('PACIENTE'),
('MEDICO'),
('ADMINISTRATIVO');

-- =====================================================
-- USUARIOS
-- =====================================================

INSERT INTO usuario (email, password, rol_id, estado_usuario_id) VALUES
('ana.torres@gmail.com', '123456', 1, 1),
('luis.mendoza@gmail.com', '123456', 1, 1),
('carla.vasquez@gmail.com', '123456', 1, 1),

('mlopez@clinica.com', '123456', 2, 1),
('cramirez@clinica.com', '123456', 2, 1),
('acastillo@clinica.com', '123456', 2, 1),
('lfernandez@clinica.com', '123456', 2, 1),
('rmendoza@clinica.com', '123456', 2, 1),

('recepcion1@clinica.com', '123456', 3, 1),
('recepcion2@clinica.com', '123456', 3, 1);
INSERT INTO usuario (email, password, rol_id, estado_usuario_id) VALUES
('luisbarboza0503@gmail.com', '123456', 1, 1);

-- =====================================================
-- PACIENTES
-- =====================================================

INSERT INTO paciente (usuario_id, nombres, apellidos, dni, celular, fecha_nacimiento, genero) VALUES
(1, 'Ana', 'Torres Díaz', '71234567', '987654321', '2000-05-10', 'Femenino'),
(2, 'Luis', 'Mendoza Ruiz', '72345678', '912345678', '1998-08-21', 'Masculino'),
(3, 'Carla', 'Vásquez Soto', '73456789', '998877665', '2002-01-15', 'Femenino');
INSERT INTO paciente (usuario_id, nombres, apellidos, dni, celular, fecha_nacimiento, genero) VALUES
(11, 'Luis Miguel', 'Barboza Vilchez', '71573896', '992712408', '2002-05-03', 'Masculino');

-- =====================================================
-- ADMINISTRATIVOS
-- =====================================================

INSERT INTO administrativo (usuario_id, nombres, apellidos, dni, celular, cargo, area) VALUES
(9, 'Patricia', 'Campos Ríos', '74567890', '955111222', 'Recepcionista', 'Admisión'),
(10, 'Miguel', 'Paredes León', '75678901', '955222333', 'Asistente administrativo', 'Caja');

-- =====================================================
-- ESPECIALIDADES
-- =====================================================

INSERT INTO especialidad (nombre, descripcion, imagen_url) VALUES
('Pediatría', 'Atención médica especializada para niños y adolescentes', '1.jpg'),
('Cardiología', 'Diagnóstico y tratamiento de enfermedades del corazón', '1.jpg'),
('Dermatología', 'Atención de enfermedades y cuidados de la piel', '1.jpg'),
('Medicina General', 'Atención médica inicial y control de enfermedades comunes', '1.jpg'),
('Ginecología', 'Atención integral de la salud de la mujer', '1.jpg');

-- =====================================================
-- MÉDICOS
-- =====================================================

INSERT INTO medico (usuario_id, nombres, apellidos, dni, cmp, telefono, consultorio, estado_medico_id, imagen_url) VALUES
(4, 'María', 'López Gómez', '76789012', 'CMP1001', '955333444', '101', 1, '2.png'),
(5, 'Carlos', 'Ramírez Torres', '77890123', 'CMP1002', '955444555', '202', 1, '2.png'),
(6, 'Andrea', 'Castillo Pérez', '78901234', 'CMP1003', '955555666', '203', 1, '3.png'),
(7, 'Luis', 'Fernández Díaz', '79012345', 'CMP1004', '955666777', '104', 1, '4.png'),
(8, 'Rosa', 'Mendoza Silva', '70123456', 'CMP1005', '955777888', '305', 1, '5.png');

-- =====================================================
-- RELACIÓN MÉDICO - ESPECIALIDAD
-- =====================================================

INSERT INTO medico_especialidad (medico_id, especialidad_id) VALUES
(1, 1),
(2, 2),
(3, 3),
(4, 4),
(5, 5);

-- =====================================================
-- HORARIOS DISPONIBLES
-- Cada fila es un bloque reservable
-- =====================================================

INSERT INTO horario_disponible (
    medico_id, especialidad_id, fecha, hora_inicio, hora_fin, estado_horario_disponible_id
) VALUES

-- JUNIO 2026
(1,1,'2026-06-24','08:00:00','08:30:00',1),
(1,1,'2026-06-24','08:30:00','09:00:00',1),
(2,2,'2026-06-25','15:00:00','15:30:00',1),
(3,3,'2026-06-26','09:00:00','09:30:00',2),
(4,4,'2026-06-27','10:00:00','10:30:00',1),
(5,5,'2026-06-28','14:00:00','14:30:00',1),
(1,1,'2026-06-30','09:00:00','09:30:00',1),

-- JULIO 2026 (muchos registros)
(1,1,'2026-07-01','08:00:00','08:30:00',1),
(1,1,'2026-07-01','08:30:00','09:00:00',1),
(1,1,'2026-07-01','09:00:00','09:30:00',2),

(2,2,'2026-07-02','15:00:00','15:30:00',1),
(2,2,'2026-07-02','15:30:00','16:00:00',1),
(2,2,'2026-07-02','16:00:00','16:30:00',2),

(3,3,'2026-07-03','09:00:00','09:30:00',1),
(3,3,'2026-07-03','09:30:00','10:00:00',1),
(3,3,'2026-07-03','10:00:00','10:30:00',1),

(4,4,'2026-07-06','08:00:00','08:30:00',1),
(4,4,'2026-07-06','08:30:00','09:00:00',1),
(4,4,'2026-07-06','09:00:00','09:30:00',2),

(5,5,'2026-07-07','14:00:00','14:30:00',1),
(5,5,'2026-07-07','14:30:00','15:00:00',1),
(5,5,'2026-07-07','15:00:00','15:30:00',1),

(1,1,'2026-07-08','08:00:00','08:30:00',1),
(1,1,'2026-07-08','08:30:00','09:00:00',2),

(2,2,'2026-07-09','15:00:00','15:30:00',1),
(2,2,'2026-07-09','15:30:00','16:00:00',1),

(3,3,'2026-07-10','09:00:00','09:30:00',1),
(3,3,'2026-07-10','09:30:00','10:00:00',2),

(4,4,'2026-07-13','08:00:00','08:30:00',1),
(4,4,'2026-07-13','08:30:00','09:00:00',1),
(4,4,'2026-07-13','09:00:00','09:30:00',1),

(5,5,'2026-07-14','14:00:00','14:30:00',1),
(5,5,'2026-07-14','14:30:00','15:00:00',2),
(5,5,'2026-07-14','15:00:00','15:30:00',1),

(1,1,'2026-07-15','08:00:00','08:30:00',1),
(1,1,'2026-07-15','08:30:00','09:00:00',1),
(2,2,'2026-07-16','15:00:00','15:30:00',1),
(2,2,'2026-07-16','15:30:00','16:00:00',2),
(3,3,'2026-07-17','09:00:00','09:30:00',1),
(3,3,'2026-07-17','09:30:00','10:00:00',1),

(4,4,'2026-07-20','08:00:00','08:30:00',1),
(4,4,'2026-07-20','08:30:00','09:00:00',1),
(5,5,'2026-07-21','14:00:00','14:30:00',1),
(5,5,'2026-07-21','14:30:00','15:00:00',1),

(1,1,'2026-07-22','08:00:00','08:30:00',1),
(1,1,'2026-07-22','08:30:00','09:00:00',2),
(2,2,'2026-07-23','15:00:00','15:30:00',1),
(2,2,'2026-07-23','15:30:00','16:00:00',1),

(3,3,'2026-07-24','09:00:00','09:30:00',1),
(3,3,'2026-07-24','09:30:00','10:00:00',1),
(4,4,'2026-07-27','08:00:00','08:30:00',1),
(4,4,'2026-07-27','08:30:00','09:00:00',1),

(5,5,'2026-07-28','14:00:00','14:30:00',1),
(5,5,'2026-07-28','14:30:00','15:00:00',2),
(1,1,'2026-07-29','08:00:00','08:30:00',1),
(1,1,'2026-07-29','08:30:00','09:00:00',1),
(2,2,'2026-07-30','15:00:00','15:30:00',1),
(2,2,'2026-07-30','15:30:00','16:00:00',1),
(3,3,'2026-07-31','09:00:00','09:30:00',1),

-- AGOSTO 2026
(4,4,'2026-08-01','08:00:00','08:30:00',1),
(4,4,'2026-08-01','08:30:00','09:00:00',1),
(5,5,'2026-08-02','14:00:00','14:30:00',1),
(5,5,'2026-08-02','14:30:00','15:00:00',1);

-- =====================================================
-- CITAS DE PRUEBA
-- =====================================================

INSERT INTO cita (paciente_id, horario_disponible_id, motivo, paciente_oncologico, estado_cita_id, creado_por_usuario_id) VALUES
(1, 2, 'Dolor de garganta y fiebre', FALSE, 2, 1),
(1, 5, 'Erupción en la piel', FALSE, 1, 1),
(2, 8, 'Chequeo cardiológico', FALSE, 2, 9),
(3,10, 'Control ginecológico', FALSE, 1, 3),
(1, 3, 'Control médico general', TRUE, 1, 9);

UPDATE usuario SET PASSWORD = '$argon2id$v=19$m=65536,t=3,p=4$DhuQucaekZr1yu11XfTSzQ$+72Neob1Licd0LMxPmTp9DdVMdVGbsNIwigVp73uIxo'