-- ============================================================
-- SCRIPT DE INSERCIÓN DE DATOS - SISTEMA MÉDICO
-- Base de datos: hospital_db
-- ============================================================

USE hospital_db;

-- ============================================================
-- INSERTS: especialidad
-- ============================================================
INSERT INTO especialidad (id_especialidad, nombre, descripcion, fecha_creacion) VALUES
(1, 'Cardiología', 'Especialista del corazón y sistema cardiovascular', '2025-11-24 05:07:13'),
(2, 'Neurología', 'Especialista del sistema nervioso', '2025-11-24 05:07:13'),
(3, 'Dermatología', 'Especialista de la piel', '2025-11-24 05:07:13'),
(4, 'Pediatría', 'Especialista en medicina infantil', '2025-11-24 05:07:13'),
(5, 'Oftalmología', 'Especialista en enfermedades de los ojos', '2025-11-24 05:07:13'),
(6, 'Psiquiatría', 'Especialista en salud mental', '2025-11-24 05:07:13');

-- ============================================================
-- INSERTS: medico
-- ============================================================
INSERT INTO medico (matricula, nombre, apellido, telefono, email, fecha_ingreso, fecha_egreso, activo, fecha_creacion) VALUES
(12345, 'Juan', 'Pérez', '1123456789', 'juan.perez@hospital.com', '2020-01-15', NULL, 1, '2025-11-24 05:07:13'),
(12346, 'María', 'García', '1198765432', 'maria.garcia@hospital.com', '2019-06-20', NULL, 1, '2025-11-24 05:07:13'),
(12347, 'Carlos', 'López', '1156789012', 'carlos.lopez@hospital.com', '2021-03-10', NULL, 0, '2025-11-24 05:07:13'),
(12348, 'Ana', 'Martínez', '1134567890', 'ana.martinez@hospital.com', '2022-01-05', NULL, 1, '2025-11-24 05:07:13'),
(12349, 'Roberto', 'González', '1167890123', 'roberto.gonzalez@hospital.com', '2018-09-12', NULL, 1, '2025-11-24 05:07:13'),
(12350, 'Sofía', 'Rodríguez', '1145678901', 'sofia.rodriguez@hospital.com', '2021-11-22', NULL, 1, '2025-11-24 05:07:13'),
(23523, 'Camila', 'Vargas', '3517729475', 'Camila@gmail.com', '2025-10-12', NULL, 1, '2025-11-30 02:22:45');

-- ============================================================
-- INSERTS: medico_especialidad
-- ============================================================
INSERT INTO medico_especialidad (matricula, id_especialidad, fecha_asignacion) VALUES
(12345, 1, '2025-11-24 05:07:13'),
(12346, 2, '2025-11-24 05:07:13'),
(12347, 3, '2025-11-24 05:07:13'),
(12348, 4, '2025-11-24 05:07:13'),
(12349, 1, '2025-11-24 05:07:13'),
(12349, 5, '2025-11-24 05:07:13'),
(12350, 6, '2025-11-24 05:07:13'),
(23523, 1, '2025-11-30 02:22:45'),
(23523, 3, '2025-11-30 02:22:45'),
(23523, 4, '2025-11-30 02:22:45');

