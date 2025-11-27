from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from recetas.receta import Receta
    from models.medicamento import Medicamento


class DetalleDeReceta:
    """Clase que representa un detalle (medicamento) en una receta"""
    
    def __init__(self, nro_item: int, receta: 'Receta', 
                 medicamento: 'Medicamento', indicacion: str):
        self.__nro_item = nro_item
        self.__receta = receta
        self.__medicamento = medicamento
        self.__indicacion = indicacion
    
    def get_nro_item(self) -> int:
        return self.__nro_item
    
    def get_receta(self) -> 'Receta':
        return self.__receta
    
    def get_medicamento(self) -> 'Medicamento':
        return self.__medicamento
    
    def get_indicacion(self) -> str:
        return self.__indicacion
    
    def set_indicacion(self, indicacion: str) -> None:
        if not indicacion or not isinstance(indicacion, str):
            raise ValueError("Indicación debe ser una cadena válida")
        self.__indicacion = indicacion
    
    def __str__(self) -> str:
        return (f"Item #{self.__nro_item} | {self.__medicamento.get_nombre()} "
                f"({self.__medicamento.get_dosis()}) | {self.__indicacion}")