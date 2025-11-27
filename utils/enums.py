from enum import Enum


class EstadoNotificacionEnum(Enum):
    """Enumeración para estados de notificaciones"""
    PENDIENTE = "pendiente"
    ENVIADO = "enviado"
    ERROR = "error"


class TipoLaboratorioEnum(Enum):
    """Enumeración para tipos de laboratorio"""
    PRIVADO = "privado"
    PUBLICO = "publico"
    HOSPITAL = "hospital"