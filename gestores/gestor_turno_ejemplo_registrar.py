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
    print("\n1. Registrar nuevo turno")
    print("2. Listar turnos (en memoria)")
    print("3. Listar turnos de la base de datos")
    print("4. Consultar turnos por médico")
    print("5. Consultar turnos por paciente")
    print("6. Consultar turnos por fecha")
    print("7. Cancelar turno")
    print("8. Salir")
    print("\n" + "-" * 60)


def cargar_medicos_bd() -> list:
    """Carga los médicos de la base de datos"""
    db = Database()
    if not db.conectar("127.0.0.1:3306/hospital_db"):
        print("[ERROR] No se pudo conectar a la base de datos")
        return []
    
    try:
        medicos = db.obtener_registros("SELECT matricula, nombre, apellido FROM Medico WHERE activo = TRUE ORDER BY nombre, apellido")
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
        pacientes = db.obtener_registros("SELECT id_paciente, nombre, apellido FROM Paciente WHERE activo = 1 ORDER BY nombre, apellido")
        db.desconectar()
        return pacientes
    except Exception as e:
        print(f"[ERROR] Error al cargar pacientes: {str(e)}")
        db.desconectar()
        return []


def cargar_turnos_libres_medico_bd(matricula: int) -> list:
    """Carga los turnos disponibles (Libre) de un médico desde la BD"""
    db = Database()
    if not db.conectar("127.0.0.1:3306/hospital_db"):
        print("[ERROR] No se pudo conectar a la base de datos")
        return []
    
    try:
        query = """
        SELECT t.id_turno, t.fecha, t.hora_inicio, t.hora_fin, t.id_consultorio,
               c.numero as consultorio_numero, t.estado
        FROM Turno t
        JOIN Consultorio c ON t.id_consultorio = c.id_consultorio
        WHERE t.matricula = %s AND t.estado = 'Libre' AND t.fecha >= CURDATE()
        ORDER BY t.fecha, t.hora_inicio
        LIMIT 20
        """
        
        turnos = db.obtener_registros(query, (matricula,))
        db.desconectar()
        return turnos
    except Exception as e:
        print(f"[ERROR] Error al cargar turnos disponibles: {str(e)}")
        db.desconectar()
        return []


def seleccionar_medico() -> dict:
    """Permite seleccionar un médico"""
    medicos = cargar_medicos_bd()
    
    if not medicos:
        print("[ERROR] No hay médicos disponibles")
        return None
    
    print("\nMédicos disponibles:")
    for i, medico in enumerate(medicos, 1):
        print(f"   {i}. Dr/Dra. {medico['nombre']} {medico['apellido']} (Mat: {medico['matricula']})")
    
    while True:
        try:
            opcion = int(input("\nSelecciona un médico (número): ")) - 1
            if 0 <= opcion < len(medicos):
                return medicos[opcion]
            else:
                print("[ERROR] Opción no válida")
        except ValueError:
            print("[ERROR] Ingresa un número válido")


def seleccionar_turno_disponible(medico_dict: dict) -> dict:
    """Permite seleccionar un turno disponible de un médico"""
    matricula = medico_dict['matricula']
    turnos = cargar_turnos_libres_medico_bd(matricula)
    
    if not turnos:
        print(f"\n[ERROR] No hay turnos disponibles para Dr/Dra. {medico_dict['nombre']} {medico_dict['apellido']}")
        return None
    
    print(f"\nTurnos disponibles para Dr/Dra. {medico_dict['nombre']} {medico_dict['apellido']}:")
    print("-" * 60)
    for i, turno in enumerate(turnos, 1):
        print(f"   {i}. {turno['fecha']} - {turno['hora_inicio']} a {turno['hora_fin']} (Consultorio #{turno['consultorio_numero']})")
    print("-" * 60)
    
    while True:
        try:
            opcion = int(input("\nSelecciona un turno (número): ")) - 1
            if 0 <= opcion < len(turnos):
                return turnos[opcion]
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


