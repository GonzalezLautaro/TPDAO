# -*- coding: utf-8 -*-
"""
Ejemplo de uso del ABMC de Turnos con entrada interactiva y almacenamiento en BD
"""

from datetime import date, time
import sys
import os

# Agregar el directorio padre al path para importar módulos
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from gestor_turno import GestorTurno
from data.database import Database


def limpiar_pantalla():
    """Limpia la pantalla de la consola"""
    os.system('cls' if os.name == 'nt' else 'clear')


def mostrar_menu():
    """Muestra el menú principal"""
    print("\n" + "=" * 60)
    print("SISTEMA ABMC DE TURNOS")
    print("=" * 60)
    print("\n1. Crear nuevos turnos")
    print("2. Listar turnos (en memoria)")
    print("3. Listar turnos de la base de datos")
    print("4. Guardar turnos en base de datos")
    print("5. Consultar turnos por médico")
    print("6. Consultar turnos por paciente")
    print("7. Consultar turnos por fecha")
    print("8. Eliminar turno")
    print("9. Salir")
    print("\n" + "-" * 60)


def cargar_medicos_bd() -> list:
    """Carga los médicos de la base de datos"""
    db = Database()
    if not db.conectar("127.0.0.1:3306/hospital_db"):
        print("[ERROR] No se pudo conectar a la base de datos")
        return []
    
    try:
        medicos = db.obtener_registros("SELECT matricula, nombre, apellido FROM Medico WHERE activo = TRUE")
        db.desconectar()
        return medicos
    except Exception as e:
        print(f"[ERROR] Error al cargar médicos: {str(e)}")
        db.desconectar()
        return []


def cargar_pacientes_bd() -> list:
    """Carga los pacientes de la base de datos"""
    db = Database()
    if not db.conectar("127.0.0.1:3306/hospital_db"):
        print("[ERROR] No se pudo conectar a la base de datos")
        return []
    
    try:
        pacientes = db.obtener_registros("SELECT id_paciente, nombre, apellido FROM Paciente WHERE activo = TRUE")
        db.desconectar()
        return pacientes
    except Exception as e:
        print(f"[ERROR] Error al cargar pacientes: {str(e)}")
        db.desconectar()
        return []


def cargar_consultorios_bd() -> list:
    """Carga los consultorios de la base de datos"""
    db = Database()
    if not db.conectar("127.0.0.1:3306/hospital_db"):
        print("[ERROR] No se pudo conectar a la base de datos")
        return []
    
    try:
        consultorios = db.obtener_registros("SELECT id_consultorio, numero FROM Consultorio")
        db.desconectar()
        return consultorios
    except Exception as e:
        print(f"[ERROR] Error al cargar consultorios: {str(e)}")
        db.desconectar()
        return []


def cargar_agendas_medico_bd(matricula: int) -> list:
    """Carga las agendas de un médico desde la base de datos"""
    db = Database()
    if not db.conectar("127.0.0.1:3306/hospital_db"):
        print("[ERROR] No se pudo conectar a la base de datos")
        return []
    
    try:
        query = """
        SELECT a.id_agenda, a.dia_semana, a.hora_inicio, a.hora_fin, 
               c.id_consultorio, c.numero as consultorio_numero
        FROM Agenda a
        JOIN Consultorio c ON a.id_consultorio = c.id_consultorio
        WHERE a.matricula = %s AND a.activa = TRUE
        ORDER BY a.dia_semana, a.hora_inicio
        """
        
        agendas = db.obtener_registros(query, (matricula,))
        db.desconectar()
        return agendas
    except Exception as e:
        print(f"[ERROR] Error al cargar agendas: {str(e)}")
        db.desconectar()
        return []


def obtener_dia_semana(fecha: date) -> str:
    """Obtiene el día de la semana en español"""
    dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    return dias[fecha.weekday()]


def seleccionar_medico() -> dict:
    """Permite seleccionar un médico"""
    medicos = cargar_medicos_bd()
    
    if not medicos:
        print("[ERROR] No hay médicos disponibles")
        return None
    
    print("\nMédicos disponibles:")
    for i, medico in enumerate(medicos, 1):
        print(f"   {i}. {medico['nombre']} {medico['apellido']} (Mat: {medico['matricula']})")
    
    while True:
        try:
            opcion = int(input("\nSelecciona un médico (número): ")) - 1
            if 0 <= opcion < len(medicos):
                return medicos[opcion]
            else:
                print("[ERROR] Opción no válida")
        except ValueError:
            print("[ERROR] Ingresa un número válido")