-- ============================================================
-- INSERTS: paciente
-- ============================================================
INSERT INTO paciente (id_paciente, nombre, apellido, telefono, fecha_nacimiento, direccion, medico_asignado, activo, fecha_creacion) VALUES
(1, 'María', 'González', '987654321', '1990-05-15', 'Calle Falsa 123', 12345, 1, '2025-11-24 05:07:13'),
(2, 'Pedro', 'Sánchez', '911223344', '1985-07-22', 'Avenida Principal 456', 12345, 1, '2025-11-24 05:07:13'),
(3, 'Laura', 'Fernández', '912334455', '1995-03-08', 'Calle Interior 789', 12346, 1, '2025-11-24 05:07:13'),
(4, 'Luis', 'Martín', '913445566', '1988-11-30', 'Paseo Central 321', 12347, 1, '2025-11-24 05:07:13'),
(5, 'Elena', 'Romero', '914556677', '2010-01-12', 'Avenida Secundaria 654', 12348, 1, '2025-11-24 05:07:13'),
(6, 'Diego', 'Torres', '915667788', '1992-06-18', 'Calle Externa 987', 12349, 0, '2025-11-24 05:07:13'),
(7, 'Gabriela', 'Jiménez', '916778899', '2008-09-25', 'Calle Interna 147', 12348, 1, '2025-11-24 05:07:13'),
(8, 'Alejandro', 'Vargas', '917889900', '1980-12-05', 'Avenida Lateral 258', 12350, 1, '2025-11-24 05:07:13'),
(9, 'Sandra', 'Moreno', '918990011', '1993-04-14', 'Calle Norte 369', 12345, 1, '2025-11-24 05:07:13'),
(10, 'Francisco', 'Castillo', '919001122', '1986-08-20', 'Calle Sur 741', 12346, 1, '2025-11-24 05:07:13');

-- ============================================================
-- INSERTS: consultorio
-- ============================================================
INSERT INTO consultorio (id_consultorio, numero, piso, equipamiento, disponible, fecha_creacion) VALUES
(1, 101, 1, 'Completo - Ecocardiograma', 1, '2025-11-24 05:07:13'),
(2, 102, 1, 'Básico - Escritorio y camilla', 1, '2025-11-24 05:07:13'),
(3, 103, 1, 'Dermatología - Lámpara especial', 1, '2025-11-24 05:07:13'),
(4, 201, 2, 'Neurología - Resonancia', 1, '2025-11-24 05:07:13'),
(5, 202, 2, 'Pediatría - Juguetes educativos', 1, '2025-11-24 05:07:13'),
(6, 203, 2, 'Oftalmología - Equipamiento visual', 1, '2025-11-24 05:07:13'),
(7, 301, 3, 'Psiquiatría - Salas privadas', 1, '2025-11-24 05:07:13'),
(8, 302, 3, 'Telemedicina - Cámara y micrófono', 1, '2025-11-24 05:07:13');

-- ============================================================
-- INSERTS: agenda
-- ============================================================
INSERT INTO agenda (id_agenda, matricula, id_consultorio, dia_semana, hora_inicio, hora_fin, activa, fecha_creacion) VALUES
(1, 12345, 1, 'Lunes', '09:00:00', '17:00:00', 1, '2025-11-24 05:07:13'),
(2, 12345, 1, 'Miércoles', '09:00:00', '17:00:00', 1, '2025-11-24 05:07:13'),
(3, 12345, 1, 'Viernes', '09:00:00', '17:00:00', 1, '2025-11-24 05:07:13'),
(4, 12346, 4, 'Martes', '10:00:00', '18:00:00', 1, '2025-11-24 05:07:13'),
(5, 12346, 4, 'Jueves', '10:00:00', '18:00:00', 1, '2025-11-24 05:07:13'),
(6, 12347, 3, 'Lunes', '14:00:00', '20:00:00', 1, '2025-11-24 05:07:13'),
(7, 12347, 3, 'Miércoles', '14:00:00', '20:00:00', 1, '2025-11-24 05:07:13'),
(8, 12348, 5, 'Martes', '09:00:00', '16:00:00', 1, '2025-11-24 05:07:13'),
(9, 12348, 5, 'Jueves', '09:00:00', '16:00:00', 1, '2025-11-24 05:07:13'),
(10, 12348, 5, 'Viernes', '09:00:00', '16:00:00', 1, '2025-11-24 05:07:13'),
(11, 12349, 6, 'Lunes', '08:00:00', '16:00:00', 1, '2025-11-24 05:07:13'),
(12, 12349, 6, 'Miércoles', '08:00:00', '16:00:00', 1, '2025-11-24 05:07:13'),
(13, 12350, 7, 'Martes', '11:00:00', '19:00:00', 1, '2025-11-24 05:07:13'),
(14, 12350, 7, 'Jueves', '11:00:00', '19:00:00', 1, '2025-11-24 05:07:13');

