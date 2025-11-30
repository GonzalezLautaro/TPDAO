import tkinter as tk
from tkinter import ttk, messagebox
from ..controllers.turno_controller import TurnoController
from ..dialogs.programar_turno_dialog import ProgramarTurnoDialog
from ..dialogs.atender_turno_dialog import AtenderTurnoDialog


class TurnosView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=12)
        self.ctrl = TurnoController()
        
        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill="x", pady=(0, 10))
        
        ttk.Button(btn_frame, text="➕ Programar Turno", command=self._programar_turno).pack(side="left")
        ttk.Button(btn_frame, text="🔄 Refrescar", command=self._refresh).pack(side="left", padx=5)
        
        tabla_frame = ttk.LabelFrame(self, text="Turnos Programados")
        tabla_frame.pack(fill="both", expand=True)
        
        self.tree = ttk.Treeview(
            tabla_frame,
            columns=("id", "paciente", "medico", "consultorio", "fecha", "horario", "estado", "acciones"),
            show="headings",
            height=14
        )
        
        headers = [
            ("id", "ID", 50),
            ("paciente", "Paciente", 150),
            ("medico", "Médico", 150),
            ("consultorio", "Consult.", 70),
            ("fecha", "Fecha", 100),
            ("horario", "Horario", 120),
            ("estado", "Estado", 100),
            ("acciones", "Acciones", 200)
        ]
        
        for col, text, width in headers:
            self.tree.heading(col, text=text)
            self.tree.column(col, width=width)
        
        scrollbar = ttk.Scrollbar(tabla_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind para clicks
        self.tree.bind("<Button-1>", self._on_tree_click)
        
        self._refresh()
    
    def _programar_turno(self):
        """Abre el diálogo para programar un nuevo turno"""
        dialog = ProgramarTurnoDialog(self.winfo_toplevel(), self.ctrl)
        self.winfo_toplevel().wait_window(dialog.window)
        self._refresh()
    
    def _on_tree_click(self, event):
        """Maneja clicks en la tabla"""
        try:
            item = self.tree.identify("item", event.x, event.y)
            if not item:
                return
            
            # Detectar columna clickeada
            col_num = 0
            col_x = 0
            
            for i, col in enumerate(["id", "paciente", "medico", "consultorio", "fecha", "horario", "estado", "acciones"]):
                col_width = self.tree.column(col, "width")
                if event.x < col_x + col_width:
                    col_num = i
                    break
                col_x += col_width
            
            # Si es la columna de acciones (columna 7)
            if col_num == 7:
                valores = self.tree.item(item)["values"]
                id_turno = valores[0]
                paciente = valores[1]
                medico = valores[2]
                consultorio = valores[3]
                fecha = valores[4]
                horario = valores[5]
                estado = valores[6]
                
                # Determinar ancho de la columna de acciones
                acciones_col_width = self.tree.column("acciones", "width")
                acciones_col_x = col_x
                
                # Dividir en tres partes: Atender | Cancelar | No Asistió
                tercio = acciones_col_width / 3
                
                turno_data = {
                    "id": id_turno,
                    "paciente": paciente,
                    "medico": medico,
                    "consultorio": consultorio,
                    "fecha": fecha,
                    "horario": horario,
                    "estado": estado
                }
                
                if event.x < acciones_col_x + tercio:
                    # Atender
                    if estado == "Programado":
                        self._atender_turno(turno_data)
                    else:
                        messagebox.showinfo("Información", f"Este turno ya está en estado: {estado}")
                
                elif event.x < acciones_col_x + (tercio * 2):
                    # Cancelar
                    self._cancelar_turno(id_turno, paciente, estado)
                
                else:
                    # No Asistió
                    self._marcar_inasistencia(id_turno, paciente, estado)
        
        except Exception as e:
            print(f"[ERROR] Error en click: {str(e)}")
            import traceback
            traceback.print_exc()
    
    def _atender_turno(self, turno_data):
        """Abre el diálogo para atender el turno"""
        dialog = AtenderTurnoDialog(self.winfo_toplevel(), turno_data)
        self.winfo_toplevel().wait_window(dialog.window)
        self._refresh()
    
    def _cancelar_turno(self, id_turno, paciente, estado):
        """Cancela un turno"""
        if estado == "Atendido":
            messagebox.showwarning("Advertencia", "No se puede cancelar un turno ya atendido")
            return
        
        respuesta = messagebox.askyesno(
            "Confirmar",
            f"¿Deseas cancelar el turno de {paciente}?"
        )
        
        if respuesta:
            ok, msg = self.ctrl.cambiar_estado_turno(id_turno, "Cancelado")
            if ok:
                messagebox.showinfo("Éxito", "✓ Turno cancelado correctamente")
                self._refresh()
            else:
                messagebox.showerror("Error", msg)
    
    def _marcar_inasistencia(self, id_turno, paciente, estado):
        """Marca un turno como inasistencia"""
        if estado == "Atendido":
            messagebox.showwarning("Advertencia", "No se puede marcar como inasistencia un turno ya atendido")
            return
        
        respuesta = messagebox.askyesno(
            "Confirmar",
            f"¿Marcar como 'No Asistió' el turno de {paciente}?"
        )
        
        if respuesta:
            ok, msg = self.ctrl.cambiar_estado_turno(id_turno, "Inasistencia")
            if ok:
                messagebox.showinfo("Éxito", "✓ Turno marcado como inasistencia")
                self._refresh()
            else:
                messagebox.showerror("Error", msg)
    
    def _refresh(self):
        """Recarga la lista de turnos programados"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        turnos = self.ctrl.obtener_turnos_programados()
        
        for t in turnos:
            # Determinar texto de acciones según estado
            if t['estado'] == 'Programado':
                acciones = "✓ Atender | ✕ Cancelar | ⚠ No Asistió"
            elif t['estado'] == 'Atendido':
                acciones = "— | ✕ Cancelar | ⚠ No Asistió"
            else:
                acciones = "— | — | —"
            
            self.tree.insert("", "end", values=(
                t["id_turno"],
                t["paciente"],
                t["medico"],
                t["consultorio"],
                t["fecha"],
                f"{t['hora_inicio']} - {t['hora_fin']}",
                t["estado"],
                acciones
            ))
