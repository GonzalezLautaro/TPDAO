import tkinter as tk
from tkinter import ttk


class VentanaReporteDialog(tk.Toplevel):
    """Ventana para mostrar el reporte de pacientes atendidos"""
    
    def __init__(self, parent, reporte, fecha_inicio, fecha_fin):
        super().__init__(parent)
        self.reporte = reporte
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.title("Reporte de Pacientes Atendidos")
        self.geometry("700x700")
        self._build_ui()

    def _build_ui(self):
        # Canvas con scroll
        canvas = tk.Canvas(self)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        frame = ttk.Frame(canvas)

        frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Contenido del reporte
        self._agregar_titulo(frame)
        self._agregar_total(frame)
        self._agregar_seccion(frame, "📋 Pacientes por Especialidad", self.reporte['por_especialidad'])
        self._agregar_seccion_turnos(frame, "📊 Turnos Atendidos por Especialidad", self.reporte.get('turnos_por_especialidad', {}))
        self._agregar_seccion(frame, "👨‍⚕️ Pacientes por Médico", self.reporte['por_medico'])
        self._agregar_detalle_fechas(frame)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        ttk.Button(self, text="Cerrar", command=self.destroy).pack(pady=10)

    def _agregar_titulo(self, parent):
        titulo = tk.Label(
            parent,
            text=f"Reporte: {self.fecha_inicio} a {self.fecha_fin}",
            font=("Arial", 14, "bold"),
            fg="darkblue"
        )
        titulo.pack(pady=15)

    def _agregar_total(self, parent):
        total_label = tk.Label(
            parent,
            text=f"Total General: {self.reporte['total_general']} pacientes",
            font=("Arial", 12, "bold"),
            fg="green"
        )
        total_label.pack(pady=10)
        ttk.Separator(parent, orient="horizontal").pack(fill="x", pady=10)

    def _agregar_seccion(self, parent, titulo, datos):
        tk.Label(parent, text=titulo, font=("Arial", 11, "bold")).pack(anchor="w", padx=20, pady=(10, 5))
        
        if datos:
            for clave, valor in sorted(datos.items()):
                tk.Label(parent, text=f"  • {clave}: {valor}", font=("Arial", 10)).pack(anchor="w", padx=40)
        else:
            tk.Label(parent, text="  Sin datos", font=("Arial", 10)).pack(anchor="w", padx=40)
        
        ttk.Separator(parent, orient="horizontal").pack(fill="x", pady=10)

    def _agregar_seccion_turnos(self, parent, titulo, datos):
        """Agrega sección de turnos con formato especial"""
        tk.Label(parent, text=titulo, font=("Arial", 11, "bold")).pack(anchor="w", padx=20, pady=(10, 5))
        
        if datos:
            # Ordenar por cantidad de turnos (descendente)
            datos_ordenados = sorted(datos.items(), key=lambda x: x[1], reverse=True)
            for clave, valor in datos_ordenados:
                tk.Label(
                    parent, 
                    text=f"  • {clave}: {valor} turnos", 
                    font=("Arial", 10)
                ).pack(anchor="w", padx=40)
        else:
            tk.Label(parent, text="  Sin datos", font=("Arial", 10)).pack(anchor="w", padx=40)
        
        ttk.Separator(parent, orient="horizontal").pack(fill="x", pady=10)

    def _agregar_detalle_fechas(self, parent):
        tk.Label(parent, text="📅 Detalle por Fecha", font=("Arial", 11, "bold")).pack(anchor="w", padx=20, pady=(10, 5))
        
        if self.reporte['por_fecha']:
            for fecha, datos in sorted(self.reporte['por_fecha'].items(), reverse=True):
                tk.Label(
                    parent,
                    text=f"\n{fecha} - Total: {datos['total']}",
                    font=("Arial", 10, "bold")
                ).pack(anchor="w", padx=40)
                
                for detalle in datos['detalles']:
                    texto = f"    {detalle['medico']} ({detalle['especialidad']}): {detalle['pacientes']}"
                    tk.Label(parent, text=texto, font=("Arial", 9)).pack(anchor="w", padx=50)
        else:
            tk.Label(parent, text="  Sin datos", font=("Arial", 10)).pack(anchor="w", padx=40)