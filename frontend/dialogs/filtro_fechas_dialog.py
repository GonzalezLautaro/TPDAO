import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry


class FiltrFechasDialog(tk.Toplevel):
    """Diálogo para seleccionar rango de fechas"""
    
    def __init__(self, parent, callback):
        super().__init__(parent)
        self.callback = callback
        self.title("Filtrar por Fechas")
        self.geometry("400x250")
        self.resizable(False, False)
        self._build_ui()

    def _build_ui(self):
        frame = ttk.Frame(self, padding=20)
        frame.pack(fill="both", expand=True)

        # Fecha Inicio
        ttk.Label(frame, text="Fecha Inicio:", font=("Arial", 10)).pack(anchor="w", pady=(10, 5))
        self.entrada_inicio = DateEntry(
            frame,
            width=30,
            background='darkblue',
            foreground='white',
            borderwidth=2
        )
        self.entrada_inicio.pack(anchor="w", pady=(0, 15))

        # Fecha Fin
        ttk.Label(frame, text="Fecha Fin:", font=("Arial", 10)).pack(anchor="w", pady=(10, 5))
        self.entrada_fin = DateEntry(
            frame,
            width=30,
            background='darkblue',
            foreground='white',
            borderwidth=2
        )
        self.entrada_fin.pack(anchor="w", pady=(0, 20))

        # Botones
        frame_botones = ttk.Frame(frame)
        frame_botones.pack(fill="x", pady=(20, 10))

        # Botón Cancelar
        btn_cancelar = tk.Button(
            frame_botones,
            text="Cancelar",
            command=self.destroy,
            width=12,
            height=2,
            font=("Arial", 10),
            bg="#f0f0f0",
            activebackground="#e0e0e0",
            relief=tk.RAISED,
            bd=2,
            cursor="hand2"
        )
        btn_cancelar.pack(side="right", padx=(10, 5), ipadx=10, ipady=5)

        # Botón Generar
        btn_generar = tk.Button(
            frame_botones,
            text="Generar",
            command=self._aceptar,
            width=12,
            height=2,
            font=("Arial", 10, "bold"),
            bg="#4CAF50",
            fg="white",
            activebackground="#45a049",
            activeforeground="white",
            relief=tk.RAISED,
            bd=2,
            cursor="hand2"
        )
        btn_generar.pack(side="right", padx=(5, 10), ipadx=10, ipady=5)

    def _aceptar(self):
        fecha_inicio = self.entrada_inicio.get_date()
        fecha_fin = self.entrada_fin.get_date()

        if fecha_inicio > fecha_fin:
            messagebox.showerror("Error", "Fecha inicio debe ser menor a fecha fin")
            return

        self.destroy()
        self.callback(fecha_inicio, fecha_fin)