def registrar_turno_interactivo(gestor: GestorTurno) -> bool:
    """Permite registrar un nuevo turno de forma interactiva"""
    print("\n--- Registrar Nuevo Turno ---")
    
    # Paso 1: Seleccionar médico
    print("\n[PASO 1] Seleccionar Médico")
    medico_dict = seleccionar_medico()
    if not medico_dict:
        return False
    
    # Paso 2: Seleccionar turno disponible
    print("\n[PASO 2] Seleccionar Turno Disponible")
    turno_dict = seleccionar_turno_disponible(medico_dict)
    if not turno_dict:
        return False
    
    # Paso 3: Seleccionar paciente
    print("\n[PASO 3] Seleccionar Paciente")
    paciente_dict = seleccionar_paciente()
    if not paciente_dict:
        return False
    
    # Paso 4: Ingresar descripción/observaciones
    print("\n[PASO 4] Ingresar Descripción")
    observaciones = input("Descripción/Observaciones del turno (opcional): ").strip()
    
    # Paso 5: Confirmar datos
    print("\n" + "=" * 60)
    print("CONFIRMAR REGISTRO DE TURNO")
    print("=" * 60)
    print(f"Médico: Dr/Dra. {medico_dict['nombre']} {medico_dict['apellido']}")
    print(f"Paciente: {paciente_dict['nombre']} {paciente_dict['apellido']}")
    print(f"Fecha: {turno_dict['fecha']}")
    print(f"Hora: {turno_dict['hora_inicio']} - {turno_dict['hora_fin']}")
    print(f"Consultorio: #{turno_dict['consultorio_numero']}")
    if observaciones:
        print(f"Observaciones: {observaciones}")
    print("=" * 60)
    
    confirmacion = input("\n¿Confirmar registro del turno? (s/n): ").strip().lower()
    
    if confirmacion != 's':
        print("\n[INFO] Registro cancelado")
        return False
    
    # Paso 6: Guardar en la base de datos
    print("\n[PASO 5] Guardando en Base de Datos...")
    
    db = Database()
    if not db.conectar("127.0.0.1:3306/hospital_db"):
        print("[ERROR] No se pudo conectar a la base de datos")
        return False
    
    try:
        # Actualizar el turno: asignar paciente, cambiar estado a "Programado" y agregar observaciones
        query = """
        UPDATE Turno 
        SET id_paciente = %s, estado = 'Programado', observaciones = %s
        WHERE id_turno = %s AND estado = 'Libre'
        """
        
        params = (
            paciente_dict['id_paciente'],
            observaciones,
            turno_dict['id_turno']
        )
        
        resultado = db.ejecutar_consulta(query, params)
        
        if resultado is not None and resultado > 0:
            print("\n[OK] ¡Turno registrado exitosamente!")
            print(f"     ID Turno: {turno_dict['id_turno']}")
            print(f"     Paciente: {paciente_dict['nombre']} {paciente_dict['apellido']}")
            print(f"     Médico: Dr/Dra. {medico_dict['nombre']} {medico_dict['apellido']}")
            print(f"     Fecha y Hora: {turno_dict['fecha']} a las {turno_dict['hora_inicio']}")
            print(f"     Estado: PROGRAMADO")
            db.desconectar()
            return True
        else:
            print("\n[ERROR] No se pudo registrar el turno. El turno puede haber sido ocupado por otro usuario.")
            db.desconectar()
            return False
    
    except Exception as e:
        print(f"\n[ERROR] Error al registrar turno: {str(e)}")
        db.desconectar()
        return False


def listar_turnos_bd() -> bool:
    """Lista todos los turnos de la base de datos"""
    print("\n--- Turnos en Base de Datos ---")
    
    db = Database()
    
    if not db.conectar("127.0.0.1:3306/hospital_db"):
        print("[ERROR] No se pudo conectar a la base de datos")
        return False
    
    try:
        query = """
        SELECT t.id_turno, 
               CASE WHEN t.id_paciente IS NOT NULL 
                    THEN CONCAT(p.nombre, ' ', p.apellido)
                    ELSE '--- Libre ---'
               END as paciente,
               CONCAT(m.nombre, ' ', m.apellido) as medico,
               c.numero as consultorio, t.fecha, t.hora_inicio, t.hora_fin, t.estado
        FROM Turno t
        JOIN Medico m ON t.matricula = m.matricula
        LEFT JOIN Paciente p ON t.id_paciente = p.id_paciente
        JOIN Consultorio c ON t.id_consultorio = c.id_consultorio
        ORDER BY t.fecha, t.hora_inicio
        LIMIT 50
        """
        
        turnos = db.obtener_registros(query)
        
        if turnos:
            print(f"\n[OK] Se encontraron {len(turnos)} turno(s) en la base de datos:\n")
            print("-" * 100)
            print(f"{'ID':<5} {'Paciente':<25} {'Médico':<25} {'Consultorio':<12} {'Fecha':<12} {'Hora':<15} {'Estado':<15}")
            print("-" * 100)
            for turno in turnos:
                print(f"{turno['id_turno']:<5} {turno['paciente']:<25} {turno['medico']:<25} {turno['consultorio']:<12} {turno['fecha']:<12} {str(turno['hora_inicio']) + ' - ' + str(turno['hora_fin']):<15} {turno['estado']:<15}")
            print("-" * 100)
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
    
    while True:
        limpiar_pantalla()
        mostrar_menu()
        
        opcion = input("Selecciona una opción: ").strip()
        
        if opcion == "1":
            limpiar_pantalla()
            print("=" * 60)
            print("REGISTRAR NUEVO TURNO")
            print("=" * 60)
            registrar_turno_interactivo(gestor)
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
            print("CONSULTAR TURNOS POR MÉDICO")
            print("=" * 60)
            matricula = input("Ingresa matrícula del médico: ").strip()
            try:
                gestor.consultar_turnos_medico_bd(int(matricula))
            except ValueError:
                print("[ERROR] Matrícula inválida")
            input("\n[ENTER] para continuar...")
        
        elif opcion == "5":
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
        
        elif opcion == "6":
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
        
        elif opcion == "7":
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
        
        elif opcion == "8":
            print("\n[OK] ¡Hasta luego!")            
            break
        
        else:
            print("[ERROR] Opción no válida")
            input("\n[ENTER] para continuar...")


if __name__ == "__main__":
    main()
