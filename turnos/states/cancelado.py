from turnos.states.estado_turno import EstadoTurno


class Cancelado(EstadoTurno):
    """Estado: Turno cancelado"""
    
    def __init__(self):
        super().__init__("Cancelado", "Turno cancelado por el paciente")
    
    def puede_cancelar(self) -> bool:
        return False
    
    def puede_atender(self) -> bool:
        return False
    
    def puede_marcar_ausencia(self) -> bool:
        return False