from typing import Optional, TYPE_CHECKING
from datetime import date

if TYPE_CHECKING:
    from turnos.turno import Turno
    from models.paciente import Paciente
    from recetas.receta import Receta


class HistorialClinico:
    """Clase que representa el historial clínico de un turno"""
    
    def __init__(self, nro_historial: int, turno: 'Turno', 
                 paciente: 'Paciente', diagnostico: str = "",
                 observaciones: str = "", tratamiento: str = ""):
        self.__nro_historial = nro_historial
        self.__turno = turno
        self.__paciente = paciente
        self.__diagnostico = diagnostico
        self.__observaciones = observaciones
        self.__tratamiento = tratamiento
        self.__receta: Optional['Receta'] = None
        self.__fecha_creacion = date.today()
    
    def get_nro_historial(self) -> int:
        return self.__nro_historial
    
    def get_turno(self) -> 'Turno':
        return self.__turno
    
    def get_paciente(self) -> 'Paciente':
        return self.__paciente
    
    def get_diagnostico(self) -> str:
        return self.__diagnostico
    
    def get_observaciones(self) -> str:
        return self.__observaciones
    
    def get_tratamiento(self) -> str:
        return self.__tratamiento
    
    def get_receta(self) -> Optional['Receta']:
        return self.__receta
    
    def get_fecha_creacion(self) -> date:
        return self.__fecha_creacion
    
    def set_diagnostico(self, diagnostico: str) -> None:
        if not diagnostico or not isinstance(diagnostico, str):
            raise ValueError("Diagnóstico debe ser una cadena válida")
        self.__diagnostico = diagnostico
    
    def set_observaciones(self, observaciones: str) -> None:
        if not isinstance(observaciones, str):
            raise ValueError("Observaciones debe ser una cadena válida")
        self.__observaciones = observaciones
    
    def set_tratamiento(self, tratamiento: str) -> None:
        if not tratamiento or not isinstance(tratamiento, str):
            raise ValueError("Tratamiento debe ser una cadena válida")
        self.__tratamiento = tratamiento
    
    def set_receta(self, receta: 'Receta') -> None:
        self.__receta = receta
    
    def __str__(self) -> str:
        return (f"Historial #{self.__nro_historial} | Paciente: {self.__paciente.get_nombre()} "
                f"| Diagnóstico: {self.__diagnostico}")