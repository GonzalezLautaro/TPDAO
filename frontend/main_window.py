import tkinter as tk
from tkinter import messagebox
import traceback
import sys
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE not in sys.path:
    sys.path.insert(0, BASE)

from frontend.views.turnos_view import TurnosView
from frontend.views.pacientes_view import PacientesView
from frontend.views.medicos_view import MedicosView
from frontend.views.especialidades_view import EspecialidadesView


class MainWindow(tk.Tk):
    """Ventana principal de la aplicación"""
    
    def __init__(self):
        super().__init__()
        
        self.title("Sistema de Gestión Médica")
        self.geometry("1200x700")
        self.resizable(True, True)
        
        # Estilo
        style = self._configurar_estilo()
        
        # Frame superior con título
        header_frame = tk.Frame(self, bg="#2c3e50", height=60)
        header_frame.pack(fill=tk.X, side=tk.TOP)
        header_frame.pack_propagate(False)
        
        titulo = tk.Label(
            header_frame,
            text="🏥 SISTEMA DE GESTIÓN MÉDICA",
            font=("Arial", 16, "bold"),
            bg="#2c3e50",
            fg="white"
        )
        titulo.pack(pady=10)
        
        # Notebook (tabs)
        try:
            from tkinter import ttk
            self.notebook = ttk.Notebook(self)
            self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            # Agregar tabs con manejo de errores individual
            self._agregar_tab_turnos()
            self._agregar_tab_pacientes()
            self._agregar_tab_medicos()
            self._agregar_tab_especialidades()
            
        except Exception as e:
            messagebox.showerror("Error Crítico", f"Error al crear tabs: {str(e)}\n\n{traceback.format_exc()}")
            raise
    
    def _agregar_tab_turnos(self):
        """Agrega tab de turnos"""
        try:
            turnos_view = TurnosView(self.notebook)
            self.notebook.add(turnos_view, text="📅 Turnos")
            print("[OK] Tab Turnos cargado")
        except Exception as e:
            print(f"[ERROR] Error al cargar tab Turnos: {str(e)}")
            traceback.print_exc()
            # No lanzar excepción, solo mostrar en consola
    
    def _agregar_tab_pacientes(self):
        """Agrega tab de pacientes"""
        try:
            pacientes_view = PacientesView(self.notebook)
            self.notebook.add(pacientes_view, text="👥 Pacientes")
            print("[OK] Tab Pacientes cargado")
        except Exception as e:
            print(f"[ERROR] Error al cargar tab Pacientes: {str(e)}")
            traceback.print_exc()
    
    def _agregar_tab_medicos(self):
        """Agrega tab de médicos"""
        try:
            medicos_view = MedicosView(self.notebook)
            self.notebook.add(medicos_view, text="👨‍⚕️ Médicos")
            print("[OK] Tab Médicos cargado")
        except Exception as e:
            print(f"[ERROR] Error al cargar tab Médicos: {str(e)}")
            traceback.print_exc()
    
    def _agregar_tab_especialidades(self):
        """Agrega tab de especialidades"""
        try:
            especialidades_view = EspecialidadesView(self.notebook)
            self.notebook.add(especialidades_view, text="🏥 Especialidades")
            print("[OK] Tab Especialidades cargado")
        except Exception as e:
            print(f"[ERROR] Error al cargar tab Especialidades: {str(e)}")
            traceback.print_exc()
    
    def _configurar_estilo(self):
        """Configura el estilo de la aplicación"""
        try:
            from tkinter import ttk
            style = ttk.Style()
            style.theme_use('clam')
            return style
        except:
            return None


def run_app():
    """Ejecuta la aplicación"""
    try:
        app = MainWindow()
        app.mainloop()
    except Exception as e:
        print(f"[ERROR] Error fatal: {str(e)}")
        traceback.print_exc()
        raise


if __name__ == "__main__":
    run_app()
