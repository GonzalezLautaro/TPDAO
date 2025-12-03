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
        # TODO: Implementar
        pass

    def _cantidad_turnos_especialidad(self):
        """Genera un reporte de cantidad de turnos por especialidad"""
        from frontend.dialogs.filtro_fechas_dialog import FiltrFechasDialog
        FiltrFechasDialog(self, self._generar_reporte_especialidad)

    def _generar_reporte_especialidad(self, fecha_inicio, fecha_fin):
        """Consulta la BD y muestra reporte de turnos por especialidad"""
        try:
            db = Database()
            if not db.conectar():
                messagebox.showerror("Error", "No se pudo conectar a la BD")
                return

            query = """
            SELECT 
                e.nombre AS especialidad,
                SUM(CASE WHEN t.estado = 'Atendido'     THEN 1 ELSE 0 END) AS atendidos,
                SUM(CASE WHEN t.estado = 'Inasistencia' THEN 1 ELSE 0 END) AS inasistencias,
                SUM(CASE WHEN t.estado = 'Cancelado'    THEN 1 ELSE 0 END) AS cancelados,
                SUM(CASE WHEN t.estado = 'Programado'   THEN 1 ELSE 0 END) AS programados,
                SUM(CASE 
                        WHEN t.estado IN ('Atendido','Inasistencia','Cancelado','Programado')
                        THEN 1 ELSE 0 
                    END) AS total
            FROM Turno t
            JOIN Medico m               ON m.matricula = t.matricula
            JOIN Medico_especialidad me ON me.matricula = m.matricula
            JOIN Especialidad e         ON e.id_especialidad = me.id_especialidad
            WHERE t.fecha BETWEEN %s AND %s
            AND t.estado IN ('Atendido','Inasistencia','Cancelado','Programado')
            GROUP BY e.nombre
            ORDER BY total DESC;
            """

            datos = db.obtener_registros(query, (fecha_inicio, fecha_fin))
            db.desconectar()

            if not datos:
                messagebox.showinfo("Sin datos", "No hay turnos en ese rango")
                return

            # Mostrar ventana con tabla
            from frontend.dialogs.ventana_tabla_especialidades import VentanaTablaEspecialidades
            VentanaTablaEspecialidades(self, datos, fecha_inicio, fecha_fin)

        except Exception as e:
            messagebox.showerror("Error", f"Error al generar reporte: {e}")


    def _mostrar_tabla_especialidades(self, filas, fecha_inicio, fecha_fin):
        """Muestra una ventana con la tabla (Treeview) y totales al pie"""
        win = tk.Toplevel(self)
        win.title("Turnos por especialidad")
        win.geometry("900x500")

        header = ttk.Label(
            win,
            text=f"Cantidad de turnos por especialidad – {fecha_inicio} a {fecha_fin}",
            font=("Arial", 12, "bold")
        )
        header.pack(pady=10)

        cols = ("especialidad", "total", "atendidos", "inasistencias", "cancelados", "programados")
        tree = ttk.Treeview(win, columns=cols, show="headings", height=18)
        widths = [280, 90, 100, 110, 100, 110]
        headers = ["Especialidad", "Total", "Atendidos", "Inasist.", "Cancelados", "Programados"]

        for c, w, h in zip(cols, widths, headers):
            tree.heading(c, text=h)
            tree.column(c, width=w, anchor="center")

        # cargar filas y acumular totales
        tot_total = tot_at = tot_in = tot_ca = tot_pr = 0
        for f in filas:
            row = (
                f["especialidad"],
                f["total"] or 0,
                f["atendidos"] or 0,
                f["inasistencias"] or 0,
                f["cancelados"] or 0,
                f["programados"] or 0,
            )
            tot_total += row[1]
            tot_at += row[2]
            tot_in += row[3]
            tot_ca += row[4]
            tot_pr += row[5]
            tree.insert("", "end", values=row)

        tree.pack(fill="both", expand=True, padx=10, pady=(0, 8))

        # Totales
        footer = ttk.Frame(win)
        footer.pack(fill="x", padx=10, pady=6)

        ttk.Label(
            footer,
            text=(
                f"Totales  |  Total: {tot_total}  |  "
                f"Atendidos: {tot_at}  |  "
                f"Inasist.: {tot_in}  |  "
                f"Cancelados: {tot_ca}  |  "
                f"Programados: {tot_pr}"
            ),
            font=("Arial", 10, "bold")
        ).pack(side="left")

        ttk.Button(footer, text="Cerrar", command=win.destroy).pack(side="right")




    def _pacientes_atendidos_rango(self):
        """Abre diálogo para filtrar por fechas"""
        FiltrFechasDialog(self, self._generar_reporte_pacientes)

    def _generar_reporte_pacientes(self, fecha_inicio, fecha_fin):
        """Genera el reporte con las fechas seleccionadas"""
        try:
            db = Database()
            if not db.conectar():
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
        query = """
        SELECT 
            t.fecha,
            COUNT(DISTINCT t.id_paciente) AS total_pacientes_dia,
            m.matricula,
            CONCAT(m.nombre, ' ', m.apellido) AS medico,
            e.nombre AS especialidad,
            COUNT(DISTINCT t.id_paciente) AS pacientes_por_medico
        FROM Turno t
        JOIN Medico m ON t.matricula = m.matricula
        JOIN Medico_especialidad me ON m.matricula = me.matricula
        JOIN Especialidad e ON me.id_especialidad = e.id_especialidad
        WHERE t.estado = 'Atendido' 
            AND t.fecha BETWEEN %s AND %s
        GROUP BY t.fecha, m.matricula, e.id_especialidad
        ORDER BY t.fecha DESC, m.nombre
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
            'por_especialidad': {}
        }

        if not resultados:
            return reporte

        for fila in resultados:
            fecha = str(fila['fecha'])
            medico = fila['medico']
            especialidad = fila['especialidad']
            pacientes = fila['pacientes_por_medico']

            reporte['total_general'] += pacientes

            if fecha not in reporte['por_fecha']:
                reporte['por_fecha'][fecha] = {'total': 0, 'detalles': []}
            reporte['por_fecha'][fecha]['total'] += pacientes
            reporte['por_fecha'][fecha]['detalles'].append({
                'medico': medico,
                'especialidad': especialidad,
                'pacientes': pacientes
            })

            reporte['por_medico'][medico] = reporte['por_medico'].get(medico, 0) + pacientes
            reporte['por_especialidad'][especialidad] = reporte['por_especialidad'].get(especialidad, 0) + pacientes

        return reporte

    def _grafico_asistencia(self):
        """Genera el gráfico de asistencia vs inasistencia"""
        from reports.asistencia import grafico_asistencia_bd

        ruta = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            "reports", "out", "asistencia.png"
        )

        try:
            db_config = Database()
            
            png = grafico_asistencia_bd(
                ruta,
                host=db_config.host,
                user=db_config.user,
                password=db_config.password,
                database=db_config.database,
                port=db_config.port,
                tipo="pie"
            )

            messagebox.showinfo("Reporte listo", f"Gráfico generado en:\n{png}")

            try:
                os.startfile(png)
            except Exception:
                pass

        except Exception as e:
            messagebox.showerror("Error", f"No pude generar el gráfico:\n{e}")
    
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
            'por_especialidad': {}
        }

        if not resultados:
            return reporte

        # Conjuntos para contar pacientes únicos
        pacientes_unicos_general = set()
        pacientes_por_fecha = {}  # {fecha: set(id_paciente)}
        pacientes_por_medico = {}  # {medico: set(id_paciente)}
        pacientes_por_especialidad = {}  # {especialidad: set(id_paciente)}
        
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
        
