from datetime import date, time
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from models.medico import Medico
    from models.paciente import Paciente
    from models.consultorio import Consultorio
    from notificaciones.notificacion import Notificacion

from turnos.states.libre import Libre
from turnos.states.programado import Programado
from turnos.states.atendido import Atendido
from turnos.states.cancelado import Cancelado
from turnos.states.inasistencia import Inasistencia
from utils.cambio_estado import CambioEstado


class Turno:
    """Clase que representa un turno médico (Patrón State)"""
    
    def __init__(self, nro_turno: int, medico: 'Medico', 
                 paciente: 'Paciente', consultorio: 'Consultorio',
                 fecha: date, hora_inicio: time, hora_fin: time,
                 id_turno: int = None):
        self.__id_turno = id_turno
        self.__nro_turno = nro_turno
        self.__medico = medico
        self.__paciente = paciente
        self.__consultorio = consultorio
        self.__fecha = fecha
        self.__hora_inicio = hora_inicio
        self.__hora_fin = hora_fin
        self.__observaciones = ""
        self.__estado_turno = Libre()  # Estado inicial
        self.__cambios_estado: List[CambioEstado] = []
        self.__notificaciones: List['Notificacion'] = []
    
    # Getters
    def get_id_turno(self) -> int:
        return self.__id_turno
    
    def get_nro_turno(self) -> int:
        return self.__nro_turno
    
    def get_medico(self) -> 'Medico':
        return self.__medico
    
    def get_paciente(self) -> 'Paciente':
        return self.__paciente
    
    def get_consultorio(self) -> 'Consultorio':
        return self.__consultorio
    
    def get_fecha(self) -> date:
        return self.__fecha
    
    def get_hora_inicio(self) -> time:
        return self.__hora_inicio
    
    def get_hora_fin(self) -> time:
        return self.__hora_fin
    
    def get_observaciones(self) -> str:
        return self.__observaciones
    
    def get_estado_turno(self):
        """Retorna el estado actual del turno"""
        return self.__estado_turno
    
    def get_cambios_estado(self) -> List[CambioEstado]:
        return self.__cambios_estado

    def agregar_notificacion(self, notificacion: 'Notificacion') -> None:
        """Agrega una notificación al turno"""
        if notificacion not in self.__notificaciones:
            self.__notificaciones.append(notificacion)
    
    def get_notificaciones(self) -> List['Notificacion']:
        """Retorna las notificaciones del turno"""
        return self.__notificaciones.copy()

    # Setters
    def set_observaciones(self, observaciones: str) -> None:
        if not observaciones or not isinstance(observaciones, str):
            raise ValueError("Observaciones debe ser una cadena válida")
        self.__observaciones = observaciones
    
    def set_estado_turno(self, nuevo_estado) -> None:
        """Cambia el estado del turno y registra el cambio (Patrón State)"""
        estado_anterior = self.__estado_turno
        self.__estado_turno = nuevo_estado
        
        # Registrar cambio
        cambio = CambioEstado(
            fecha_inicio=date.today(),
            fecha_fin=date.today(),
            estado_turno=nuevo_estado
        )
        self.__cambios_estado.append(cambio)
        
        print(f"✓ Estado cambiado: {estado_anterior.get_nombre()} → {nuevo_estado.get_nombre()}")
    
    # Métodos que respetan el State Pattern
    def cancelar(self) -> bool:
        """Intenta cancelar el turno si el estado lo permite"""
        if self.__estado_turno.puede_cancelar():
            self.set_estado_turno(Cancelado())
            return True
        else:
            print(f"✗ No se puede cancelar un turno en estado {self.__estado_turno.get_nombre()}")
            return False
    
    def atender(self) -> bool:
        """Intenta atender el turno si el estado lo permite"""
        if self.__estado_turno.puede_atender():
            self.set_estado_turno(Atendido())
            return True
        else:
            print(f"✗ No se puede atender un turno en estado {self.__estado_turno.get_nombre()}")
            return False
    
    def marcar_inasistencia(self) -> bool:
        """Intenta marcar inasistencia si el estado lo permite"""
        if self.__estado_turno.puede_marcar_ausencia():
            self.set_estado_turno(Inasistencia())
            return True
        else:
            print(f"✗ No se puede marcar ausencia en estado {self.__estado_turno.get_nombre()}")
            return False
    
    def programar(self) -> bool:
        """Programa el turno (transiciona de Libre a Programado)"""
        if isinstance(self.__estado_turno, Libre):
            self.set_estado_turno(Programado())
            return True
        else:
            print(f"✗ No se puede programar un turno en estado {self.__estado_turno.get_nombre()}")
            return False
    
    def __str__(self) -> str:
        return (f"Turno #{self.__nro_turno} | {self.__paciente.get_nombre()} "
                f"con Dr. {self.__medico.get_nombre()} | {self.__fecha} "
                f"{self.__hora_inicio} | {self.__estado_turno.get_nombre()}")