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
        """Genera un reporte de listado de turnos por médico en un período"""
        FiltrFechasDialog(self, self._generar_reporte_turnos_medico)

    def _generar_reporte_turnos_medico(self, fecha_inicio, fecha_fin):
        """Consulta la BD y muestra reporte de turnos por médico"""
        try:
            db = Database()
            if not db.conectar():
                messagebox.showerror("Error", "No se pudo conectar a la BD")
                return

            query = """
            SELECT
                CONCAT(m.nombre, ' ', m.apellido) AS medico,
                COALESCE(
                    (SELECT GROUP_CONCAT(DISTINCT e.nombre SEPARATOR ', ')
                     FROM Medico_especialidad me
                     JOIN Especialidad e ON me.id_especialidad = e.id_especialidad
                     WHERE me.matricula = m.matricula),
                    'Sin especialidad'
                ) AS especialidad,
                t.fecha,
                t.hora_inicio,
                t.hora_fin,
                CONCAT(p.nombre, ' ', p.apellido) AS paciente,
                t.estado
            FROM Turno t
            JOIN Medico m ON t.matricula = m.matricula
            LEFT JOIN Paciente p ON t.id_paciente = p.id_paciente
            WHERE t.fecha BETWEEN %s AND %s
                AND t.estado IN ('Programado', 'Atendido', 'Cancelado', 'Inasistencia')
            ORDER BY m.apellido, m.nombre, t.fecha, t.hora_inicio
            """

            datos = db.obtener_registros(query, (fecha_inicio, fecha_fin))
            db.desconectar()

            if not datos:
                messagebox.showinfo("Sin datos", "No hay turnos en ese rango")
                return

            # Mostrar ventana con tabla
            from frontend.dialogs.ventana_tabla_turnos_medico import VentanaTablaTurnosMedico
            VentanaTablaTurnosMedico(self, datos, fecha_inicio, fecha_fin)

        except Exception as e:
            messagebox.showerror("Error", f"Error al generar reporte: {e}")
            import traceback
            traceback.print_exc()

    def _cantidad_turnos_especialidad(self):
        """Genera un reporte de cantidad de turnos por especialidad"""
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
        pacientes_por_fecha = {}
        pacientes_por_medico = {}
        pacientes_por_especialidad = {}
        detalles_por_fecha_medico = {}

        for fila in resultados:
            fecha = str(fila['fecha'])
            id_paciente = fila['id_paciente']
            medico = fila['medico']
            especialidades_str = fila.get('especialidades', 'Sin especialidad')

            especialidades = [e.strip() for e in especialidades_str.split(',')] if especialidades_str else ['Sin especialidad']

            pacientes_unicos_general.add(id_paciente)

            if fecha not in pacientes_por_fecha:
                pacientes_por_fecha[fecha] = set()
                detalles_por_fecha_medico[fecha] = {}
            pacientes_por_fecha[fecha].add(id_paciente)

            if medico not in pacientes_por_medico:
                pacientes_por_medico[medico] = set()
            pacientes_por_medico[medico].add(id_paciente)

            for especialidad in especialidades:
                if especialidad not in pacientes_por_especialidad:
                    pacientes_por_especialidad[especialidad] = set()
                pacientes_por_especialidad[especialidad].add(id_paciente)

            if medico not in detalles_por_fecha_medico[fecha]:
                detalles_por_fecha_medico[fecha][medico] = {
                    'especialidades': set(),
                    'pacientes': set()
                }
            detalles_por_fecha_medico[fecha][medico]['pacientes'].add(id_paciente)
            detalles_por_fecha_medico[fecha][medico]['especialidades'].update(especialidades)

        reporte['total_general'] = len(pacientes_unicos_general)

        for fecha, pacientes_set in pacientes_por_fecha.items():
            reporte['por_fecha'][fecha] = {
                'total': len(pacientes_set),
                'detalles': []
            }
            for medico, detalle in detalles_por_fecha_medico[fecha].items():
                especialidades_display = ', '.join(sorted(detalle['especialidades']))
                reporte['por_fecha'][fecha]['detalles'].append({
                    'medico': medico,
                    'especialidad': especialidades_display,
                    'pacientes': len(detalle['pacientes'])
                })

        for medico, pacientes_set in pacientes_por_medico.items():
            reporte['por_medico'][medico] = len(pacientes_set)

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
            import traceback
            traceback.print_exc()