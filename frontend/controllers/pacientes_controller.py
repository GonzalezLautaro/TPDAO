"""Controlador de pacientes"""

import sys
import os
from typing import List, Dict

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if BASE not in sys.path:
    sys.path.insert(0, BASE)

from gestores.gestor_paciente import GestorPaciente
from data.database import Database


class PacientesController:
    """Controlador para operaciones de pacientes"""
    
    def __init__(self):
        self.__gestor = GestorPaciente()
        self.__db = Database()
    
    def listar(self) -> List[Dict]:
        """Obtiene todos los pacientes activos"""
        if not self.__db.conectar("127.0.0.1:3306/hospital_db"):
            return []
        
        try:
            query = """
            SELECT id_paciente, 
                   CONCAT(nombre, ' ', apellido) as nombre_completo,
                   telefono, fecha_nacimiento, direccion
            FROM Paciente
            WHERE activo = TRUE
            ORDER BY nombre, apellido
            """
            
            pacientes = self.__db.obtener_registros(query)
            return pacientes if pacientes else []
        except Exception as e:
            print(f"[ERROR] {e}")
            return []
        finally:
            self.__db.desconectar()
    
    # ✅ AGREGAR ESTE MÉTODO - Lo que busca pacientes_view
    def obtener_pacientes(self) -> List[Dict]:
        """Alias de listar() para compatibilidad con pacientes_view"""
        return self.listar()
    
    # ✅ AGREGAR ESTE MÉTODO - Lo que busca dar_de_baja
    def dar_de_baja_paciente(self, id_paciente: int) -> bool:
        """Marca un paciente como inactivo"""
        return self.eliminar_paciente(id_paciente)
    
    def crear_paciente(self, nombre: str, apellido: str, telefono: str, 
                      fecha_nacimiento: str, direccion: str) -> bool:
        """Crea un nuevo paciente"""
        if not self.__db.conectar("127.0.0.1:3306/hospital_db"):
            return False
        
        try:
            query = """
            INSERT INTO Paciente (nombre, apellido, telefono, fecha_nacimiento, direccion, activo)
            VALUES (%s, %s, %s, %s, %s, TRUE)
            """
            
            params = (nombre, apellido, telefono, fecha_nacimiento, direccion)
            resultado = self.__db.ejecutar_parametrizado(query, params)
            return resultado
        except Exception as e:
            print(f"[ERROR] {e}")
            return False
        finally:
            self.__db.desconectar()
    
    def actualizar_paciente(self, id_paciente: int, nombre: str, apellido: str, 
                           telefono: str, direccion: str) -> bool:
        """Actualiza datos de un paciente"""
        if not self.__db.conectar("127.0.0.1:3306/hospital_db"):
            return False
        
        try:
            query = """
            UPDATE Paciente 
            SET nombre = %s, apellido = %s, telefono = %s, direccion = %s
            WHERE id_paciente = %s
            """
            
            params = (nombre, apellido, telefono, direccion, id_paciente)
            resultado = self.__db.ejecutar_parametrizado(query, params)
            return resultado
        except Exception as e:
            print(f"[ERROR] {e}")
            return False
        finally:
            self.__db.desconectar()
    
    def eliminar_paciente(self, id_paciente: int) -> bool:
        """Marca un paciente como inactivo"""
        if not self.__db.conectar("127.0.0.1:3306/hospital_db"):
            return False
        
        try:
            query = "UPDATE Paciente SET activo = FALSE WHERE id_paciente = %s"
            resultado = self.__db.ejecutar_parametrizado(query, (id_paciente,))
            return resultado
        except Exception as e:
            print(f"[ERROR] {e}")
            return False
        finally:
            self.__db.desconectar()
