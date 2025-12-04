from data.database import Database

db = Database()
db.conectar()
print("=== Paciente ===")
cols = db.obtener_registros('DESCRIBE Paciente')
for c in cols:
    print(c['Field'], c['Type'])
db.desconectar()

db = Database()
db.conectar()
print("\n=== Agenda ===")
cols = db.obtener_registros('DESCRIBE Agenda')
for c in cols:
    print(c['Field'], c['Type'])
db.desconectar()