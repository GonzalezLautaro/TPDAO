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
        """Crea un nuevo paciente"""
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
        
        ok = self.gestor.alta_paciente(nro_int, nombre, apellido, tel, fecha_nac, direccion)
        return (True, "Paciente creado") if ok else (False, "No se pudo crear")

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
