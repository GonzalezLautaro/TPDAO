import tkinter as tk
from tkinter import ttk, messagebox
import os
import sys

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if BASE not in sys.path:
    sys.path.insert(0, BASE)

from data.database import Database
from frontend.dialogs.filtro_fechas_dialog import FiltrFechasDialog
from frontend.dialogs.ventana_reporte_dialog import VentanaReporteDialog


class ReportesView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self._build_ui()

    def _build_ui(self):
        # Título
        title_frame = ttk.Frame(self)
        title_frame.pack(pady=20)
        
        title_label = ttk.Label(
            title_frame,
            text="Reportes",
            font=("Arial", 18, "bold")
        )
        title_label.pack()

        # Frame contenedor para los botones
        buttons_container = ttk.Frame(self)
        buttons_container.pack(pady=30, padx=50, fill="both", expand=True)

        # Botón 1: Listado de turnos por médico en un período
        btn1 = ttk.Button(
            buttons_container,
            text="Listado de turnos por médico en un período",
            command=self._listado_turnos_medico_periodo
        )
        btn1.pack(pady=15, padx=30, fill="x", ipady=10)

        # Botón 2: Cantidad de turnos por especialidad
        btn2 = ttk.Button(
            buttons_container,
            text="Cantidad de turnos por especialidad",
            command=self._cantidad_turnos_especialidad
        )
        btn2.pack(pady=15, padx=30, fill="x", ipady=10)

        # Botón 3: Pacientes atendidos en un rango de fechas
        btn3 = ttk.Button(
            buttons_container,
            text="Pacientes atendidos en un rango de fechas",
            command=self._pacientes_atendidos_rango
        )
        btn3.pack(pady=15, padx=30, fill="x", ipady=10)

        # Botón 4: Gráfico estadístico: asistencia vs. inasistencias de pacientes
        btn4 = ttk.Button(
            buttons_container,
            text="Gráfico estadístico: asistencia vs. inasistencias de pacientes",
            command=self._grafico_asistencia
        )
        btn4.pack(pady=15, padx=30, fill="x", ipady=10)

    def _listado_turnos_medico_periodo(self):
        """Listado de turnos por médico en un período"""
        # Abrir diálogo para seleccionar médico y período
        FiltrFechasDialog(self, self._generar_reporte_turnos_medico)
    
    def _generar_reporte_turnos_medico(self, fecha_inicio, fecha_fin):
        """Genera reporte de turnos por médico en un período"""
        try:
            # Primero seleccionar médico
            db = Database()
            if not db.conectar("127.0.0.1:3306/hospital_db"):
                messagebox.showerror("Error", "No se pudo conectar a la BD")
                return
            
            # Obtener lista de médicos
            query_medicos = """
            SELECT matricula, CONCAT(nombre, ' ', apellido) as nombre_completo
            FROM Medico
            WHERE activo = 1
            ORDER BY nombre, apellido
            """
            medicos = db.obtener_registros(query_medicos)
            db.desconectar()
            
            if not medicos:
                messagebox.showwarning("Advertencia", "No hay médicos disponibles")
                return
            
            # Crear diálogo para seleccionar médico
            from tkinter import simpledialog
            opciones = [f"{m['nombre_completo']} (Mat: {m['matricula']})" for m in medicos]
            
            # Usar un diálogo simple para seleccionar médico
            dialog = tk.Toplevel(self)
            dialog.title("Seleccionar Médico")
            dialog.geometry("400x300")
            dialog.transient(self.winfo_toplevel())
            dialog.grab_set()
            
            ttk.Label(dialog, text="Selecciona un médico:", font=("Arial", 10)).pack(pady=10)
            
            medico_var = tk.StringVar()
            combo = ttk.Combobox(dialog, textvariable=medico_var, values=opciones, state="readonly", width=40)
            combo.pack(pady=10)
            
            resultado = {'medico_seleccionado': None, 'nombre_medico': None}
            
            def confirmar():
                if not combo.get():
                    messagebox.showwarning("Advertencia", "Selecciona un médico")
                    return
                
                # Extraer matrícula y nombre
                texto = combo.get()
                try:
                    matricula = int(texto.split("Mat: ")[1].rstrip(")"))
                    nombre_medico = texto.split(" (Mat:")[0]
                    resultado['medico_seleccionado'] = matricula
                    resultado['nombre_medico'] = nombre_medico
                    dialog.destroy()
                except (ValueError, IndexError):
                    messagebox.showerror("Error", "Error al parsear matrícula")
            
            ttk.Button(dialog, text="Aceptar", command=confirmar).pack(pady=10)
            ttk.Button(dialog, text="Cancelar", command=dialog.destroy).pack()
            
            dialog.wait_window()
            
            if not resultado['medico_seleccionado']:
                return
            
            matricula = resultado['medico_seleccionado']
            nombre_medico = resultado['nombre_medico']
            
            # Generar reporte
            db = Database()
            if not db.conectar("127.0.0.1:3306/hospital_db"):
                messagebox.showerror("Error", "No se pudo conectar a la BD")
                return
            
            query = """
            SELECT t.id_turno, t.fecha, t.hora_inicio, t.hora_fin, t.estado,
                   CONCAT(p.nombre, ' ', p.apellido) as paciente,
                   c.numero as consultorio
            FROM Turno t
            LEFT JOIN Paciente p ON t.id_paciente = p.id_paciente
            JOIN Consultorio c ON t.id_consultorio = c.id_consultorio
            WHERE t.matricula = %s
            AND t.fecha BETWEEN %s AND %s
            ORDER BY t.fecha, t.hora_inicio
            """
            
            turnos = db.obtener_registros(query, (matricula, fecha_inicio, fecha_fin))
            db.desconectar()
            
            if not turnos:
                messagebox.showinfo("Sin datos", "No hay turnos para este médico en el período seleccionado")
                return
            
            # Mostrar reporte
            texto_reporte = f"REPORTE DE TURNOS POR MÉDICO\n"
            texto_reporte += f"Período: {fecha_inicio} a {fecha_fin}\n"
            texto_reporte += f"Médico: {nombre_medico} (Mat: {matricula})\n"
            texto_reporte += f"{'='*60}\n\n"
            texto_reporte += f"Total de turnos: {len(turnos)}\n\n"
            
            for turno in turnos:
                paciente = turno.get('paciente', 'Libre')
                texto_reporte += f"Fecha: {turno['fecha']} | Hora: {turno['hora_inicio']} - {turno['hora_fin']}\n"
                texto_reporte += f"  Paciente: {paciente} | Consultorio: {turno['consultorio']} | Estado: {turno['estado']}\n\n"
            
            VentanaReporteDialog(self, {'texto': texto_reporte}, fecha_inicio, fecha_fin)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar reporte: {e}")
            import traceback
            traceback.print_exc()
    
    def _cantidad_turnos_especialidad(self):
        """Cantidad de turnos por especialidad"""
        try:
            db = Database()
            if not db.conectar("127.0.0.1:3306/hospital_db"):
                messagebox.showerror("Error", "No se pudo conectar a la BD")
                return
            
            query = """
            SELECT 
                e.id_especialidad,
                e.nombre as especialidad,
                COUNT(t.id_turno) as cantidad_turnos
            FROM Especialidad e
            LEFT JOIN Medico_especialidad me ON e.id_especialidad = me.id_especialidad
            LEFT JOIN Turno t ON me.matricula = t.matricula
            WHERE t.estado IN ('Programado', 'Atendido')
            GROUP BY e.id_especialidad, e.nombre
            ORDER BY cantidad_turnos DESC, e.nombre
            """
            
            resultados = db.obtener_registros(query)
            db.desconectar()
            
            if not resultados:
                messagebox.showinfo("Sin datos", "No hay turnos registrados por especialidad")
                return
            
            # Generar texto del reporte
            texto_reporte = "CANTIDAD DE TURNOS POR ESPECIALIDAD\n"
            texto_reporte += f"{'='*60}\n\n"
            
            total_general = 0
            for row in resultados:
                cantidad = row['cantidad_turnos'] or 0
                total_general += cantidad
                texto_reporte += f"{row['especialidad']}: {cantidad} turnos\n"
            
            texto_reporte += f"\n{'='*60}\n"
            texto_reporte += f"TOTAL GENERAL: {total_general} turnos\n"
            
            VentanaReporteDialog(self, {'texto': texto_reporte}, None, None)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar reporte: {e}")
            import traceback
            traceback.print_exc()

    def _pacientes_atendidos_rango(self):
        """Abre diálogo para filtrar por fechas"""
        FiltrFechasDialog(self, self._generar_reporte_pacientes)

    def _generar_reporte_pacientes(self, fecha_inicio, fecha_fin):
        """Genera el reporte con las fechas seleccionadas"""
        try:
            db = Database()
            if not db.conectar("127.0.0.1:3306/hospital_db"):
                messagebox.showerror("Error", "No se pudo conectar a la BD")
                return

            reporte = self._obtener_datos_reporte(db, fecha_inicio, fecha_fin)
            db.desconectar()

            if reporte['total_general'] == 0:
                messagebox.showinfo("Sin datos", "No hay pacientes atendidos en ese rango")
                return

            VentanaReporteDialog(self, reporte, fecha_inicio, fecha_fin)

        except Exception as e:
            messagebox.showerror("Error", f"Error al generar reporte: {e}")

    def _obtener_datos_reporte(self, db, fecha_inicio, fecha_fin):
        """Obtiene datos desde BD"""
        # Query principal: pacientes únicos por fecha y médico
        query = """
        SELECT 
            t.fecha,
            t.id_paciente,
            p.nombre AS paciente_nombre,
            p.apellido AS paciente_apellido,
            m.matricula,
            CONCAT(m.nombre, ' ', m.apellido) AS medico,
            COALESCE(
                (SELECT GROUP_CONCAT(DISTINCT e.nombre SEPARATOR ', ')
                 FROM Medico_especialidad me
                 JOIN Especialidad e ON me.id_especialidad = e.id_especialidad
                 WHERE me.matricula = m.matricula),
                'Sin especialidad'
            ) AS especialidades
        FROM Turno t
        JOIN Medico m ON t.matricula = m.matricula
        LEFT JOIN Paciente p ON t.id_paciente = p.id_paciente
        WHERE t.estado = 'Atendido' 
            AND t.fecha BETWEEN %s AND %s
            AND t.id_paciente IS NOT NULL
        ORDER BY t.fecha DESC, m.nombre, p.apellido, p.nombre
        """

        resultados = db.obtener_registros(query, (fecha_inicio, fecha_fin))
        return self._procesar_reporte(resultados, fecha_inicio, fecha_fin)

    @staticmethod
    def _procesar_reporte(resultados, fecha_inicio, fecha_fin):
        """Procesa los resultados en estructura legible"""
        reporte = {
            'fecha_inicio': fecha_inicio,
            'fecha_fin': fecha_fin,
            'total_general': 0,
            'por_fecha': {},
            'por_medico': {},
            'por_especialidad': {},
            'turnos_por_especialidad': {}  # Cantidad de turnos (no pacientes únicos)
        }

        if not resultados:
            return reporte

        # Conjuntos para contar pacientes únicos
        pacientes_unicos_general = set()
        pacientes_por_fecha = {}  # {fecha: set(id_paciente)}
        pacientes_por_medico = {}  # {medico: set(id_paciente)}
        pacientes_por_especialidad = {}  # {especialidad: set(id_paciente)}
        
        # Contador de turnos por especialidad (no pacientes únicos, sino cantidad de turnos)
        turnos_por_especialidad = {}  # {especialidad: int}
        
        # Detalles por fecha y médico
        detalles_por_fecha_medico = {}  # {(fecha, medico): {'especialidades': set, 'pacientes': set}}

        for fila in resultados:
            fecha = str(fila['fecha'])
            id_paciente = fila['id_paciente']
            medico = fila['medico']
            especialidades_str = fila.get('especialidades', 'Sin especialidad')
            
            # Dividir especialidades (pueden venir separadas por coma)
            especialidades = [e.strip() for e in especialidades_str.split(',')] if especialidades_str else ['Sin especialidad']

            # Agregar a pacientes únicos generales
            pacientes_unicos_general.add(id_paciente)

            # Por fecha
            if fecha not in pacientes_por_fecha:
                pacientes_por_fecha[fecha] = set()
                detalles_por_fecha_medico[fecha] = {}
            pacientes_por_fecha[fecha].add(id_paciente)

            # Por médico
            if medico not in pacientes_por_medico:
                pacientes_por_medico[medico] = set()
            pacientes_por_medico[medico].add(id_paciente)

            # Por especialidad (pacientes únicos)
            for especialidad in especialidades:
                if especialidad not in pacientes_por_especialidad:
                    pacientes_por_especialidad[especialidad] = set()
                pacientes_por_especialidad[especialidad].add(id_paciente)
                
                # Contar turnos por especialidad (cada turno cuenta)
                if especialidad not in turnos_por_especialidad:
                    turnos_por_especialidad[especialidad] = 0
                turnos_por_especialidad[especialidad] += 1

            # Detalles por fecha y médico
            if medico not in detalles_por_fecha_medico[fecha]:
                detalles_por_fecha_medico[fecha][medico] = {
                    'especialidades': set(),
                    'pacientes': set()
                }
            detalles_por_fecha_medico[fecha][medico]['pacientes'].add(id_paciente)
            detalles_por_fecha_medico[fecha][medico]['especialidades'].update(especialidades)

        # Construir estructura final
        reporte['total_general'] = len(pacientes_unicos_general)

        # Por fecha
        for fecha, pacientes_set in pacientes_por_fecha.items():
            reporte['por_fecha'][fecha] = {
                'total': len(pacientes_set),
                'detalles': []
            }
            # Agregar detalles por médico en esa fecha
            for medico, detalle in detalles_por_fecha_medico[fecha].items():
                especialidades_display = ', '.join(sorted(detalle['especialidades']))
                reporte['por_fecha'][fecha]['detalles'].append({
                    'medico': medico,
                    'especialidad': especialidades_display,
                    'pacientes': len(detalle['pacientes'])
                })

        # Por médico
        for medico, pacientes_set in pacientes_por_medico.items():
            reporte['por_medico'][medico] = len(pacientes_set)

        # Por especialidad (pacientes únicos)
        for especialidad, pacientes_set in pacientes_por_especialidad.items():
            reporte['por_especialidad'][especialidad] = len(pacientes_set)

        # Turnos por especialidad (cantidad total de turnos)
        reporte['turnos_por_especialidad'] = turnos_por_especialidad

        return reporte

    def _grafico_asistencia(self):
        """Genera el gráfico de asistencia vs inasistencia"""
        from reports.asistencia import grafico_asistencia_bd

        ruta = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            "reports", "out", "asistencia.png"
        )

        try:
            # Usar configuración estándar
            png = grafico_asistencia_bd(
                ruta,
                host="127.0.0.1",
                user="root",
                password="",
                database="hospital_db",
                port=3306,
                tipo="pie"
            )

            messagebox.showinfo("Reporte listo", f"Gráfico generado en:\n{png}")

            try:
                os.startfile(png)
            except Exception:
                pass

        except Exception as e:
            messagebox.showerror("Error", f"No pude generar el gráfico:\n{e}")
