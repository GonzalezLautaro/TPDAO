from data.database import Database

db = Database()
db.conectar()

print('=== ESTRUCTURA DE LA TABLA TURNO ===\n')
columnas = db.obtener_registros('DESCRIBE Turno')

for col in columnas:
    null_str = 'NULL' if col['Null'] == 'YES' else 'NOT NULL'
    default_str = f"DEFAULT {col['Default']}" if col['Default'] else ''
    print(f'  {col["Field"]:20} {col["Type"]:20} {null_str:10} {default_str}')

db.desconectar()
