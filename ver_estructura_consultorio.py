from data.database import Database

db = Database()
db.conectar()
print("=== Consultorio ===")
cols = db.obtener_registros('DESCRIBE Consultorio')
for c in cols:
    print(c['Field'], c['Type'])
db.desconectar()