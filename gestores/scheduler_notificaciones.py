import time
import threading
from datetime import datetime
from gestores.gestor_notificacion import GestorNotificacion


class SchedulerNotificaciones:
    """
    Scheduler que se ejecuta en segundo plano para enviar notificaciones pendientes
    """
    
    def __init__(self, intervalo_minutos: int = 5):
        """
        Args:
            intervalo_minutos: Cada cuántos minutos revisar notificaciones pendientes (default: 5)
        """
        self.intervalo = intervalo_minutos * 60  # Convertir a segundos
        self.gestor = GestorNotificacion()
        self.thread = None
        self.activo = False
        
    def iniciar(self):
        """Inicia el scheduler en segundo plano"""
        if self.activo:
            print('[WARNING] Scheduler ya está en ejecución')
            return
        
        self.activo = True
        self.thread = threading.Thread(target=self._ejecutar, daemon=True)
        self.thread.start()
        print(f'✓ Scheduler de notificaciones iniciado (intervalo: {self.intervalo // 60} min)')
    
    def detener(self):
        """Detiene el scheduler"""
        self.activo = False
        if self.thread:
            self.thread.join(timeout=2)
        print('✓ Scheduler de notificaciones detenido')
    
    def _ejecutar(self):
        """Bucle principal del scheduler"""
        print(f'[{datetime.now().strftime("%H:%M:%S")}] Scheduler en ejecución...')
        
        while self.activo:
            try:
                self._procesar_notificaciones_pendientes()
            except Exception as e:
                print(f'[ERROR] Scheduler: {str(e)}')
            
            # Esperar el intervalo antes de la próxima revisión
            time.sleep(self.intervalo)
    
    def _procesar_notificaciones_pendientes(self):
        """Obtiene y procesa todas las notificaciones pendientes"""
        hora_actual = datetime.now().strftime('%H:%M:%S')
        
        # Obtener notificaciones pendientes
        notificaciones = self.gestor.obtener_notificaciones_pendientes()
        
        if not notificaciones:
            print(f'[{hora_actual}] No hay notificaciones pendientes')
            return
        
        print(f'[{hora_actual}] Procesando {len(notificaciones)} notificación(es)...')
        
        enviadas = 0
        fallidas = 0
        
        for notif in notificaciones:
            if self.gestor.procesar_notificacion(notif):
                enviadas += 1
            else:
                fallidas += 1
        
        print(f'[{hora_actual}] Resultado: {enviadas} enviadas, {fallidas} fallidas')
    
    def ejecutar_ahora(self):
        """Ejecuta el procesamiento inmediatamente (útil para testing)"""
        print('\n=== EJECUCIÓN MANUAL DEL SCHEDULER ===')
        self._procesar_notificaciones_pendientes()
        print('=== FIN EJECUCIÓN MANUAL ===\n')


# Para testing directo
if __name__ == '__main__':
    print('=== TEST DE SCHEDULER ===\n')
    
    scheduler = SchedulerNotificaciones(intervalo_minutos=1)
    scheduler.iniciar()
    
    try:
        # Mantener el programa corriendo
        print('Presiona Ctrl+C para detener...\n')
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print('\n\nDeteniendo scheduler...')
        scheduler.detener()
        print('\nScheduler detenido correctamente')