def seleccionar_paciente() -> dict:
    """Permite seleccionar un paciente"""
    pacientes = cargar_pacientes_bd()
    
    if not pacientes:
        print("[ERROR] No hay pacientes disponibles")
        return None
    
    print("\nPacientes disponibles:")
    for i, paciente in enumerate(pacientes, 1):
        print(f"   {i}. {paciente['nombre']} {paciente['apellido']} (ID: {paciente['id_paciente']})")
    
    while True:
        try:
            opcion = int(input("\nSelecciona un paciente (número): ")) - 1
            if 0 <= opcion < len(pacientes):
                return pacientes[opcion]
            else:
                print("[ERROR] Opción no válida")
        except ValueError:
            print("[ERROR] Ingresa un número válido")


def seleccionar_consultorio() -> dict:
    """Permite seleccionar un consultorio"""
    consultorios = cargar_consultorios_bd()
    
    if not consultorios:
        print("[ERROR] No hay consultorios disponibles")
        return None
    
    print("\nConsultorios disponibles:")
    for i, consultorio in enumerate(consultorios, 1):
        print(f"   {i}. Consultorio #{consultorio['numero']}")
    
    while True:
        try:
            opcion = int(input("\nSelecciona un consultorio (número): ")) - 1
            if 0 <= opcion < len(consultorios):
                return consultorios[opcion]
            else:
                print("[ERROR] Opción no válida")
        except ValueError:
            print("[ERROR] Ingresa un número válido")


def seleccionar_agenda_medico(medico_dict: dict) -> dict:
    """Permite seleccionar una agenda del médico"""
    matricula = medico_dict['matricula']
    agendas = cargar_agendas_medico_bd(matricula)
    
    if not agendas:
        print(f"[ERROR] El médico {medico_dict['nombre']} no tiene agendas disponibles")
        return None
    
    print(f"\nAgendas disponibles para {medico_dict['nombre']} {medico_dict['apellido']}:")
    for i, agenda in enumerate(agendas, 1):
        print(f"   {i}. {agenda['dia_semana']} ({agenda['hora_inicio']} - {agenda['hora_fin']}) - Consultorio #{agenda['consultorio_numero']}")
    
    while True:
        try:
            opcion = int(input("\nSelecciona una agenda (número): ")) - 1
            if 0 <= opcion < len(agendas):
                return agendas[opcion]
            else:
                print("[ERROR] Opción no válida")
        except ValueError:
            print("[ERROR] Ingresa un número válido")


