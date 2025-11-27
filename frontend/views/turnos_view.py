import tkinter as tk
from tkinter import ttk, messagebox
from ..controllers.turno_controller import TurnoController
from ..dialogs.programar_turno_dialog import ProgramarTurnoDialog


class TurnosView(ttk.Frame):
    """Vista para gestionar turnos"""
    
    def __init__(self, parent):
        super().__init__(parent, padding=12)
        self.ctrl = TurnoController()
        
        # Frame superior con título y botones
        top_frame = ttk.Frame(self)
        top_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(top_frame, text="📅 TURNOS PROGRAMADOS", font=("Arial", 12, "bold")).pack(side=tk.LEFT)
        
        btn_frame = ttk.Frame(top_frame)
        btn_frame.pack(side=tk.RIGHT)
        
        ttk.Button(btn_frame, text="➕ Nuevo Turno", command=self._programar_turno).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="🔄 Actualizar", command=self._refresh).pack(side=tk.LEFT, padx=5)
        
        # Tabla de turnos
        self.tree = ttk.Treeview(self, columns=("id", "paciente", "medico", "consultorio", "fecha", "horario", "estado"), height=12)
        self.tree.heading("#0", text="ID")
        self.tree.heading("id", text="ID")
        self.tree.heading("paciente", text="Paciente")
        self.tree.heading("medico", text="Médico")
        self.tree.heading("consultorio", text="Consultorio")
        self.tree.heading("fecha", text="Fecha")
        self.tree.heading("horario", text="Horario")
        self.tree.heading("estado", text="Estado")
        
        # Anchos
        self.tree.column("#0", width=0, stretch=False)
        self.tree.column("id", width=30)
        self.tree.column("paciente", width=120)
        self.tree.column("medico", width=120)
        self.tree.column("consultorio", width=80)
        self.tree.column("fecha", width=100)
        self.tree.column("horario", width=100)
        self.tree.column("estado", width=80)
        
        self.tree.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Menú contextual
        self.menu_contextual = tk.Menu(self, tearoff=0)
        self.menu_contextual.add_command(label="Marcar como Atendido", command=lambda: self._cambiar_estado("Atendido"))
        self.menu_contextual.add_command(label="Cancelar Turno", command=lambda: self._cambiar_estado("Cancelado"))
        self.tree.bind("<Button-3>", self._mostrar_menu)
        
        # Cargar datos iniciales
        self._refresh()
    
    def _refresh(self):
        """Recarga la lista de turnos programados"""
        try:
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            turnos = self.ctrl.obtener_turnos_programados()
            
            for t in turnos:
                horario = f"{t['hora_inicio']} - {t['hora_fin']}"
                # ✅ USAR id_turno, NO id
                self.tree.insert("", "end", values=(
                    t['id_turno'],
                    t.get('paciente', '---'),
                    t['medico'],
                    t['consultorio'],
                    t['fecha'],
                    horario,
                    t['estado']
                ))
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar turnos: {str(e)}")
    
    def _programar_turno(self):
        """Abre el diálogo para programar un nuevo turno"""
        try:
            dialog = ProgramarTurnoDialog(self.winfo_toplevel(), self.ctrl)
            self.winfo_toplevel().wait_window(dialog.window)
            self._refresh()
        except Exception as e:
            messagebox.showerror("Error", f"Error al abrir diálogo: {str(e)}")
    
    def _mostrar_menu(self, event):
        """Muestra menú contextual"""
        sel = self.tree.selection()
        if sel:
            try:
                self.menu_contextual.tk_popup(event.x_root, event.y_root)
            finally:
                self.menu_contextual.grab_release()
    
    def _cambiar_estado(self, nuevo_estado):
        """Cambia el estado de un turno seleccionado"""
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Advertencia", "Selecciona un turno")
            return
        
        try:
            # ✅ OBTENER id_turno DE LA PRIMERA COLUMNA
            id_turno = self.tree.item(sel[0])["values"][0]
            
            if nuevo_estado == "Atendido":
                if self.ctrl.atender_turno(id_turno):
                    messagebox.showinfo("Éxito", "Turno marcado como atendido")
                    self._refresh()
                else:
                    messagebox.showerror("Error", "No se pudo actualizar el turno")
            
            elif nuevo_estado == "Cancelado":
                if self.ctrl.cancelar_turno(id_turno):
                    messagebox.showinfo("Éxito", "Turno cancelado")
                    self._refresh()
                else:
                    messagebox.showerror("Error", "No se pudo cancelar el turno")
        
        except Exception as e:
            messagebox.showerror("Error", f"Error: {str(e)}")