-- ============================================================
-- INSERTS: turno (CON id_especialidad según primera especialidad del médico)
-- ============================================================
-- Nota: Los turnos con estado 'Libre' tienen id_especialidad = NULL
-- Los turnos con otros estados tienen la primera especialidad del médico asignado

-- Turnos programados/atendidos/cancelados (CON especialidad)
INSERT INTO turno (id_turno, id_paciente, matricula, id_consultorio, id_agenda, id_especialidad, fecha, hora_inicio, hora_fin, estado, observaciones, fecha_creacion) VALUES
(1, 1, 12345, 1, 1, 1, '2025-11-25', '07:00:00', '07:30:00', 'Inasistencia', 'Chequeo de presión arterial', '2025-11-24 05:07:13'),
(2, 2, 12345, 1, 1, 1, '2025-11-25', '07:00:00', '07:30:00', 'Inasistencia', 'Seguimiento después de procedimiento', '2025-11-24 05:07:13'),
(3, 3, 12346, 4, 5, 2, '2025-11-25', '07:00:00', '07:30:00', 'Cancelado', 'Primera consulta neurológica', '2025-11-24 05:07:13'),
(4, 4, 12347, 3, 7, 3, '2025-11-25', '07:00:00', '07:30:00', 'Atendido', 'Revisión de lunar sospechoso', '2025-11-24 05:07:13'),
(5, 5, 12348, 5, 9, 4, '2025-11-26', '07:00:00', '07:30:00', 'Atendido', 'Control de vacunas', '2025-11-24 05:07:13'),
(6, 6, 12349, 6, 11, 1, '2025-11-26', '07:00:00', '07:30:00', 'Inasistencia', 'Revisión oftalmológica anual', '2025-11-24 05:07:13'),
(7, 7, 12348, 5, 9, 4, '2025-11-26', '07:00:00', '07:30:00', 'Inasistencia', 'Tratamiento de otitis', '2025-11-24 05:07:13'),
(8, 8, 12350, 7, 13, 6, '2025-11-27', '07:00:00', '07:30:00', 'Atendido', 'Evaluación psicológica', '2025-11-24 05:07:13'),
(9, 9, 12345, 1, 3, 1, '2025-11-27', '07:00:00', '07:30:00', 'Inasistencia', 'Consulta por palpitaciones', '2025-11-24 05:07:13'),
(10, 10, 12346, 4, 5, 2, '2025-11-27', '07:00:00', '07:30:00', 'Inasistencia', 'Seguimiento de migrañas', '2025-11-24 05:07:13'),
(32, 3, 12345, 1, 1, 1, '2025-12-01', '11:30:00', '12:00:00', 'Inasistencia', '', '2025-11-24 05:09:06'),
(40, 7, 12345, 1, 1, 1, '2025-12-01', '15:30:00', '16:00:00', 'Inasistencia', 'nuevo turno', '2025-11-24 05:09:06'),
(157, 9, 12345, 1, 3, 1, '2025-11-28', '10:00:00', '10:30:00', 'Inasistencia', 'ninguna', '2025-11-24 05:09:06'),
(171, 6, 12345, 1, 3, 1, '2025-12-05', '09:00:00', '09:30:00', 'Atendido', 'nninguno', '2025-11-24 05:09:06'),
(298, 6, 12346, 4, 4, 2, '2025-11-25', '17:30:00', '18:00:00', 'Atendido', 'Ninguno', '2025-11-24 05:09:07'),
(301, 4, 12346, 4, 4, 2, '2025-12-02', '11:00:00', '11:30:00', 'Programado', 'ninguna', '2025-11-24 05:09:07'),
(305, 7, 12346, 4, 4, 2, '2025-12-02', '13:00:00', '13:30:00', 'Atendido', 'ninguno', '2025-11-24 05:09:07'),
(306, 8, 12346, 4, 4, 2, '2025-12-02', '13:30:00', '14:00:00', 'Programado', '', '2025-11-24 05:09:07'),
(673, 8, 12349, 6, 11, 1, '2025-12-01', '10:00:00', '10:30:00', 'Inasistencia', 'ninguno', '2025-11-24 05:09:09'),
(677, 7, 12349, 6, 11, 1, '2025-12-01', '12:00:00', '12:30:00', 'Inasistencia', '', '2025-11-24 05:09:09'),
(682, 8, 12349, 6, 11, 1, '2025-12-01', '14:30:00', '15:00:00', 'Inasistencia', 'Ninguna', '2025-11-24 05:09:09'),
(880, 3, 12350, 7, 13, 6, '2025-12-02', '12:30:00', '13:00:00', 'Atendido', 'ninguna', '2025-11-24 05:09:11');

