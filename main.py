"""
Script principal - Ejemplo de uso del sistema de gestión médica
"""

from datetime import date
from data.database import Database
from medico import Medico
from paciente import Paciente
from consultorio import Consultorio
from turno import Turno
from receta import Receta
from detalle_receta import DetalleDeReceta
from historial_clinico import HistorialClinico
from medicamento import Medicamento
from atendido import Atendido


def obtener_medicamento(numero_medicamento: int) -> Medicamento:
    """Obtiene un medicamento de la base de datos"""
    db = Database()  # Singleton - siempre retorna la misma instancia
    
    try:
        resultado = db.obtener_registros_parametrizados(
            "SELECT * FROM Medicamento WHERE numero_medicamento = %s",
            (numero_medicamento,)
        )
        
        if resultado:
            med = resultado[0]
            return Medicamento(
                numero_medicamento=med['numero_medicamento'],
                nombre=med['nombre'],
                dosis=med['dosis'],
                formato=med['formato']
            )
        else:
            print(f"✗ Medicamento {numero_medicamento} no encontrado")
            return None
    except Exception as e:
        print(f"✗ Error al obtener medicamento: {e}")
        return None


def menu_crear_receta(historial: HistorialClinico) -> Receta:
    """Menú para crear una receta con detalles"""
    print("\n" + "-" * 60)
    print("CREAR RECETA")
    print("-" * 60)
    
    nro_receta = int(input("\nNro. de Receta: "))
    observaciones = input("Observaciones de la receta: ").strip()
    
    receta = Receta(
        nro_receta=nro_receta,
        fecha_emision=date.today(),
        observaciones=observaciones
    )
    
    # Agregar detalles de receta
    nro_item = 1
    
    while True:
        print(f"\n📋 Detalle #{nro_item}:")
        numero_medicamento = int(input("Nro. de Medicamento: "))
        
        medicamento = obtener_medicamento(numero_medicamento)
        
        if not medicamento:
            print("✗ Medicamento no encontrado, intente nuevamente")
            continue
        
        indicacion = input(f"Indicación para '{medicamento.get_nombre()}': ").strip()
        
        if not indicacion:
            print("✗ La indicación es obligatoria")
            continue
        
        # Crear detalle de receta
        detalle = DetalleDeReceta(
            nro_item=nro_item,
            receta=receta,
            medicamento=medicamento,
            indicacion=indicacion
        )
        
        receta.agregar_detalle(detalle)
        print(f"✓ Medicamento '{medicamento.get_nombre()}' agregado (Dosis: {medicamento.get_dosis()})")
        
        nro_item += 1
        
        agregar_mas = input("\n¿Agregar otro medicamento? (s/n): ").lower()
        if agregar_mas != 's':
            break
    
    return receta


