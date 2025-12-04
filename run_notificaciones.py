# filepath: run_notificaciones.py
'''
Sistema de Notificaciones Automáticas
Ejecuta el scheduler que envía emails automáticamente
'''
from gestores.scheduler_notificaciones import SchedulerNotificaciones
import time

if __name__ == '__main__':
    print('='*70)
    print('   SISTEMA DE NOTIFICACIONES AUTOMÁTICAS - HOSPITAL DAO 2025')
    print('='*70)
    print('\n✓ Iniciando scheduler...')
    print('✓ Revisa cada 5 minutos si hay notificaciones pendientes')
    print('✓ Envía emails automáticamente\n')
    
    scheduler = SchedulerNotificaciones(intervalo_minutos=5)
    scheduler.iniciar()
    
    print('✅ Scheduler activo')
    print('\n📧 Las notificaciones se enviarán automáticamente')
    print('   - Confirmación: Al crear el turno')
    print('   - Recordatorio: 24hs antes del turno')
    print('\n⚠️  Presiona Ctrl+C para detener el sistema\n')
    print('='*70)
    
    try:
        while True:
            time.sleep(60)  # Esperar indefinidamente
    except KeyboardInterrupt:
        print('\n\n🛑 Deteniendo scheduler...')
        scheduler.detener()
        print('✓ Sistema de notificaciones detenido')
        print('\n' + '='*70)
