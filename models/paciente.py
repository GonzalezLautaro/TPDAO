from typing import List, TYPE_CHECKING
from datetime import date

if TYPE_CHECKING:
    from turnos.turno import Turno
    from historiales.historial_clinico import HistorialClinico

class Paciente:
    """Clase que representa un paciente"""
    
    def __init__(self, nro_paciente: int, nombre: str, apellido: str, 
                 telefono: str = "", fecha_nacimiento: date = None,
                 direccion: str = "", activo: bool = True):
        self.__nro_paciente = nro_paciente
        self.__nombre = nombre
        self.__apellido = apellido
        self.__telefono = telefono
        self.__fecha_nacimiento = fecha_nacimiento if fecha_nacimiento else date.today()
        self.__direccion = direccion
        self.__activo = activo
        self.__turnos: List['Turno'] = []
        self.__historiales: List['HistorialClinico'] = []
    
    # Getters
    def get_nro_paciente(self) -> int:
        return self.__nro_paciente
    
    def get_nombre(self) -> str:
        return self.__nombre
    
    def get_apellido(self) -> str:
        return self.__apellido
    
    def get_telefono(self) -> str:
        return self.__telefono
    
    def get_fecha_nacimiento(self) -> date:
        return self.__fecha_nacimiento
    
    def get_direccion(self) -> str:
        return self.__direccion
    
    def get_activo(self) -> bool:
        return self.__activo
    
    def get_turnos(self) -> List['Turno']:
        return self.__turnos.copy()
    
    def get_historiales(self) -> List['HistorialClinico']:
        return self.__historiales.copy()
    
    # Setters
    def set_nombre(self, nombre: str) -> None:
        if not nombre or not isinstance(nombre, str):
            raise ValueError("Nombre debe ser una cadena válida")
        self.__nombre = nombre
    
    def set_apellido(self, apellido: str) -> None:
        if not apellido or not isinstance(apellido, str):
            raise ValueError("Apellido debe ser una cadena válida")
        self.__apellido = apellido
    
    def set_telefono(self, telefono: str) -> None:
        if not isinstance(telefono, str):
            raise ValueError("Teléfono debe ser una cadena válida")
        self.__telefono = telefono
    
    def set_direccion(self, direccion: str) -> None:
        if not isinstance(direccion, str):
            raise ValueError("Dirección debe ser una cadena válida")
        self.__direccion = direccion
    
    def set_activo(self, activo: bool) -> None:
        if not isinstance(activo, bool):
            raise ValueError("Activo debe ser un booleano")
        self.__activo = activo
    
    # Métodos
    def agregar_turno(self, turno: 'Turno') -> None:
        """Agrega un turno al paciente"""
        if turno not in self.__turnos:
            self.__turnos.append(turno)
    
    def agregar_historial(self, historial: 'HistorialClinico') -> None:
        """Agrega un historial clínico al paciente"""
        if historial not in self.__historiales:
            self.__historiales.append(historial)
    
    def __str__(self) -> str:
        return f"{self.__nombre} {self.__apellido}"
    
    def __repr__(self) -> str:
        return f"Paciente({self.__nro_paciente}, '{self.__nombre}', '{self.__apellido}')"