"""Controlador de médicos"""

import sys
import os
from typing import List, Dict

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if BASE not in sys.path:
    sys.path.insert(0, BASE)

from gestores.gestor_medico import GestorMedico
from data.database import Database


class MedicosController:
    """Controlador para operaciones de médicos"""
    
    def __init__(self):
        self.__gestor = GestorMedico()
        self.__db = Database()
    
    def listar(self) -> List[Dict]:
        """Obtiene todos los médicos activos (método que busca medicos_view)"""
        if not self.__db.conectar("127.0.0.1:3306/hospital_db"):
            return []
        
        try:
            query = """
            SELECT matricula, nombre, apellido, telefono, email, fecha_ingreso
            FROM Medico
            WHERE activo = TRUE
            ORDER BY nombre, apellido
            """
            
            medicos = self.__db.obtener_registros(query)
            return medicos if medicos else []
        except Exception as e:
            print(f"[ERROR] {e}")
            return []
        finally:
            self.__db.desconectar()
    
    def crear_medico(self, matricula: int, nombre: str, apellido: str, 
                    telefono: str, email: str, fecha_ingreso: str) -> bool:
        """Crea un nuevo médico"""
        if not self.__db.conectar("127.0.0.1:3306/hospital_db"):
            return False
        
        try:
            query = """
            INSERT INTO Medico (matricula, nombre, apellido, telefono, email, fecha_ingreso, activo)
            VALUES (%s, %s, %s, %s, %s, %s, TRUE)
            """
            
            params = (matricula, nombre, apellido, telefono, email, fecha_ingreso)
            resultado = self.__db.ejecutar_parametrizado(query, params)
            return resultado
        except Exception as e:
            print(f"[ERROR] {e}")
            return False
        finally:
            self.__db.desconectar()
    
    def actualizar_medico(self, matricula: int, nombre: str, apellido: str, 
                         telefono: str, email: str) -> bool:
        """Actualiza datos de un médico"""
        if not self.__db.conectar("127.0.0.1:3306/hospital_db"):
            return False
        
        try:
            query = """
            UPDATE Medico 
            SET nombre = %s, apellido = %s, telefono = %s, email = %s
            WHERE matricula = %s
            """
            
            params = (nombre, apellido, telefono, email, matricula)
            resultado = self.__db.ejecutar_parametrizado(query, params)
            return resultado
        except Exception as e:
            print(f"[ERROR] {e}")
            return False
        finally:
            self.__db.desconectar()
    
    def eliminar_medico(self, matricula: int) -> bool:
        """Marca un médico como inactivo"""
        if not self.__db.conectar("127.0.0.1:3306/hospital_db"):
            return False
        
        try:
            query = "UPDATE Medico SET activo = FALSE WHERE matricula = %s"
            resultado = self.__db.ejecutar_parametrizado(query, (matricula,))
            return resultado
        except Exception as e:
            print(f"[ERROR] {e}")
            return False
        finally:
            self.__db.desconectar()
