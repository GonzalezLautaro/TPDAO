-- ============================================================
-- SCRIPT DE CREACIÓN DE BASE DE DATOS - SISTEMA MÉDICO
-- Base de datos: hospital_db_tpdao
-- ============================================================

DROP DATABASE IF EXISTS hospital_db_tpdao;
CREATE DATABASE hospital_db_tpdao CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE hospital_db_tpdao;

-- ============================================================
-- TABLA: especialidad
-- ============================================================
CREATE TABLE especialidad (
  id_especialidad INT NOT NULL AUTO_INCREMENT,
  nombre VARCHAR(100) NOT NULL,
  descripcion TEXT,
  fecha_creacion TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id_especialidad),
  UNIQUE KEY (nombre)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ============================================================
-- TABLA: medico
-- ============================================================
CREATE TABLE medico (
  matricula INT NOT NULL,
  nombre VARCHAR(100) NOT NULL,
  apellido VARCHAR(100) NOT NULL,
  telefono VARCHAR(20) DEFAULT NULL,
  email VARCHAR(100) DEFAULT NULL,
  fecha_ingreso DATE NOT NULL,
  fecha_egreso DATE DEFAULT NULL,
  activo TINYINT(1) DEFAULT '1',
  fecha_creacion TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (matricula),
  UNIQUE KEY (email),
  KEY idx_nombre (nombre, apellido),
  KEY idx_activo (activo)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ============================================================
-- TABLA: medico_especialidad
-- ============================================================
CREATE TABLE medico_especialidad (
  matricula INT NOT NULL,
  id_especialidad INT NOT NULL,
  fecha_asignacion TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (matricula, id_especialidad),
  KEY (id_especialidad),
  CONSTRAINT fk_medico_especialidad_medico FOREIGN KEY (matricula) REFERENCES medico (matricula) ON DELETE CASCADE,
  CONSTRAINT fk_medico_especialidad_especialidad FOREIGN KEY (id_especialidad) REFERENCES especialidad (id_especialidad) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ============================================================
-- TABLA: paciente
-- ============================================================
CREATE TABLE paciente (
  id_paciente INT NOT NULL AUTO_INCREMENT,
  nombre VARCHAR(100) NOT NULL,
  apellido VARCHAR(100) NOT NULL,
  telefono VARCHAR(20) DEFAULT NULL,
  fecha_nacimiento DATE NOT NULL,
  direccion VARCHAR(255) DEFAULT NULL,
  medico_asignado INT DEFAULT NULL,
  activo TINYINT(1) DEFAULT '1',
  fecha_creacion TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id_paciente),
  KEY (medico_asignado),
  KEY idx_nombre (nombre, apellido),
  KEY idx_activo (activo),
  CONSTRAINT fk_paciente_medico FOREIGN KEY (medico_asignado) REFERENCES medico (matricula) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ============================================================
-- TABLA: consultorio
-- ============================================================
CREATE TABLE consultorio (
  id_consultorio INT NOT NULL AUTO_INCREMENT,
  numero INT NOT NULL,
  piso INT NOT NULL,
  equipamiento VARCHAR(255) DEFAULT NULL,
  disponible TINYINT(1) DEFAULT '1',
  fecha_creacion TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id_consultorio),
  UNIQUE KEY (numero),
  KEY idx_numero (numero),
  KEY idx_piso (piso)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ============================================================
-- TABLA: agenda
-- ============================================================
CREATE TABLE agenda (
  id_agenda INT NOT NULL AUTO_INCREMENT,
  matricula INT NOT NULL,
  id_consultorio INT NOT NULL,
  dia_semana VARCHAR(20) NOT NULL,
  hora_inicio TIME NOT NULL,
  hora_fin TIME NOT NULL,
  activa TINYINT(1) DEFAULT '1',
  fecha_creacion TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id_agenda),
  UNIQUE KEY unique_agenda (matricula, id_consultorio, dia_semana),
  KEY idx_medico (matricula),
  KEY idx_consultorio (id_consultorio),
  CONSTRAINT fk_agenda_medico FOREIGN KEY (matricula) REFERENCES medico (matricula) ON DELETE CASCADE,
  CONSTRAINT fk_agenda_consultorio FOREIGN KEY (id_consultorio) REFERENCES consultorio (id_consultorio) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ============================================================
-- TABLA: turno (CON id_especialidad)
-- ============================================================
CREATE TABLE turno (
  id_turno INT NOT NULL AUTO_INCREMENT,
  id_paciente INT DEFAULT NULL,
  matricula INT NOT NULL,
  id_consultorio INT NOT NULL,
  id_agenda INT NOT NULL,
  id_especialidad INT DEFAULT NULL,
  fecha DATE NOT NULL,
  hora_inicio TIME NOT NULL,
  hora_fin TIME NOT NULL,
  estado VARCHAR(50) NOT NULL DEFAULT 'Libre',
  observaciones TEXT,
  fecha_creacion TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id_turno),
  UNIQUE KEY unique_turno (id_paciente, matricula, fecha, hora_inicio),
  KEY (id_consultorio),
  KEY (id_agenda),
  KEY (id_especialidad),
  KEY idx_paciente (id_paciente),
  KEY idx_medico (matricula),
  KEY idx_fecha (fecha),
  KEY idx_estado (estado),
  CONSTRAINT fk_turno_paciente FOREIGN KEY (id_paciente) REFERENCES paciente (id_paciente) ON DELETE CASCADE,
  CONSTRAINT fk_turno_medico FOREIGN KEY (matricula) REFERENCES medico (matricula) ON DELETE CASCADE,
  CONSTRAINT fk_turno_consultorio FOREIGN KEY (id_consultorio) REFERENCES consultorio (id_consultorio) ON DELETE CASCADE,
  CONSTRAINT fk_turno_agenda FOREIGN KEY (id_agenda) REFERENCES agenda (id_agenda) ON DELETE CASCADE,
  CONSTRAINT fk_turno_especialidad FOREIGN KEY (id_especialidad) REFERENCES especialidad (id_especialidad) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ============================================================
-- TABLA: cambio_estado
-- ============================================================
CREATE TABLE cambio_estado (
  id_cambio INT NOT NULL AUTO_INCREMENT,
  id_turno INT NOT NULL,
  estado_anterior VARCHAR(50) DEFAULT NULL,
  estado_nuevo VARCHAR(50) NOT NULL,
  fecha_cambio TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id_cambio),
  KEY idx_turno (id_turno),
  KEY idx_fecha (fecha_cambio),
  CONSTRAINT fk_cambio_estado_turno FOREIGN KEY (id_turno) REFERENCES turno (id_turno) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ============================================================
-- TABLA: laboratorio
-- ============================================================
CREATE TABLE laboratorio (
  id_laboratorio INT NOT NULL AUTO_INCREMENT,
  nombre VARCHAR(150) NOT NULL,
  razon_social VARCHAR(150) DEFAULT NULL,
  direccion VARCHAR(255) DEFAULT NULL,
  telefono VARCHAR(20) DEFAULT NULL,
  email VARCHAR(100) DEFAULT NULL,
  activo TINYINT(1) DEFAULT '1',
  fecha_creacion TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id_laboratorio),
  UNIQUE KEY (nombre),
  KEY idx_nombre (nombre),
  KEY idx_activo (activo)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ============================================================
-- TABLA: medicamento
-- ============================================================
CREATE TABLE medicamento (
  id_medicamento INT NOT NULL AUTO_INCREMENT,
  id_laboratorio INT NOT NULL,
  nombre VARCHAR(150) NOT NULL,
  dosis VARCHAR(100) NOT NULL,
  presentacion VARCHAR(100) DEFAULT NULL,
  observaciones TEXT,
  activo TINYINT(1) DEFAULT '1',
  fecha_creacion TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id_medicamento),
  UNIQUE KEY unique_medicamento (nombre, dosis, id_laboratorio),
  KEY idx_nombre (nombre),
  KEY idx_laboratorio (id_laboratorio),
  KEY idx_activo (activo),
  CONSTRAINT fk_medicamento_laboratorio FOREIGN KEY (id_laboratorio) REFERENCES laboratorio (id_laboratorio) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ============================================================
-- TABLA: historial_clinico
-- ============================================================
CREATE TABLE historial_clinico (
  id_historial INT NOT NULL AUTO_INCREMENT,
  id_turno INT NOT NULL,
  id_paciente INT NOT NULL,
  diagnostico TEXT,
  tratamiento TEXT,
  notas TEXT,
  observaciones TEXT,
  fecha_registro TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id_historial),
  KEY idx_turno (id_turno),
  KEY idx_paciente (id_paciente),
  KEY idx_fecha (fecha_registro),
  CONSTRAINT fk_historial_turno FOREIGN KEY (id_turno) REFERENCES turno (id_turno) ON DELETE CASCADE,
  CONSTRAINT fk_historial_paciente FOREIGN KEY (id_paciente) REFERENCES paciente (id_paciente) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ============================================================
-- TABLA: receta
-- ============================================================
CREATE TABLE receta (
  id_receta INT NOT NULL AUTO_INCREMENT,
  id_historial INT NOT NULL,
  fecha_emision DATE NOT NULL,
  fecha_vencimiento DATE DEFAULT NULL,
  observaciones TEXT,
  activa TINYINT(1) DEFAULT '1',
  fecha_creacion TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id_receta),
  KEY idx_historial (id_historial),
  KEY idx_fecha (fecha_emision),
  KEY idx_activa (activa),
  CONSTRAINT fk_receta_historial FOREIGN KEY (id_historial) REFERENCES historial_clinico (id_historial) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ============================================================
-- TABLA: detalle_receta
-- ============================================================
CREATE TABLE detalle_receta (
  id_detalle INT NOT NULL AUTO_INCREMENT,
  id_receta INT NOT NULL,
  id_medicamento INT NOT NULL,
  dosis VARCHAR(100) DEFAULT NULL,
  indicaciones TEXT NOT NULL,
  cantidad INT DEFAULT '1',
  fecha_creacion TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id_detalle),
  KEY idx_receta (id_receta),
  KEY idx_medicamento (id_medicamento),
  CONSTRAINT fk_detalle_receta FOREIGN KEY (id_receta) REFERENCES receta (id_receta) ON DELETE CASCADE,
  CONSTRAINT fk_detalle_medicamento FOREIGN KEY (id_medicamento) REFERENCES medicamento (id_medicamento) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ============================================================
-- TABLA: notificacion
-- ============================================================
CREATE TABLE notificacion (
  id_notificacion INT NOT NULL AUTO_INCREMENT,
  id_turno INT NOT NULL,
  fecha_hora_envio DATETIME NOT NULL,
  estado VARCHAR(50) NOT NULL DEFAULT 'Pendiente',
  medio_envio VARCHAR(50) DEFAULT NULL,
  intentos INT DEFAULT '0',
  fecha_envio_real DATETIME DEFAULT NULL,
  motivo_error TEXT,
  fecha_creacion TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id_notificacion),
  KEY idx_turno (id_turno),
  KEY idx_estado (estado),
  KEY idx_fecha (fecha_hora_envio),
  CONSTRAINT fk_notificacion_turno FOREIGN KEY (id_turno) REFERENCES turno (id_turno) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ============================================================
-- VISTAS
-- ============================================================

CREATE VIEW vista_medicos_disponibles AS
SELECT 
    matricula,
    CONCAT(nombre, ' ', apellido) AS nombre_completo,
    telefono,
    email,
    fecha_ingreso
FROM medico
WHERE activo = TRUE
ORDER BY nombre, apellido;

CREATE VIEW vista_pacientes_activos AS
SELECT 
    id_paciente,
    CONCAT(nombre, ' ', apellido) AS nombre_completo,
    telefono,
    fecha_nacimiento,
    direccion,
    fecha_creacion
FROM paciente
WHERE activo = TRUE
ORDER BY nombre, apellido;

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
FROM turno t
JOIN medico m ON t.matricula = m.matricula
JOIN paciente p ON t.id_paciente = p.id_paciente
JOIN consultorio c ON t.id_consultorio = c.id_consultorio
ORDER BY t.fecha, t.hora_inicio;
