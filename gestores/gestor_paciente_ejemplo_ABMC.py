# -*- coding: utf-8 -*-
"""
Ejemplo de uso del ABMC de Pacientes con entrada interactiva y almacenamiento en BD
"""

from datetime import date
import sys
import os

# Agregar el directorio padre al path para importar módulos
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# ✅ IMPORTAR CORRECTAMENTE
from gestor_paciente import GestorPaciente
from data.database import Database


def limpiar_pantalla():
    """Limpia la pantalla de la consola"""
    os.system('cls' if os.name == 'nt' else 'clear')


def mostrar_menu():
    """Muestra el menú principal"""
    print("\n" + "=" * 60)
    print("SISTEMA ABMC DE PACIENTES")
    print("=" * 60)
    print("\n1. Crear nuevos pacientes")
    print("2. Listar pacientes (en memoria)")
    print("3. Listar pacientes de la base de datos")
    print("4. Guardar pacientes en base de datos")
    print("5. Modificar paciente")
    print("6. Eliminar paciente (marcar como inactivo)")
    print("7. Salir")
    print("\n" + "-" * 60)


def ingreso_cantidad_pacientes() -> int:
    """Solicita la cantidad de pacientes a crear"""
    while True:
        try:
            cantidad = int(input("\n¿Cuántos pacientes deseas crear? "))
            if cantidad <= 0:
                print("[ERROR] La cantidad debe ser mayor a 0")
                continue
            return cantidad
        except ValueError:
            print("[ERROR] Ingresa un número válido")


def ingreso_datos_paciente(numero: int) -> dict:
    """
    Solicita los datos de un paciente
    
    Args:
        numero: Número de paciente a ingresar
    
    Returns:
        Diccionario con los datos del paciente
    """
    print(f"\n--- Paciente #{numero} ---")
    
    # Nombre
    while True:
        nombre = input("Nombre: ").strip()
        if nombre:
            break
        print("[ERROR] El nombre no puede estar vacío")
    
    # Apellido
    while True:
        apellido = input("Apellido: ").strip()
        if apellido:
            break
        print("[ERROR] El apellido no puede estar vacío")
    
    # Teléfono
    telefono = input("Teléfono: ").strip()
    
    # Fecha de nacimiento
    while True:
        try:
            fecha_str = input("Fecha de nacimiento (YYYY-MM-DD): ").strip()
            fecha_nacimiento = date.fromisoformat(fecha_str)
            break
        except ValueError:
            print("[ERROR] Formato de fecha inválido. Usa YYYY-MM-DD")
    
    # Dirección
    while True:
        direccion = input("Dirección: ").strip()
        if direccion:
            break
        print("[ERROR] La dirección no puede estar vacía")
    
    return {
        "nombre": nombre,
        "apellido": apellido,
        "telefono": telefono,
        "fecha_nacimiento": fecha_nacimiento,
        "direccion": direccion
    }


def crear_pacientes_interactivo(gestor: GestorPaciente) -> bool:
    """
    Permite crear múltiples pacientes de forma interactiva
    
    Args:
        gestor: Instancia del GestorPaciente
    
    Returns:
        True si se crearon pacientes, False en caso contrario
    """
    cantidad = ingreso_cantidad_pacientes()
    pacientes_creados = []
    
    for i in range(1, cantidad + 1):
        datos = ingreso_datos_paciente(i)
        
        paciente = gestor.alta_paciente(
            nombre=datos["nombre"],
            apellido=datos["apellido"],
            telefono=datos["telefono"],
            fecha_nacimiento=datos["fecha_nacimiento"],
            direccion=datos["direccion"]
        )
        
        if paciente:
            pacientes_creados.append(paciente)
    
    if pacientes_creados:
        print(f"\n[OK] Se crearon {len(pacientes_creados)} paciente(s) exitosamente")
        return True
    else:
        print("\n[ERROR] No se pudo crear ningún paciente")
        return False


