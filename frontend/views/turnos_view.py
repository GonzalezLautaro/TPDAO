import tkinter as tk
from tkinter import ttk, messagebox
from ..controllers.turno_controller import TurnoController
from ..dialogs.programar_turno_dialog import ProgramarTurnoDialog


class TurnosView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=12)
        self.ctrl = TurnoController()
        
        # Frame superior con botones
        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill="x", pady=(0, 10))
        
        ttk.Button(btn_frame, text="➕ Programar Turno", command=self._programar_turno).pack(side="left")
        ttk.Button(btn_frame, text="🔄 Refrescar", command=self._refresh).pack(side="left", padx=5)
        
        # Tabla de turnos programados
        tabla_frame = ttk.LabelFrame(self, text="Turnos Programados")
        tabla_frame.pack(fill="both", expand=True)
        
        self.tree = ttk.Treeview(tabla_frame, columns=("id", "paciente", "medico", "consultorio", "fecha", "horario", "estado"), show="headings", height=15)
        
        headers = [
            ("id", "ID", 50),
            ("paciente", "Paciente", 150),
            ("medico", "Médico", 150),
            ("consultorio", "Consult.", 60),
            ("fecha", "Fecha", 100),
            ("horario", "Horario", 110),
            ("estado", "Estado", 80)
        ]
        
        for col, text, width in headers:
            self.tree.heading(col, text=text)
            self.tree.column(col, width=width)
        
        scrollbar = ttk.Scrollbar(tabla_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Frame inferior con acciones
        acc_frame = ttk.Frame(self)
        acc_frame.pack(fill="x", pady=(10, 0))
        
        ttk.Button(acc_frame, text="📋 Atender", command=lambda: self._cambiar_estado("Atendido")).pack(side="left")
        ttk.Button(acc_frame, text="❌ Cancelar", command=lambda: self._cambiar_estado("Cancelado")).pack(side="left", padx=5)
        ttk.Button(acc_frame, text="⚠️ No Asistió", command=lambda: self._cambiar_estado("Inasistencia")).pack(side="left", padx=5)
        
        self._refresh()
    
    def _programar_turno(self):
        """Abre el diálogo para programar un nuevo turno"""
        dialog = ProgramarTurnoDialog(self.winfo_toplevel(), self.ctrl)
        self.winfo_toplevel().wait_window(dialog.window)
        self._refresh()
    
    def _cambiar_estado(self, nuevo_estado):
        """Cambia el estado de un turno seleccionado"""
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Advertencia", "Selecciona un turno")
            return
        
        id_turno = self.tree.item(sel[0])["values"][0]
        
        ok, msg = self.ctrl.cambiar_estado_turno(id_turno, nuevo_estado)
        if ok:
            messagebox.showinfo("Éxito", msg)
            self._refresh()
        else:
            messagebox.showerror("Error", msg)
    
    def _refresh(self):
        """Recarga la lista de turnos programados"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        turnos = self.ctrl.listar_turnos_programados()
        for t in turnos:
            horario = f"{t['hora_inicio']} - {t['hora_fin']}"
            self.tree.insert("", "end", values=(
                t["id_turno"],
                t["paciente"],
                t["medico"],
                t["consultorio"],
                t["fecha"],
                horario,
                t["estado"]
            ))
