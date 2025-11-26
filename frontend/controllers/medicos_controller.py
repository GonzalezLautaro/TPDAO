from datetime import date
import sys, os

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if BASE not in sys.path:
    sys.path.insert(0, BASE)

from gestores.gestor_medico import GestorMedico
from data.database import Database


class MedicosController:
    def __init__(self):
        self.gestor = GestorMedico()

    def crear(self, matricula, nombre, apellido, tel, email, fecha_alta):
        """Crea un nuevo médico"""
        if not matricula or not nombre or not apellido or not email:
            return False, "Faltan datos obligatorios"
        
        try:
            matricula_int = int(matricula)
        except ValueError:
            return False, "La matrícula debe ser un número"
        
        try:
            fecha = date.fromisoformat(fecha_alta)
        except Exception:
            return False, "Fecha inválida (YYYY-MM-DD)"
        
        ok = self.gestor.alta_medico(matricula_int, nombre, apellido, tel, email, fecha)
        return (True, "Médico creado") if ok else (False, "No se pudo crear médico")

    def modificar(self, matricula, nombre, apellido, telefono, email, fecha_alta):
        """Modifica un médico en la BD"""
        db = Database()
        if not db.conectar("127.0.0.1:3306/hospital_db"):
            return False, "No se pudo conectar a la BD"
        
        try:
            # Validar fecha
            try:
                fecha_alta_obj = date.fromisoformat(fecha_alta)
            except Exception:
                return False, "Fecha inválida (YYYY-MM-DD)"
            
            query = """
            UPDATE Medico 
            SET nombre = %s, apellido = %s, telefono = %s, email = %s, fecha_ingreso = %s
            WHERE matricula = %s
            """
            
            params = (nombre, apellido, telefono, email, fecha_alta_obj, int(matricula))
            resultado = db.ejecutar_consulta(query, params)
            
            db.desconectar()
            
            if resultado is not None and resultado > 0:
                return True, "Médico modificado exitosamente"
            else:
                return False, "No se pudo modificar el médico"
        
        except Exception as e:
            db.desconectar()
            return False, f"Error: {str(e)}"

    def dar_de_baja(self, matricula):
        """Da de baja un médico en la BD"""
        db = Database()
        if not db.conectar("127.0.0.1:3306/hospital_db"):
            return False, "No se pudo conectar a la BD"
        
        try:
            # Verificar que el médico existe
            query_check = "SELECT matricula, nombre, apellido FROM Medico WHERE matricula = %s"
            medico = db.obtener_registro(query_check, (int(matricula),))
            
            if not medico:
                return False, f"No se encontró médico con matrícula {matricula}"
            
            # Actualizar activo a 0
            query = "UPDATE Medico SET activo = 0 WHERE matricula = %s"
            resultado = db.ejecutar_consulta(query, (int(matricula),))
            
            db.desconectar()
            
            if resultado is not None and resultado > 0:
                return True, f"Médico {medico['nombre']} {medico['apellido']} dado de baja"
            else:
                return False, "No se pudo dar de baja al médico"
        
        except Exception as e:
            db.desconectar()
            return False, f"Error: {str(e)}"

    def listar(self):
        """Lista todos los médicos de la BD"""
        db = Database()
        if not db.conectar("127.0.0.1:3306/hospital_db"):
            return []
        
        try:
            query = "SELECT matricula, nombre, apellido, telefono, email, fecha_ingreso FROM Medico WHERE activo = 1 ORDER BY nombre, apellido"
            medicos = db.obtener_registros(query)
            db.desconectar()
            
            res = []
            if medicos:
                for m in medicos:
                    res.append({
                        "matricula": m["matricula"],
                        "nombre": m["nombre"],
                        "apellido": m["apellido"],
                        "telefono": m["telefono"],
                        "email": m["email"],
                        "fecha_alta": str(m["fecha_ingreso"])
                    })
            return res
        except Exception as e:
            print(f"[ERROR] Error al listar médicos: {str(e)}")
            db.desconectar()
            return []
