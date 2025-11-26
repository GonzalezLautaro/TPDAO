from estado_turno import EstadoTurno


class Programado(EstadoTurno):
    """Estado: Turno reservado"""
    
    def __init__(self):
        super().__init__("Programado", "Turno reservado por un paciente")
    
    def puede_cancelar(self) -> bool:
        return True  # Sí se puede cancelar un turno programado
    
    def puede_atender(self) -> bool:
        return True  # Sí se puede atender un turno programado
    
    def puede_marcar_ausencia(self) -> bool:
        return True  # Sí se puede marcar ausencia