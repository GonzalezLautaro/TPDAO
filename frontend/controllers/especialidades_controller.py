"""Controlador de especialidades"""

import sys
import os
from typing import List, Dict

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if BASE not in sys.path:
    sys.path.insert(0, BASE)

from gestores.gestor_especialidad import GestorEspecialidad
from data.database import Database


class EspecialidadesController:
    """Controlador para operaciones de especialidades"""
    
    def __init__(self):
        self.__gestor = GestorEspecialidad()
        self.__db = Database()
    
    def listar(self) -> List[Dict]:
        """Obtiene todas las especialidades (método que busca especialidades_view)"""
        if not self.__db.conectar("127.0.0.1:3306/hospital_db"):
            return []
        
        try:
            query = """
            SELECT id_especialidad, nombre, descripcion
            FROM Especialidad
            ORDER BY nombre
            """
            
            especialidades = self.__db.obtener_registros(query)
            return especialidades if especialidades else []
        except Exception as e:
            print(f"[ERROR] {e}")
            return []
        finally:
            self.__db.desconectar()
    
    def crear_especialidad(self, nombre: str, descripcion: str = "") -> bool:
        """Crea una nueva especialidad"""
        if not self.__db.conectar("127.0.0.1:3306/hospital_db"):
            return False
        
        try:
            query = """
            INSERT INTO Especialidad (nombre, descripcion)
            VALUES (%s, %s)
            """
            
            params = (nombre, descripcion)
            resultado = self.__db.ejecutar_parametrizado(query, params)
            return resultado
        except Exception as e:
            print(f"[ERROR] {e}")
            return False
        finally:
            self.__db.desconectar()
    
    def actualizar_especialidad(self, id_especialidad: int, nombre: str, descripcion: str) -> bool:
        """Actualiza una especialidad"""
        if not self.__db.conectar("127.0.0.1:3306/hospital_db"):
            return False
        
        try:
            query = """
            UPDATE Especialidad 
            SET nombre = %s, descripcion = %s
            WHERE id_especialidad = %s
            """
            
            params = (nombre, descripcion, id_especialidad)
            resultado = self.__db.ejecutar_parametrizado(query, params)
            return resultado
        except Exception as e:
            print(f"[ERROR] {e}")
            return False
        finally:
            self.__db.desconectar()
    
    def eliminar_especialidad(self, id_especialidad: int) -> bool:
        """Elimina una especialidad"""
        if not self.__db.conectar("127.0.0.1:3306/hospital_db"):
            return False
        
        try:
            query = "DELETE FROM Especialidad WHERE id_especialidad = %s"
            resultado = self.__db.ejecutar_parametrizado(query, (id_especialidad,))
            return resultado
        except Exception as e:
            print(f"[ERROR] {e}")
            return False
        finally:
            self.__db.desconectar()