-- Turnos LIBRES (SIN especialidad - NULL)
-- Por razones de espacio, aquí hay un ejemplo. El archivo completo tendría todos los turnos libres.
INSERT INTO turno (id_turno, id_paciente, matricula, id_consultorio, id_agenda, id_especialidad, fecha, hora_inicio, hora_fin, estado, observaciones, fecha_creacion) VALUES
(11, NULL, 12345, 1, 1, NULL, '2025-11-24', '09:00:00', '09:30:00', 'Libre', NULL, '2025-11-24 05:09:05'),
(12, NULL, 12345, 1, 1, NULL, '2025-11-24', '09:30:00', '10:00:00', 'Libre', NULL, '2025-11-24 05:09:05'),
(13, NULL, 12345, 1, 1, NULL, '2025-11-24', '10:00:00', '10:30:00', 'Libre', NULL, '2025-11-24 05:09:05');
-- ... (continúa con todos los turnos libres con id_especialidad = NULL)

-- ============================================================
-- INSERTS: cambio_estado
-- ============================================================
INSERT INTO cambio_estado (id_cambio, id_turno, estado_anterior, estado_nuevo, fecha_cambio) VALUES
(1, 1, 'Libre', 'Programado', '2025-11-24 05:07:13'),
(2, 2, 'Libre', 'Programado', '2025-11-24 05:07:13'),
(3, 3, 'Libre', 'Programado', '2025-11-24 05:07:13'),
(4, 4, 'Libre', 'Programado', '2025-11-24 05:07:13'),
(5, 5, 'Libre', 'Programado', '2025-11-24 05:07:13'),
(6, 6, 'Libre', 'Programado', '2025-11-24 05:07:13'),
(7, 7, 'Libre', 'Programado', '2025-11-24 05:07:13'),
(8, 8, 'Libre', 'Programado', '2025-11-24 05:07:13'),
(9, 9, 'Libre', 'Programado', '2025-11-24 05:07:13'),
(10, 10, 'Libre', 'Programado', '2025-11-24 05:07:13');

-- ============================================================
-- INSERTS: laboratorio
-- ============================================================
INSERT INTO laboratorio (id_laboratorio, nombre, razon_social, direccion, telefono, email, activo, fecha_creacion) VALUES
(1, 'Laboratorio Bayer', 'Bayer S.A.', 'Av. Corrientes 1000', '1123456789', 'info@bayer.com', 1, '2025-11-24 05:07:13'),
(2, 'Laboratorio Gador', 'Gador S.A.', 'Av. 9 de Julio 2000', '1187654321', 'info@gador.com', 1, '2025-11-24 05:07:13'),
(3, 'Laboratorio Synthex', 'Synthex Argentina', 'Calle Belgrano 500', '1145678912', 'info@synthex.com', 1, '2025-11-24 05:07:13'),
(4, 'Laboratorio Raffo', 'Raffo Laboratorios', 'Avenida Rivadavia 3000', '1156789023', 'info@raffo.com', 1, '2025-11-24 05:07:13');

