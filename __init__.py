"""Sistema de Gestión Médica - TPI DAO"""

__version__ = "1.0.0"
__author__ = "Tu Nombre"

from config.settings import APP_NAME, APP_VERSION
from data.database import Database

__all__ = [
    'Database',
    'APP_NAME',
    'APP_VERSION'
]