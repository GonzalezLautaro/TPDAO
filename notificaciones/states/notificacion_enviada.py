from notificaciones.states.estado_notificacion import EstadoNotificacion


class Enviado(EstadoNotificacion):
    """Estado: Notificación enviada"""
    
    def __init__(self):
        super().__init__("Enviado", "Notificación enviada exitosamente")
    
    def puede_enviar(self) -> bool:
        return False
    
    def puede_reintentar(self) -> bool:
        return False