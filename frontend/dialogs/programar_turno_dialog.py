import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if BASE not in sys.path:
    sys.path.insert(0, BASE)

from frontend.controllers.turno_controller import TurnoController


class ProgramarTurnoDialog:
    """Dialog para programar turnos - Wizard de 3 pasos"""
    
    def __init__(self, parent, controller):
        self.controller = controller
        self.medico_seleccionado = None
        self.turno_seleccionado = None
        self.tree = None
        
        self.window = tk.Toplevel(parent)
        self.window.title("Programar Turno")
        self.window.geometry("700x500")
        self.window.resizable(False, False)
        
        # Configurar el modal
        self.window.transient(parent)
        self.window.grab_set()
        
        self._mostrar_paso_1()
    
    def _mostrar_paso_1(self):
        """Paso 1: Seleccionar médico"""
        self._limpiar_frame()
        
        frame = ttk.Frame(self.window, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="PASO 1: Selecciona un Médico", 
                 font=("Arial", 13, "bold")).pack(pady=(0, 20))
        
        try:
            medicos = self.controller.obtener_medicos()
            
            if not medicos:
                messagebox.showerror("Error", "No hay médicos disponibles")
                self.window.destroy()
                return
            
            # Crear combobox
            ttk.Label(frame, text="Médico:", font=("Arial", 10)).pack(pady=(0, 5))
            self.combo_medicos = ttk.Combobox(frame, width=50, state="readonly", font=("Arial", 10))
            self.combo_medicos.pack(pady=(0, 20))
            
            # Llenar combobox
            self.medicos_dict = {}
            opciones = []
            for medico in medicos:
                key = medico['matricula']
                self.medicos_dict[key] = medico
                opciones.append(f"Dr/Dra. {medico['nombre_completo']} (Mat: {key})")
            
            self.combo_medicos['values'] = opciones
            
            # Botón siguiente
            btn_frame = ttk.Frame(frame)
            btn_frame.pack(fill=tk.X, pady=20)
            
            ttk.Button(btn_frame, text="Siguiente →", 
                      command=self._mostrar_paso_2).pack(side=tk.RIGHT, padx=5)
            ttk.Button(btn_frame, text="Cancelar", 
                      command=self.window.destroy).pack(side=tk.RIGHT)
        
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar médicos: {str(e)}")
            self.window.destroy()
    
    def _mostrar_paso_2(self):
        """Paso 2: Seleccionar turno disponible"""
        if not self.combo_medicos.get():
            messagebox.showwarning("Advertencia", "Selecciona un médico")
            return
        
        # Obtener médico seleccionado
        texto = self.combo_medicos.get()
        try:
            matricula = int(texto.split("Mat: ")[1].rstrip(")"))
        except (ValueError, IndexError):
            messagebox.showerror("Error", "Error al parsear matrícula")
            return
        
        self.medico_seleccionado = self.medicos_dict.get(matricula)
        
        self._limpiar_frame()
        
        frame = ttk.Frame(self.window, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="PASO 2: Selecciona un Turno Libre", 
                 font=("Arial", 13, "bold")).pack(pady=(0, 20))
        
        try:
            turnos = self.controller.obtener_turnos_libres_medico(matricula)
            
            if not turnos:
                messagebox.showinfo("Info", f"No hay turnos libres para Dr/Dra. {self.medico_seleccionado['nombre_completo']}")
                self.window.destroy()
                return
            
            # Crear tabla
            tree_frame = ttk.Frame(frame)
            tree_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
            
            self.tree = ttk.Treeview(tree_frame, columns=("consultorio", "fecha", "hora"), height=10, selectmode='browse')
            self.tree.heading("#0", text="ID")
            self.tree.heading("consultorio", text="Consultorio")
            self.tree.heading("fecha", text="Fecha")
            self.tree.heading("hora", text="Horario")
            
            self.tree.column("#0", width=30)
            self.tree.column("consultorio", width=80)
            self.tree.column("fecha", width=100)
            self.tree.column("hora", width=150)
            
            # Llenar tabla
            self.turnos_dict = {}
            for turno in turnos:
                key = turno['id_turno']
                self.turnos_dict[key] = turno
                horario = f"{turno['hora_inicio']} - {turno['hora_fin']}"
                self.tree.insert("", "end", text=key, values=(
                    turno['consultorio'],
                    turno['fecha'],
                    horario
                ))
            
            # Scrollbar
            scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
            self.tree.configure(yscroll=scrollbar.set)
            
            self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            # Botones
            btn_frame = ttk.Frame(frame)
            btn_frame.pack(fill=tk.X)
            
            ttk.Button(btn_frame, text="Siguiente →", 
                      command=self._mostrar_paso_3).pack(side=tk.RIGHT, padx=5)
            ttk.Button(btn_frame, text="← Atrás", 
                      command=self._mostrar_paso_1).pack(side=tk.RIGHT)
        
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar turnos: {str(e)}")
            import traceback
            traceback.print_exc()
            self.window.destroy()
    
    def _mostrar_paso_3(self):
        """Paso 3: Seleccionar paciente"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Advertencia", "Selecciona un turno")
            return
        
        try:
            self.turno_seleccionado = self.turnos_dict[int(selection[0])]
        except (ValueError, KeyError):
            messagebox.showerror("Error", "Error al seleccionar turno")
            return
        
        self._limpiar_frame()
        
        frame = ttk.Frame(self.window, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="PASO 3: Selecciona un Paciente", 
                 font=("Arial", 13, "bold")).pack(pady=(0, 20))
        
        try:
            pacientes = self.controller.obtener_pacientes()
            
            if not pacientes:
                messagebox.showerror("Error", "No hay pacientes disponibles")
                self.window.destroy()
                return
            
            # Crear combobox
            ttk.Label(frame, text="Paciente:", font=("Arial", 10)).pack(pady=(0, 5))
            self.combo_pacientes = ttk.Combobox(frame, width=50, state="readonly", font=("Arial", 10))
            self.combo_pacientes.pack(pady=(0, 20))
            
            # Llenar combobox
            self.pacientes_dict = {}
            opciones = []
            for paciente in pacientes:
                key = paciente['id_paciente']
                self.pacientes_dict[key] = paciente
                opciones.append(f"{paciente['nombre_completo']} (ID: {key})")
            
            self.combo_pacientes['values'] = opciones
            
            # Botones
            btn_frame = ttk.Frame(frame)
            btn_frame.pack(fill=tk.X, pady=20)
            
            ttk.Button(btn_frame, text="Programar Turno ✓", 
                      command=self._programar).pack(side=tk.RIGHT, padx=5)
            ttk.Button(btn_frame, text="← Atrás", 
                      command=self._mostrar_paso_2).pack(side=tk.RIGHT)
        
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar pacientes: {str(e)}")
            self.window.destroy()
    
    def _programar(self):
        """Programa el turno"""
        if not self.combo_pacientes.get():
            messagebox.showwarning("Advertencia", "Selecciona un paciente")
            return
        
        try:
            texto = self.combo_pacientes.get()
            id_paciente = int(texto.split("ID: ")[1].rstrip(")"))
            
            # Programar turno
            if self.controller.programar_turno(self.turno_seleccionado['id_turno'], id_paciente):
                messagebox.showinfo("Éxito", "✓ Turno programado correctamente")
                self.window.destroy()
            else:
                messagebox.showerror("Error", "No se pudo programar el turno")
        except Exception as e:
            messagebox.showerror("Error", f"Error: {str(e)}")
            import traceback
            traceback.print_exc()
    
    def _limpiar_frame(self):
        """Limpia todos los widgets del frame"""
        for widget in self.window.winfo_children():
            widget.destroy()