def guardar_en_base_datos(gestor: GestorPaciente) -> bool:
    """
    Guarda los pacientes en la base de datos
    
    Args:
        gestor: Instancia del GestorPaciente
    
    Returns:
        True si se guardó correctamente, False en caso contrario
    """
    pacientes = gestor.get_pacientes()
    
    if not pacientes:
        print("[ERROR] No hay pacientes para guardar")
        return False
    
    print("\n--- Conectando a Base de Datos ---")
    
    db = Database()
    
    if not db.conectar("127.0.0.1:3306/hospital_db"):
        print("[ERROR] No se pudo conectar a la base de datos")
        return False
    
    guardados = 0
    
    for paciente in pacientes:
        try:
            query = """
            INSERT INTO Paciente (nombre, apellido, telefono, fecha_nacimiento, direccion, activo)
            VALUES (%s, %s, %s, %s, %s, TRUE)
            """
            
            params = (
                paciente.get_nombre(),
                paciente.get_apellido(),
                paciente.get_telefono(),
                paciente.get_fecha_nacimiento(),
                paciente.get_direccion()
            )
            
            resultado = db.ejecutar_consulta(query, params)
            
            if resultado is not None:
                guardados += 1
                print(f"[OK] Paciente {paciente.get_nombre()} {paciente.get_apellido()} guardado en BD")
        
        except Exception as e:
            print(f"[ERROR] Error al guardar {paciente.get_nombre()}: {str(e)}")
    
    db.desconectar()
    
    if guardados > 0:
        print(f"\n[OK] {guardados} paciente(s) guardado(s) en la base de datos")
        return True
    else:
        print("\n[ERROR] No se pudo guardar ningún paciente")
        return False


def listar_pacientes_bd() -> bool:
    """
    Lista todos los pacientes de la base de datos
    
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
        SELECT nombre, apellido, telefono, fecha_nacimiento, 
               direccion, activo
        FROM Paciente
        ORDER BY nombre, apellido
        """
        
        pacientes = db.obtener_registros(query)
        
        if pacientes:
            print(f"\n[OK] Se encontraron {len(pacientes)} paciente(s) en la base de datos:\n")
            for paciente in pacientes:
                estado = "Activo" if paciente['activo'] else "Inactivo"
                print(f"   Nombre: {paciente['nombre']} {paciente['apellido']}")
                print(f"   Teléfono: {paciente['telefono']}")
                print(f"   Fecha de nacimiento: {paciente['fecha_nacimiento']}")
                print(f"   Dirección: {paciente['direccion']}")
                print(f"   Estado: {estado}")
                print()
            return True
        else:
            print("\n[INFO] No hay pacientes registrados en la base de datos")
            return False
    
    except Exception as e:
        print(f"[ERROR] Error al listar pacientes: {str(e)}")
        return False
    
    finally:
        db.desconectar()


def eliminar_paciente_bd() -> bool:
    """
    Marca un paciente como inactivo en la base de datos
    
    Returns:
        True si se eliminó correctamente, False en caso contrario
    """
    print("\n--- Eliminar Paciente ---")
    
    nombre = input("Nombre del paciente: ").strip()
    apellido = input("Apellido del paciente: ").strip()
    
    db = Database()
    
    if not db.conectar("127.0.0.1:3306/hospital_db"):
        print("[ERROR] No se pudo conectar a la base de datos")
        return False
    
    try:
        # Verificar que el paciente existe
        query_check = "SELECT nombre, apellido FROM Paciente WHERE nombre = %s AND apellido = %s"
        paciente = db.obtener_registro(query_check, (nombre, apellido))
        
        if not paciente:
            print(f"[ERROR] No se encontró paciente con nombre {nombre} {apellido}")
            db.desconectar()
            return False
        
        # Actualizar activo a 0
        query = "UPDATE Paciente SET activo = 0 WHERE nombre = %s AND apellido = %s"
        resultado = db.ejecutar_consulta(query, (nombre, apellido))
        
        if resultado is not None and resultado > 0:
            print(f"[OK] Paciente {nombre} {apellido} marcado como inactivo")
            db.desconectar()
            return True
        else:
            print("[ERROR] No se pudo marcar el paciente como inactivo")
            db.desconectar()
            return False
    
    except Exception as e:
        print(f"[ERROR] Error al eliminar paciente: {str(e)}")
        db.desconectar()
        return False


