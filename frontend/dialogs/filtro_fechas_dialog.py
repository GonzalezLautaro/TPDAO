import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry


class FiltrFechasDialog:
    def __init__(self, parent, callback):
        self.callback = callback

        self.window = tk.Toplevel(parent)
        self.window.title("Filtrar por Fechas")
        self.window.geometry("350x250")
        self.window.resizable(False, False)
        self.window.grab_set()

        frm = ttk.Frame(self.window, padding=20)
        frm.pack(fill="both", expand=True)

        # ---- Fecha Inicio ----
        ttk.Label(frm, text="Fecha Inicio:").pack(anchor="w")
        self.fecha_inicio = DateEntry(
    frm, width=18, date_pattern="y-mm-dd",
    state="normal", showweeknumbers=False
)


        self.fecha_inicio.pack(pady=5)

        # Forzar foco correctamente (FIX DEL BUG)
        self.window.after(150, lambda: self.fecha_inicio.focus_force())

        # ---- Fecha Fin ----
        ttk.Label(frm, text="Fecha Fin:").pack(anchor="w", pady=(15, 0))
        self.fecha_fin = DateEntry(
    frm, width=18, date_pattern="y-mm-dd",
    state="normal", showweeknumbers=False
)

        self.fecha_fin.pack(pady=5)

        # ---- Botones ----
        btns = ttk.Frame(frm)
        btns.pack(pady=25)

        ttk.Button(btns, text="Cancelar", command=self.window.destroy)\
            .pack(side="left", padx=10)

        ttk.Button(btns, text="Generar", command=self._emitir)\
            .pack(side="left", padx=10)

    def _emitir(self):
        f1 = self.fecha_inicio.get_date()
        f2 = self.fecha_fin.get_date()
        self.callback(f1, f2)
        self.window.destroy()
