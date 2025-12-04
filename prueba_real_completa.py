print('='*70)
print('   PRUEBA REAL: CREAR TURNO Y VER SI LLEGAN LOS EMAILS')
print('='*70)

# 1. LIMPIAR TODO
print('\n[1] Limpiando base de datos...')
from data.database import Database
db = Database()
db.conectar()
db.ejecutar_consulta('DELETE FROM Notificacion')
db.ejecutar_consulta('DELETE FROM Turno')
print('✓ Tablas limpiadas')
db.desconectar()

# 2. CREAR UN TURNO NUEVO (como lo haría la aplicación real)
print('\n[2] Creando turno nuevo...')
from datetime import date, time, timedelta
from gestores.gestor_turno import GestorTurno

gestor = GestorTurno()
fecha_turno = date.today() + timedelta(days=5)  # Turno en 5 días
hora_inicio = time(15, 30)
hora_fin = time(16, 0)

print(f'   Paciente: ID 1')
print(f'   Médico: Matrícula 12345')
print(f'   Fecha: {fecha_turno}')
print(f'   Hora: {hora_inicio}')

resultado = gestor.alta_turno(
    id_paciente=1,
    matricula=12345,
    id_consultorio=1,
    fecha=fecha_turno,
    hora_inicio=hora_inicio,
    hora_fin=hora_fin,
    observaciones='Prueba sistema notificaciones'
)

if not resultado:
    print('\n❌ ERROR: No se pudo crear el turno')
    exit()

print('✓ Turno creado')

# 3. VERIFICAR QUE SE CREARON LAS NOTIFICACIONES
print('\n[3] Verificando notificaciones en BD...')
db.conectar()
notifs = db.obtener_registros('SELECT * FROM Notificacion ORDER BY fecha_hora_envio')
db.desconectar()

if len(notifs) == 0:
    print('❌ ERROR: NO se crearon notificaciones automáticamente')
    print('   El sistema NO está funcionando')
    exit()

print(f'✓ Se crearon {len(notifs)} notificaciones:')
for n in notifs:
    print(f'   - ID {n["id_notificacion"]}: {n["medio_envio"]} - Estado: {n["estado"]} - Envío: {n["fecha_hora_envio"]}')

# 4. FORZAR ENVÍO DE LA PRIMERA (confirmación inmediata)
print('\n[4] Forzando envío de confirmación inmediata...')
db.conectar()
db.ejecutar_consulta('UPDATE Notificacion SET fecha_hora_envio = NOW() WHERE id_notificacion = 1')
db.desconectar()

# 5. EJECUTAR SCHEDULER (simular envío automático)
print('\n[5] Ejecutando scheduler (simula envío cada 5 min)...')
from gestores.scheduler_notificaciones import SchedulerNotificaciones
scheduler = SchedulerNotificaciones()
scheduler.ejecutar_ahora()

# 6. VERIFICAR RESULTADO FINAL
print('\n[6] Verificando resultado...')
db.conectar()
notif_enviada = db.obtener_registro('SELECT * FROM Notificacion WHERE id_notificacion = 1')
email_paciente = db.obtener_registro('''
    SELECT cp.valor_contacto 
    FROM Turno t
    JOIN Contactos_Paciente cp ON t.id_paciente = cp.id_paciente
    WHERE t.id_turno = 1 AND cp.tipo_contacto = 'Email' AND cp.es_principal = TRUE
''')
db.desconectar()

print('\n' + '='*70)
if notif_enviada and notif_enviada['estado'] == 'Enviado':
    print('   ✅ PRUEBA EXITOSA - SISTEMA FUNCIONA')
    print('='*70)
    print(f'\n   📧 Email enviado a: {email_paciente["valor_contacto"]}')
    print(f'   📅 Fecha envío: {notif_enviada["fecha_envio_real"]}')
    print(f'\n   🎯 El sistema está funcionando correctamente')
else:
    print('   ❌ PRUEBA FALLIDA')
    print('='*70)
    if notif_enviada:
        print(f'   Estado: {notif_enviada["estado"]}')
        if notif_enviada.get('motivo_error'):
            print(f'   Error: {notif_enviada["motivo_error"]}')
    else:
        print('   No se encontró la notificación')

print('\n' + '='*70)