def modificar_paciente_bd() -> bool:
    """
    Modifica los datos de un paciente en la base de datos
    
    Returns:
        True si se modificó correctamente, False en caso contrario
    """
    print("\n--- Modificar Paciente ---")
    
    nombre = input("Nombre del paciente a modificar: ").strip()
    apellido = input("Apellido del paciente: ").strip()
    
    db = Database()
    
    if not db.conectar("127.0.0.1:3306/hospital_db"):
        print("[ERROR] No se pudo conectar a la base de datos")
        return False
    
    try:
        # Verificar que el paciente existe
        query_check = "SELECT nombre, apellido, telefono, fecha_nacimiento, direccion FROM Paciente WHERE nombre = %s AND apellido = %s"
        paciente = db.obtener_registro(query_check, (nombre, apellido))
        
        if not paciente:
            print(f"[ERROR] No se encontró paciente con nombre {nombre} {apellido}")
            db.desconectar()
            return False
        
        print(f"\n[INFO] Paciente encontrado: {paciente['nombre']} {paciente['apellido']}")
        print("\n¿Qué deseas modificar?")
        print("1. Nombre")
        print("2. Apellido")
        print("3. Teléfono")
        print("4. Fecha de nacimiento")
        print("5. Dirección")
        print("6. Modificar todo")
        print("7. Cancelar")
        
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
            nuevo_apellido = input("Nuevo apellido: ").strip()
            if nuevo_apellido:
                datos_actualizar['apellido'] = nuevo_apellido
            else:
                print("[ERROR] El apellido no puede estar vacío")
                db.desconectar()
                return False
        
        elif opcion == "3":
            nuevo_telefono = input("Nuevo teléfono: ").strip()
            if nuevo_telefono:
                datos_actualizar['telefono'] = nuevo_telefono
        
        elif opcion == "4":
            while True:
                try:
                    fecha_str = input("Nueva fecha de nacimiento (YYYY-MM-DD): ").strip()
                    nueva_fecha = date.fromisoformat(fecha_str)
                    datos_actualizar['fecha_nacimiento'] = nueva_fecha
                    break
                except ValueError:
                    print("[ERROR] Formato de fecha inválido. Usa YYYY-MM-DD")
        
        elif opcion == "5":
            nueva_direccion = input("Nueva dirección: ").strip()
            if nueva_direccion:
                datos_actualizar['direccion'] = nueva_direccion
        
        elif opcion == "6":
            nuevo_nombre = input("Nuevo nombre: ").strip()
            if nuevo_nombre:
                datos_actualizar['nombre'] = nuevo_nombre
            
            nuevo_apellido = input("Nuevo apellido: ").strip()
            if nuevo_apellido:
                datos_actualizar['apellido'] = nuevo_apellido
            
            nuevo_telefono = input("Nuevo teléfono: ").strip()
            if nuevo_telefono:
                datos_actualizar['telefono'] = nuevo_telefono
            
            while True:
                try:
                    fecha_str = input("Nueva fecha de nacimiento (YYYY-MM-DD): ").strip()
                    nueva_fecha = date.fromisoformat(fecha_str)
                    datos_actualizar['fecha_nacimiento'] = nueva_fecha
                    break
                except ValueError:
                    print("[ERROR] Formato de fecha inválido. Usa YYYY-MM-DD")
            
            nueva_direccion = input("Nueva dirección: ").strip()
            if nueva_direccion:
                datos_actualizar['direccion'] = nueva_direccion
        
        elif opcion == "7":
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
        valores.extend([nombre, apellido])
        
        query = f"UPDATE Paciente SET {campos} WHERE nombre = %s AND apellido = %s"
        resultado = db.ejecutar_consulta(query, tuple(valores))
        
        if resultado is not None and resultado > 0:
            print(f"[OK] Paciente {nombre} {apellido} modificado exitosamente")
            db.desconectar()
            return True
        else:
            print("[ERROR] No se pudo modificar el paciente")
            db.desconectar()
            return False
    
    except Exception as e:
        print(f"[ERROR] Error al modificar paciente: {str(e)}")
        db.desconectar()
        return False


def main():
    gestor = GestorPaciente()
    
    while True:
        limpiar_pantalla()
        mostrar_menu()
        
        opcion = input("Selecciona una opción: ").strip()
        
        if opcion == "1":
            limpiar_pantalla()
            print("=" * 60)
            print("CREAR NUEVOS PACIENTES")
            print("=" * 60)
            crear_pacientes_interactivo(gestor)
            input("\n[ENTER] para continuar...")
        
        elif opcion == "2":
            limpiar_pantalla()
            print("=" * 60)
            print("PACIENTES REGISTRADOS (En Memoria)")
            print("=" * 60)
            gestor.listar_todos_pacientes()
            input("\n[ENTER] para continuar...")
        
        elif opcion == "3":
            limpiar_pantalla()
            print("=" * 60)
            print("PACIENTES EN BASE DE DATOS")
            print("=" * 60)
            listar_pacientes_bd()
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
            print("MODIFICAR PACIENTE")
            print("=" * 60)
            modificar_paciente_bd()
            input("\n[ENTER] para continuar...")
        
        elif opcion == "6":
            limpiar_pantalla()
            eliminar_paciente_bd()
            input("\n[ENTER] para continuar...")
        
        elif opcion == "7":
            print("\n[OK] ¡Hasta luego!")
            break
        
        else:
            print("[ERROR] Opción no válida")
            input("\n[ENTER] para continuar...")


if __name__ == "__main__":
    main()