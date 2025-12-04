from datetime import date, datetime, timedelta, time
import sys, os

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if BASE not in sys.path:
    sys.path.insert(0, BASE)

from gestores.gestor_medico import GestorMedico
from data.database import Database


class MedicosController:
    def __init__(self):
        self.gestor = GestorMedico()

    def crear(self, matricula, nombre, apellido, tel, email, fecha_alta, especialidades_ids=None, agenda_data=None):
        """Crea un nuevo médico, asigna especialidades, crea agenda y genera turnos"""
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
        
        db = Database()
        if not db.conectar("127.0.0.1:3306/hospital_db"):
            return False, "No se pudo conectar a la base de datos"
        
        try:
            # 1. Insertar médico
            query = """
            INSERT INTO Medico (matricula, nombre, apellido, telefono, email, fecha_ingreso, activo)
            VALUES (%s, %s, %s, %s, %s, %s, 1)
            """
            resultado = db.ejecutar_consulta(query, (matricula_int, nombre, apellido, tel, email, fecha))
            
            if resultado is None or resultado == 0:
                db.desconectar()
                return False, "Error al guardar médico en BD"
            
            # 2. Asignar especialidades
            if especialidades_ids:
                for esp_id in especialidades_ids:
                    try:
                        query_esp = """
                        INSERT INTO Medico_especialidad (matricula, id_especialidad)
                        VALUES (%s, %s)
                        """
                        db.ejecutar_consulta(query_esp, (matricula_int, int(esp_id)))
                    except Exception as e:
                        print(f"[WARNING] Error al asignar especialidad {esp_id}: {str(e)}")
            
            # 3. Crear agenda y generar turnos
            if agenda_data:
                for agenda_item in agenda_data:
                    try:
                        # Insertar agenda
                        query_agenda = """
                        INSERT INTO Agenda (matricula, id_consultorio, dia_semana, hora_inicio, hora_fin, activa)
                        VALUES (%s, %s, %s, %s, %s, TRUE)
                        """
                        db.ejecutar_consulta(query_agenda, (
                            matricula_int,
                            agenda_item['id_consultorio'],
                            agenda_item['dia'],
                            agenda_item['hora_inicio'],
                            agenda_item['hora_fin']
                        ))
                        
                        id_agenda = db.get_last_insert_id()
                        
                        # Generar turnos para los próximos 30 días
                        self._generar_turnos_para_agenda(
                            db, id_agenda, matricula_int, 
                            agenda_item['id_consultorio'],
                            agenda_item['dia'],
                            agenda_item['hora_inicio'],
                            agenda_item['hora_fin']
                        )
                        
                    except Exception as e:
                        print(f"[WARNING] Error al crear agenda para {agenda_item['dia']}: {str(e)}")
            
            db.desconectar()
            return True, "Médico creado exitosamente"
        
        except Exception as e:
            db.desconectar()
            return False, f"Error: {str(e)}"
    
    def _generar_turnos_para_agenda(self, db, id_agenda, matricula, id_consultorio, dia_semana, hora_inicio, hora_fin):
        """Genera turnos de 30 minutos para una agenda específica (próximos 30 días)"""
        dias_semana_map = {
            "Lunes": 0, "Martes": 1, "Miércoles": 2, "Jueves": 3,
            "Viernes": 4, "Sábado": 5, "Domingo": 6
        }
        
        numero_dia = dias_semana_map.get(dia_semana)
        if numero_dia is None:
            return
        
        fecha_actual = date.today()
        fecha_fin = fecha_actual + timedelta(days=30)
        
        while fecha_actual < fecha_fin:
            if fecha_actual.weekday() == numero_dia:
                # Generar turnos para este día
                hora_actual = datetime.combine(fecha_actual, hora_inicio)
                hora_fin_dt = datetime.combine(fecha_actual, hora_fin)
                
                while hora_actual < hora_fin_dt:
                    hora_inicio_turno = hora_actual.time()
                    hora_fin_turno = (hora_actual + timedelta(minutes=30)).time()
                    
                    if hora_fin_turno > hora_fin:
                        break
                    
                    try:
                        query = """
                        INSERT INTO Turno (matricula, id_consultorio, id_agenda, id_especialidad, 
                                          fecha, hora_inicio, hora_fin, estado)
                        VALUES (%s, %s, %s, NULL, %s, %s, %s, 'Libre')
                        """
                        db.ejecutar_consulta(query, (
                            matricula, id_consultorio, id_agenda, 
                            fecha_actual, hora_inicio_turno, hora_fin_turno
                        ))
                    except Exception as e:
                        print(f"[WARNING] Error al crear turno: {str(e)}")
                    
                    hora_actual += timedelta(minutes=30)
            
            fecha_actual += timedelta(days=1)

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
