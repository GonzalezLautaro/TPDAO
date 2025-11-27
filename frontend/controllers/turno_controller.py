"""Controlador de turnos - gestiona lógica de negocio para la vista"""

import sys
import os
from typing import List, Dict
from datetime import date, time

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if BASE not in sys.path:
    sys.path.insert(0, BASE)

from gestores.gestor_turno import GestorTurno
from data.database import Database


class TurnoController:
    """Controlador para operaciones de turnos"""
    
    def __init__(self):
        self.__gestor = GestorTurno()
        self.__db = Database()
    
    def obtener_turnos_programados(self) -> List[Dict]:
        """Obtiene todos los turnos programados de la BD"""
        if not self.__db.conectar("127.0.0.1:3306/hospital_db"):
            return []
        
        try:
            query = """
            SELECT t.id_turno, 
                   CONCAT(p.nombre, ' ', p.apellido) as paciente,
                   CONCAT(m.nombre, ' ', m.apellido) as medico,
                   c.numero as consultorio,
                   t.fecha, t.hora_inicio, t.hora_fin, t.estado
            FROM Turno t
            JOIN Medico m ON t.matricula = m.matricula
            LEFT JOIN Paciente p ON t.id_paciente = p.id_paciente
            JOIN Consultorio c ON t.id_consultorio = c.id_consultorio
            WHERE t.estado = 'Programado'
            ORDER BY t.fecha DESC, t.hora_inicio DESC
            LIMIT 100
            """
            
            turnos = self.__db.obtener_registros(query)
            return turnos if turnos else []
        except Exception as e:
            print(f"[ERROR] {e}")
            return []
        finally:
            self.__db.desconectar()
    
    def obtener_turnos_libres(self) -> List[Dict]:
        """Obtiene todos los turnos libres de la BD"""
        if not self.__db.conectar("127.0.0.1:3306/hospital_db"):
            return []
        
        try:
            query = """
            SELECT t.id_turno, 
                   CONCAT(m.nombre, ' ', m.apellido) as medico,
                   c.numero as consultorio,
                   t.fecha, t.hora_inicio, t.hora_fin, t.estado
            FROM Turno t
            JOIN Medico m ON t.matricula = m.matricula
            JOIN Consultorio c ON t.id_consultorio = c.id_consultorio
            WHERE t.estado = 'Libre'
            ORDER BY t.fecha ASC, t.hora_inicio ASC
            LIMIT 100
            """
            
            turnos = self.__db.obtener_registros(query)
            return turnos if turnos else []
        except Exception as e:
            print(f"[ERROR] {e}")
            return []
        finally:
            self.__db.desconectar()
    
    def obtener_turnos_libres_medico(self, matricula: int) -> List[Dict]:
        """Obtiene turnos libres de un médico específico"""
        if not self.__db.conectar("127.0.0.1:3306/hospital_db"):
            return []
        
        try:
            # ✅ AGREGAR: c.numero as consultorio
            query = """
            SELECT t.id_turno, 
                   c.numero as consultorio,
                   t.fecha, 
                   t.hora_inicio, 
                   t.hora_fin, 
                   t.estado
            FROM Turno t
            JOIN Consultorio c ON t.id_consultorio = c.id_consultorio
            WHERE t.matricula = %s 
            AND t.estado = 'Libre' 
            AND t.fecha >= CURDATE()
            AND t.id_paciente IS NULL
            ORDER BY t.fecha ASC, t.hora_inicio ASC
            LIMIT 20
            """
            
            turnos = self.__db.obtener_registros(query, (matricula,))
            return turnos if turnos else []
        except Exception as e:
            print(f"[ERROR] {e}")
            return False
        finally:
            self.__db.desconectar()
    
    def obtener_medicos(self) -> List[Dict]:
        """Obtiene lista de médicos activos"""
        if not self.__db.conectar("127.0.0.1:3306/hospital_db"):
            return []
        
        try:
            query = """
            SELECT matricula, CONCAT(nombre, ' ', apellido) as nombre_completo, email
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
    
    def obtener_pacientes(self) -> List[Dict]:
        """Obtiene lista de pacientes activos"""
        if not self.__db.conectar("127.0.0.1:3306/hospital_db"):
            return []
        
        try:
            query = """
            SELECT id_paciente, CONCAT(nombre, ' ', apellido) as nombre_completo, telefono
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
    
    def programar_turno(self, id_turno: int, id_paciente: int) -> bool:
        """Programa un turno asignando un paciente"""
        if not self.__db.conectar("127.0.0.1:3306/hospital_db"):
            return False
        
        try:
            query = """
            UPDATE Turno 
            SET estado = 'Programado', id_paciente = %s 
            WHERE id_turno = %s AND estado = 'Libre'
            """
            
            resultado = self.__db.ejecutar_parametrizado(query, (id_paciente, id_turno))
            return resultado
        except Exception as e:
            print(f"[ERROR] {e}")
            return False
        finally:
            self.__db.desconectar()
    
    def atender_turno(self, id_turno: int) -> bool:
        """Marca un turno como atendido"""
        if not self.__db.conectar("127.0.0.1:3306/hospital_db"):
            return False
        
        try:
            query = """
            UPDATE Turno 
            SET estado = 'Atendido' 
            WHERE id_turno = %s
            """
            
            resultado = self.__db.ejecutar_parametrizado(query, (id_turno,))
            return resultado
        except Exception as e:
            print(f"[ERROR] {e}")
            return False
        finally:
            self.__db.desconectar()
    
    def cancelar_turno(self, id_turno: int) -> bool:
        """Cancela un turno"""
        if not self.__db.conectar("127.0.0.1:3306/hospital_db"):
            return False
        
        try:
            query = """
            UPDATE Turno 
            SET estado = 'Cancelado' 
            WHERE id_turno = %s
            """
            
            resultado = self.__db.ejecutar_parametrizado(query, (id_turno,))
            return resultado
        except Exception as e:
            print(f"[ERROR] {e}")
            return False
        finally:
            self.__db.desconectar()
