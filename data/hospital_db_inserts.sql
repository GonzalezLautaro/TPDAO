-- ============================================================
-- SCRIPT DE INSERCIÓN DE DATOS - SISTEMA MÉDICO
-- ============================================================
-- Datos de ejemplo para el sistema de gestión médica

USE hospital_db;

-- ============================================================
-- 1. INSERTAR ESPECIALIDADES
-- ============================================================
INSERT INTO Especialidad (nombre, descripcion) VALUES
('Cardiología', 'Especialista del corazón y sistema cardiovascular'),
('Neurología', 'Especialista del sistema nervioso'),
('Dermatología', 'Especialista de la piel'),
('Pediatría', 'Especialista en medicina infantil'),
('Oftalmología', 'Especialista en enfermedades de los ojos'),
('Psiquiatría', 'Especialista en salud mental');

-- ============================================================
-- 2. INSERTAR MÉDICOS
-- ============================================================
INSERT INTO Medico (matricula, nombre, apellido, telefono, email, fecha_ingreso, activo) VALUES
(12345, 'Juan', 'Pérez', '1123456789', 'juan.perez@hospital.com', '2020-01-15', TRUE),
(12346, 'María', 'García', '1198765432', 'maria.garcia@hospital.com', '2019-06-20', TRUE),
(12347, 'Carlos', 'López', '1156789012', 'carlos.lopez@hospital.com', '2021-03-10', TRUE),
(12348, 'Ana', 'Martínez', '1134567890', 'ana.martinez@hospital.com', '2022-01-05', TRUE),
(12349, 'Roberto', 'González', '1167890123', 'roberto.gonzalez@hospital.com', '2018-09-12', TRUE),
(12350, 'Sofía', 'Rodríguez', '1145678901', 'sofia.rodriguez@hospital.com', '2021-11-22', TRUE);

-- ============================================================
-- 3. ASIGNAR ESPECIALIDADES A MÉDICOS
-- ============================================================
INSERT INTO Medico_especialidad (matricula, id_especialidad) VALUES
-- Juan Pérez - Cardiología
(12345, 1),
-- María García - Neurología
(12346, 2),
-- Carlos López - Dermatología
(12347, 3),
-- Ana Martínez - Pediatría
(12348, 4),
-- Roberto González - Oftalmología y Cardiología
(12349, 5),
(12349, 1),
-- Sofía Rodríguez - Psiquiatría
(12350, 6);

-- ============================================================
-- 4. INSERTAR CONSULTORIOS
-- ============================================================
INSERT INTO Consultorio (numero, piso, equipamiento, disponible) VALUES
(101, 1, 'Completo - Ecocardiograma', TRUE),
(102, 1, 'Básico - Escritorio y camilla', TRUE),
(103, 1, 'Dermatología - Lámpara especial', TRUE),
(201, 2, 'Neurología - Resonancia', TRUE),
(202, 2, 'Pediatría - Juguetes educativos', TRUE),
(203, 2, 'Oftalmología - Equipamiento visual', TRUE),
(301, 3, 'Psiquiatría - Salas privadas', TRUE),
(302, 3, 'Telemedicina - Cámara y micrófono', TRUE);

-- ============================================================
-- 5. INSERTAR AGENDAS
-- ============================================================
INSERT INTO Agenda (matricula, id_consultorio, dia_semana, hora_inicio, hora_fin, activa) VALUES
-- Juan Pérez (Cardiología) - Consultorio 101
(12345, 1, 'Lunes', '09:00:00', '17:00:00', TRUE),
(12345, 1, 'Miércoles', '09:00:00', '17:00:00', TRUE),
(12345, 1, 'Viernes', '09:00:00', '17:00:00', TRUE),
-- María García (Neurología) - Consultorio 201
(12346, 4, 'Martes', '10:00:00', '18:00:00', TRUE),
(12346, 4, 'Jueves', '10:00:00', '18:00:00', TRUE),
-- Carlos López (Dermatología) - Consultorio 103
(12347, 3, 'Lunes', '14:00:00', '20:00:00', TRUE),
(12347, 3, 'Miércoles', '14:00:00', '20:00:00', TRUE),
-- Ana Martínez (Pediatría) - Consultorio 202
(12348, 5, 'Martes', '09:00:00', '16:00:00', TRUE),
(12348, 5, 'Jueves', '09:00:00', '16:00:00', TRUE),
(12348, 5, 'Viernes', '09:00:00', '16:00:00', TRUE),
-- Roberto González (Oftalmología) - Consultorio 203
(12349, 6, 'Lunes', '08:00:00', '16:00:00', TRUE),
(12349, 6, 'Miércoles', '08:00:00', '16:00:00', TRUE),
-- Sofía Rodríguez (Psiquiatría) - Consultorio 301
(12350, 7, 'Martes', '11:00:00', '19:00:00', TRUE),
(12350, 7, 'Jueves', '11:00:00', '19:00:00', TRUE);

