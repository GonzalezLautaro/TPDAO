from datetime import date, time, timedelta, datetime
from gestores.gestor_turno import GestorTurno
from data.database import Database

print('='*70)
print('   PRUEBA COMPLETA: SISTEMA DE NOTIFICACIONES AUTOMÁTICO')
print('='*70)

# PASO 1: Crear turno con horario único
print('\n[PASO 1] Creando turno de prueba...')
gestor = GestorTurno()

# Turno para dentro de 3 días con hora única (minuto actual)
fecha_turno = date.today() + timedelta(days=3)
minuto_actual = datetime.now().minute
hora_inicio = time(14, minuto_actual)
hora_fin = time(14, minuto_actual + 30 if minuto_actual < 30 else 59)

print(f'   Fecha turno: {fecha_turno}')
print(f'   Hora: {hora_inicio} - {hora_fin}')

resultado = gestor.alta_turno(
    id_paciente=1,
    matricula=12345,
    id_consultorio=1,
    fecha=fecha_turno,
    hora_inicio=hora_inicio,
    hora_fin=hora_fin,
    observaciones=f'Prueba automática {datetime.now()}'
)

if not resultado:
    print('\n❌ Error al crear turno')
    exit()

print('\n✅ Turno creado exitosamente')

# PASO 2: Verificar notificaciones creadas
print('\n[PASO 2] Verificando notificaciones creadas...')
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
        print(f'      - Destinatario: {n["destinatario"]}')
        print(f'      - Envío programado: {n["fecha_hora_envio"]}')
        print(f'      - Estado: {n["estado"]}')
else:
    print(f'\n❌ No se crearon notificaciones')
    db.desconectar()
    exit()

# PASO 3: Forzar envío de la primera notificación (confirmación)
print('\n[PASO 3] Forzando envío de confirmación inmediata...')
db.ejecutar_consulta(
    'UPDATE Notificacion SET fecha_hora_envio = NOW() WHERE id_notificacion = %s',
    (notifs[0]['id_notificacion'],)
)
db.desconectar()

# Ejecutar scheduler
from gestores.scheduler_notificaciones import SchedulerNotificaciones
scheduler = SchedulerNotificaciones()
scheduler.ejecutar_ahora()

# Verificar resultado
db.conectar()
notif_enviada = db.obtener_registro(
    'SELECT * FROM Notificacion WHERE id_notificacion = %s',
    (notifs[0]['id_notificacion'],)
)
db.desconectar()

print('\n' + '='*70)
if notif_enviada['estado'] == 'Enviado':
    print('   ✅ ¡PRUEBA EXITOSA - SISTEMA FUNCIONANDO 100%!')
    print('='*70)
    print(f'\n📧 Email enviado a: {notif_enviada["destinatario"]}')
    print(f'   Fecha envío: {notif_enviada["fecha_envio_real"]}')
    
    if len(notifs) > 1:
        print(f'\n📅 Recordatorio programado:')
        print(f'   - ID: {notifs[1]["id_notificacion"]}')
        print(f'   - Envío: {notifs[1]["fecha_hora_envio"]}')
        print(f'   - Se enviará automáticamente 24hs antes del turno')
    
    print(f'\n🎉 Sistema completamente automático y funcional')
else:
    print('   ❌ ERROR EN EL ENVÍO')
    print('='*70)
    print(f'   Estado: {notif_enviada["estado"]}')
    if notif_enviada.get('motivo_error'):
        print(f'   Error: {notif_enviada["motivo_error"]}')

print('\n' + '='*70)
