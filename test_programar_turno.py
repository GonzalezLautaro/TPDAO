"""
Script para programar un turno de prueba y verificar la notificación
"""

from frontend.controllers.turno_controller import TurnoController
from datetime import date, time

print("=" * 80)
print("PRUEBA DE PROGRAMACIÓN DE TURNO CON NOTIFICACIÓN")
print("=" * 80)

controller = TurnoController()

# Buscar un turno libre
print("\n1. Buscando turnos libres para médico matrícula 12345...")
turnos_libres = controller.obtener_turnos_libres_medico(12345)

if not turnos_libres:
    print("   ❌ No hay turnos libres para ese médico")
    exit()

print(f"   ✓ Encontrados {len(turnos_libres)} turnos libres")
print(f"\n2. Seleccionando primer turno disponible:")
turno = turnos_libres[0]
print(f"   ID: {turno['id_turno']}")
print(f"   Fecha: {turno['fecha']}")
print(f"   Hora: {turno['hora_inicio']}")

# Programar el turno para María González (id_paciente = 1)
print(f"\n3. Programando turno para María González (ID: 1)...")
print("=" * 80)

exito, mensaje = controller.programar_turno(
    id_paciente=1,
    matricula=12345,
    id_turno=turno['id_turno'],
    observaciones="Turno de prueba - Sistema de notificaciones"
)

print("\n" + "=" * 80)
if exito:
    print("✅ RESULTADO: Turno programado exitosamente")
    print("   La notificación debería haber aparecido arriba ↑")
else:
    print(f"❌ ERROR: {mensaje}")

print("=" * 80)
