"""
Script principal - Ejemplo de uso del sistema de gestión médica
"""

from datetime import date
from data.database import Database
from models.medicamento import Medicamento
from turnos.turno import Turno
from turnos.states.atendido import Atendido
from recetas.receta import Receta
from recetas.detalle_receta import DetalleDeReceta
from historiales.historial_clinico import HistorialClinico


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
        # Guardar historial clínicoco en la base de datos"""
        query_historial = """db = Database()  # Singleton
            INSERT INTO HistorialClinico 
            (nro_historial, id_turno, id_paciente, diagnostico, observaciones, tratamiento, fecha_creacion)
            VALUES (%s, %s, %s, %s, %s, %s, %s)línico
        """
        params_historial = (
            historial.get_nro_historial(),te, diagnostico, observaciones, tratamiento, fecha_creacion)
            historial.get_turno().get_id_turno(), VALUES (%s, %s, %s, %s, %s, %s, %s)
            historial.get_paciente().get_nro_paciente(),
            historial.get_diagnostico(),
            historial.get_observaciones(),
            historial.get_tratamiento(),
            historial.get_fecha_creacion()_nro_paciente(),
        )
        ),
        if not db.ejecutar_parametrizado(query_historial, params_historial):
            return False   historial.get_fecha_creacion()
        )
        # Si hay receta, guardarla también
        if historial.get_receta():ar_parametrizado(query_historial, params_historial):
            receta = historial.get_receta()    return False
            
            # Guardar receta también
            query_receta = """
                INSERT INTO Receta receta = historial.get_receta()
                (nro_receta, nro_historial, fecha_emision, observaciones)
                VALUES (%s, %s, %s, %s)
            """
            params_receta = (
                receta.get_nro_receta(),ial, fecha_emision, observaciones)
                historial.get_nro_historial(), VALUES (%s, %s, %s, %s)
                receta.get_fecha_emision(),
                receta.get_observaciones()
            )
            (),
            if not db.ejecutar_parametrizado(query_receta, params_receta):,
                return False   receta.get_observaciones()
            )
            # Guardar detalles de receta
            for detalle in receta.get_detalles():ar_parametrizado(query_receta, params_receta):
                query_detalle = """    return False
                    INSERT INTO DetalleReceta 
                    (nro_item, nro_receta, numero_medicamento, indicacion)
                    VALUES (%s, %s, %s, %s)et_detalles():
                """
                params_detalle = (
                    detalle.get_nro_item(),numero_medicamento, indicacion)
                    receta.get_nro_receta(), VALUES (%s, %s, %s, %s)
                    detalle.get_medicamento().get_numero_medicamento(),
                    detalle.get_indicacion()
                )
                
                if not db.ejecutar_parametrizado(query_detalle, params_detalle):).get_numero_medicamento(),
                    return False   detalle.get_indicacion()
        )
        return True
    except Exception as e:ar_parametrizado(query_detalle, params_detalle):
        print(f"✗ Error al guardar historial: {e}")            return False
        return False


