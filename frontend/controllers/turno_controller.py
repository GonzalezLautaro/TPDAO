from datetime import datetime, timedelta
import sys, os
from typing import List, Dict, Tuple

# asegurar tpdao en sys.path
BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if BASE not in sys.path:
    sys.path.insert(0, BASE)

# importar tu backend real
from gestores.gestor_turno import GestorTurno
from data.database import Database


class TurnoController:
    def __init__(self):
        self.gestor = GestorTurno()

    # ========== OBTENER DATOS ==========
    def obtener_medicos(self) -> List[Dict]:
        """Obtiene lista de médicos activos"""
        db = Database()
        if not db.conectar("127.0.0.1:3306/hospital_db"):
            print("[DEBUG] Error conectando a BD")
            return []
        
        try:
            # Debug: Ver si la conexión funciona
            print("[DEBUG] === OBTENER MEDICOS ===")
            
            # Intenta con query simple
            query = "SELECT COUNT(*) as total FROM Medico"
            result = db.obtener_registro(query)
            print(f"[DEBUG] Total de médicos en BD: {result}")
            
            # Ahora obtener lista completa
            query = "SELECT matricula, nombre, apellido FROM Medico"
            print(f"[DEBUG] Ejecutando query: {query}")
            
            medicos = db.obtener_registros(query)
            
            print(f"[DEBUG] Tipo de resultado: {type(medicos)}")
            print(f"[DEBUG] Resultado raw: {medicos}")
            
            db.desconectar()
            
            if medicos:
                print(f"[DEBUG] ✓ Médicos cargados: {len(medicos)}")
                for i, m in enumerate(medicos, 1):
                    print(f"[DEBUG]   {i}. {m}")
                return medicos
            else:
                print("[DEBUG] ✗ Lista vacía")
                return []
        
        except Exception as e:
            print(f"[ERROR] Error al cargar médicos: {str(e)}")
            import traceback
            traceback.print_exc()
            db.desconectar()
            return []

    def obtener_pacientes(self) -> List[Dict]:
        """Obtiene lista de pacientes activos"""
        db = Database()
        if not db.conectar("127.0.0.1:3306/hospital_db"):
            print("[DEBUG] Error conectando a BD")
            return []
        
        try:
            query = "SELECT id_paciente, nombre, apellido FROM Paciente ORDER BY nombre, apellido"
            pacientes = db.obtener_registros(query)
            
            db.desconectar()
            
            if pacientes:
                print(f"[DEBUG] ✓ Pacientes cargados: {len(pacientes)}")
                return pacientes
            else:
                print("[DEBUG] ✗ No se encontraron pacientes en la BD")
                return []
        
        except Exception as e:
            print(f"[ERROR] Error al cargar pacientes: {str(e)}")
            import traceback
            traceback.print_exc()
            db.desconectar()
            return []

    def obtener_turnos_libres_medico(self, matricula: int) -> List[Dict]:
        """Obtiene turnos libres de un médico, agrupados por día"""
        db = Database()
        if not db.conectar("127.0.0.1:3306/hospital_db"):
            return []
        
        try:
            query = """
            SELECT t.id_turno, t.fecha, t.hora_inicio, t.hora_fin, t.id_consultorio,
                   c.numero as consultorio_numero
            FROM Turno t
            JOIN Consultorio c ON t.id_consultorio = c.id_consultorio
            WHERE t.matricula = %s AND t.estado = 'Libre' AND t.fecha >= CURDATE()
            ORDER BY t.fecha, t.hora_inicio
            LIMIT 50
            """
            
            turnos = db.obtener_registros(query, (matricula,))
            db.desconectar()
            return turnos if turnos else []
        except Exception as e:
            print(f"[ERROR] Error al cargar turnos: {str(e)}")
            db.desconectar()
            return []

    def obtener_turnos_programados(self) -> List[Dict]:
        """Obtiene todos los turnos programados"""
        db = Database()
        if not db.conectar("127.0.0.1:3306/hospital_db"):
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
            
            turnos = db.obtener_registros(query)
            db.desconectar()
            return turnos if turnos else []
        except Exception as e:
            print(f"[ERROR] Error al cargar turnos programados: {str(e)}")
            db.desconectar()
            return []

    # ========== CREAR TURNO ==========
    def programar_turno(self, id_paciente: int, matricula: int, id_turno: int, 
                        observaciones: str = "") -> Tuple[bool, str]:
        """
        Programa un turno existente (cambia de Libre a Programado)
        
        Args:
            id_paciente: ID del paciente
            matricula: Matrícula del médico
            id_turno: ID del turno a programar
            observaciones: Observaciones adicionales
        
        Returns:
            (True/False, mensaje)
        """
        db = Database()
        if not db.conectar("127.0.0.1:3306/hospital_db"):
            return False, "[ERROR] No se pudo conectar a la base de datos"
        
        try:
            # Verificar que el turno existe y está libre
            query_check = "SELECT id_turno, estado FROM Turno WHERE id_turno = %s"
            turno = db.obtener_registro(query_check, (id_turno,))
            
            if not turno:
                return False, "[ERROR] Turno no encontrado"
            
            if turno['estado'] != 'Libre':
                return False, f"[ERROR] El turno no está disponible (estado: {turno['estado']})"
            
            # Actualizar el turno
            query_update = """
            UPDATE Turno 
            SET id_paciente = %s, estado = 'Programado', observaciones = %s
            WHERE id_turno = %s AND estado = 'Libre'
            """
            
            resultado = db.ejecutar_consulta(query_update, (id_paciente, observaciones, id_turno))
            
            if resultado is not None and resultado > 0:
                db.desconectar()
                return True, "[OK] Turno programado exitosamente"
            else:
                db.desconectar()
                return False, "[ERROR] No se pudo programar el turno"
        
        except Exception as e:
            db.desconectar()
            return False, f"[ERROR] {str(e)}"

    # ========== CAMBIAR ESTADO ==========
    def cambiar_estado_turno(self, id_turno: int, nuevo_estado: str) -> Tuple[bool, str]:
        """Cambia el estado de un turno"""
        estados_validos = ['Libre', 'Programado', 'Atendido', 'Cancelado', 'Inasistencia']
        
        if nuevo_estado not in estados_validos:
            return False, f"[ERROR] Estado inválido. Válidos: {', '.join(estados_validos)}"
        
        ok = self.gestor.modificar_turno_bd(id_turno, estado=nuevo_estado)
        return (True, "Estado actualizado") if ok else (False, "No se pudo cambiar estado")

    def cancelar_turno(self, id_turno: int) -> Tuple[bool, str]:
        """Cancela un turno"""
        ok = self.gestor.baja_turno_bd(id_turno)
        return (True, "Turno cancelado") if ok else (False, "No se pudo cancelar el turno")

    # ========== LISTAR ==========
    def listar_turnos_programados(self) -> List[Dict]:
        """Lista turnos programados formateados"""
        return self.obtener_turnos_programados()
    
    def programar(self, id_paciente: str, matricula: str, fecha_str: str) -> Tuple[bool, str]:
        """Método legacy - mantener para compatibilidad"""
        try:
            return self.programar_turno(int(id_paciente), int(matricula), 0, "")
        except:
            return False, "Error en programación"
