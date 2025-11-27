from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from models.agenda import Agenda

class Consultorio:
    """Clase que representa un consultorio"""
    
    def __init__(self, id_consultorio: int, numero: int, piso: int, 
                 equipamiento: str = ""):
        self.__id_consultorio = id_consultorio
        self.__numero = numero
        self.__piso = piso
        self.__equipamiento = equipamiento
        self.__agendas: List['Agenda'] = []
    
    # Getters
    def get_id_consultorio(self) -> int:
        return self.__id_consultorio
    
    def get_numero(self) -> int:
        return self.__numero
    
    def get_piso(self) -> int:
        return self.__piso
    
    def get_equipamiento(self) -> str:
        return self.__equipamiento
    
    def get_agendas(self) -> List['Agenda']:
        return self.__agendas.copy()
    
    # Setters
    def set_numero(self, numero: int) -> None:
        if not isinstance(numero, int) or numero < 0:
            raise ValueError("Número debe ser un entero positivo")
        self.__numero = numero
    
    def set_piso(self, piso: int) -> None:
        if not isinstance(piso, int) or piso < 0:
            raise ValueError("Piso debe ser un entero positivo")
        self.__piso = piso
    
    def set_equipamiento(self, equipamiento: str) -> None:
        if not isinstance(equipamiento, str):
            raise ValueError("Equipamiento debe ser una cadena válida")
        self.__equipamiento = equipamiento
    
    # Métodos
    def agregar_agenda(self, agenda: 'Agenda') -> None:
        """Agrega una agenda al consultorio"""
        if agenda not in self.__agendas:
            self.__agendas.append(agenda)
    
    def __str__(self) -> str:
        return f"Consultorio {self.__numero} (Piso {self.__piso})"
    
    def __repr__(self) -> str:
        return f"Consultorio({self.__id_consultorio}, {self.__numero}, {self.__piso})"