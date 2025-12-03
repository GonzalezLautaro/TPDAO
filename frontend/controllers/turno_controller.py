"""Controlador de turnos - gestiona lógica de negocio para la vista"""

import sys
import os
from typing import List, Dict, Tuple
from datetime import datetime, timedelta, date, time

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
    
    def marcar_inasistencias_automaticas(self) -> int:
        """
        Marca automáticamente como 'Inasistencia' los turnos programados 
        cuya fecha ya pasó (más de 1 día)
        
        Returns:
            Cantidad de turnos marcados como inasistencia
        """
        if not self.__db.conectar("127.0.0.1:3306/hospital_db"):
            return 0
        
        try:
            # Obtener fecha de ayer (cualquier turno de ayer o antes que siga "Programado" se marca como inasistencia)
            fecha_limite = date.today() - timedelta(days=1)
            
            # Actualizar turnos programados vencidos
            query = """
            UPDATE Turno 
            SET estado = 'Inasistencia'
            WHERE estado = 'Programado' 
            AND fecha <= %s
            """
            
            resultado = self.__db.ejecutar_consulta(query, (fecha_limite,))
            
            if resultado and resultado > 0:
                print(f"[INFO] {resultado} turno(s) marcado(s) automáticamente como inasistencia")
                return resultado
            
            return 0
        except Exception as e:
            print(f"[ERROR] Error al marcar inasistencias automáticas: {str(e)}")
            return 0
        finally:
            self.__db.desconectar()
    
    def obtener_turnos_programados(self) -> List[Dict]:
        """Obtiene todos los turnos programados de la BD"""
        # Primero marcar automáticamente las inasistencias
        self.marcar_inasistencias_automaticas()
        
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
            AND t.id_paciente IS NOT NULL
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
            query = """
            SELECT t.id_turno, 
                   c.numero as consultorio_numero,
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
            LIMIT 50
            """
            
            turnos = self.__db.obtener_registros(query, (matricula,))
            
            if not turnos:
                return []
            
            # Filtrar turnos del día actual que ya pasaron
            hoy = date.today()
            hora_actual = datetime.now().time()
            
            turnos_validos = []
            for turno in turnos:
                fecha_turno = turno['fecha']
                hora_turno = turno['hora_inicio']
                
                # Convertir hora_inicio si es timedelta
                if isinstance(hora_turno, timedelta):
                    total_seconds = int(hora_turno.total_seconds())
                    hora_turno = time(total_seconds // 3600, (total_seconds % 3600) // 60)
                
                # Si es hoy, solo incluir si la hora no pasó
                if fecha_turno == hoy:
                    if hora_turno > hora_actual:
                        turnos_validos.append(turno)
                else:
                    # Si es fecha futura, siempre incluir
                    turnos_validos.append(turno)
            
            return turnos_validos
        except Exception as e:
            print(f"[ERROR] {e}")
            return []
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
    
    def programar_turno_con_especialidad(self, id_paciente: int, matricula: int, id_turno: int, 
                        id_especialidad: int, observaciones: str = "") -> Tuple[bool, str]:
        """
        Programa un turno existente INCLUYENDO la especialidad
        
        Args:
            id_paciente: ID del paciente
            matricula: Matrícula del médico
            id_turno: ID del turno a programar
            id_especialidad: ID de la especialidad seleccionada
            observaciones: Observaciones adicionales
        
        Returns:
            (True/False, mensaje)
        """
        if not self.__db.conectar("127.0.0.1:3306/hospital_db"):
            return False, "[ERROR] No se pudo conectar a la base de datos"
        
        try:
            # Verificar que el turno existe y está libre
            query_check = "SELECT id_turno, estado FROM Turno WHERE id_turno = %s"
            turno = self.__db.obtener_registro(query_check, (id_turno,))
            
            if not turno:
                return False, "[ERROR] Turno no encontrado"
            
            if turno['estado'] != 'Libre':
                return False, f"[ERROR] El turno no está disponible (estado: {turno['estado']})"
            
            # Actualizar el turno (sin id_especialidad porque esa columna no existe en la tabla)
            query_update = """
            UPDATE Turno 
            SET id_paciente = %s, estado = 'Programado', observaciones = %s
            WHERE id_turno = %s AND estado = 'Libre'
            """
            
            resultado = self.__db.ejecutar_consulta(query_update, (id_paciente, observaciones, id_turno))
            
            if resultado is not None and resultado > 0:
                return True, "[OK] Turno programado exitosamente"
            else:
                return False, "[ERROR] No se pudo programar el turno"
        
        except Exception as e:
            return False, f"[ERROR] {str(e)}"
        finally:
            self.__db.desconectar()
    
    def cambiar_estado_turno(self, id_turno: int, nuevo_estado: str) -> Tuple[bool, str]:
        """Cambia el estado de un turno"""
        estados_validos = ['Libre', 'Programado', 'Atendido', 'Cancelado', 'Inasistencia']
        
        if nuevo_estado not in estados_validos:
            return False, f"[ERROR] Estado inválido. Válidos: {', '.join(estados_validos)}"
        
        if not self.__db.conectar("127.0.0.1:3306/hospital_db"):
            return False, "[ERROR] No se pudo conectar a la base de datos"
        
        try:
            query = "UPDATE Turno SET estado = %s WHERE id_turno = %s"
            resultado = self.__db.ejecutar_parametrizado(query, (nuevo_estado, id_turno))
            return (True, "Estado actualizado") if resultado else (False, "No se pudo cambiar estado")
        except Exception as e:
            return False, f"[ERROR] {str(e)}"
        finally:
            self.__db.desconectar()
    
    def cancelar_turno(self, id_turno: int) -> Tuple[bool, str]:
        """Cancela un turno"""
        return self.cambiar_estado_turno(id_turno, "Cancelado")
    
    def atender_turno(self, id_turno: int) -> bool:
        """Marca un turno como atendido"""
        ok, msg = self.cambiar_estado_turno(id_turno, "Atendido")
        return ok
    
    def obtener_turnos_con_doble_filtro(self, filtro_fecha: str = "hoy", filtro_estado: str = "todos_estados") -> List[Dict]:
        """
        Obtiene turnos aplicando dos filtros: por fecha y por estado
        INCLUYENDO EL NOMBRE DE LA ESPECIALIDAD
        """
        self.marcar_inasistencias_automaticas()
        
        if not self.__db.conectar("127.0.0.1:3306/hospital_db"):
            return []
        
        try:
            # Base de la query CON especialidad (obtenida desde médico-especialidad)
            # Incluye turnos libres (sin paciente) para que se puedan ver y programar
            query_base = """
            SELECT t.id_turno, 
                   COALESCE(CONCAT(p.nombre, ' ', p.apellido), 'Libre') as paciente,
                   CONCAT(m.nombre, ' ', m.apellido) as medico,
                   c.numero as consultorio,
                   COALESCE(
                       (SELECT GROUP_CONCAT(DISTINCT e.nombre SEPARATOR ', ')
                        FROM Medico_especialidad me
                        JOIN Especialidad e ON me.id_especialidad = e.id_especialidad
                        WHERE me.matricula = m.matricula),
                       'Sin especialidad'
                   ) as especialidad,
                   t.fecha, t.hora_inicio, t.hora_fin, t.estado
            FROM Turno t
            JOIN Medico m ON t.matricula = m.matricula
            LEFT JOIN Paciente p ON t.id_paciente = p.id_paciente
            JOIN Consultorio c ON t.id_consultorio = c.id_consultorio
            WHERE 1=1
            """
            
            # Agregar condiciones según filtro
            condiciones = []
            params = []
            
            hoy = date.today()
            
            if filtro_fecha == "hoy":
                condiciones.append("t.fecha = %s")
                params.append(hoy)
            elif filtro_fecha == "proximos":
                condiciones.append("t.fecha > %s")
                params.append(hoy)
            
            if filtro_estado == "programados":
                condiciones.append("t.estado = 'Programado'")
            elif filtro_estado == "atendidos":
                condiciones.append("t.estado = 'Atendido'")
            elif filtro_estado == "cancelados":
                condiciones.append("t.estado = 'Cancelado'")
            elif filtro_estado == "inasistencia":
                condiciones.append("t.estado = 'Inasistencia'")
            else:
                # "todos_estados" incluye también los turnos "Libre" generados
                condiciones.append("t.estado IN ('Libre', 'Programado', 'Atendido', 'Cancelado', 'Inasistencia')")
            
            if condiciones:
                query = query_base + " AND " + " AND ".join(condiciones)
            else:
                query = query_base
            
            query += " ORDER BY t.fecha DESC, t.hora_inicio DESC LIMIT 100"
            
            if params:
                turnos = self.__db.obtener_registros(query, tuple(params))
            else:
                turnos = self.__db.obtener_registros(query)
            
            return turnos if turnos else []
        except Exception as e:
            print(f"[ERROR] Error al cargar turnos con doble filtro: {str(e)}")
            return []
        finally:
            self.__db.desconectar()
