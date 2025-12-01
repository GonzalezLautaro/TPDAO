-- ============================================================
-- SCRIPT DE CREACIÓN DE BASE DE DATOS - SISTEMA MÉDICO
-- ============================================================
-- Base de datos para gestión de turnos médicos, pacientes,
-- médicos, recetas, notificaciones y control de agendas

DROP DATABASE IF EXISTS hospital_db;
CREATE DATABASE hospital_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE hospital_db;

-- ============================================================
-- TABLA: Especialidad
-- ============================================================
CREATE TABLE Especialidad (
    id_especialidad INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    descripcion TEXT,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================================
-- TABLA: Médico
-- ============================================================
CREATE TABLE Medico (
    matricula INT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    telefono VARCHAR(20),
    email VARCHAR(100) UNIQUE,
    fecha_ingreso DATE NOT NULL,
    fecha_egreso DATE,
    activo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_nombre (nombre, apellido),
    INDEX idx_activo (activo)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================================
-- TABLA: Medico_especialidad (Relación muchos a muchos)
-- ============================================================
CREATE TABLE Medico_especialidad (
    matricula INT NOT NULL,
    id_especialidad INT NOT NULL,
    fecha_asignacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (matricula, id_especialidad),
    FOREIGN KEY (matricula) REFERENCES Medico(matricula) ON DELETE CASCADE,
    FOREIGN KEY (id_especialidad) REFERENCES Especialidad(id_especialidad) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================================
-- TABLA: Paciente
-- ============================================================
CREATE TABLE Paciente (
    id_paciente INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    telefono VARCHAR(20),
    fecha_nacimiento DATE NOT NULL,
    direccion VARCHAR(255),
    medico_asignado INT,
    activo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (medico_asignado) REFERENCES Medico(matricula) ON DELETE SET NULL,
    INDEX idx_nombre (nombre, apellido),
    INDEX idx_activo (activo)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================================
-- TABLA: Consultorio
-- ============================================================
CREATE TABLE Consultorio (
    id_consultorio INT PRIMARY KEY AUTO_INCREMENT,
    numero INT NOT NULL UNIQUE,
    piso INT NOT NULL,
    equipamiento VARCHAR(255),
    disponible BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_numero (numero),
    INDEX idx_piso (piso)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================================
-- TABLA: Agenda
-- ============================================================
CREATE TABLE Agenda (
    id_agenda INT PRIMARY KEY AUTO_INCREMENT,
    matricula INT NOT NULL,
    id_consultorio INT NOT NULL,
    dia_semana VARCHAR(20) NOT NULL,
    hora_inicio TIME NOT NULL,
    hora_fin TIME NOT NULL,
    activa BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (matricula) REFERENCES Medico(matricula) ON DELETE CASCADE,
    FOREIGN KEY (id_consultorio) REFERENCES Consultorio(id_consultorio) ON DELETE CASCADE,
    INDEX idx_medico (matricula),
    INDEX idx_consultorio (id_consultorio),
    UNIQUE KEY unique_agenda (matricula, id_consultorio, dia_semana)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================================
-- TABLA: Turno
-- ============================================================
CREATE TABLE Turno (
    id_turno INT AUTO_INCREMENT PRIMARY KEY,
    id_paciente INT NULL,
    matricula INT NOT NULL,
    id_consultorio INT NOT NULL,
    id_agenda INT NULL,
    fecha DATE NOT NULL,
    hora_inicio TIME NOT NULL,
    hora_fin TIME NOT NULL,
    estado ENUM('Libre', 'Programado', 'Atendido', 'Cancelado', 'Inasistencia') DEFAULT 'Libre',
    observaciones TEXT,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_paciente) REFERENCES Paciente(id_paciente),
    FOREIGN KEY (matricula) REFERENCES Medico(matricula),
    FOREIGN KEY (id_consultorio) REFERENCES Consultorio(id_consultorio),
    FOREIGN KEY (id_agenda) REFERENCES Agenda(id_agenda)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================================
-- TABLA: Cambio_estado
-- ============================================================
CREATE TABLE Cambio_estado (
    id_cambio INT PRIMARY KEY AUTO_INCREMENT,
    id_turno INT NOT NULL,
    estado_anterior VARCHAR(50),
    estado_nuevo VARCHAR(50) NOT NULL,
    fecha_cambio TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_turno) REFERENCES Turno(id_turno) ON DELETE CASCADE,
    INDEX idx_turno (id_turno),
    INDEX idx_fecha (fecha_cambio)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================================
-- TABLA: Laboratorio
-- ============================================================
CREATE TABLE Laboratorio (
    id_laboratorio INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(150) NOT NULL UNIQUE,
    razon_social VARCHAR(150),
    direccion VARCHAR(255),
    telefono VARCHAR(20),
    email VARCHAR(100),
    activo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_nombre (nombre),
    INDEX idx_activo (activo)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================================
-- TABLA: Medicamento
-- ============================================================
CREATE TABLE Medicamento (
    id_medicamento INT PRIMARY KEY AUTO_INCREMENT,
    id_laboratorio INT NOT NULL,
    nombre VARCHAR(150) NOT NULL,
    dosis VARCHAR(100) NOT NULL,
    presentacion VARCHAR(100),
    observaciones TEXT,
    activo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_laboratorio) REFERENCES Laboratorio(id_laboratorio) ON DELETE CASCADE,
    INDEX idx_nombre (nombre),
    INDEX idx_laboratorio (id_laboratorio),
    INDEX idx_activo (activo),
    UNIQUE KEY unique_medicamento (nombre, dosis, id_laboratorio)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================================
-- TABLA: Historial_clinico
-- ============================================================
CREATE TABLE Historial_clinico (
    id_historial INT PRIMARY KEY AUTO_INCREMENT,
    id_turno INT NOT NULL,
    id_paciente INT NOT NULL,
    diagnostico TEXT,
    tratamiento TEXT,
    notas TEXT,
    observaciones TEXT,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_turno) REFERENCES Turno(id_turno) ON DELETE CASCADE,
    FOREIGN KEY (id_paciente) REFERENCES Paciente(id_paciente) ON DELETE CASCADE,
    INDEX idx_turno (id_turno),
    INDEX idx_paciente (id_paciente),
    INDEX idx_fecha (fecha_registro)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================================
-- TABLA: Receta
-- ============================================================
CREATE TABLE Receta (
    id_receta INT PRIMARY KEY AUTO_INCREMENT,
    id_historial INT NOT NULL,
    fecha_emision DATE NOT NULL,
    fecha_vencimiento DATE,
    observaciones TEXT,
    activa BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_historial) REFERENCES Historial_clinico(id_historial) ON DELETE CASCADE,
    INDEX idx_historial (id_historial),
    INDEX idx_fecha (fecha_emision),
    INDEX idx_activa (activa)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================================
-- TABLA: Detalle_receta
-- ============================================================
CREATE TABLE Detalle_receta (
    id_detalle INT PRIMARY KEY AUTO_INCREMENT,
    id_receta INT NOT NULL,
    id_medicamento INT NOT NULL,
    dosis VARCHAR(100),
    indicaciones TEXT NOT NULL,
    cantidad INT DEFAULT 1,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_receta) REFERENCES Receta(id_receta) ON DELETE CASCADE,
    FOREIGN KEY (id_medicamento) REFERENCES Medicamento(id_medicamento) ON DELETE CASCADE,
    INDEX idx_receta (id_receta),
    INDEX idx_medicamento (id_medicamento)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================================
-- TABLA: Notificacion
-- ============================================================
CREATE TABLE Notificacion (
    id_notificacion INT PRIMARY KEY AUTO_INCREMENT,
    id_turno INT NOT NULL,
    fecha_hora_envio DATETIME NOT NULL,
    estado VARCHAR(50) NOT NULL DEFAULT 'Pendiente',
    medio_envio VARCHAR(50),
    intentos INT DEFAULT 0,
    fecha_envio_real DATETIME,
    motivo_error TEXT,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_turno) REFERENCES Turno(id_turno) ON DELETE CASCADE,
    INDEX idx_turno (id_turno),
    INDEX idx_estado (estado),
    INDEX idx_fecha (fecha_hora_envio)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================================
-- VISTAS ÚTILES
-- ============================================================

-- Vista: Turnos programados por médico
CREATE VIEW vista_turnos_medico AS
SELECT 
    t.id_turno,
    m.matricula,
    CONCAT(m.nombre, ' ', m.apellido) AS medico,
    CONCAT(p.nombre, ' ', p.apellido) AS paciente,
    t.fecha,
    CONCAT(t.hora_inicio, ' - ', t.hora_fin) AS horario,
    t.estado,
    c.numero AS consultorio
FROM Turno t
JOIN Medico m ON t.matricula = m.matricula
JOIN Paciente p ON t.id_paciente = p.id_paciente
JOIN Consultorio c ON t.id_consultorio = c.id_consultorio
ORDER BY t.fecha, t.hora_inicio;

-- Vista: Pacientes activos
CREATE VIEW vista_pacientes_activos AS
SELECT 
    id_paciente,
    CONCAT(nombre, ' ', apellido) AS nombre_completo,
    telefono,
    fecha_nacimiento,
    direccion,
    fecha_creacion
FROM Paciente
WHERE activo = TRUE
ORDER BY nombre, apellido;

-- Vista: Médicos disponibles
CREATE VIEW vista_medicos_disponibles AS
SELECT 
    matricula,
    CONCAT(nombre, ' ', apellido) AS nombre_completo,
    telefono,
    email,
    fecha_ingreso
FROM Medico
WHERE activo = TRUE
ORDER BY nombre, apellido;