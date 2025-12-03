import tkinter as tk
from tkinter import ttk


class VerHistorialDialog:
    def __init__(self, parent, nombre, apellido, historial):
        self.window = tk.Toplevel(parent)
        self.window.title("Historial Clínico")
        self.window.geometry("900x600")
        self.window.resizable(True, True)
        
        # Container principal
        container = ttk.Frame(self.window, padding=15)
        container.pack(fill="both", expand=True)
        
        # Título
        titulo = ttk.Label(
            container,
            text=f"Historial Clínico: {nombre} {apellido}",
            font=("Arial", 14, "bold")
        )
        titulo.pack(pady=(0, 15))
        
        # Frame para tabla
        tabla_frame = ttk.LabelFrame(container, text="Registro de Consultas", padding=10)
        tabla_frame.pack(fill="both", expand=True, pady=(0, 10))
        
        # Crear Treeview
        self.tree = ttk.Treeview(
            tabla_frame,
            columns=("fecha", "hora", "medico", "tratamiento", "observaciones"),
            show="headings",
            height=15
        )
        
        headers = [
            ("fecha", "Fecha", 100),
            ("hora", "Hora", 80),
            ("medico", "Médico", 150),
            ("tratamiento", "Tratamiento", 250),
            ("observaciones", "Observaciones", 250)
        ]
        
        for col, text, width in headers:
            self.tree.heading(col, text=text)
            self.tree.column(col, width=width)
        
        scrollbar = ttk.Scrollbar(tabla_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Agregar datos
        for h in historial:
            self.tree.insert("", "end", values=(
                str(h['fecha']),
                str(h['hora_inicio']) if h.get('hora_inicio') else "",
                h['medico'],
                h['tratamiento'] if h.get('tratamiento') else "---",
                h['observaciones'] if h.get('observaciones') else "---"
            ))
        
        # Frame de botones
        btn_frame = ttk.Frame(container)
        btn_frame.pack(fill="x", side="bottom")
        
        btn_frame.columnconfigure(0, weight=1)
        ttk.Button(btn_frame, text="Cerrar", command=self.window.destroy).grid(row=0, column=1, padx=5)