-- ============================================================
-- 6. INSERTAR PACIENTES
-- ============================================================
INSERT INTO Paciente (nombre, apellido, telefono, fecha_nacimiento, direccion, medico_asignado, activo) VALUES
('María', 'González', '987654321', '1990-05-15', 'Calle Falsa 123', 12345, TRUE),
('Pedro', 'Sánchez', '911223344', '1985-07-22', 'Avenida Principal 456', 12345, TRUE),
('Laura', 'Fernández', '912334455', '1995-03-08', 'Calle Interior 789', 12346, TRUE),
('Luis', 'Martín', '913445566', '1988-11-30', 'Paseo Central 321', 12347, TRUE),
('Elena', 'Romero', '914556677', '2010-01-12', 'Avenida Secundaria 654', 12348, TRUE),
('Diego', 'Torres', '915667788', '1992-06-18', 'Calle Externa 987', 12349, TRUE),
('Gabriela', 'Jiménez', '916778899', '2008-09-25', 'Calle Interna 147', 12348, TRUE),
('Alejandro', 'Vargas', '917889900', '1980-12-05', 'Avenida Lateral 258', 12350, TRUE),
('Sandra', 'Moreno', '918990011', '1993-04-14', 'Calle Norte 369', 12345, TRUE),
('Francisco', 'Castillo', '919001122', '1986-08-20', 'Calle Sur 741', 12346, TRUE);

-- ============================================================
-- 7. INSERTAR LABORATORIOS
-- ============================================================
INSERT INTO Laboratorio (nombre, razon_social, direccion, telefono, email, activo) VALUES
('Laboratorio Bayer', 'Bayer S.A.', 'Av. Corrientes 1000', '1123456789', 'info@bayer.com', TRUE),
('Laboratorio Gador', 'Gador S.A.', 'Av. 9 de Julio 2000', '1187654321', 'info@gador.com', TRUE),
('Laboratorio Synthex', 'Synthex Argentina', 'Calle Belgrano 500', '1145678912', 'info@synthex.com', TRUE),
('Laboratorio Raffo', 'Raffo Laboratorios', 'Avenida Rivadavia 3000', '1156789023', 'info@raffo.com', TRUE);

-- ============================================================
-- 8. INSERTAR MEDICAMENTOS
-- ============================================================
INSERT INTO Medicamento (id_laboratorio, nombre, dosis, presentacion, observaciones, activo) VALUES
-- Laboratorio Bayer
(1, 'Digoxina', '0.25 mg', 'Comprimido', 'Para problemas cardíacos', TRUE),
(1, 'Metoprolol', '50 mg', 'Comprimido', 'Betabloqueante para hipertensión', TRUE),
(1, 'Aspirina', '500 mg', 'Comprimido', 'Analgésico y anticoagulante', TRUE),
-- Laboratorio Gador
(2, 'Ibuprofeno', '400 mg', 'Comprimido', 'Antiinflamatorio', TRUE),
(2, 'Paracetamol', '500 mg', 'Comprimido', 'Analgésico', TRUE),
(2, 'Amoxicilina', '500 mg', 'Cápsula', 'Antibiótico penicilínico', TRUE),
-- Laboratorio Synthex
(3, 'Loratadina', '10 mg', 'Comprimido', 'Antihistamínico', TRUE),
(3, 'Omeprazol', '20 mg', 'Cápsula', 'Inhibidor de bomba de protones', TRUE),
-- Laboratorio Raffo
(4, 'Sertraline', '50 mg', 'Comprimido', 'Antidepresivo ISRS', TRUE),
(4, 'Alprazolam', '0.5 mg', 'Comprimido', 'Ansiolítico', TRUE);

-- ============================================================
-- 9. INSERTAR TURNOS (Próximos días)
-- ============================================================
INSERT INTO Turno (id_paciente, matricula, id_consultorio, id_agenda, fecha, hora_inicio, hora_fin, estado, observaciones) VALUES
-- Turnos del 25 de Noviembre de 2025
(1, 12345, 1, 1, '2025-11-25', '07:00:00', '07:30:00', 'Programado', 'Chequeo de presión arterial'),
(2, 12345, 1, 1, '2025-11-25', '07:00:00', '07:30:00', 'Programado', 'Seguimiento después de procedimiento'),
(3, 12346, 4, 5, '2025-11-25', '07:00:00', '07:30:00', 'Programado', 'Primera consulta neurológica'),
(4, 12347, 3, 7, '2025-11-25', '07:00:00', '07:30:00', 'Programado', 'Revisión de lunar sospechoso'),

-- Turnos del 26 de Noviembre de 2025
(5, 12348, 5, 9, '2025-11-26', '07:00:00', '07:30:00', 'Programado', 'Control de vacunas'),
(6, 12349, 6, 11, '2025-11-26', '07:00:00', '07:30:00', 'Programado', 'Revisión oftalmológica anual'),
(7, 12348, 5, 9, '2025-11-26', '07:00:00', '07:30:00', 'Programado', 'Tratamiento de otitis'),

