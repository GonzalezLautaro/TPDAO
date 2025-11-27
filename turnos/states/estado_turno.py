from abc import ABC, abstractmethod


class EstadoTurno(ABC):
    """Clase base abstracta para estados de turno (Patrón State)"""
    
    def __init__(self, nombre: str, descripcion: str):
        self.__nombre = nombre
        self.__descripcion = descripcion
    
    def get_nombre(self) -> str:
        return self.__nombre
    
    def get_descripcion(self) -> str:
        return self.__descripcion
    
    @abstractmethod
    def puede_cancelar(self) -> bool:
        pass
    
    @abstractmethod
    def puede_atender(self) -> bool:
        pass
    
    @abstractmethod
    def puede_marcar_ausencia(self) -> bool:
        pass
    
    def __str__(self) -> str:
        return f"{self.__nombre}: {self.__descripcion}"