from datetime import date, time, timedelta
from gestores.gestor_turno import GestorTurno
from data.database import Database

print('='*70)
print('   PRUEBA COMPLETA: SISTEMA DE NOTIFICACIONES AUTOMÁTICO')
print('='*70)

# PASO 1: Crear turno
print('\n[PASO 1] Creando turno de prueba...')
gestor = GestorTurno()

# Turno para dentro de 3 días (así se crean AMBAS notificaciones)
fecha_turno = date.today() + timedelta(days=3)
hora_inicio = time(10, 0)
hora_fin = time(10, 30)

print(f'   Fecha turno: {fecha_turno}')
print(f'   Hora: {hora_inicio} - {hora_fin}')

resultado = gestor.alta_turno(
    id_paciente=1,
    matricula=12345,
    id_consultorio=1,
    fecha=fecha_turno,
    hora_inicio=hora_inicio,
    hora_fin=hora_fin,
    observaciones='Prueba sistema automático completo'
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

if len(notifs) == 2:
    print(f'\n✅ Se crearon {len(notifs)} notificaciones correctamente:')
    print(f'\n   1. CONFIRMACIÓN INMEDIATA:')
    print(f'      - ID: {notifs[0]["id_notificacion"]}')
    print(f'      - Envío: {notifs[0]["fecha_hora_envio"]}')
    print(f'      - Estado: {notifs[0]["estado"]}')
    print(f'\n   2. RECORDATORIO (24hs antes):')
    print(f'      - ID: {notifs[1]["id_notificacion"]}')
    print(f'      - Envío: {notifs[1]["fecha_hora_envio"]}')
    print(f'      - Estado: {notifs[1]["estado"]}')
else:
    print(f'\n⚠️ Se crearon {len(notifs)} notificaciones (se esperaban 2)')

# PASO 3: Forzar envío de la confirmación inmediata
print('\n[PASO 3] Enviando confirmación inmediata...')
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
    print('   ✅ PRUEBA EXITOSA - SISTEMA FUNCIONANDO AL 100%')
    print('='*70)
    print(f'\n📧 Confirmación enviada a: {notif_enviada["destinatario"]}')
    print(f'   Fecha envío: {notif_enviada["fecha_envio_real"]}')
    print(f'\n📅 Recordatorio programado para: {notifs[1]["fecha_hora_envio"]}')
    print(f'   (Se enviará automáticamente 24hs antes del turno)')
else:
    print('   ❌ ERROR EN EL ENVÍO')
    print('='*70)
    print(f'   Estado: {notif_enviada["estado"]}')

print('\n' + '='*70)