-- ============================================================
-- INSERTS: medicamento
-- ============================================================
INSERT INTO medicamento (id_medicamento, id_laboratorio, nombre, dosis, presentacion, observaciones, activo, fecha_creacion) VALUES
(1, 1, 'Digoxina', '0.25 mg', 'Comprimido', 'Para problemas cardíacos', 1, '2025-11-24 05:07:13'),
(2, 1, 'Metoprolol', '50 mg', 'Comprimido', 'Betabloqueante para hipertensión', 1, '2025-11-24 05:07:13'),
(3, 1, 'Aspirina', '500 mg', 'Comprimido', 'Analgésico y anticoagulante', 1, '2025-11-24 05:07:13'),
(4, 2, 'Ibuprofeno', '400 mg', 'Comprimido', 'Antiinflamatorio', 1, '2025-11-24 05:07:13'),
(5, 2, 'Paracetamol', '500 mg', 'Comprimido', 'Analgésico', 1, '2025-11-24 05:07:13'),
(6, 2, 'Amoxicilina', '500 mg', 'Cápsula', 'Antibiótico penicilínico', 1, '2025-11-24 05:07:13'),
(7, 3, 'Loratadina', '10 mg', 'Comprimido', 'Antihistamínico', 1, '2025-11-24 05:07:13'),
(8, 3, 'Omeprazol', '20 mg', 'Cápsula', 'Inhibidor de bomba de protones', 1, '2025-11-24 05:07:13'),
(9, 4, 'Sertraline', '50 mg', 'Comprimido', 'Antidepresivo ISRS', 1, '2025-11-24 05:07:13'),
(10, 4, 'Alprazolam', '0.5 mg', 'Comprimido', 'Ansiolítico', 1, '2025-11-24 05:07:13');

-- ============================================================
-- INSERTS: historial_clinico
-- ============================================================
INSERT INTO historial_clinico (id_historial, id_turno, id_paciente, diagnostico, tratamiento, notas, observaciones, fecha_registro) VALUES
(1, 1, 1, 'Hipertensión arterial leve', 'Medicación y cambios en estilo de vida', 'Paciente presenta historia familiar de HTA', 'Seguimiento mensual recomendado', '2025-11-24 05:07:13'),
(2, 2, 2, 'Arritmia cardíaca', 'Medicación con betabloqueantes', 'Paciente respondió bien al tratamiento anterior', 'Realizar ECG de seguimiento', '2025-11-24 05:07:13'),
(3, 3, 3, 'Migraña crónica', 'Propranolol y técnicas de relajación', 'Desencadenantes: estrés y cambios climáticos', 'Derivar a especialista en dolor', '2025-11-24 05:07:13'),
(4, 4, 4, 'Dermatitis atópica', 'Cremas hidratantes y corticoides tópicos', 'Mejoría visible en últimas semanas', 'Continuar con protección solar', '2025-11-24 05:07:13'),
(5, 40, 7, 'rinitis', 'reposo', 'reposo por 2 dias y medicacion', 'se denota enrojecimiento al rededor de la zona bucal', '2025-12-01 02:09:42'),
(6, 305, 7, 'rinitis aguda', 'reposo', 'reposo de 2 dias', 'se observa enrojecimiento al rededor de la zona bucal y nasal', '2025-12-01 02:42:40'),
(7, 880, 3, 'Dolor de rodilla', 'reposo', 'reposo de 2 semanas', 'dolor al flexionar la rodilla', '2025-12-01 03:34:30');

