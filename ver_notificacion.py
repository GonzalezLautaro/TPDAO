from data.database import Database

db = Database()
db.conectar()

print('=== ESTRUCTURA DE LA TABLA NOTIFICACION ===\n')
columnas = db.obtener_registros('DESCRIBE Notificacion')

for col in columnas:
    print(f'  {col["Field"]} - {col["Type"]}')

db.desconectar()
