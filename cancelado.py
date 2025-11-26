from estado_turno import EstadoTurno


class Cancelado(EstadoTurno):
    """Estado: Turno cancelado"""
    
    def __init__(self):
        super().__init__("Cancelado", "Turno cancelado por el paciente")
    
    def puede_cancelar(self) -> bool:
        return False  # Ya está cancelado
    
    def puede_atender(self) -> bool:
        return False  # No se puede atender un turno cancelado
    
    def puede_marcar_ausencia(self) -> bool:
        return False  # No tiene sentido