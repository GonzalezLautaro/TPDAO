from gestores.gestor_turno import GestorTurno
from gestores.gestor_notificacion import GestorNotificacion
from datetime import date, time, timedelta

# Crear turno de prueba
gestor_turno = GestorTurno()
fecha_turno = date.today() + timedelta(days=2)  # Cambia el día
hora_inicio = time(11, 0)                       # Cambia la hora
hora_fin = time(11, 30)

resultado = gestor_turno.alta_turno(
    id_paciente=1,
    matricula=12345,
    id_consultorio=1,
    fecha=fecha_turno,
    hora_inicio=hora_inicio,
    hora_fin=hora_fin,
    observaciones='Turno SMS prueba'
)

if resultado:
    print("✓ Turno creado correctamente")
    # Obtener el último turno creado
    from data.database import Database
    db = Database()
    db.conectar()
    turno = db.obtener_registro('SELECT id_turno FROM Turno ORDER BY id_turno DESC LIMIT 1')
    db.desconectar()
    id_turno = turno['id_turno']
    # Enviar SMS
    gestor_notif = GestorNotificacion()
    gestor_notif.crear_notificaciones_turno(id_turno, telefono_destino='+543517424323')
else:
    print("❌ Error al crear el turno")