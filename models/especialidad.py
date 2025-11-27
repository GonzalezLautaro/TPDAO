from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from models.medico import Medico

class Especialidad:
    """Clase que representa una especialidad médica"""
    
    def __init__(self, nro_especialidad: int, nombre: str, descripcion: str = ""):
        self.__nro_especialidad = nro_especialidad
        self.__nombre = nombre
        self.__descripcion = descripcion
        self.__medicos: List['Medico'] = []
    
    # Getters
    def get_nro_especialidad(self) -> int:
        return self.__nro_especialidad
    
    def get_nombre(self) -> str:
        return self.__nombre
    
    def get_descripcion(self) -> str:
        return self.__descripcion
    
    def get_medicos(self) -> List['Medico']:
        return self.__medicos.copy()
    
    # Setters
    def set_nombre(self, nombre: str) -> None:
        if not nombre or not isinstance(nombre, str):
            raise ValueError("Nombre debe ser una cadena válida")
        self.__nombre = nombre
    
    def set_descripcion(self, descripcion: str) -> None:
        if not isinstance(descripcion, str):
            raise ValueError("Descripción debe ser una cadena válida")
        self.__descripcion = descripcion
    
    # Métodos
    def agregar_medico(self, medico: 'Medico') -> None:
        """Agrega un médico a esta especialidad"""
        if medico not in self.__medicos:
            self.__medicos.append(medico)
    
    def __str__(self) -> str:
        return f"{self.__nombre}"
    
    def __repr__(self) -> str:
        return f"Especialidad({self.__nro_especialidad}, '{self.__nombre}')"