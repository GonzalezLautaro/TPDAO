class Medicamento:
    """Clase que representa un medicamento"""
    
    def __init__(self, numero_medicamento: int, nombre: str, dosis: str, 
                 formato: str = ""):
        self.__numero_medicamento = numero_medicamento
        self.__nombre = nombre
        self.__dosis = dosis
        self.__formato = formato
    
    # Getters
    def get_numero_medicamento(self) -> int:
        return self.__numero_medicamento
    
    def get_nombre(self) -> str:
        return self.__nombre
    
    def get_dosis(self) -> str:
        return self.__dosis
    
    def get_formato(self) -> str:
        return self.__formato
    
    # Setters
    def set_nombre(self, nombre: str) -> None:
        if not nombre or not isinstance(nombre, str):
            raise ValueError("Nombre debe ser una cadena válida")
        self.__nombre = nombre
    
    def set_dosis(self, dosis: str) -> None:
        if not dosis or not isinstance(dosis, str):
            raise ValueError("Dosis debe ser una cadena válida")
        self.__dosis = dosis
    
    def set_formato(self, formato: str) -> None:
        if not isinstance(formato, str):
            raise ValueError("Formato debe ser una cadena válida")
        self.__formato = formato
    
    def __str__(self) -> str:
        return f"{self.__nombre} ({self.__dosis}) - {self.__formato}"
    
    def __repr__(self) -> str:
        return f"Medicamento({self.__numero_medicamento}, '{self.__nombre}')"