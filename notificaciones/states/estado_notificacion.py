from abc import ABC, abstractmethod


class EstadoNotificacion(ABC):
    """Clase base abstracta para estados de notificación (Patrón State)"""
    
    def __init__(self, nombre: str, descripcion: str):
        self.__nombre = nombre
        self.__descripcion = descripcion
    
    def get_nombre(self) -> str:
        return self.__nombre
    
    def get_descripcion(self) -> str:
        return self.__descripcion
    
    @abstractmethod
    def puede_enviar(self) -> bool:
        pass
    
    @abstractmethod
    def puede_reintentar(self) -> bool:
        pass
    
    def __str__(self) -> str:
        return f"{self.__nombre}: {self.__descripcion}"