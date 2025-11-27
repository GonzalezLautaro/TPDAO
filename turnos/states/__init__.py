"""Estados del turno (Patrón State)"""

from turnos.states.estado_turno import EstadoTurno
from turnos.states.libre import Libre
from turnos.states.programado import Programado
from turnos.states.atendido import Atendido
from turnos.states.cancelado import Cancelado
from turnos.states.inasistencia import Inasistencia

__all__ = [
    'EstadoTurno',
    'Libre',
    'Programado',
    'Atendido',
    'Cancelado',
    'Inasistencia'
]