def menu_atender_turno(turno: Turno) -> bool:ror al guardar historial: {e}")
    """Menú para atender un turno y crear historial clínico"""        return False
    print("\n" + "=" * 60)
    print("ATENDER TURNO")
    print("=" * 60)
    print(f"\n{turno}")n turno y crear historial clínico"""
    
    # Validar que el turno pueda ser atendidoTURNO")
    if not turno.get_estado_turno().puede_atender():
        print(f"✗ No se puede atender un turno en estado {turno.get_estado_turno().get_nombre()}")print(f"\n{turno}")
        return False
    
    # Datos del historial clínico
    print("\n📝 Ingrese los datos del historial clínico:") se puede atender un turno en estado {turno.get_estado_turno().get_nombre()}")
    diagnostico = input("Diagnóstico: ").strip()    return False
    observaciones = input("Observaciones: ").strip()
    tratamiento = input("Tratamiento: ").strip()
    clínico:")
    # Validar datos obligatorios
    if not diagnostico or not tratamiento:ip()
        print("✗ Diagnóstico y Tratamiento son obligatorios")tratamiento = input("Tratamiento: ").strip()
        return False
    
    # Crear historial clínico
    nro_historial = int(input("\nNro. de Historial: "))gnóstico y Tratamiento son obligatorios")
    historial = HistorialClinico(    return False
        nro_historial=nro_historial,
        turno=turno,
        paciente=turno.get_paciente(),Nro. de Historial: "))
        diagnostico=diagnostico,
        observaciones=observaciones,l=nro_historial,
        tratamiento=tratamiento
    )nte(),
    
    # Preguntar si desea agregar recetaones,
    agregar_receta = input("\n¿Desea agregar una receta? (s/n): ").lower()   tratamiento=tratamiento
    )
    if agregar_receta == 's':
        receta = menu_crear_receta(historial)
        historial.set_receta(receta)agregar_receta = input("\n¿Desea agregar una receta? (s/n): ").lower()
    
    # Guardar en base de datos
    if guardar_historial_clinico(historial):istorial)
        print("\n✓ Historial clínico guardado exitosamente")    historial.set_receta(receta)
        
        # Cambiar estado del turno a Atendido
        turno.set_estado_turno(Atendido())
        print("✓ Turno marcado como Atendido")print("\n✓ Historial clínico guardado exitosamente")
        
        # Actualizar estado en BDido
        db = Database()  # Singleton
        db.ejecutar_parametrizado(print("✓ Turno marcado como Atendido")
            "UPDATE Turno SET estado = %s WHERE id_turno = %s",
            ("Atendido", turno.get_id_turno())
        )on
        
        return TrueE id_turno = %s",
    else:   ("Atendido", turno.get_id_turno())
        print("\n✗ Error al guardar el historial clínico"))
        return False
eturn True

def obtener_turno(turno_id: int) -> Turno:rror al guardar el historial clínico")
    """Obtiene un turno de la base de datos"""        return False
    db = Database()  # Singleton
    
    try:
        resultado = db.obtener_registros_parametrizados(se de datos"""
            """SELECT t.* FROM Turno t db = Database()  # Singleton
               WHERE t.id_turno = %s AND t.estado = 'Programado'""",
            (turno_id,)
        )s_parametrizados(
        
        if resultado:id_turno = %s AND t.estado = 'Programado'""",
            t = resultado[0]   (turno_id,)
            print("✓ Turno encontrado"))
            return t
        else:
            print(f"✗ Turno {turno_id} no encontrado o no está programado")
            return None objeto Turno completo
    except Exception as e: Turno encontrado")
        print(f"✗ Error al obtener turno: {e}")eturn t
        return None
urno {turno_id} no encontrado o no está programado")

def mostrar_turnos() -> None:
    """Muestra los turnos programados"""rror al obtener turno: {e}")
    db = Database()  # Singleton        return None
    
    print("\n⏰ TURNOS PROGRAMADOS:")
    print("=" * 60)
    mados"""
    try:db = Database()  # Singleton
        turnos = db.obtener_registros("""
            SELECT t.id_turno, m.nombre as medico, p.nombre as paciente, OS PROGRAMADOS:")
                   t.fecha, t.hora, t.estadoprint("=" * 60)
            FROM Turno t
            JOIN Medico m ON t.matricula = m.matricula
            JOIN Paciente p ON t.id_paciente = p.id_paciente
            WHERE t.estado = 'Programado'edico, p.nombre as paciente, 
            ORDER BY t.fecha, t.horaha, t.hora, t.estado
        """)
        
        if not turnos:nte = p.id_paciente
            print("   No hay turnos programados")mado'
            returnORDER BY t.fecha, t.hora
        """)
        for turno in turnos:
            print(f"   #{turno['id_turno']:3} | {turno['paciente']:20} | "
                  f"Dr. {turno['medico']:20} | {turno['fecha']} {turno['hora']}")"   No hay turnos programados")
    except Exception as e:    return
        print(f"✗ Error: {e}")


def mostrar_especialidades() -> None:urno['medico']:20} | {turno['fecha']} {turno['hora']}")
    """Muestra las especialidades disponibles"""
    db = Database()  # Singleton        print(f"✗ Error: {e}")
    
    print("\n📚 ESPECIALIDADES:")
    print("=" * 60)
    s disponibles"""
    try:db = Database()  # Singleton
        especialidades = db.obtener_registros("SELECT * FROM Especialidad")
        ECIALIDADES:")
        if not especialidades:print("=" * 60)
            print("   No hay especialidades registradas")
            return
        especialidades = db.obtener_registros("SELECT * FROM Especialidad")
        for esp in especialidades:
            print(f"   {esp['nro_especialidad']} - {esp['nombre']}: {esp['descripcion']}")
    except Exception as e:"   No hay especialidades registradas")
        print(f"✗ Error: {e}")    return


def menu_principal(db: Database) -> None:p['nro_especialidad']} - {esp['nombre']}: {esp['descripcion']}")
    """Menú principal del sistema"""
    while True:        print(f"✗ Error: {e}")
        print("\n" + "=" * 60)
        print("SISTEMA DE GESTIÓN MÉDICA")
        print("=" * 60)None:
        print("1. Ver turnos programados")ncipal del sistema"""
        print("2. Atender turno")
        print("3. Ver especialidades")
        print("4. Salir")DE GESTIÓN MÉDICA")
        
        opcion = input("\nSeleccione una opción: ").strip()ramados")
        
        if opcion == "1":ecialidades")
            mostrar_turnos()print("4. Salir")
        
        elif opcion == "2":opcion = input("\nSeleccione una opción: ").strip()
            mostrar_turnos()
            try:
                turno_id = int(input("\nIngrese ID del turno a atender: "))    mostrar_turnos()
                turno = obtener_turno(turno_id)
                
                if turno:rar_turnos()
                    menu_atender_turno(turno)
                else: ID del turno a atender: "))
                    print("✗ Turno no encontrado")turno = obtener_turno(turno_id)
            except ValueError:
                print("✗ ID inválido")
        enu_atender_turno(turno)
        elif opcion == "3":
            mostrar_especialidades()urno no encontrado")
        
        elif opcion == "4":        print("✗ ID inválido")
            print("\n👋 ¡Hasta luego!")
            break
            mostrar_especialidades()
        else:
            print("✗ Opción inválida")
("\n👋 ¡Hasta luego!")
    break
def main():
    print("\n" + "=" * 60)
    print("SISTEMA DE GESTIÓN MÉDICA")            print("✗ Opción inválida")
    print("=" * 60)
    
    # Obtener instancia Singleton de Database
    db = Database()
    DE GESTIÓN MÉDICA")
    if db.conectar("127.0.0.1:3306/hospital_db"):print("=" * 60)
        print(f"✓ {db}")
        menu_principal(db)ncia Singleton de Database
        db.desconectar()db = Database()
    else:
        print("✗ No se pudo conectar a la base de datos")0.0.1:3306/hospital_db"):

b)
if __name__ == "__main__":b.desconectar()
    main()    main()