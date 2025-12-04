from data.database import Database
from datetime import date, time, timedelta

print('=== DIAGNÓSTICO: Verificar creación de turno ===\n')

# 1. Limpiar
db = Database()
db.conectar()
db.ejecutar_consulta('DELETE FROM Notificacion')
db.ejecutar_consulta('DELETE FROM Turno')
print('✓ Tablas limpiadas\n')

# 2. Crear turno manualmente
print('[PASO 1] Creando turno directamente en BD...')
fecha_turno = date.today() + timedelta(days=5)
hora_inicio = time(15, 30)
hora_fin = time(16, 0)

query = '''
INSERT INTO Turno (id_paciente, matricula, id_consultorio, fecha, hora_inicio, hora_fin, observaciones, estado)
VALUES (%s, %s, %s, %s, %s, %s, %s, 'Confirmado')
'''
db.ejecutar_consulta(query, (1, 12345, 1, fecha_turno, hora_inicio, hora_fin, 'Prueba'))
print('✓ Turno insertado\n')

# 3. Verificar que existe
print('[PASO 2] Verificando que el turno existe...')
turno = db.obtener_registro('SELECT * FROM Turno WHERE id_turno = 1')
if turno:
    print(f'✓ Turno encontrado: ID {turno["id_turno"]}')
    print(f'  Paciente: {turno["id_paciente"]}')
    print(f'  Fecha: {turno["fecha"]}')
    print(f'  Hora inicio: {turno["hora_inicio"]} (tipo: {type(turno["hora_inicio"])})')
else:
    print('❌ No se encontró el turno')
    db.desconectar()
    exit()

# 4. Probar la consulta del gestor
print('\n[PASO 3] Probando consulta del gestor_notificacion...')
query_turno = '''
SELECT t.*, 
       CONCAT(p.nombre, ' ', p.apellido) as nombre_paciente,
       CONCAT(m.nombre, ' ', m.apellido) as nombre_medico,
       m.email as email_medico
FROM Turno t
JOIN Paciente p ON t.id_paciente = p.id_paciente
JOIN Medico m ON t.matricula = m.matricula
WHERE t.id_turno = %s
'''

turno_completo = db.obtener_registro(query_turno, (1,))
if turno_completo:
    print('✓ Consulta del gestor FUNCIONA')
    print(f'  Paciente: {turno_completo["nombre_paciente"]}')
    print(f'  Médico: {turno_completo["nombre_medico"]}')
else:
    print('❌ Consulta del gestor FALLA')
    print('   Verificando si existen los registros necesarios...')
    
    # Verificar paciente
    paciente = db.obtener_registro('SELECT * FROM Paciente WHERE id_paciente = 1')
    if not paciente:
        print('   ❌ NO existe paciente con id_paciente = 1')
    else:
        print(f'   ✓ Paciente existe: {paciente["nombre"]} {paciente["apellido"]}')
    
    # Verificar médico
    medico = db.obtener_registro('SELECT * FROM Medico WHERE matricula = 12345')
    if not medico:
        print('   ❌ NO existe médico con matricula = 12345')
    else:
        print(f'   ✓ Médico existe: {medico["nombre"]} {medico["apellido"]}')

db.desconectar()
print('\n' + '='*60)
