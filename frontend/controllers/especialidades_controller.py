import sys, os
from typing import List, Dict, Tuple

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if BASE not in sys.path:
    sys.path.insert(0, BASE)

from data.database import Database


class EspecialidadesController:
    def __init__(self):
        pass

    def crear(self, id_especialidad, nombre, descripcion):
        """Crea una nueva especialidad"""
        if not id_especialidad or not nombre or not descripcion:
            return False, "Faltan datos obligatorios"
        
        try:
            id_int = int(id_especialidad)
        except ValueError:
            return False, "El ID debe ser un número"
        
        db = Database()
        if not db.conectar("127.0.0.1:3306/hospital_db"):
            return False, "No se pudo conectar a la BD"
        
        try:
            # Verificar que no exista una especialidad con el mismo ID
            query_check = "SELECT id_especialidad FROM Especialidad WHERE id_especialidad = %s"
            existe = db.obtener_registro(query_check, (id_int,))
            
            if existe:
                db.desconectar()
                return False, f"Ya existe una especialidad con ID {id_int}"
            
            # Insertar
            query = """
            INSERT INTO Especialidad (id_especialidad, nombre, descripcion)
            VALUES (%s, %s, %s)
            """
            
            resultado = db.ejecutar_consulta(query, (id_int, nombre, descripcion))
            db.desconectar()
            
            if resultado is not None and resultado > 0:
                return True, "Especialidad creada exitosamente"
            else:
                return False, "No se pudo crear la especialidad"
        
        except Exception as e:
            db.desconectar()
            return False, f"Error: {str(e)}"

    def modificar(self, id_especialidad, nombre, descripcion):
        """Modifica una especialidad"""
        db = Database()
        if not db.conectar("127.0.0.1:3306/hospital_db"):
            return False, "No se pudo conectar a la BD"
        
        try:
            # Verificar que existe
            query_check = "SELECT id_especialidad FROM Especialidad WHERE id_especialidad = %s"
            existe = db.obtener_registro(query_check, (int(id_especialidad),))
            
            if not existe:
                db.desconectar()
                return False, f"No se encontró especialidad con ID {id_especialidad}"
            
            # Actualizar
            query = """
            UPDATE Especialidad 
            SET nombre = %s, descripcion = %s
            WHERE id_especialidad = %s
            """
            
            resultado = db.ejecutar_consulta(query, (nombre, descripcion, int(id_especialidad)))
            db.desconectar()
            
            if resultado is not None and resultado > 0:
                return True, "Especialidad modificada exitosamente"
            else:
                return False, "No se pudo modificar la especialidad"
        
        except Exception as e:
            db.desconectar()
            return False, f"Error: {str(e)}"

    def eliminar(self, id_especialidad):
        """Elimina una especialidad"""
        db = Database()
        if not db.conectar("127.0.0.1:3306/hospital_db"):
            return False, "No se pudo conectar a la BD"
        
        try:
            # Verificar que existe
            query_check = "SELECT id_especialidad FROM Especialidad WHERE id_especialidad = %s"
            existe = db.obtener_registro(query_check, (int(id_especialidad),))
            
            if not existe:
                db.desconectar()
                return False, f"No se encontró especialidad con ID {id_especialidad}"
            
            # Verificar si tiene médicos asignados
            query_medicos = "SELECT COUNT(*) as total FROM Medico_especialidad WHERE id_especialidad = %s"
            resultado_medicos = db.obtener_registro(query_medicos, (int(id_especialidad),))
            
            if resultado_medicos and resultado_medicos['total'] > 0:
                db.desconectar()
                return False, f"No se puede eliminar. Hay {resultado_medicos['total']} médico(s) asignado(s)"
            
            # Eliminar
            query = "DELETE FROM Especialidad WHERE id_especialidad = %s"
            resultado = db.ejecutar_consulta(query, (int(id_especialidad),))
            db.desconectar()
            
            if resultado is not None and resultado > 0:
                return True, "Especialidad eliminada exitosamente"
            else:
                return False, "No se pudo eliminar la especialidad"
        
        except Exception as e:
            db.desconectar()
            return False, f"Error: {str(e)}"

    def listar(self) -> List[Dict]:
        """Lista todas las especialidades de la BD"""
        db = Database()
        if not db.conectar("127.0.0.1:3306/hospital_db"):
            return []
        
        try:
            query = "SELECT id_especialidad, nombre, descripcion FROM Especialidad ORDER BY nombre"
            especialidades = db.obtener_registros(query)
            db.desconectar()
            
            res = []
            if especialidades:
                for e in especialidades:
                    res.append({
                        "id": e["id_especialidad"],
                        "nombre": e["nombre"],
                        "descripcion": e["descripcion"]
                    })
            return res
        except Exception as e:
            print(f"[ERROR] Error al listar especialidades: {str(e)}")
            db.desconectar()
            return []
