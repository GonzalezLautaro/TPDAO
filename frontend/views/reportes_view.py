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
        # TODO: Implementar
        pass

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