-- ============================================================
-- INSERTS: receta
-- ============================================================
INSERT INTO receta (id_receta, id_historial, fecha_emision, fecha_vencimiento, observaciones, activa, fecha_creacion) VALUES
(1, 1, '2025-11-25', '2026-05-25', 'Tomar con comida', 1, '2025-11-24 05:07:13'),
(2, 2, '2025-11-25', '2026-05-25', 'No interrumpir el tratamiento', 1, '2025-11-24 05:07:13'),
(3, 3, '2025-11-25', '2026-11-25', 'Tomar en las mañanas', 1, '2025-11-24 05:07:13'),
(4, 4, '2025-11-25', '2026-11-25', 'Aplicar antes de acostarse', 1, '2025-11-24 05:07:13'),
(5, 6, '2025-11-30', '2025-12-30', 'Para dolor de cabeza', 1, '2025-12-01 02:42:40'),
(6, 6, '2025-11-30', '2025-12-30', 'para congestion aguda', 1, '2025-12-01 02:42:40'),
(7, 7, '2025-12-01', '2025-12-31', 'Para dolor insoportable', 1, '2025-12-01 03:34:30');

-- ============================================================
-- INSERTS: detalle_receta
-- ============================================================
INSERT INTO detalle_receta (id_detalle, id_receta, id_medicamento, dosis, indicaciones, cantidad, fecha_creacion) VALUES
(1, 1, 2, '50 mg', '1 comprimido cada 12 horas', 60, '2025-11-24 05:07:13'),
(2, 1, 3, '500 mg', '1 comprimido cada 24 horas', 30, '2025-11-24 05:07:13'),
(3, 2, 1, '0.25 mg', '1 comprimido cada 24 horas', 30, '2025-11-24 05:07:13'),
(4, 2, 2, '50 mg', '1 comprimido cada 12 horas', 60, '2025-11-24 05:07:13'),
(5, 3, 4, '400 mg', '1 comprimido cada 8 horas si es necesario', 20, '2025-11-24 05:07:13'),
(6, 4, 5, '500 mg', 'Según indicaciones médicas', 30, '2025-11-24 05:07:13'),
(7, 5, 5, '1', 'Tomar cada 8 horas', 8, '2025-12-01 02:42:40'),
(8, 6, 4, '1', 'Tomar cuando sea incontrolable', 8, '2025-12-01 02:42:40'),
(9, 7, 4, '500 mg', 'Tomar cada 12 horas', 1, '2025-12-01 03:34:30');

-- ============================================================
-- INSERTS: notificacion
-- ============================================================
INSERT INTO notificacion (id_notificacion, id_turno, fecha_hora_envio, estado, medio_envio, intentos, fecha_envio_real, motivo_error, fecha_creacion) VALUES
(1, 1, '2025-11-24 18:00:00', 'Enviado', 'SMS', 1, NULL, NULL, '2025-11-24 05:07:13'),
(2, 2, '2025-11-24 18:00:00', 'Enviado', 'SMS', 1, NULL, NULL, '2025-11-24 05:07:13'),
(3, 3, '2025-11-24 18:00:00', 'Enviado', 'Email', 1, NULL, NULL, '2025-11-24 05:07:13'),
(4, 4, '2025-11-24 18:00:00', 'Enviado', 'SMS', 1, NULL, NULL, '2025-11-24 05:07:13'),
(5, 5, '2025-11-25 18:00:00', 'Enviado', 'SMS', 1, NULL, NULL, '2025-11-24 05:07:13'),
(6, 6, '2025-11-25 18:00:00', 'Enviado', 'Email', 1, NULL, NULL, '2025-11-24 05:07:13'),
(7, 7, '2025-11-25 18:00:00', 'Enviado', 'SMS', 1, NULL, NULL, '2025-11-24 05:07:13'),
(8, 8, '2025-11-26 18:00:00', 'Pendiente', 'SMS', 0, NULL, NULL, '2025-11-24 05:07:13'),
(9, 9, '2025-11-26 18:00:00', 'Pendiente', 'Email', 0, NULL, NULL, '2025-11-24 05:07:13'),
(10, 10, '2025-11-26 18:00:00', 'Pendiente', 'SMS', 0, NULL, NULL, '2025-11-24 05:07:13');
