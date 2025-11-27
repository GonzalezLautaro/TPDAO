from datetime import date
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from turnos.states.estado_turno import EstadoTurno


class CambioEstado:
    """Clase que registra cambios de estado en turno"""
    
    def __init__(self, fecha_inicio: date, fecha_fin: date, 
                 estado_turno: 'EstadoTurno'):
        self.__fecha_inicio = fecha_inicio
        self.__fecha_fin = fecha_fin
        self.__estado_turno = estado_turno
    
    def get_fecha_inicio(self) -> date:
        return self.__fecha_inicio
    
    def get_fecha_fin(self) -> date:
        return self.__fecha_fin
    
    def get_estado_turno(self) -> 'EstadoTurno':
        return self.__estado_turno
    
    def __str__(self) -> str:
        return (f"Cambio: {self.__estado_turno.get_nombre()} "
                f"({self.__fecha_inicio} - {self.__fecha_fin})")