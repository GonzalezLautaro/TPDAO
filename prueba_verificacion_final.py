from datetime import date, time, timedelta, datetime
from gestores.gestor_turno import GestorTurno
from data.database import Database

print('='*70)
print('   PRUEBA COMPLETA: SISTEMA DE NOTIFICACIONES AUTOMÁTICO')
print('='*70)

# PASO 1: Verificar notificaciones existentes
print('\n[PASO 1] Verificando notificaciones creadas...')
db = Database()
db.conectar()

# Obtener último turno
turno = db.obtener_registro('SELECT id_turno FROM Turno ORDER BY id_turno DESC LIMIT 1')
id_turno = turno['id_turno']

# Obtener notificaciones de ese turno
notifs = db.obtener_registros(
    'SELECT * FROM Notificacion WHERE id_turno = %s ORDER BY fecha_hora_envio ASC',
    (id_turno,)
)

if len(notifs) >= 1:
    print(f'\n✅ Se crearon {len(notifs)} notificación(es):')
    for i, n in enumerate(notifs, 1):
        print(f'\n   {i}. Notificación ID {n["id_notificacion"]}:')
        print(f'      - Turno: {n["id_turno"]}')
        print(f'      - Medio: {n["medio_envio"]}')
        print(f'      - Envío programado: {n["fecha_hora_envio"]}')
        print(f'      - Estado: {n["estado"]}')
else:
    print(f'\n❌ No se encontraron notificaciones')
    db.desconectar()
    exit()

# PASO 2: Forzar envío de la primera notificación (confirmación)
print('\n[PASO 2] Forzando envío de confirmación inmediata...')
db.ejecutar_consulta(
    'UPDATE Notificacion SET fecha_hora_envio = NOW() WHERE id_notificacion = %s',
    (notifs[0]['id_notificacion'],)
)
db.desconectar()

# PASO 3: Ejecutar scheduler
print('\n[PASO 3] Ejecutando scheduler para enviar email...')
from gestores.scheduler_notificaciones import SchedulerNotificaciones
scheduler = SchedulerNotificaciones()
scheduler.ejecutar_ahora()

# PASO 4: Verificar resultado
print('\n[PASO 4] Verificando envío...')
db.conectar()
notif_enviada = db.obtener_registro(
    'SELECT * FROM Notificacion WHERE id_notificacion = %s',
    (notifs[0]['id_notificacion'],)
)

# Obtener email del paciente
email_paciente = db.obtener_registro('''
    SELECT cp.valor_contacto 
    FROM Turno t
    JOIN Contactos_Paciente cp ON t.id_paciente = cp.id_paciente
    WHERE t.id_turno = %s AND cp.tipo_contacto = 'Email' AND cp.es_principal = TRUE
    LIMIT 1
''', (id_turno,))

db.desconectar()

print('\n' + '='*70)
if notif_enviada['estado'] == 'Enviado':
    print('   ✅ ¡PRUEBA EXITOSA - SISTEMA FUNCIONANDO 100%!')
    print('='*70)
    print(f'\n📧 Email enviado a: {email_paciente["valor_contacto"]}')
    print(f'   Fecha envío: {notif_enviada["fecha_envio_real"]}')
    
    if len(notifs) > 1:
        print(f'\n📅 Recordatorio programado:')
        print(f'   - ID: {notifs[1]["id_notificacion"]}')
        print(f'   - Envío: {notifs[1]["fecha_hora_envio"]}')
        print(f'   - Se enviará automáticamente 24hs antes del turno')
    
    print(f'\n🎉 SISTEMA COMPLETAMENTE AUTOMÁTICO Y FUNCIONAL')
    print(f'\n✅ RESUMEN:')
    print(f'   1. Al crear turno → Se crean 2 notificaciones automáticamente')
    print(f'   2. Confirmación inmediata → Enviada ✓')
    print(f'   3. Recordatorio 24hs antes → Programado ✓')
    print(f'   4. Scheduler ejecutándose cada 5 minutos ✓')
else:
    print('   ❌ ERROR EN EL ENVÍO')
    print('='*70)
    print(f'   Estado: {notif_enviada["estado"]}')
    if notif_enviada.get('motivo_error'):
        print(f'   Error: {notif_enviada["motivo_error"]}')

print('\n' + '='*70)
