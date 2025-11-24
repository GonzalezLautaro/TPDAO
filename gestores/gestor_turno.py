from typing import List, Optional, Dict
from datetime import date, time
import sys
import os

# Agregar el directorio padre al path para importar módulos
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from turno import Turno
from data.database import Database


class GestorTurno:
    """Clase gestora de operaciones ABMC de turnos"""
    
    def __init__(self):
        self.__turnos: List[Turno] = []
        self.__turnos_bd: List[Dict] = []
    
    # ========== CARGAR DE BASE DE DATOS ==========
    def cargar_turnos_bd(self) -> bool:
        """
        Carga todos los turnos de la base de datos
        
        Returns:
            True si se cargaron correctamente, False en caso contrario
        """
        db = Database()
        
        if not db.conectar("127.0.0.1:3306/hospital_db"):
            print("[ERROR] No se pudo conectar a la base de datos")
            return False
        
        try:
            query = """
            SELECT t.id_turno, t.id_paciente, t.matricula, t.id_consultorio,
                   t.fecha, t.hora, t.estado, t.observaciones,
                   p.nombre as paciente_nombre, p.apellido as paciente_apellido,
                   m.nombre as medico_nombre, m.apellido as medico_apellido,
                   c.numero as consultorio_numero
            FROM Turno t
            JOIN Paciente p ON t.id_paciente = p.id_paciente
            JOIN Medico m ON t.matricula = m.matricula
            JOIN Consultorio c ON t.id_consultorio = c.id_consultorio
            ORDER BY t.fecha, t.hora
            """
            
            turnos = db.obtener_registros(query)
            
            if turnos:
                self.__turnos_bd = turnos
                print(f"[OK] Se cargaron {len(turnos)} turno(s) de la base de datos")
                return True
            else:
                print("[INFO] No hay turnos en la base de datos")
                return False
        
        except Exception as e:
            print(f"[ERROR] Error al cargar turnos: {str(e)}")
            return False
        
        finally:
            db.desconectar()
    
    # ========== LISTAR TURNOS DE BD ==========
    def listar_turnos_bd(self) -> bool:
        """
        Lista todos los turnos de la base de datos
        
        Returns:
            True si se listaron correctamente
        """
        if not self.__turnos_bd:
            if not self.cargar_turnos_bd():
                return False
        
        if self.__turnos_bd:
            print(f"\n[INFO] Total de turnos: {len(self.__turnos_bd)}\n")
            for turno in self.__turnos_bd:
                self._mostrar_turno_bd(turno)
            return True
        else:
            print("[INFO] No hay turnos registrados")
            return False
    
    # ========== ALTA (CREATE) ==========
    def alta_turno(self, id_paciente: int, matricula: int, id_consultorio: int,
                   fecha: date, hora: time, observaciones: str = "") -> bool:
        """
        Da de alta un nuevo turno en la base de datos
        
        Args:
            id_paciente: ID del paciente
            matricula: Matrícula del médico
            id_consultorio: ID del consultorio
            fecha: Fecha del turno
            hora: Hora del turno
            observaciones: Observaciones (opcional)
        
        Returns:
            True si se creó exitosamente, False en caso contrario
        """
        db = Database()
        
        if not db.conectar("127.0.0.1:3306/hospital_db"):
            print("[ERROR] No se pudo conectar a la base de datos")
            return False
        
        try:
            # Verificar que el paciente existe
            query_check_paciente = "SELECT id_paciente FROM Paciente WHERE id_paciente = %s AND activo = TRUE"
            paciente = db.obtener_registro(query_check_paciente, (id_paciente,))
            
            if not paciente:
                print(f"[ERROR] Paciente con ID {id_paciente} no existe o está inactivo")
                db.desconectar()
                return False
            
            # Verificar que el médico existe
            query_check_medico = "SELECT matricula FROM Medico WHERE matricula = %s AND activo = TRUE"
            medico = db.obtener_registro(query_check_medico, (matricula,))
            
            if not medico:
                print(f"[ERROR] Médico con matrícula {matricula} no existe o está inactivo")
                db.desconectar()
                return False
            
            # Verificar que el consultorio existe
            query_check_consultorio = "SELECT id_consultorio FROM Consultorio WHERE id_consultorio = %s"
            consultorio = db.obtener_registro(query_check_consultorio, (id_consultorio,))
            
            if not consultorio:
                print(f"[ERROR] Consultorio con ID {id_consultorio} no existe")
                db.desconectar()
                return False
            
            # Verificar que no existe un turno duplicado
            query_check_turno = """
            SELECT id_turno FROM Turno 
            WHERE id_paciente = %s AND matricula = %s AND fecha = %s AND hora = %s
            """
            turno_existe = db.obtener_registro(query_check_turno, (id_paciente, matricula, fecha, hora))
            
            if turno_existe:
                print("[ERROR] Ya existe un turno para este paciente, médico y horario")
                db.desconectar()
                return False
            
            # Crear el turno
            query = """
            INSERT INTO Turno (id_paciente, matricula, id_consultorio, fecha, hora, estado, observaciones, id_agenda)
            VALUES (%s, %s, %s, %s, %s, 'Programado', %s, NULL)
            """
            
            params = (id_paciente, matricula, id_consultorio, fecha, hora, observaciones)
            resultado = db.ejecutar_consulta(query, params)
            
            if resultado is not None and resultado > 0:
                print(f"[OK] Turno creado exitosamente")
                print(f"     Fecha: {fecha} a las {hora}")
                print(f"     Consultorio: {id_consultorio}")
                self.__turnos_bd = []  # Recargar
                db.desconectar()
                return True
            else:
                print("[ERROR] No se pudo crear el turno")
                db.desconectar()
                return False
        
        except Exception as e:
            print(f"[ERROR] Error al crear turno: {str(e)}")
            db.desconectar()
            return False
    
    # ========== BAJA (DELETE) ==========
    def baja_turno_bd(self, id_turno: int) -> bool:
        """
        Da de baja un turno en la base de datos
        
        Args:
            id_turno: ID del turno a eliminar
        
        Returns:
            True si se eliminó, False en caso contrario
        """
        db = Database()
        
        if not db.conectar("127.0.0.1:3306/hospital_db"):
            print("[ERROR] No se pudo conectar a la base de datos")
            return False
        
        try:
            # Verificar que el turno existe
            query_check = """
            SELECT t.id_turno, p.nombre as paciente_nombre, p.apellido as paciente_apellido,
                   t.fecha, t.hora
            FROM Turno t
            JOIN Paciente p ON t.id_paciente = p.id_paciente
            WHERE t.id_turno = %s
            """
            
            turno = db.obtener_registro(query_check, (id_turno,))
            
            if not turno:
                print(f"[ERROR] No se encontró turno con ID {id_turno}")
                db.desconectar()
                return False
            
            # Eliminar el turno
            query = "DELETE FROM Turno WHERE id_turno = %s"
            resultado = db.ejecutar_consulta(query, (id_turno,))
            
            if resultado is not None and resultado > 0:
                print(f"[OK] Turno #{id_turno} eliminado exitosamente")
                print(f"     Paciente: {turno['paciente_nombre']} {turno['paciente_apellido']}")
                print(f"     Fecha: {turno['fecha']} a las {turno['hora']}")
                self.__turnos_bd = []  # Recargar
                db.desconectar()
                return True
            else:
                print("[ERROR] No se pudo eliminar el turno")
                db.desconectar()
                return False
        
        except Exception as e:
            print(f"[ERROR] Error al eliminar turno: {str(e)}")
            db.desconectar()
            return False
    
    # ========== MODIFICACIÓN (UPDATE) ==========
    def modificar_turno_bd(self, id_turno: int, fecha: Optional[date] = None,
                          hora: Optional[time] = None, 
                          estado: Optional[str] = None,
                          observaciones: Optional[str] = None) -> bool:
        """
        Modifica un turno en la base de datos
        
        Args:
            id_turno: ID del turno a modificar
            fecha: Nueva fecha (opcional)
            hora: Nueva hora (opcional)
            estado: Nuevo estado (opcional)
            observaciones: Nuevas observaciones (opcional)
        
        Returns:
            True si se modificó, False en caso contrario
        """
        db = Database()
        
        if not db.conectar("127.0.0.1:3306/hospital_db"):
            print("[ERROR] No se pudo conectar a la base de datos")
            return False
        
        try:
            # Verificar que el turno existe
            query_check = "SELECT id_turno FROM Turno WHERE id_turno = %s"
            turno = db.obtener_registro(query_check, (id_turno,))
            
            if not turno:
                print(f"[ERROR] No se encontró turno con ID {id_turno}")
                db.desconectar()
                return False
            
            datos_actualizar = {}
            
            if fecha:
                datos_actualizar['fecha'] = fecha
            if hora:
                datos_actualizar['hora'] = hora
            if estado:
                # Validar estados válidos
                estados_validos = ['Libre', 'Programado', 'Atendido', 'Cancelado', 'Inasistencia']
                if estado not in estados_validos:
                    print(f"[ERROR] Estado '{estado}' no válido. Válidos: {', '.join(estados_validos)}")
                    db.desconectar()
                    return False
                datos_actualizar['estado'] = estado
            if observaciones:
                datos_actualizar['observaciones'] = observaciones
            
            if not datos_actualizar:
                print("[ERROR] No hay datos para actualizar")
                db.desconectar()
                return False
            
            # Construir la consulta UPDATE dinámicamente
            campos = ", ".join([f"{campo} = %s" for campo in datos_actualizar.keys()])
            valores = list(datos_actualizar.values())
            valores.append(id_turno)
            
            query = f"UPDATE Turno SET {campos} WHERE id_turno = %s"
            resultado = db.ejecutar_consulta(query, tuple(valores))
            
            if resultado is not None and resultado > 0:
                print(f"[OK] Turno #{id_turno} modificado exitosamente")
                self.__turnos_bd = []  # Recargar
                db.desconectar()
                return True
            else:
                print("[ERROR] No se pudo modificar el turno")
                db.desconectar()
                return False
        
        except Exception as e:
            print(f"[ERROR] Error al modificar turno: {str(e)}")
            db.desconectar()
            return False
    
    # ========== CONSULTA (READ) ==========
    def consultar_turnos_paciente_bd(self, id_paciente: int) -> bool:
        """
        Consulta turnos de un paciente desde BD
        
        Args:
            id_paciente: ID del paciente
        
        Returns:
            True si se encontraron turnos
        """
        db = Database()
        
        if not db.conectar("127.0.0.1:3306/hospital_db"):
            print("[ERROR] No se pudo conectar a la base de datos")
            return False
        
        try:
            query = """
            SELECT t.id_turno, t.fecha, t.hora, t.estado, t.observaciones,
                   m.nombre as medico_nombre, m.apellido as medico_apellido,
                   c.numero as consultorio_numero
            FROM Turno t
            JOIN Medico m ON t.matricula = m.matricula
            JOIN Consultorio c ON t.id_consultorio = c.id_consultorio
            WHERE t.id_paciente = %s
            ORDER BY t.fecha, t.hora
            """
            
            turnos = db.obtener_registros(query, (id_paciente,))
            
            if turnos:
                print(f"\n[OK] Se encontraron {len(turnos)} turno(s) para paciente ID {id_paciente}:\n")
                for turno in turnos:
                    self._mostrar_turno_bd(turno)
                db.desconectar()
                return True
            else:
                print(f"[ERROR] No se encontraron turnos para paciente ID {id_paciente}")
                db.desconectar()
                return False
        
        except Exception as e:
            print(f"[ERROR] Error al consultar turnos: {str(e)}")
            db.desconectar()
            return False
    
    def consultar_turnos_medico_bd(self, matricula: int) -> bool:
        """
        Consulta turnos de un médico desde BD
        
        Args:
            matricula: Matrícula del médico
        
        Returns:
            True si se encontraron turnos
        """
        db = Database()
        
        if not db.conectar("127.0.0.1:3306/hospital_db"):
            print("[ERROR] No se pudo conectar a la base de datos")
            return False
        
        try:
            query = """
            SELECT t.id_turno, t.matricula, t.fecha, t.hora, t.estado, t.observaciones,
                   p.nombre as paciente_nombre, p.apellido as paciente_apellido,
                   c.numero as consultorio_numero
            FROM Turno t
            JOIN Paciente p ON t.id_paciente = p.id_paciente
            JOIN Consultorio c ON t.id_consultorio = c.id_consultorio
            WHERE t.matricula = %s
            ORDER BY t.fecha, t.hora
            """
            
            turnos = db.obtener_registros(query, (matricula,))
            
            if turnos:
                print(f"\n[OK] Se encontraron {len(turnos)} turno(s) para médico matrícula {matricula}:\n")
                for turno in turnos:
                    self._mostrar_turno_bd(turno)
                db.desconectar()
                return True
            else:
                print(f"[ERROR] No se encontraron turnos para médico matrícula {matricula}")
                db.desconectar()
                return False
        
        except Exception as e:
            print(f"[ERROR] Error al consultar turnos: {str(e)}")
            db.desconectar()
            return False
    
    def consultar_turnos_fecha_bd(self, fecha: date) -> bool:
        """
        Consulta turnos de una fecha específica desde BD
        
        Args:
            fecha: Fecha a consultar
        
        Returns:
            True si se encontraron turnos
        """
        db = Database()
        
        if not db.conectar("127.0.0.1:3306/hospital_db"):
            print("[ERROR] No se pudo conectar a la base de datos")
            return False
        
        try:
            query = """
            SELECT t.id_turno, t.hora, t.estado, t.observaciones,
                   p.nombre as paciente_nombre, p.apellido as paciente_apellido,
                   m.nombre as medico_nombre, m.apellido as medico_apellido,
                   c.numero as consultorio_numero
            FROM Turno t
            JOIN Paciente p ON t.id_paciente = p.id_paciente
            JOIN Medico m ON t.matricula = m.matricula
            JOIN Consultorio c ON t.id_consultorio = c.id_consultorio
            WHERE t.fecha = %s
            ORDER BY t.hora
            """
            
            turnos = db.obtener_registros(query, (fecha,))
            
            if turnos:
                print(f"\n[OK] Se encontraron {len(turnos)} turno(s) para {fecha}:\n")
                for turno in turnos:
                    self._mostrar_turno_bd(turno)
                db.desconectar()
                return True
            else:
                print(f"[ERROR] No se encontraron turnos para {fecha}")
                db.desconectar()
                return False
        
        except Exception as e:
            print(f"[ERROR] Error al consultar turnos: {str(e)}")
            db.desconectar()
            return False
    
    # ========== MÉTODOS AUXILIARES ==========
    def _mostrar_turno_bd(self, turno: Dict) -> None:
        """Muestra los datos de un turno de BD formateados"""
        print(f"   ID Turno: {turno['id_turno']}")
        if 'paciente_nombre' in turno:
            print(f"   Paciente: {turno['paciente_nombre']} {turno['paciente_apellido']}")
        if 'medico_nombre' in turno:
            print(f"   Médico: {turno['medico_nombre']} {turno['medico_apellido']}")
        print(f"   Consultorio: #{turno['consultorio_numero']}")
        if 'fecha' in turno:
            print(f"   Fecha: {turno['fecha']}")
        print(f"   Hora: {turno['hora']}")
        print(f"   Estado: {turno['estado']}")
        if turno.get('observaciones'):
            print(f"   Observaciones: {turno['observaciones']}")
        print()

    def get_turnos_bd(self) -> List[Dict]:
        """Retorna la lista de turnos de BD"""
        return self.__turnos_bd.copy()
    
    def __repr__(self) -> str:
        return f"GestorTurno(Turnos en BD: {len(self.__turnos_bd)})"
