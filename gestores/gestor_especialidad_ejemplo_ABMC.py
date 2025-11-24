# -*- coding: utf-8 -*-
"""
Ejemplo de uso del ABMC de Especialidades con entrada interactiva y almacenamiento en BD
"""

import sys
import os

# Agregar el directorio padre al path para importar módulos
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gestor_especialidad import GestorEspecialidad
from data.database import Database


def limpiar_pantalla():
    """Limpia la pantalla de la consola"""
    os.system('cls' if os.name == 'nt' else 'clear')


def mostrar_menu():
    """Muestra el menú principal"""
    print("\n" + "=" * 60)
    print("SISTEMA ABMC DE ESPECIALIDADES")
    print("=" * 60)
    print("\n1. Crear nuevas especialidades")
    print("2. Listar especialidades (en memoria)")
    print("3. Listar especialidades de la base de datos")
    print("4. Guardar especialidades en base de datos")
    print("5. Modificar especialidad")
    print("6. Eliminar especialidad")
    print("7. Salir")
    print("\n" + "-" * 60)


def ingreso_cantidad_especialidades() -> int:
    """Solicita la cantidad de especialidades a crear"""
    while True:
        try:
            cantidad = int(input("\n¿Cuántas especialidades deseas crear? "))
            if cantidad <= 0:
                print("[ERROR] La cantidad debe ser mayor a 0")
                continue
            return cantidad
        except ValueError:
            print("[ERROR] Ingresa un número válido")


def ingreso_datos_especialidad(numero: int) -> dict:
    """
    Solicita los datos de una especialidad
    
    Args:
        numero: Número de especialidad a ingresar
    
    Returns:
        Diccionario con los datos de la especialidad
    """
    print(f"\n--- Especialidad #{numero} ---")
    
    # ID de especialidad
    while True:
        try:
            nro_especialidad = int(input("ID de especialidad: ").strip())
            if nro_especialidad <= 0:
                print("[ERROR] El ID debe ser un número positivo")
                continue
            break
        except ValueError:
            print("[ERROR] El ID debe ser un número válido")
    
    # Nombre
    while True:
        nombre = input("Nombre: ").strip()
        if nombre:
            break
        print("[ERROR] El nombre no puede estar vacío")
    
    # Descripción
    while True:
        descripcion = input("Descripción: ").strip()
        if descripcion:
            break
        print("[ERROR] La descripción no puede estar vacía")
    
    return {
        "nro_especialidad": nro_especialidad,
        "nombre": nombre,
        "descripcion": descripcion
    }


def crear_especialidades_interactivo(gestor: GestorEspecialidad) -> bool:
    """
    Permite crear múltiples especialidades de forma interactiva
    
    Args:
        gestor: Instancia del GestorEspecialidad
    
    Returns:
        True si se crearon especialidades, False en caso contrario
    """
    cantidad = ingreso_cantidad_especialidades()
    especialidades_creadas = []
    
    for i in range(1, cantidad + 1):
        datos = ingreso_datos_especialidad(i)
        
        especialidad = gestor.alta_especialidad(
            nro_especialidad=datos["nro_especialidad"],
            nombre=datos["nombre"],
            descripcion=datos["descripcion"]
        )
        
        if especialidad:
            especialidades_creadas.append(especialidad)
    
    if especialidades_creadas:
        print(f"\n[OK] Se crearon {len(especialidades_creadas)} especialidad(es) exitosamente")
        return True
    else:
        print("\n[ERROR] No se pudo crear ninguna especialidad")
        return False


def guardar_en_base_datos(gestor: GestorEspecialidad) -> bool:
    """
    Guarda las especialidades en la base de datos
    
    Args:
        gestor: Instancia del GestorEspecialidad
    
    Returns:
        True si se guardó correctamente, False en caso contrario
    """
    especialidades = gestor.get_especialidades()
    
    if not especialidades:
        print("[ERROR] No hay especialidades para guardar")
        return False
    
    print("\n--- Conectando a Base de Datos ---")
    
    db = Database()
    
    if not db.conectar("127.0.0.1:3306/hospital_db"):
        print("[ERROR] No se pudo conectar a la base de datos")
        return False
    
    guardadas = 0
    
    for especialidad in especialidades:
        try:
            query = """
            INSERT INTO Especialidad (id_especialidad, nombre, descripcion)
            VALUES (%s, %s, %s)
            """
            
            params = (
                especialidad.get_nro_especialidad(),
                especialidad.get_nombre(),
                especialidad.get_descripcion()
            )
            
            resultado = db.ejecutar_consulta(query, params)
            
            if resultado is not None:
                guardadas += 1
                print(f"[OK] Especialidad {especialidad.get_nombre()} guardada en BD")
        
        except Exception as e:
            print(f"[ERROR] Error al guardar {especialidad.get_nombre()}: {str(e)}")
    
    db.desconectar()
    
    if guardadas > 0:
        print(f"\n[OK] {guardadas} especialidad(es) guardada(s) en la base de datos")
        return True
    else:
        print("\n[ERROR] No se pudo guardar ninguna especialidad")
        return False


