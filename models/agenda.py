from datetime import time
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.medico import Medico
    from models.consultorio import Consultorio

class Agenda:
    """Clase que representa la agenda de un médico en un consultorio"""
    
    def __init__(self, id_agenda: int, medico: 'Medico', consultorio: 'Consultorio',
                 dia_semana: str, hora_inicio: time, hora_fin: time):
        self.__id_agenda = id_agenda
        self.__medico = medico
        self.__consultorio = consultorio
        self.__dia_semana = dia_semana
        self.__hora_inicio = hora_inicio
        self.__hora_fin = hora_fin
    
    # Getters
    def get_id_agenda(self) -> int:
        return self.__id_agenda
    
    def get_medico(self) -> 'Medico':
        return self.__medico
    
    def get_consultorio(self) -> 'Consultorio':
        return self.__consultorio
    
    def get_dia_semana(self) -> str:
        return self.__dia_semana
    
    def get_hora_inicio(self) -> time:
        return self.__hora_inicio
    
    def get_hora_fin(self) -> time:
        return self.__hora_fin
    
    # Setters
    def set_dia_semana(self, dia_semana: str) -> None:
        dias_validos = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
        if dia_semana not in dias_validos:
            raise ValueError(f"Día debe ser uno de: {dias_validos}")
        self.__dia_semana = dia_semana
    
    def set_hora_inicio(self, hora_inicio: time) -> None:
        if not isinstance(hora_inicio, time):
            raise ValueError("Hora inicio debe ser un objeto time")
        self.__hora_inicio = hora_inicio
    
    def set_hora_fin(self, hora_fin: time) -> None:
        if not isinstance(hora_fin, time):
            raise ValueError("Hora fin debe ser un objeto time")
        self.__hora_fin = hora_fin
    
    def __str__(self) -> str:
        return (f"Agenda: {self.__medico.get_nombre()} - {self.__dia_semana} "
                f"{self.__hora_inicio} a {self.__hora_fin}")
    
    def __repr__(self) -> str:
        return f"Agenda({self.__id_agenda}, {self.__medico}, {self.__consultorio})"