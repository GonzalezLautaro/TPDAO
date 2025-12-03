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
        # Frame principal con padding
        main_frame = ttk.Frame(self, padding=10)
        main_frame.pack(fill="both", expand=True)
        
        # Canvas con scroll
        canvas = tk.Canvas(main_frame, bg="#f5f5f5", highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        frame = ttk.Frame(canvas, padding=20)

        frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Verificar si es un reporte de texto simple o estructurado
        if 'texto' in self.reporte:
            # Reporte de texto simple
            self._agregar_titulo_simple(frame)
            self._agregar_texto_reporte(frame, self.reporte['texto'])
        else:
            # Reporte estructurado (pacientes atendidos)
            self._agregar_titulo(frame)
            self._agregar_total(frame)
            self._agregar_seccion(frame, "📋 Pacientes por Especialidad", self.reporte.get('por_especialidad', {}))
            self._agregar_seccion_turnos(frame, "📊 Turnos Atendidos por Especialidad", self.reporte.get('turnos_por_especialidad', {}))
            self._agregar_seccion(frame, "👨‍⚕️ Pacientes por Médico", self.reporte.get('por_medico', {}))
            self._agregar_detalle_fechas(frame)

        canvas.pack(side="left", fill="both", expand=True, padx=(0, 5))
        scrollbar.pack(side="right", fill="y")

        # Botón cerrar mejorado
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill="x", pady=(10, 0))
        
        btn_cerrar = tk.Button(
            btn_frame,
            text="Cerrar",
            command=self.destroy,
            width=15,
            height=1,
            font=("Arial", 10, "bold"),
            bg="#6c757d",
            fg="white",
            activebackground="#5a6268",
            activeforeground="white",
            relief=tk.RAISED,
            bd=2,
            cursor="hand2"
        )
        btn_cerrar.pack(side="right", padx=10)

    def _agregar_titulo_simple(self, parent):
        """Título simple para reportes de texto"""
        titulo_frame = tk.Frame(parent, bg="#2c3e50", relief=tk.RAISED, bd=2)
        titulo_frame.pack(fill="x", pady=(0, 20), padx=10)
        
        titulo = tk.Label(
            titulo_frame,
            text="📊 Reporte",
            font=("Arial", 16, "bold"),
            fg="white",
            bg="#2c3e50"
        )
        titulo.pack(pady=10)
        
        if self.fecha_inicio and self.fecha_fin:
            subtitulo = tk.Label(
                titulo_frame,
                text=f"Período: {self.fecha_inicio} a {self.fecha_fin}",
                font=("Arial", 11),
                fg="#ecf0f1",
                bg="#2c3e50"
            )
            subtitulo.pack(pady=(0, 10))
    
    def _agregar_texto_reporte(self, parent, texto):
        """Agrega texto del reporte en formato simple"""
        texto_frame = tk.Frame(parent, bg="white", relief=tk.GROOVE, bd=1)
        texto_frame.pack(fill="both", expand=True, padx=10, pady=(0, 15))
        
        # Text widget con scroll
        text_widget = tk.Text(
            texto_frame,
            wrap=tk.WORD,
            font=("Courier", 10),
            bg="white",
            fg="#2c3e50",
            padx=15,
            pady=15,
            relief=tk.FLAT
        )
        text_widget.insert("1.0", texto)
        text_widget.config(state=tk.DISABLED)
        
        scrollbar_text = ttk.Scrollbar(texto_frame, orient="vertical", command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar_text.set)
        
        text_widget.pack(side="left", fill="both", expand=True)
        scrollbar_text.pack(side="right", fill="y")
    
    def _agregar_titulo(self, parent):
        # Frame para el título con fondo
        titulo_frame = tk.Frame(parent, bg="#2c3e50", relief=tk.RAISED, bd=2)
        titulo_frame.pack(fill="x", pady=(0, 20), padx=10)
        
        titulo = tk.Label(
            titulo_frame,
            text=f"📊 Reporte de Pacientes Atendidos",
            font=("Arial", 16, "bold"),
            fg="white",
            bg="#2c3e50"
        )
        titulo.pack(pady=10)
        
        subtitulo = tk.Label(
            titulo_frame,
            text=f"Período: {self.fecha_inicio} a {self.fecha_fin}",
            font=("Arial", 11),
            fg="#ecf0f1",
            bg="#2c3e50"
        )
        subtitulo.pack(pady=(0, 10))

    def _agregar_total(self, parent):
        # Frame para el total con estilo destacado
        total_frame = tk.Frame(parent, bg="#27ae60", relief=tk.RAISED, bd=2)
        total_frame.pack(fill="x", pady=(0, 20), padx=10)
        
        total_label = tk.Label(
            total_frame,
            text=f"Total General: {self.reporte['total_general']} pacientes únicos",
            font=("Arial", 14, "bold"),
            fg="white",
            bg="#27ae60"
        )
        total_label.pack(pady=12)

    def _agregar_seccion(self, parent, titulo, datos):
        # Frame para la sección con borde
        seccion_frame = tk.Frame(parent, bg="white", relief=tk.GROOVE, bd=1)
        seccion_frame.pack(fill="x", pady=(0, 15), padx=10)
        
        # Título de la sección
        titulo_label = tk.Label(
            seccion_frame,
            text=titulo,
            font=("Arial", 12, "bold"),
            fg="#2c3e50",
            bg="white",
            anchor="w"
        )
        titulo_label.pack(fill="x", padx=15, pady=(12, 8))
        
        # Contenido
        contenido_frame = tk.Frame(seccion_frame, bg="white")
        contenido_frame.pack(fill="x", padx=15, pady=(0, 12))
        
        if datos:
            for clave, valor in sorted(datos.items()):
                item_frame = tk.Frame(contenido_frame, bg="white")
                item_frame.pack(fill="x", pady=3)
                
                tk.Label(
                    item_frame,
                    text="•",
                    font=("Arial", 12),
                    fg="#3498db",
                    bg="white"
                ).pack(side="left", padx=(0, 8))
                
                tk.Label(
                    item_frame,
                    text=f"{clave}:",
                    font=("Arial", 10, "bold"),
                    fg="#34495e",
                    bg="white"
                ).pack(side="left", padx=(0, 5))
                
                tk.Label(
                    item_frame,
                    text=f"{valor}",
                    font=("Arial", 10),
                    fg="#27ae60",
                    bg="white"
                ).pack(side="left")
        else:
            tk.Label(
                contenido_frame,
                text="Sin datos disponibles",
                font=("Arial", 10, "italic"),
                fg="#95a5a6",
                bg="white"
            ).pack(anchor="w", pady=5)

    def _agregar_seccion_turnos(self, parent, titulo, datos):
        """Agrega sección de turnos con formato especial"""
        # Frame para la sección con borde
        seccion_frame = tk.Frame(parent, bg="white", relief=tk.GROOVE, bd=1)
        seccion_frame.pack(fill="x", pady=(0, 15), padx=10)
        
        # Título de la sección
        titulo_label = tk.Label(
            seccion_frame,
            text=titulo,
            font=("Arial", 12, "bold"),
            fg="#2c3e50",
            bg="white",
            anchor="w"
        )
        titulo_label.pack(fill="x", padx=15, pady=(12, 8))
        
        # Contenido
        contenido_frame = tk.Frame(seccion_frame, bg="white")
        contenido_frame.pack(fill="x", padx=15, pady=(0, 12))
        
        if datos:
            # Ordenar por cantidad de turnos (descendente)
            datos_ordenados = sorted(datos.items(), key=lambda x: x[1], reverse=True)
            for clave, valor in datos_ordenados:
                item_frame = tk.Frame(contenido_frame, bg="white")
                item_frame.pack(fill="x", pady=3)
                
                tk.Label(
                    item_frame,
                    text="•",
                    font=("Arial", 12),
                    fg="#e74c3c",
                    bg="white"
                ).pack(side="left", padx=(0, 8))
                
                tk.Label(
                    item_frame,
                    text=f"{clave}:",
                    font=("Arial", 10, "bold"),
                    fg="#34495e",
                    bg="white"
                ).pack(side="left", padx=(0, 5))
                
                tk.Label(
                    item_frame,
                    text=f"{valor} turnos",
                    font=("Arial", 10),
                    fg="#e74c3c",
                    bg="white"
                ).pack(side="left")
        else:
            tk.Label(
                contenido_frame,
                text="Sin datos disponibles",
                font=("Arial", 10, "italic"),
                fg="#95a5a6",
                bg="white"
            ).pack(anchor="w", pady=5)

    def _agregar_detalle_fechas(self, parent):
        # Frame para la sección con borde
        seccion_frame = tk.Frame(parent, bg="white", relief=tk.GROOVE, bd=1)
        seccion_frame.pack(fill="x", pady=(0, 15), padx=10)
        
        # Título de la sección
        titulo_label = tk.Label(
            seccion_frame,
            text="📅 Detalle por Fecha",
            font=("Arial", 12, "bold"),
            fg="#2c3e50",
            bg="white",
            anchor="w"
        )
        titulo_label.pack(fill="x", padx=15, pady=(12, 8))
        
        # Contenido
        contenido_frame = tk.Frame(seccion_frame, bg="white")
        contenido_frame.pack(fill="x", padx=15, pady=(0, 12))
        
        if self.reporte['por_fecha']:
            for fecha, datos in sorted(self.reporte['por_fecha'].items(), reverse=True):
                # Frame para cada fecha
                fecha_frame = tk.Frame(contenido_frame, bg="#ecf0f1", relief=tk.RAISED, bd=1)
                fecha_frame.pack(fill="x", pady=8, padx=5)
                
                # Título de la fecha
                fecha_label = tk.Label(
                    fecha_frame,
                    text=f"📆 {fecha} - Total: {datos['total']} pacientes",
                    font=("Arial", 11, "bold"),
                    fg="#2c3e50",
                    bg="#ecf0f1"
                )
                fecha_label.pack(anchor="w", padx=10, pady=(8, 5))
                
                # Detalles de médicos
                detalles_frame = tk.Frame(fecha_frame, bg="#ecf0f1")
                detalles_frame.pack(fill="x", padx=10, pady=(0, 8))
                
                for detalle in datos['detalles']:
                    detalle_item = tk.Frame(detalles_frame, bg="#ecf0f1")
                    detalle_item.pack(fill="x", pady=2)
                    
                    tk.Label(
                        detalle_item,
                        text="  →",
                        font=("Arial", 10),
                        fg="#7f8c8d",
                        bg="#ecf0f1"
                    ).pack(side="left", padx=(0, 5))
                    
                    tk.Label(
                        detalle_item,
                        text=f"{detalle['medico']}",
                        font=("Arial", 10, "bold"),
                        fg="#34495e",
                        bg="#ecf0f1"
                    ).pack(side="left", padx=(0, 5))
                    
                    tk.Label(
                        detalle_item,
                        text=f"({detalle['especialidad']})",
                        font=("Arial", 9),
                        fg="#7f8c8d",
                        bg="#ecf0f1"
                    ).pack(side="left", padx=(0, 5))
                    
                    tk.Label(
                        detalle_item,
                        text=f": {detalle['pacientes']} pacientes",
                        font=("Arial", 10),
                        fg="#27ae60",
                        bg="#ecf0f1"
                    ).pack(side="left")
        else:
            tk.Label(
                contenido_frame,
                text="Sin datos disponibles",
                font=("Arial", 10, "italic"),
                fg="#95a5a6",
                bg="white"
            ).pack(anchor="w", pady=5)