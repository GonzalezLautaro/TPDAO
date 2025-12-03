import tkinter as tk
from tkinter import ttk
from .views.turnos_view import TurnosView
from .views.pacientes_view import PacientesView
from .views.medicos_view import MedicosView
from .views.especialidades_view import EspecialidadesView
from .views.reportes_view import ReportesView
from .styles.theme import setup_theme

# Importar scheduler de notificaciones
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from gestores.scheduler_notificaciones import SchedulerNotificaciones


def run_app():
    root = tk.Tk()
    root.title("Turnero Médico – Front Tkinter")
    root.geometry("1100x650")

    setup_theme()

    # ✨ INICIAR SCHEDULER DE NOTIFICACIONES
    scheduler = SchedulerNotificaciones(intervalo_minutos=5)
    scheduler.iniciar()
    print("📲 Sistema de notificaciones automáticas activado")

    nb = ttk.Notebook(root)
    nb.pack(fill="both", expand=True)

    nb.add(TurnosView(nb), text="Turnos")
    nb.add(PacientesView(nb), text="Pacientes")
    nb.add(MedicosView(nb), text="Médicos")
    nb.add(EspecialidadesView(nb), text="Especialidades")
    nb.add(ReportesView(nb), text="Reportes")

    # Detener scheduler al cerrar la aplicación
    def on_closing():
        scheduler.detener()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)

    root.mainloop()