def listar_especialidades_bd() -> bool:
    """
    Lista todas las especialidades de la base de datos
    
    Returns:
        True si se listaron correctamente, False en caso contrario
    """
    print("\n--- Conectando a Base de Datos ---")
    
    db = Database()
    
    if not db.conectar("127.0.0.1:3306/hospital_db"):
        print("[ERROR] No se pudo conectar a la base de datos")
        return False
    
    try:
        query = """
        SELECT e.id_especialidad, e.nombre, e.descripcion,
               COUNT(me.matricula) AS cantidad_medicos
        FROM Especialidad e
        LEFT JOIN Medico_especialidad me ON e.id_especialidad = me.id_especialidad
        GROUP BY e.id_especialidad, e.nombre, e.descripcion
        ORDER BY e.nombre
        """
        
        especialidades = db.obtener_registros(query)
        
        if especialidades:
            print(f"\n[OK] Se encontraron {len(especialidades)} especialidad(es) en la base de datos:\n")
            for especialidad in especialidades:
                print(f"   Nro Especialidad: {especialidad['id_especialidad']}")
                print(f"   Nombre: {especialidad['nombre']}")
                print(f"   Descripción: {especialidad['descripcion']}")
                print(f"   Médicos asignados: {especialidad['cantidad_medicos']}")
                print()
            return True
        else:
            print("\n[INFO] No hay especialidades registradas en la base de datos")
            return False
    
    except Exception as e:
        print(f"[ERROR] Error al listar especialidades: {str(e)}")
        return False
    
    finally:
        db.desconectar()


def eliminar_especialidad_bd() -> bool:
    """
    Elimina una especialidad de la base de datos
    
    Returns:
        True si se eliminó correctamente, False en caso contrario
    """
    print("\n--- Eliminar Especialidad ---")
    
    try:
        nro_especialidad = int(input("Ingresa el ID de la especialidad a eliminar: ").strip())
    except ValueError:
        print("[ERROR] El ID debe ser un número válido")
        return False
    
    db = Database()
    
    if not db.conectar("127.0.0.1:3306/hospital_db"):
        print("[ERROR] No se pudo conectar a la base de datos")
        return False
    
    try:
        # Verificar que la especialidad existe
        query_check = "SELECT id_especialidad, nombre FROM Especialidad WHERE id_especialidad = %s"
        especialidad = db.obtener_registro(query_check, (nro_especialidad,))
        
        if not especialidad:
            print(f"[ERROR] No se encontró especialidad con ID {nro_especialidad}")
            db.desconectar()
            return False
        
        # Verificar si tiene médicos asignados
        query_check_medicos = "SELECT COUNT(*) as total FROM Medico_especialidad WHERE id_especialidad = %s"
        resultado = db.obtener_registro(query_check_medicos, (nro_especialidad,))
        
        if resultado and resultado['total'] > 0:
            print(f"[ERROR] No se puede eliminar. La especialidad tiene {resultado['total']} médico(s) asignado(s)")
            db.desconectar()
            return False
        
        # Eliminar la especialidad
        query = "DELETE FROM Especialidad WHERE id_especialidad = %s"
        resultado = db.ejecutar_consulta(query, (nro_especialidad,))
        
        if resultado is not None and resultado > 0:
            print(f"[OK] Especialidad {especialidad['nombre']} eliminada exitosamente")
            db.desconectar()
            return True
        else:
            print("[ERROR] No se pudo eliminar la especialidad")
            db.desconectar()
            return False
    
    except Exception as e:
        print(f"[ERROR] Error al eliminar especialidad: {str(e)}")
        db.desconectar()
        return False


