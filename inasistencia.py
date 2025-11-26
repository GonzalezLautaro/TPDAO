from estado_turno import EstadoTurno


class Inasistencia(EstadoTurno):
    """Estado: Paciente no asistió"""
    
    def __init__(self):
        super().__init__("Inasistencia", "Paciente no asistió al turno")
    
    def puede_cancelar(self) -> bool:
        return False  # Ya no asistió
    
    def puede_atender(self) -> bool:
        return False  # No se puede atender sin presencia
    
    def puede_marcar_ausencia(self) -> bool:
        return False  # Ya está marcado como ausencia