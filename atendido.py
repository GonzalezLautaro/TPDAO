from estado_turno import EstadoTurno


class Atendido(EstadoTurno):
    """Estado: Turno completado"""
    
    def __init__(self):
        super().__init__("Atendido", "Turno completado exitosamente")
    
    def puede_cancelar(self) -> bool:
        return False  # No se puede cancelar un turno ya atendido
    
    def puede_atender(self) -> bool:
        return False  # Ya fue atendido
    
    def puede_marcar_ausencia(self) -> bool:
        return False  # Ya fue atendido