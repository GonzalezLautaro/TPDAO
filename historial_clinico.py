from typing import Optional, TYPE_CHECKING
from datetime import date

if TYPE_CHECKING:
    from turno import Turno
    from paciente import Paciente
    from receta import Receta


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
    
    # Getters
    def get_nro_historial(self) -> int:
        """Obtiene el número de historial"""
        return self.__nro_historial
    
    def get_turno(self) -> 'Turno':
        """Obtiene el turno asociado"""
        return self.__turno
    
    def get_paciente(self) -> 'Paciente':
        """Obtiene el paciente"""
        return self.__paciente
    
    def get_diagnostico(self) -> str:
        """Obtiene el diagnóstico"""
        return self.__diagnostico
    
    def get_observaciones(self) -> str:
        """Obtiene las observaciones"""
        return self.__observaciones
    
    def get_tratamiento(self) -> str:
        """Obtiene el tratamiento"""
        return self.__tratamiento
    
    def get_receta(self) -> Optional['Receta']:
        """Obtiene la receta"""
        return self.__receta
    
    def get_fecha_creacion(self) -> date:
        """Obtiene la fecha de creación del historial clínico"""
        return self.__fecha_creacion
    
    # Setters con validación
    def set_diagnostico(self, diagnostico: str) -> None:
        """Modifica el diagnóstico"""
        if not diagnostico or not isinstance(diagnostico, str):
            raise ValueError("Diagnóstico debe ser una cadena válida")
        self.__diagnostico = diagnostico
    
    def set_observaciones(self, observaciones: str) -> None:
        """Modifica las observaciones"""
        if not isinstance(observaciones, str):
            raise ValueError("Observaciones debe ser una cadena válida")
        self.__observaciones = observaciones
    
    def set_tratamiento(self, tratamiento: str) -> None:
        """Modifica el tratamiento"""
        if not tratamiento or not isinstance(tratamiento, str):
            raise ValueError("Tratamiento debe ser una cadena válida")
        self.__tratamiento = tratamiento
    
    def set_receta(self, receta: 'Receta') -> None:
        """Vincula una receta al historial clínico"""
        self.__receta = receta
    
    def __str__(self) -> str:
        return (f"Historial #{self.__nro_historial} | Paciente: {self.__paciente.get_nombre()} "
                f"| Diagnóstico: {self.__diagnostico}")