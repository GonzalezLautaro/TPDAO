from notificaciones.states.estado_notificacion import EstadoNotificacion


class Error(EstadoNotificacion):
    """Estado: Error en notificación"""
    
    def __init__(self):
        super().__init__("Error", "Hubo un error al enviar la notificación")
    
    def puede_enviar(self) -> bool:
        return False
    
    def puede_reintentar(self) -> bool:
        return True