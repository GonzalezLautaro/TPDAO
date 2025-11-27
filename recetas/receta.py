from datetime import date
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from recetas.detalle_receta import DetalleDeReceta


class Receta:
    """Clase que representa una receta médica"""
    
    def __init__(self, nro_receta: int, fecha_emision: date, 
                 observaciones: str = ""):
        self.__nro_receta = nro_receta
        self.__fecha_emision = fecha_emision
        self.__observaciones = observaciones
        self.__detalles: List['DetalleDeReceta'] = []
    
    def get_nro_receta(self) -> int:
        return self.__nro_receta
    
    def get_fecha_emision(self) -> date:
        return self.__fecha_emision
    
    def get_observaciones(self) -> str:
        return self.__observaciones
    
    def get_detalles(self) -> List['DetalleDeReceta']:
        return self.__detalles
    
    def set_observaciones(self, observaciones: str) -> None:
        if not isinstance(observaciones, str):
            raise ValueError("Observaciones debe ser una cadena válida")
        self.__observaciones = observaciones
    
    def agregar_detalle(self, detalle: 'DetalleDeReceta') -> None:
        """Agrega un detalle (medicamento) a la receta"""
        if not detalle:
            raise ValueError("El detalle no puede ser nulo")
        self.__detalles.append(detalle)
    
    def __str__(self) -> str:
        return f"Receta #{self.__nro_receta} | {len(self.__detalles)} medicamentos"