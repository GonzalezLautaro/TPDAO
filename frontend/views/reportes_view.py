import tkinter as tk
from tkinter import ttk


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
        # TODO: Implementar
        pass

    def _grafico_asistencia(self):
        # TODO: Implementar
        pass