def guardar_historial_clinico(historial: HistorialClinico) -> bool:
    """Guarda el historial clínico en la base de datos"""
    db = Database()  # Singleton
    
    try:
        # Guardar historial clínico
        query_historial = """
            INSERT INTO HistorialClinico 
            (nro_historial, id_turno, id_paciente, diagnostico, observaciones, tratamiento, fecha_creacion)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        params_historial = (
            historial.get_nro_historial(),
            historial.get_turno().get_id_turno(),
            historial.get_paciente().get_nro_paciente(),
            historial.get_diagnostico(),
            historial.get_observaciones(),
            historial.get_tratamiento(),
            historial.get_fecha_creacion()
        )
        
        if not db.ejecutar_parametrizado(query_historial, params_historial):
            return False
        
        # Si hay receta, guardarla también
        if historial.get_receta():
            receta = historial.get_receta()
            
            # Guardar receta
            query_receta = """
                INSERT INTO Receta 
                (nro_receta, nro_historial, fecha_emision, observaciones)
                VALUES (%s, %s, %s, %s)
            """
            params_receta = (
                receta.get_nro_receta(),
                historial.get_nro_historial(),
                receta.get_fecha_emision(),
                receta.get_observaciones()
            )
            
            if not db.ejecutar_parametrizado(query_receta, params_receta):
                return False
            
            # Guardar detalles de receta
            for detalle in receta.get_detalles():
                query_detalle = """
                    INSERT INTO DetalleReceta 
                    (nro_item, nro_receta, numero_medicamento, indicacion)
                    VALUES (%s, %s, %s, %s)
                """
                params_detalle = (
                    detalle.get_nro_item(),
                    receta.get_nro_receta(),
                    detalle.get_medicamento().get_numero_medicamento(),
                    detalle.get_indicacion()
                )
                
                if not db.ejecutar_parametrizado(query_detalle, params_detalle):
                    return False
        
        return True
    except Exception as e:
        print(f"✗ Error al guardar historial: {e}")
        return False


def menu_atender_turno(turno: Turno) -> bool:
    """Menú para atender un turno y crear historial clínico"""
    print("\n" + "=" * 60)
    print("ATENDER TURNO")
    print("=" * 60)
    print(f"\n{turno}")
    
    # Validar que el turno pueda ser atendido
    if not turno.get_estado_turno().puede_atender():
        print(f"✗ No se puede atender un turno en estado {turno.get_estado_turno().get_nombre()}")
        return False
    
    # Datos del historial clínico
    print("\n📝 Ingrese los datos del historial clínico:")
    diagnostico = input("Diagnóstico: ").strip()
    observaciones = input("Observaciones: ").strip()
    tratamiento = input("Tratamiento: ").strip()
    
    # Validar datos obligatorios
    if not diagnostico or not tratamiento:
        print("✗ Diagnóstico y Tratamiento son obligatorios")
        return False
    
    # Crear historial clínico
    nro_historial = int(input("\nNro. de Historial: "))
    historial = HistorialClinico(
        nro_historial=nro_historial,
        turno=turno,
        paciente=turno.get_paciente(),
        diagnostico=diagnostico,
        observaciones=observaciones,
        tratamiento=tratamiento
    )
    
    # Preguntar si desea agregar receta
    agregar_receta = input("\n¿Desea agregar una receta? (s/n): ").lower()
    
    if agregar_receta == 's':
        receta = menu_crear_receta(historial)
        historial.set_receta(receta)
    
    # Guardar en base de datos
    if guardar_historial_clinico(historial):
        print("\n✓ Historial clínico guardado exitosamente")
        
        # Cambiar estado del turno a Atendido
        turno.set_estado_turno(Atendido())
        print("✓ Turno marcado como Atendido")
        
        # Actualizar estado en BD
        db = Database()  # Singleton
        db.ejecutar_parametrizado(
            "UPDATE Turno SET estado = %s WHERE id_turno = %s",
            ("Atendido", turno.get_id_turno())
        )
        
        return True
    else:
        print("\n✗ Error al guardar el historial clínico")
        return False


def obtener_turno(turno_id: int) -> Turno:
    """Obtiene un turno de la base de datos"""
    db = Database()  # Singleton
    
    try:
        resultado = db.obtener_registros_parametrizados(
            """SELECT t.* FROM Turno t 
               WHERE t.id_turno = %s AND t.estado = 'Programado'""",
            (turno_id,)
        )
        
        if resultado:
            t = resultado[0]
            # Aquí deberías mapear a tu objeto Turno completo
            print("✓ Turno encontrado")
            return t
        else:
            print(f"✗ Turno {turno_id} no encontrado o no está programado")
            return None
    except Exception as e:
        print(f"✗ Error al obtener turno: {e}")
        return None


def mostrar_turnos() -> None:
    """Muestra los turnos programados"""
    db = Database()  # Singleton
    
    print("\n⏰ TURNOS PROGRAMADOS:")
    print("=" * 60)
    
    try:
        turnos = db.obtener_registros("""
            SELECT t.id_turno, m.nombre as medico, p.nombre as paciente, 
                   t.fecha, t.hora, t.estado
            FROM Turno t
            JOIN Medico m ON t.matricula = m.matricula
            JOIN Paciente p ON t.id_paciente = p.id_paciente
            WHERE t.estado = 'Programado'
            ORDER BY t.fecha, t.hora
        """)
        
        if not turnos:
            print("   No hay turnos programados")
            return
        
        for turno in turnos:
            print(f"   #{turno['id_turno']:3} | {turno['paciente']:20} | "
                  f"Dr. {turno['medico']:20} | {turno['fecha']} {turno['hora']}")
    except Exception as e:
        print(f"✗ Error: {e}")


def mostrar_especialidades() -> None:
    """Muestra las especialidades disponibles"""
    db = Database()  # Singleton
    
    print("\n📚 ESPECIALIDADES:")
    print("=" * 60)
    
    try:
        especialidades = db.obtener_registros("SELECT * FROM Especialidad")
        
        if not especialidades:
            print("   No hay especialidades registradas")
            return
        
        for esp in especialidades:
            print(f"   {esp['nro_especialidad']} - {esp['nombre']}: {esp['descripcion']}")
    except Exception as e:
        print(f"✗ Error: {e}")


def menu_principal(db: Database) -> None:
    """Menú principal del sistema"""
    while True:
        print("\n" + "=" * 60)
        print("SISTEMA DE GESTIÓN MÉDICA")
        print("=" * 60)
        print("1. Ver turnos programados")
        print("2. Atender turno")
        print("3. Ver especialidades")
        print("4. Salir")
        
        opcion = input("\nSeleccione una opción: ").strip()
        
        if opcion == "1":
            mostrar_turnos()
        
        elif opcion == "2":
            mostrar_turnos()
            try:
                turno_id = int(input("\nIngrese ID del turno a atender: "))
                turno = obtener_turno(turno_id)
                
                if turno:
                    menu_atender_turno(turno)
                else:
                    print("✗ Turno no encontrado")
            except ValueError:
                print("✗ ID inválido")
        
        elif opcion == "3":
            mostrar_especialidades()
        
        elif opcion == "4":
            print("\n👋 ¡Hasta luego!")
            break
        
        else:
            print("✗ Opción inválida")


def main():
    print("\n" + "=" * 60)
    print("SISTEMA DE GESTIÓN MÉDICA")
    print("=" * 60)
    
    # Obtener instancia Singleton de Database
    db = Database()
    
    if db.conectar("127.0.0.1:3306/hospital_db"):
        print(f"✓ {db}")
        menu_principal(db)
        db.desconectar()
    else:
        print("✗ No se pudo conectar a la base de datos")


if __name__ == "__main__":
    main()