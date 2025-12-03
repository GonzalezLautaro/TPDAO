from datetime import date
import sys, os

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if BASE not in sys.path:
    sys.path.insert(0, BASE)

from gestores.gestor_paciente import GestorPaciente
from data.database import Database


class PacientesController:
    def __init__(self):
        self.gestor = GestorPaciente()

    def crear(self, nro, nombre, apellido, tel, nacimiento, direccion):
        """Crea un nuevo paciente y lo guarda en la BD"""
        if not nro or not nombre or not apellido:
            return False, "Faltan datos (id, nombre, apellido)"
        try:
            nro_int = int(nro)
        except ValueError:
            return False, "El ID debe ser un número"
        
        try:
            fecha_nac = date.fromisoformat(nacimiento)
        except Exception:
            return False, "Fecha de nacimiento inválida (YYYY-MM-DD)"
        
        # Guardar directamente en BD
        db = Database()
        if not db.conectar("127.0.0.1:3306/hospital_db"):
            return False, "No se pudo conectar a la BD"
        
        try:
            # Verificar si ya existe
            query_check = "SELECT id_paciente FROM Paciente WHERE id_paciente = %s"
            existe = db.obtener_registro(query_check, (nro_int,))
            
            if existe:
                db.desconectar()
                return False, f"Ya existe un paciente con ID {nro_int}"
            
            # Insertar paciente
            query = """
            INSERT INTO Paciente (id_paciente, nombre, apellido, telefono, fecha_nacimiento, direccion, activo)
            VALUES (%s, %s, %s, %s, %s, %s, 1)
            """
            
            resultado = db.ejecutar_consulta(query, (nro_int, nombre, apellido, tel, fecha_nac, direccion))
            db.desconectar()
            
            if resultado is not None and resultado > 0:
                return True, "Paciente creado exitosamente"
            else:
                return False, "No se pudo crear el paciente"
        
        except Exception as e:
            db.desconectar()
            return False, f"Error: {str(e)}"

    def modificar(self, id_paciente, nombre, apellido, telefono, nacimiento, direccion):
        """Modifica un paciente en la BD"""
        db = Database()
        if not db.conectar("127.0.0.1:3306/hospital_db"):
            return False, "No se pudo conectar a la BD"
        
        try:
            # Validar fecha
            try:
                fecha_nac = date.fromisoformat(nacimiento)
            except Exception:
                return False, "Fecha de nacimiento inválida (YYYY-MM-DD)"
            
            query = """
            UPDATE Paciente 
            SET nombre = %s, apellido = %s, telefono = %s, fecha_nacimiento = %s, direccion = %s
            WHERE id_paciente = %s
            """
            
            params = (nombre, apellido, telefono, fecha_nac, direccion, int(id_paciente))
            resultado = db.ejecutar_consulta(query, params)
            
            db.desconectar()
            
            if resultado is not None and resultado > 0:
                return True, "Paciente modificado exitosamente"
            else:
                return False, "No se pudo modificar el paciente"
        
        except Exception as e:
            db.desconectar()
            return False, f"Error: {str(e)}"

    def dar_de_baja(self, id_paciente):
        """Da de baja un paciente en la BD"""
        db = Database()
        if not db.conectar("127.0.0.1:3306/hospital_db"):
            return False, "No se pudo conectar a la BD"
        
        try:
            # Verificar que el paciente existe
            query_check = "SELECT id_paciente, nombre, apellido FROM Paciente WHERE id_paciente = %s"
            paciente = db.obtener_registro(query_check, (int(id_paciente),))
            
            if not paciente:
                return False, f"No se encontró paciente con ID {id_paciente}"
            
            # Actualizar activo a 0
            query = "UPDATE Paciente SET activo = 0 WHERE id_paciente = %s"
            resultado = db.ejecutar_consulta(query, (int(id_paciente),))
            
            db.desconectar()
            
            if resultado is not None and resultado > 0:
                return True, f"Paciente {paciente['nombre']} {paciente['apellido']} dado de baja"
            else:
                return False, "No se pudo dar de baja al paciente"
        
        except Exception as e:
            db.desconectar()
            return False, f"Error: {str(e)}"

    def listar(self):
        """Lista todos los pacientes de la BD"""
        db = Database()
        if not db.conectar("127.0.0.1:3306/hospital_db"):
            return []
        
        try:
            query = "SELECT id_paciente, nombre, apellido, telefono, fecha_nacimiento, direccion FROM Paciente WHERE activo = 1 ORDER BY nombre, apellido"
            pacientes = db.obtener_registros(query)
            db.desconectar()
            
            res = []
            if pacientes:
                for p in pacientes:
                    res.append({
                        "id": p["id_paciente"],
                        "nombre": p["nombre"],
                        "apellido": p["apellido"],
                        "telefono": p["telefono"],
                        "nacimiento": str(p["fecha_nacimiento"]),
                        "direccion": p["direccion"]
                    })
            return res
        except Exception as e:
            print(f"[ERROR] Error al listar pacientes: {str(e)}")
            db.desconectar()
            return []

    def obtener_pacientes(self):
        """Obtiene la lista de todos los pacientes"""
        db = Database()
        if not db.conectar("127.0.0.1:3306/hospital_db"):
            return []
        
        try:
            query = "SELECT id_paciente, nombre, apellido, telefono, fecha_nacimiento, direccion FROM Paciente WHERE activo = 1 ORDER BY nombre, apellido"
            pacientes = db.obtener_registros(query)
            db.desconectar()
            
            res = []
            if pacientes:
                for p in pacientes:
                    res.append({
                        "id": p["id_paciente"],
                        "nombre": p["nombre"],
                        "apellido": p["apellido"],
                        "telefono": p["telefono"],
                        "nacimiento": str(p["fecha_nacimiento"]),
                        "direccion": p["direccion"]
                    })
            return res
        except Exception as e:
            print(f"[ERROR] Error al obtener pacientes: {str(e)}")
            db.desconectar()
            return []

    def obtener_historial(self, id_paciente):
        """Obtiene el historial clínico de un paciente"""
        db = Database()
        if not db.conectar("127.0.0.1:3306/hospital_db"):
            return []
        
        try:
            id_pac = int(id_paciente)
            
            # Query según estructura real de la BD
            query = """
            SELECT 
                h.id_historial,
                h.diagnostico,
                h.tratamiento,
                h.notas,
                h.observaciones,
                h.fecha_registro,
                t.fecha,
                t.hora_inicio,
                CONCAT(m.nombre, ' ', m.apellido) as medico
            FROM Historial_clinico h
            JOIN Turno t ON h.id_turno = t.id_turno
            JOIN Medico m ON t.matricula = m.matricula
            WHERE h.id_paciente = %s
            ORDER BY h.fecha_registro DESC
            """
            
            historiales = db.obtener_registros(query, (id_pac,))
            db.desconectar()
            
            return historiales if historiales else []
        
        except Exception as e:
            print(f"[ERROR] Error al obtener historial: {str(e)}")
            import traceback
            traceback.print_exc()
            db.desconectar()
            return []
    
    def dar_de_baja_paciente(self, id_paciente):
        """Da de baja un paciente (alias para usar desde vista)"""
        return self.dar_de_baja(id_paciente)
