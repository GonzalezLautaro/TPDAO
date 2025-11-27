from turnos.states.estado_turno import EstadoTurno


class Libre(EstadoTurno):
    """Estado: Turno disponible"""
    
    def __init__(self):
        super().__init__("Libre", "Turno disponible para reservar")
    
    def puede_cancelar(self) -> bool:
        return False
    
    def puede_atender(self) -> bool:
        return False
    
    def puede_marcar_ausencia(self) -> bool:
        return False