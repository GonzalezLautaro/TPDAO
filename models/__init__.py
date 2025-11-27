"""Módulo de modelos del dominio"""

from models.medico import Medico
from models.paciente import Paciente
from models.especialidad import Especialidad
from models.consultorio import Consultorio
from models.medicamento import Medicamento
from models.laboratorio import Laboratorio
from models.agenda import Agenda

__all__ = [
    'Medico',
    'Paciente',
    'Especialidad',
    'Consultorio',
    'Medicamento',
    'Laboratorio',
    'Agenda'
]