from abc import ABC, abstractmethod


class EstadoTurno(ABC):
    """Clase base abstracta para estados de turno (Patrón State)"""
    
    def __init__(self, nombre: str, descripcion: str):
        self.__nombre = nombre
        self.__descripcion = descripcion
    
    # Getters
    def get_nombre(self) -> str:
        """Obtiene el nombre del estado"""
        return self.__nombre
    
    def get_descripcion(self) -> str:
        """Obtiene la descripción del estado"""
        return self.__descripcion
    
    # Setters
    def set_nombre(self, nombre: str) -> None:
        """Modifica el nombre del estado"""
        if nombre and len(nombre) > 0:
            self.__nombre = nombre
        else:
            raise ValueError("El nombre no puede estar vacío")
    
    # Métodos que pueden ser sobrescritos por cada estado
    @abstractmethod
    def puede_cancelar(self) -> bool:
        """Define si este estado permite cancelación"""
        pass
    
    @abstractmethod
    def puede_atender(self) -> bool:
        """Define si este estado permite atención"""
        pass
    
    @abstractmethod
    def puede_marcar_ausencia(self) -> bool:
        """Define si este estado permite marcar inasistencia"""
        pass
    
    def __str__(self) -> str:
        return f"{self.__nombre}: {self.__descripcion}"