from notificaciones.states.estado_notificacion import EstadoNotificacion


class Pendiente(EstadoNotificacion):
    """Estado: Notificación pendiente"""
    
    def __init__(self):
        super().__init__("Pendiente", "Notificación pendiente de envío")
    
    def puede_enviar(self) -> bool:
        return True
    
    def puede_reintentar(self) -> bool:
        return False