from data.database import Database

db = Database()
db.conectar()

# Paciente
db.ejecutar_consulta(
    "INSERT IGNORE INTO Paciente (id_paciente, nombre, apellido, fecha_nacimiento, activo) VALUES (1, 'Juan', 'Pérez', '1990-01-01', 1)"
)

# Médico
db.ejecutar_consulta(
    "INSERT IGNORE INTO Medico (matricula, nombre, apellido, email, activo) VALUES (12345, 'Ana', 'García', 'medico@hospital.com', 1)"
)

# Consultorio (usando los campos correctos)
db.ejecutar_consulta(
    "INSERT IGNORE INTO Consultorio (id_consultorio, numero, piso, equipamiento, disponible) VALUES (1, 101, 1, 'Básico', 1)"
)

# Agenda
db.ejecutar_consulta(
    "INSERT IGNORE INTO Agenda (id_agenda, matricula, id_consultorio, dia_semana, hora_inicio, hora_fin, activa) VALUES (1, 12345, 1, 'Lunes', '08:00:00', '17:00:00', 1)"
)

# Contacto principal del paciente
db.ejecutar_consulta(
    "INSERT IGNORE INTO Contactos_Paciente (id_contacto, id_paciente, tipo_contacto, valor_contacto, activo, es_principal) VALUES (1, 1, 'Email', 'turnoshospitaldao2025@gmail.com', 1, 1)"
)

db.desconectar()
print("✓ Datos mínimos creados")