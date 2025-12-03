import tkinter as tk
from tkinter import ttk

class VentanaTablaEspecialidades(tk.Toplevel):
    def __init__(self, parent, datos, fecha_inicio, fecha_fin):
        super().__init__(parent)
        self.title("Turnos por especialidad")
        self.geometry("1000x550")

        titulo = ttk.Label(
            self,
            text=f"Cantidad de turnos por especialidad – {fecha_inicio} a {fecha_fin}",
            font=("Arial", 15, "bold")
        )
        titulo.pack(pady=15)

        frame = ttk.Frame(self)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        cols = ["Especialidad", "Total", "Atendidos", "Inasist.", "Cancelados", "Programados"]
        tree = ttk.Treeview(frame, columns=cols, show="headings")
        for c in cols:
            tree.heading(c, text=c)
            tree.column(c, width=150)

        for fila in datos:
            tree.insert("", "end", values=(
                fila["especialidad"],
                fila["total"],
                fila["atendidos"],
                fila["inasistencias"],
                fila["cancelados"],
                fila["programados"],
            ))

        tree.pack(fill="both", expand=True)
