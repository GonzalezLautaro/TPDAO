from estado_turno import EstadoTurno


class Libre(EstadoTurno):
    """Estado: Turno disponible"""
    
    def __init__(self):
        super().__init__("Libre", "Turno disponible para reservar")
    
    def puede_cancelar(self) -> bool:
        return False  # No se puede cancelar un turno libre
    
    def puede_atender(self) -> bool:
        return False  # No se puede atender un turno no programado
    
    def puede_marcar_ausencia(self) -> bool:
        return False  # No tiene sentido marcar ausencia en turno libre