def _timedelta_a_time(td) -> time:
    """Convierte timedelta a time"""
    if isinstance(td, time):
        return td
    total_seconds = int(td.total_seconds())
    return time(total_seconds // 3600, (total_seconds % 3600) // 60)


def validar_turno_en_agenda(fecha: date, hora: time, agenda: dict) -> bool:
    """Valida que el turno esté dentro del horario de la agenda"""
    dia_turno = obtener_dia_semana(fecha)
    
    # Verificar que sea el mismo día de la semana
    if dia_turno != agenda['dia_semana']:
        print(f"[ERROR] El turno es {dia_turno} pero la agenda es {agenda['dia_semana']}")
        return False
    
    # Convertir timedelta a time si es necesario
    hora_inicio = _timedelta_a_time(agenda['hora_inicio'])
    hora_fin = _timedelta_a_time(agenda['hora_fin'])
    
    # Verificar que esté dentro del horario
    if not (hora_inicio <= hora < hora_fin):
        print(f"[ERROR] La hora {hora} no está dentro del horario {hora_inicio} - {hora_fin}")
        return False
    
    return True


def ingreso_datos_turno() -> dict:
    """Solicita los datos de un turno"""
    print("\n--- Datos del Turno ---")
    
    # Fecha
    while True:
        try:
            fecha_str = input("Fecha del turno (YYYY-MM-DD): ").strip()
            fecha = date.fromisoformat(fecha_str)
            break
        except ValueError:
            print("[ERROR] Formato de fecha inválido. Usa YYYY-MM-DD")
    
    # Hora
    while True:
        try:
            hora_str = input("Hora del turno (HH:MM): ").strip()
            hora = time.fromisoformat(hora_str)
            break
        except ValueError:
            print("[ERROR] Formato de hora inválido. Usa HH:MM")
    
    # Observaciones
    observaciones = input("Observaciones (opcional): ").strip()
    
    return {
        "fecha": fecha,
        "hora": hora,
        "observaciones": observaciones
    }


def ingreso_datos_turno_con_agenda(agenda: dict) -> dict:
    """Solicita los datos de un turno validando contra la agenda"""
    print("\n--- Datos del Turno ---")
    print(f"Agenda: {agenda['dia_semana']} ({agenda['hora_inicio']} - {agenda['hora_fin']}) - Consultorio #{agenda['consultorio_numero']}")
    
    # Fecha
    while True:
        try:
            fecha_str = input(f"Fecha del turno (YYYY-MM-DD) [{obtener_dia_semana(date.today())} será {date.today()}]: ").strip()
            if not fecha_str:
                fecha = date.today()
            else:
                fecha = date.fromisoformat(fecha_str)
            
            # Validar que sea el día correcto de la semana
            if obtener_dia_semana(fecha) != agenda['dia_semana']:
                print(f"[ERROR] La fecha debe ser un {agenda['dia_semana']}")
                continue
            
            break
        except ValueError:
            print("[ERROR] Formato de fecha inválido. Usa YYYY-MM-DD")
    
    # Hora
    while True:
        try:
            hora_str = input(f"Hora del turno (HH:MM) [Entre {agenda['hora_inicio']} y {agenda['hora_fin']}]: ").strip()
            hora = time.fromisoformat(hora_str)
            
            # Validar que esté dentro de la agenda
            if not validar_turno_en_agenda(fecha, hora, agenda):
                continue
            
            break
        except ValueError:
            print("[ERROR] Formato de hora inválido. Usa HH:MM")
    
    # Observaciones
    observaciones = input("Observaciones (opcional): ").strip()
    
    return {
        "fecha": fecha,
        "hora": hora,
        "observaciones": observaciones,
        "id_agenda": agenda['id_agenda'],
        "id_consultorio": agenda['id_consultorio']
    }


def crear_turnos_interactivo(gestor: GestorTurno) -> bool:
    """Permite crear turnos de forma interactiva"""
    cantidad = 1
    turnos_creados = []
    
    while True:
        print(f"\n--- Turno #{cantidad} ---")
        
        # Seleccionar médico
        medico_dict = seleccionar_medico()
        if not medico_dict:
            break
        
        # Seleccionar paciente
        paciente_dict = seleccionar_paciente()
        if not paciente_dict:
            break
        
        # Seleccionar consultorio
        consultorio_dict = seleccionar_consultorio()
        if not consultorio_dict:
            break
        
        # Ingresar datos del turno
        datos = ingreso_datos_turno()
        
        # Crear objeto turno (temporal para demostración)
        # En una aplicación real, necesitaríamos los objetos Medico, Paciente, Consultorio
        print(f"\n[OK] Turno creado:")
        print(f"     Paciente: {paciente_dict['nombre']} {paciente_dict['apellido']}")
        print(f"     Médico: {medico_dict['nombre']} {medico_dict['apellido']}")
        print(f"     Consultorio: {consultorio_dict['numero']}")
        print(f"     Fecha: {datos['fecha']} a las {datos['hora']}")
        
        turnos_creados.append({
            "medico": medico_dict,
            "paciente": paciente_dict,
            "consultorio": consultorio_dict,
            "fecha": datos['fecha'],
            "hora": datos['hora'],
            "observaciones": datos['observaciones']
        })
        
        opcion = input("\n¿Crear otro turno? (s/n): ")

        if opcion != 's':
            break
        cantidad += 1
    
    if turnos_creados:
        print(f"\n[OK] Se crearon {len(turnos_creados)} turno(s) exitosamente")
        return True
    else:
        print("\n[ERROR] No se crearon turnos")
        return False


def crear_turnos_interactivo_con_agenda(gestor: GestorTurno) -> bool:
    """Permite crear turnos de forma interactiva usando agendas"""
    cantidad = 1
    turnos_creados = []
    
    while True:
        print(f"\n--- Turno #{cantidad} ---")
        
        # Seleccionar médico
        medico_dict = seleccionar_medico()
        if not medico_dict:
            break
        
        # Cargar y seleccionar agenda del médico
        agenda = seleccionar_agenda_medico(medico_dict)
        if not agenda:
            break
        
        # Seleccionar paciente
        paciente_dict = seleccionar_paciente()
        if not paciente_dict:
            break
        
        # Ingresar datos del turno validando contra la agenda
        datos = ingreso_datos_turno_con_agenda(agenda)
        
        print(f"\n[OK] Turno creado:")
        print(f"     Paciente: {paciente_dict['nombre']} {paciente_dict['apellido']}")
        print(f"     Médico: {medico_dict['nombre']} {medico_dict['apellido']}")
        print(f"     Consultorio: {datos['id_consultorio']}")
        print(f"     Fecha: {datos['fecha']} ({obtener_dia_semana(datos['fecha'])}) a las {datos['hora']}")
        print(f"     Agenda: {agenda['dia_semana']} ({agenda['hora_inicio']} - {agenda['hora_fin']})")
        
        turnos_creados.append({
            "medico": medico_dict,
            "paciente": paciente_dict,
            "consultorio": datos['id_consultorio'],
            "fecha": datos['fecha'],
            "hora": datos['hora'],
            "observaciones": datos['observaciones'],
            "id_agenda": datos['id_agenda']
        })
        
        opcion = input("\n¿Crear otro turno? (s/n): ").strip().lower()
        if opcion != 's':
            break
        cantidad += 1
    
    if turnos_creados:
        print(f"\n[OK] Se crearon {len(turnos_creados)} turno(s) exitosamente")
        return turnos_creados
    else:
        print("\n[ERROR] No se crearon turnos")
        return []


def guardar_turnos_en_bd(turnos: list) -> bool:
    """Guarda los turnos en la base de datos"""
    if not turnos:
        print("[ERROR] No hay turnos para guardar")
        return False
    
    print("\n--- Conectando a Base de Datos ---")
    
    db = Database()
    
    if not db.conectar("127.0.0.1:3306/hospital_db"):
        print("[ERROR] No se pudo conectar a la base de datos")
        return False
    
    guardados = 0
    
    for turno in turnos:
        try:
            query = """
            INSERT INTO Turno (id_paciente, matricula, id_consultorio, fecha, hora, estado, observaciones, id_agenda)
            VALUES (%s, %s, %s, %s, %s, 'Programado', %s, %s)
            """
            
            params = (
                turno['paciente']['id_paciente'],
                turno['medico']['matricula'],
                turno['consultorio'],
                turno['fecha'],
                turno['hora'],
                turno['observaciones'],
                turno['id_agenda']
            )
            
            resultado = db.ejecutar_consulta(query, params)
            
            if resultado is not None:
                guardados += 1
                print(f"[OK] Turno guardado - {turno['paciente']['nombre']} con Dr. {turno['medico']['nombre']}")
        
        except Exception as e:
            print(f"[ERROR] Error al guardar turno: {str(e)}")
    
    db.desconectar()
    
    if guardados > 0:
        print(f"\n[OK] {guardados} turno(s) guardado(s) en la base de datos")
        return True
    else:
        print("\n[ERROR] No se pudo guardar ningún turno")
        return False


def listar_turnos_bd() -> bool:
    """Lista todos los turnos de la base de datos"""
    print("\n--- Conectando a Base de Datos ---")
    
    db = Database()
    
    if not db.conectar("127.0.0.1:3306/hospital_db"):
        print("[ERROR] No se pudo conectar a la base de datos")
        return False
    
    try:
        query = """
        SELECT t.id_turno, p.nombre as paciente_nombre, p.apellido as paciente_apellido,
               m.nombre as medico_nombre, m.apellido as medico_apellido,
               c.numero as consultorio, t.fecha, t.hora, t.estado, t.observaciones
        FROM Turno t
        JOIN Paciente p ON t.id_paciente = p.id_paciente
        JOIN Medico m ON t.matricula = m.matricula
        JOIN Consultorio c ON t.id_consultorio = c.id_consultorio
        ORDER BY t.fecha, t.hora
        """
        
        turnos = db.obtener_registros(query)
        
        if turnos:
            print(f"\n[OK] Se encontraron {len(turnos)} turno(s) en la base de datos:\n")
            for turno in turnos:
                print(f"   Turno #: {turno['id_turno']}")
                print(f"   Paciente: {turno['paciente_nombre']} {turno['paciente_apellido']}")
                print(f"   Médico: {turno['medico_nombre']} {turno['medico_apellido']}")
                print(f"   Consultorio: {turno['consultorio']}")
                print(f"   Fecha: {turno['fecha']} a las {turno['hora']}")
                print(f"   Estado: {turno['estado']}")
                if turno['observaciones']:
                    print(f"   Observaciones: {turno['observaciones']}")
                print()
            return True
        else:
            print("\n[INFO] No hay turnos registrados en la base de datos")
            return False
    
    except Exception as e:
        print(f"[ERROR] Error al listar turnos: {str(e)}")
        return False
    
    finally:
        db.desconectar()


def main():
    gestor = GestorTurno()
    turnos_temporales = []
    
    while True:
        limpiar_pantalla()
        mostrar_menu()
        
        opcion = input("Selecciona una opción: ").strip()
        
        if opcion == "1":
            limpiar_pantalla()
            print("=" * 60)
            print("CREAR NUEVOS TURNOS")
            print("=" * 60)
            turnos_creados = crear_turnos_interactivo_con_agenda(gestor)
            if turnos_creados:
                turnos_temporales = turnos_creados
            input("\n[ENTER] para continuar...")
        
        elif opcion == "2":
            limpiar_pantalla()
            print("=" * 60)
            print("TURNOS REGISTRADOS (En Memoria)")
            print("=" * 60)
            print("[INFO] No implementado para este ejemplo")
            input("\n[ENTER] para continuar...")
        
        elif opcion == "3":
            limpiar_pantalla()
            print("=" * 60)
            print("TURNOS EN BASE DE DATOS")
            print("=" * 60)
            listar_turnos_bd()
            input("\n[ENTER] para continuar...")
        
        elif opcion == "4":
            limpiar_pantalla()
            print("=" * 60)
            print("GUARDAR EN BASE DE DATOS")
            print("=" * 60)
            guardar_turnos_en_bd(turnos_temporales)
            turnos_temporales = []
            input("\n[ENTER] para continuar...")
        
        elif opcion == "5":
            limpiar_pantalla()
            print("=" * 60)
            print("CONSULTAR TURNOS POR MÉDICO")
            print("=" * 60)
            matricula = input("Ingresa matrícula del médico: ").strip()
            try:
                gestor.consultar_turnos_medico_bd(int(matricula))
            except ValueError:
                print("[ERROR] Matrícula inválida")
            input("\n[ENTER] para continuar...")
        
        elif opcion == "6":
            limpiar_pantalla()
            print("=" * 60)
            print("CONSULTAR TURNOS POR PACIENTE")
            print("=" * 60)
            id_paciente = input("Ingresa ID del paciente: ").strip()
            try:
                gestor.consultar_turnos_paciente_bd(int(id_paciente))
            except ValueError:
                print("[ERROR] ID inválido")
            input("\n[ENTER] para continuar...")
        
        elif opcion == "7":
            limpiar_pantalla()
            print("=" * 60)
            print("CONSULTAR TURNOS POR FECHA")
            print("=" * 60)
            fecha_str = input("Ingresa fecha (YYYY-MM-DD): ").strip()
            try:
                fecha = date.fromisoformat(fecha_str)
                gestor.consultar_turnos_fecha_bd(fecha)
            except ValueError:
                print("[ERROR] Formato de fecha inválido")
            input("\n[ENTER] para continuar...")
        
        elif opcion == "8":
            limpiar_pantalla()
            print("=" * 60)
            print("ELIMINAR TURNO")
            print("=" * 60)
            id_turno = input("Ingresa ID del turno a eliminar: ").strip()
            try:
                gestor.baja_turno_bd(int(id_turno))
            except ValueError:
                print("[ERROR] ID inválido")
            input("\n[ENTER] para continuar...")
        
        elif opcion == "9":
            print("\n[OK] ¡Hasta luego!")            
            break
        
        else:
            print("[ERROR] Opción no válida")
            input("\n[ENTER] para continuar...")


if __name__ == "__main__":
    main()
