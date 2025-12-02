import tkinter as tk
from tkinter import ttk
from .views.turnos_view import TurnosView
from .views.pacientes_view import PacientesView
from .views.medicos_view import MedicosView
from .views.especialidades_view import EspecialidadesView
from .views.reportes_view import ReportesView
from .styles.theme import setup_theme


def run_app():
    root = tk.Tk()
    root.title("Turnero Médico – Front Tkinter")
    root.geometry("1100x650")

    setup_theme()

    nb = ttk.Notebook(root)
    nb.pack(fill="both", expand=True)

    nb.add(TurnosView(nb), text="Turnos")
    nb.add(PacientesView(nb), text="Pacientes")
    nb.add(MedicosView(nb), text="Médicos")
    nb.add(EspecialidadesView(nb), text="Especialidades")
    nb.add(ReportesView(nb), text="Reportes")

    root.mainloop()