def modificar_especialidad_bd() -> bool:
    """
    Modifica los datos de una especialidad en la base de datos
    
    Returns:
        True si se modificó correctamente, False en caso contrario
    """
    print("\n--- Modificar Especialidad ---")
    
    try:
        nro_especialidad = int(input("Ingresa el ID de la especialidad a modificar: ").strip())
    except ValueError:
        print("[ERROR] El ID debe ser un número válido")
        return False
    
    db = Database()
    
    if not db.conectar("127.0.0.1:3306/hospital_db"):
        print("[ERROR] No se pudo conectar a la base de datos")
        return False
    
    try:
        # Verificar que la especialidad existe
        query_check = "SELECT id_especialidad, nombre, descripcion FROM Especialidad WHERE id_especialidad = %s"
        especialidad = db.obtener_registro(query_check, (nro_especialidad,))
        
        if not especialidad:
            print(f"[ERROR] No se encontró especialidad con ID {nro_especialidad}")
            db.desconectar()
            return False
        
        print(f"\n[INFO] Especialidad encontrada: {especialidad['nombre']}")
        print("\n¿Qué deseas modificar?")
        print("1. Nombre")
        print("2. Descripción")
        print("3. Modificar todo")
        print("4. Cancelar")
        
        opcion = input("\nSelecciona una opción: ").strip()
        
        datos_actualizar = {}
        
        if opcion == "1":
            nuevo_nombre = input("Nuevo nombre: ").strip()
            if nuevo_nombre:
                datos_actualizar['nombre'] = nuevo_nombre
            else:
                print("[ERROR] El nombre no puede estar vacío")
                db.desconectar()
                return False
        
        elif opcion == "2":
            nueva_descripcion = input("Nueva descripción: ").strip()
            if nueva_descripcion:
                datos_actualizar['descripcion'] = nueva_descripcion
            else:
                print("[ERROR] La descripción no puede estar vacía")
                db.desconectar()
                return False
        
        elif opcion == "3":
            nuevo_nombre = input("Nuevo nombre: ").strip()
            if nuevo_nombre:
                datos_actualizar['nombre'] = nuevo_nombre
            
            nueva_descripcion = input("Nueva descripción: ").strip()
            if nueva_descripcion:
                datos_actualizar['descripcion'] = nueva_descripcion
        
        elif opcion == "4":
            print("[INFO] Modificación cancelada")
            db.desconectar()
            return False
        
        else:
            print("[ERROR] Opción no válida")
            db.desconectar()
            return False
        
        if not datos_actualizar:
            print("[ERROR] No hay datos para actualizar")
            db.desconectar()
            return False
        
        # Construir la consulta UPDATE dinámicamente
        campos = ", ".join([f"{campo} = %s" for campo in datos_actualizar.keys()])
        valores = list(datos_actualizar.values())
        valores.append(nro_especialidad)
        
        query = f"UPDATE Especialidad SET {campos} WHERE id_especialidad = %s"
        resultado = db.ejecutar_consulta(query, tuple(valores))
        
        if resultado is not None and resultado > 0:
            print(f"[OK] Especialidad {especialidad['nombre']} modificada exitosamente")
            db.desconectar()
            return True
        else:
            print("[ERROR] No se pudo modificar la especialidad")
            db.desconectar()
            return False
    
    except Exception as e:
        print(f"[ERROR] Error al modificar especialidad: {str(e)}")
        db.desconectar()
        return False


def main():
    gestor = GestorEspecialidad()
    
    while True:
        limpiar_pantalla()
        mostrar_menu()
        
        opcion = input("Selecciona una opción: ").strip()
        
        if opcion == "1":
            limpiar_pantalla()
            print("=" * 60)
            print("CREAR NUEVAS ESPECIALIDADES")
            print("=" * 60)
            crear_especialidades_interactivo(gestor)
            input("\n[ENTER] para continuar...")
        
        elif opcion == "2":
            limpiar_pantalla()
            print("=" * 60)
            print("ESPECIALIDADES REGISTRADAS (En Memoria)")
            print("=" * 60)
            gestor.listar_todas_especialidades()
            input("\n[ENTER] para continuar...")
        
        elif opcion == "3":
            limpiar_pantalla()
            print("=" * 60)
            print("ESPECIALIDADES EN BASE DE DATOS")
            print("=" * 60)
            listar_especialidades_bd()
            input("\n[ENTER] para continuar...")
        
        elif opcion == "4":
            limpiar_pantalla()
            print("=" * 60)
            print("GUARDAR EN BASE DE DATOS")
            print("=" * 60)
            guardar_en_base_datos(gestor)
            input("\n[ENTER] para continuar...")
        
        elif opcion == "5":
            limpiar_pantalla()
            print("=" * 60)
            print("MODIFICAR ESPECIALIDAD")
            print("=" * 60)
            modificar_especialidad_bd()
            input("\n[ENTER] para continuar...")
        
        elif opcion == "6":
            limpiar_pantalla()
            eliminar_especialidad_bd()
            input("\n[ENTER] para continuar...")
        
        elif opcion == "7":
            print("\n[OK] ¡Hasta luego!")
            break
        
        else:
            print("[ERROR] Opción no válida")
            input("\n[ENTER] para continuar...")


if __name__ == "__main__":
    main()
