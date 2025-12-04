from gestores.gestor_turno import GestorTurno
from datetime import date, time, timedelta

gestor = GestorTurno()

# Turno para dentro de 3 días
fecha_turno = date.today() + timedelta(days=3)
hora_inicio = time(10, 0)
hora_fin = time(10, 30)

resultado = gestor.alta_turno(
    id_paciente=1,
    matricula=12345,
    id_consultorio=1,
    fecha=fecha_turno,
    hora_inicio=hora_inicio,
    hora_fin=hora_fin,
    observaciones='Turno de prueba'
)

if resultado:
    print("✓ Turno creado correctamente")
else:
    print("❌ Error al crear el turno")