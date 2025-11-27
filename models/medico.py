from typing import List, TYPE_CHECKING
from datetime import date

if TYPE_CHECKING:
    from models.especialidad import Especialidad
    from turnos.turno import Turno

class Medico:
    """Clase que representa un médico"""
    
    def __init__(self, matricula: int, nombre: str, apellido: str, 
                 telefono: str = "", email: str = "", 
                 fecha_ingreso: date = None, activo: bool = True):
        self.__matricula = matricula
        self.__nombre = nombre
        self.__apellido = apellido
        self.__telefono = telefono
        self.__email = email
        self.__fecha_ingreso = fecha_ingreso if fecha_ingreso else date.today()
        self.__activo = activo
        self.__especialidades: List['Especialidad'] = []
        self.__turnos: List['Turno'] = []
    
    # Getters
    def get_matricula(self) -> int:
        return self.__matricula
    
    def get_nombre(self) -> str:
        return self.__nombre
    
    def get_apellido(self) -> str:
        return self.__apellido
    
    def get_telefono(self) -> str:
        return self.__telefono
    
    def get_email(self) -> str:
        return self.__email
    
    def get_fecha_ingreso(self) -> date:
        return self.__fecha_ingreso
    
    def get_activo(self) -> bool:
        return self.__activo
    
    def get_especialidades(self) -> List['Especialidad']:
        return self.__especialidades.copy()
    
    def get_turnos(self) -> List['Turno']:
        return self.__turnos.copy()
    
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
    
    def set_email(self, email: str) -> None:
        if not isinstance(email, str):
            raise ValueError("Email debe ser una cadena válida")
        self.__email = email
    
    def set_activo(self, activo: bool) -> None:
        if not isinstance(activo, bool):
            raise ValueError("Activo debe ser un booleano")
        self.__activo = activo
    
    # Métodos
    def agregar_especialidad(self, especialidad: 'Especialidad') -> None:
        """Agrega una especialidad al médico"""
        if especialidad not in self.__especialidades:
            self.__especialidades.append(especialidad)
    
    def agregar_turno(self, turno: 'Turno') -> None:
        """Agrega un turno al médico"""
        if turno not in self.__turnos:
            self.__turnos.append(turno)
    
    def __str__(self) -> str:
        return f"Dr. {self.__nombre} {self.__apellido} (Mat. {self.__matricula})"
    
    def __repr__(self) -> str:
        return f"Medico({self.__matricula}, '{self.__nombre}', '{self.__apellido}')"