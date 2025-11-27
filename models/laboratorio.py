class Laboratorio:
    """Clase que representa un laboratorio"""
    
    def __init__(self, numero_laboratorio: int, nombre: str, tipo: str = ""):
        self.__numero_laboratorio = numero_laboratorio
        self.__nombre = nombre
        self.__tipo = tipo
    
    # Getters
    def get_numero_laboratorio(self) -> int:
        return self.__numero_laboratorio
    
    def get_nombre(self) -> str:
        return self.__nombre
    
    def get_tipo(self) -> str:
        return self.__tipo
    
    # Setters
    def set_nombre(self, nombre: str) -> None:
        if not nombre or not isinstance(nombre, str):
            raise ValueError("Nombre debe ser una cadena válida")
        self.__nombre = nombre
    
    def set_tipo(self, tipo: str) -> None:
        if not isinstance(tipo, str):
            raise ValueError("Tipo debe ser una cadena válida")
        self.__tipo = tipo
    
    def __str__(self) -> str:
        return f"{self.__nombre} ({self.__tipo})"
    
    def __repr__(self) -> str:
        return f"Laboratorio({self.__numero_laboratorio}, '{self.__nombre}')"