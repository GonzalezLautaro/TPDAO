from data.database import Database

db = Database()
db.conectar()

print('Limpiando tablas...')
db.ejecutar_consulta('DELETE FROM Notificacion')
db.ejecutar_consulta('DELETE FROM Turno WHERE id_turno > 0')
db.ejecutar_consulta('ALTER TABLE Turno AUTO_INCREMENT = 1')
db.ejecutar_consulta('ALTER TABLE Notificacion AUTO_INCREMENT = 1')

print('✓ Tablas limpiadas')
db.desconectar()
