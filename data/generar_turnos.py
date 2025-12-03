# -*- coding: utf-8 -*-
"""
Script para generar turnos automáticamente basados en las agendas
Crea turnos de 30 minutos para cada rango horario de agenda
Estado inicial: 'Libre'
"""

import sys
import os
from datetime import datetime, timedelta, date, time

# Agregar el directorio padre al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.database import Database


def generar_turnos_desde_agendas(fecha_inicio: date = None, dias_adelante: int = 30):
    """
    Genera turnos de 30 minutos basados en las agendas registradas
    
    Args:
        fecha_inicio: Fecha desde la cual generar turnos (por defecto hoy)
        dias_adelante: Cantidad de días a generar turnos (por defecto 30)
    """
    
    if fecha_inicio is None:
        fecha_inicio = date.today()
    
    db = Database()
    
    if not db.conectar("127.0.0.1:3306/hospital_db"):
        print("[ERROR] No se pudo conectar a la base de datos")
        return False
    
    try:
        # Cargar todas las agendas activas
        query_agendas = """
        SELECT a.id_agenda, a.matricula, a.id_consultorio, a.dia_semana,
               a.hora_inicio, a.hora_fin
        FROM Agenda a
        WHERE a.activa = TRUE
        ORDER BY a.matricula, a.dia_semana
        """
        
        agendas = db.obtener_registros(query_agendas)
        
        if not agendas:
            print("[ERROR] No hay agendas registradas en la base de datos")
            db.desconectar()
            return False
        
        print(f"\n{'='*80}")
        print(f"GENERANDO TURNOS DESDE {fecha_inicio} POR {dias_adelante} DÍAS")
        print(f"{'='*80}\n")
        
        # Mapeo de días de semana
        dias_semana = {
            0: "Lunes",
            1: "Martes",
            2: "Miércoles",
            3: "Jueves",
            4: "Viernes",
            5: "Sábado",
            6: "Domingo"
        }
        
        dias_semana_inverso = {v: k for k, v in dias_semana.items()}
        
        total_turnos_creados = 0
        total_errores = 0
        
        # Iterar sobre cada agenda
        for agenda in agendas:
            id_agenda = agenda['id_agenda']
            matricula = agenda['matricula']
            id_consultorio = agenda['id_consultorio']
            dia_agenda = agenda['dia_semana']
            hora_inicio_agenda = agenda['hora_inicio']
            hora_fin_agenda = agenda['hora_fin']
            
            # Convertir timedelta o string a time
            if isinstance(hora_inicio_agenda, timedelta):
                total_seconds = int(hora_inicio_agenda.total_seconds())
                hora_inicio_agenda = time(total_seconds // 3600, (total_seconds % 3600) // 60)
            elif isinstance(hora_inicio_agenda, str):
                hora_inicio_agenda = datetime.strptime(hora_inicio_agenda, "%H:%M:%S").time()
            
            if isinstance(hora_fin_agenda, timedelta):
                total_seconds = int(hora_fin_agenda.total_seconds())
                hora_fin_agenda = time(total_seconds // 3600, (total_seconds % 3600) // 60)
            elif isinstance(hora_fin_agenda, str):
                hora_fin_agenda = datetime.strptime(hora_fin_agenda, "%H:%M:%S").time()
            
            numero_dia_semana = dias_semana_inverso.get(dia_agenda)
            
            if numero_dia_semana is None:
                print(f"[ERROR] Día de semana inválido: {dia_agenda}")
                total_errores += 1
                continue
            
            print(f"\n{'─'*80}")
            print(f"Agenda #{id_agenda} - Médico: {matricula} | Consultorio: {id_consultorio}")
            print(f"Día: {dia_agenda} | Horario: {hora_inicio_agenda} - {hora_fin_agenda}")
            print(f"{'─'*80}\n")
            
            # Iterar sobre los días del rango
            fecha_actual = fecha_inicio
            fecha_fin = fecha_inicio + timedelta(days=dias_adelante)
            
            while fecha_actual < fecha_fin:
                # Verificar si es el día de semana correcto
                if fecha_actual.weekday() == numero_dia_semana:
                    
                    # Generar turnos cada 30 minutos dentro del horario
                    hora_actual = datetime.combine(fecha_actual, hora_inicio_agenda)
                    hora_fin_dt = datetime.combine(fecha_actual, hora_fin_agenda)
                    
                    while hora_actual < hora_fin_dt:
                        hora_inicio_turno = hora_actual.time()
                        hora_fin_turno_dt = hora_actual + timedelta(minutes=30)
                        hora_fin_turno = hora_fin_turno_dt.time()
                        
                        # Verificar que hora_fin_turno no exceda hora_fin_agenda
                        if hora_fin_turno > hora_fin_agenda:
                            break
                        
                        # Ejecutar la query parametrizada
                        try:
                            resultado = db.ejecutar_parametrizado(
                                """INSERT INTO Turno (matricula, id_consultorio, id_agenda, fecha, hora_inicio, hora_fin, estado)
                                VALUES (%s, %s, %s, %s, %s, %s, 'Libre')""",
                                (matricula, id_consultorio, id_agenda, fecha_actual, hora_inicio_turno, hora_fin_turno)
                            )
                            
                            if resultado:
                                print(f"[OK] Turno creado: {fecha_actual} {hora_inicio_turno}-{hora_fin_turno}")
                                total_turnos_creados += 1
                            else:
                                print(f"[ERROR] Error al crear turno: {fecha_actual} {hora_inicio_turno}-{hora_fin_turno}")
                                total_errores += 1
                        
                        except Exception as e:
                            print(f"[ERROR] Error: {str(e)}")
                            total_errores += 1
                        
                        # Avanzar 30 minutos
                        hora_actual += timedelta(minutes=30)
                
                # Avanzar al siguiente día
                fecha_actual += timedelta(days=1)
        
        print(f"\n{'='*80}")
        print(f"RESUMEN")
        print(f"{'='*80}")
        print(f"[OK] Turnos creados: {total_turnos_creados}")
        print(f"[ERROR] Errores: {total_errores}")
        print(f"{'='*80}\n")
        
        db.desconectar()
        return True
    
    except Exception as e:
        print(f"[ERROR] Error durante la generación de turnos: {str(e)}")
        db.desconectar()
        return False


if __name__ == "__main__":
    # Generar turnos para los próximos 30 días
    generar_turnos_desde_agendas(
        fecha_inicio=date.today(),
        dias_adelante=30
    )