-- Turnos del 27 de Noviembre de 2025
(8, 12350, 7, 13, '2025-11-27', '07:00:00', '07:30:00', 'Programado', 'Evaluación psicológica'),
(9, 12345, 1, 3, '2025-11-27', '07:00:00', '07:30:00', 'Programado', 'Consulta por palpitaciones'),
(10, 12346, 4, 5, '2025-11-27', '07:00:00', '07:30:00', 'Programado', 'Seguimiento de migrañas');


-- ============================================================
-- 10. REGISTRAR CAMBIOS DE ESTADO DE TURNOS
-- ============================================================
INSERT INTO Cambio_estado (id_turno, estado_anterior, estado_nuevo) VALUES
(1, 'Libre', 'Programado'),
(2, 'Libre', 'Programado'),
(3, 'Libre', 'Programado'),
(4, 'Libre', 'Programado'),
(5, 'Libre', 'Programado'),
(6, 'Libre', 'Programado'),
(7, 'Libre', 'Programado'),
(8, 'Libre', 'Programado'),
(9, 'Libre', 'Programado'),
(10, 'Libre', 'Programado');

-- ============================================================
-- 11. INSERTAR HISTORIALES CLÍNICOS
-- ============================================================
INSERT INTO Historial_clinico (id_turno, id_paciente, diagnostico, tratamiento, notas, observaciones) VALUES
(1, 1, 'Hipertensión arterial leve', 'Medicación y cambios en estilo de vida', 'Paciente presenta historia familiar de HTA', 'Seguimiento mensual recomendado'),
(2, 2, 'Arritmia cardíaca', 'Medicación con betabloqueantes', 'Paciente respondió bien al tratamiento anterior', 'Realizar ECG de seguimiento'),
(3, 3, 'Migraña crónica', 'Propranolol y técnicas de relajación', 'Desencadenantes: estrés y cambios climáticos', 'Derivar a especialista en dolor'),
(4, 4, 'Dermatitis atópica', 'Cremas hidratantes y corticoides tópicos', 'Mejoría visible en últimas semanas', 'Continuar con protección solar');

-- ============================================================
-- 12. INSERTAR RECETAS
-- ============================================================
INSERT INTO Receta (id_historial, fecha_emision, fecha_vencimiento, observaciones, activa) VALUES
(1, '2025-11-25', '2026-05-25', 'Tomar con comida', TRUE),
(2, '2025-11-25', '2026-05-25', 'No interrumpir el tratamiento', TRUE),
(3, '2025-11-25', '2026-11-25', 'Tomar en las mañanas', TRUE),
(4, '2025-11-25', '2026-11-25', 'Aplicar antes de acostarse', TRUE);

-- ============================================================
-- 13. INSERTAR DETALLES DE RECETAS
-- ============================================================
INSERT INTO Detalle_receta (id_receta, id_medicamento, dosis, indicaciones, cantidad) VALUES
-- Receta 1 - Hipertensión
(1, 2, '50 mg', '1 comprimido cada 12 horas', 60),
(1, 3, '500 mg', '1 comprimido cada 24 horas', 30),
-- Receta 2 - Arritmia
(2, 1, '0.25 mg', '1 comprimido cada 24 horas', 30),
(2, 2, '50 mg', '1 comprimido cada 12 horas', 60),
-- Receta 3 - Migraña
(3, 4, '400 mg', '1 comprimido cada 8 horas si es necesario', 20),
-- Receta 4 - Dermatitis
(4, 5, '500 mg', 'Según indicaciones médicas', 30);

-- ============================================================
-- 14. INSERTAR NOTIFICACIONES
-- ============================================================
INSERT INTO Notificacion (id_turno, fecha_hora_envio, estado, medio_envio, intentos) VALUES
(1, '2025-11-24 18:00:00', 'Enviado', 'SMS', 1),
(2, '2025-11-24 18:00:00', 'Enviado', 'SMS', 1),
(3, '2025-11-24 18:00:00', 'Enviado', 'Email', 1),
(4, '2025-11-24 18:00:00', 'Enviado', 'SMS', 1),
(5, '2025-11-25 18:00:00', 'Enviado', 'SMS', 1),
(6, '2025-11-25 18:00:00', 'Enviado', 'Email', 1),
(7, '2025-11-25 18:00:00', 'Enviado', 'SMS', 1),
(8, '2025-11-26 18:00:00', 'Pendiente', 'SMS', 0),
(9, '2025-11-26 18:00:00', 'Pendiente', 'Email', 0),
(10, '2025-11-26 18:00:00', 'Pendiente', 'SMS', 0);

-- ============================================================
-- FIN DEL SCRIPT DE INSERCIÓN
-- ============================================================