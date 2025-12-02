import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
from ..controllers.turno_controller import TurnoController
from ..dialogs.programar_turno_dialog import ProgramarTurnoDialog
from ..dialogs.atender_turno_dialog import AtenderTurnoDialog


class TurnosView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=12)
        self.ctrl = TurnoController()
        
        # Frame superior con botones
        top_frame = ttk.Frame(self)
        top_frame.pack(fill="x", pady=(0, 10))
        
        ttk.Button(top_frame, text="➕ Programar Turno", command=self._programar_turno).pack(side="left")
        ttk.Button(top_frame, text="🔄 Refrescar", command=self._refresh).pack(side="left", padx=5)
        ttk.Button(top_frame, text="🖨 Imprimir Receta", command=self._imprimir_receta).pack(side="left", padx=5)
        ttk.Button(top_frame, text="📊 Asistencia", command=self._generar_asistencia).pack(side="left", padx=5)


        
        # Frame de filtros por FECHA (primer nivel)
        filtro_fecha_frame = ttk.LabelFrame(self, text="Filtrar por Fecha:", padding=8)
        filtro_fecha_frame.pack(fill="x", pady=(0, 5))
        
        self.filtro_fecha_var = tk.StringVar(value="hoy")
        
        filtros_fecha = [
            ("hoy", "📅 Hoy"),
            ("proximos", "📆 Próximos"),
            ("todos", "📋 Todos")
        ]
        
        for valor, texto in filtros_fecha:
            ttk.Radiobutton(
                filtro_fecha_frame, 
                text=texto, 
                variable=self.filtro_fecha_var, 
                value=valor,
                command=self._refresh
            ).pack(side="left", padx=8)
        
        # Frame de filtros por ESTADO (segundo nivel)
        filtro_estado_frame = ttk.LabelFrame(self, text="Filtrar por Estado:", padding=8)
        filtro_estado_frame.pack(fill="x", pady=(0, 10))
        
        self.filtro_estado_var = tk.StringVar(value="programados")
        
        filtros_estado = [
            ("todos_estados", "📋 Todos"),
            ("programados", "✓ Programados"),
            ("atendidos", "✅ Atendidos"),
            ("cancelados", "❌ Cancelados"),
            ("inasistencia", "⚠️ Inasistencia")
        ]
        
        for valor, texto in filtros_estado:
            ttk.Radiobutton(
                filtro_estado_frame, 
                text=texto, 
                variable=self.filtro_estado_var, 
                value=valor,
                command=self._refresh
            ).pack(side="left", padx=8)
        
        # Tabla de turnos
        tabla_frame = ttk.LabelFrame(self, text="Turnos")
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
                
                # Verificar si el turno ya pasó
                try:
                    fecha_turno = date.fromisoformat(str(fecha))
                    turno_pasado = fecha_turno < date.today()
                except:
                    turno_pasado = False
                
                # Si el turno ya pasó, o está Atendido, Cancelado o Inasistencia, no hacer nada
                if turno_pasado or estado in ['Atendido', 'Cancelado', 'Inasistencia']:
                    return
                
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

    def _imprimir_receta(self):
            """Genera PDF de una receta ya guardada en BD"""
            
            sel = self.tree.focus()
            if not sel:
                messagebox.showerror("Error", "Seleccioná un turno.")
                return

            valores = self.tree.item(sel)["values"]

            # En tu tabla, valores[0] es id_turno ✔️
            try:
                id_turno = int(valores[0])
            except:
                messagebox.showerror("Error", "No pude leer el ID del turno.")
                return

            # Import tardío para no romper nada
            from ..controllers.recetas_controller import RecetasController
            ctrl = RecetasController()

            # Ver receta existente asociada al turno
            id_receta = ctrl.id_receta_de_turno(id_turno)
            if not id_receta:
                messagebox.showerror("Sin receta", "Este turno no tiene receta registrada.")
                return

            # Elegir destino del PDF
            from tkinter import filedialog
            archivo = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                initialfile=f"receta_{id_receta}.pdf",
                filetypes=[("PDF", "*.pdf")]
            )
            if not archivo:
                return

            # Generar PDF
            ok = ctrl.generar_pdf(id_receta, archivo)
            if ok:
                messagebox.showinfo("Éxito", f"Receta #{id_receta} generada:\n{archivo}")
            else:
                messagebox.showerror("Error", "Fallo al generar el PDF (instalá reportlab).")

    def _generar_asistencia(self):
        from tkinter import messagebox
        import os
        from reports.asistencia import grafico_asistencia_bd

        ruta = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            "reports", "out", "asistencia.png"
        )

        try:
            # SIN incluir_cancelados (ya no existe)
            png = grafico_asistencia_bd(
                ruta,
                host="127.0.0.1",
                user="root",
                password="vleksel17db",
                database="hospital_db",
                port=3306,
                tipo="pie"
            )

            messagebox.showinfo("Reporte listo", f"Gráfico generado en:\n{png}")

            try:
                os.startfile(png)  # abrir en Windows
            except Exception:
                pass

        except Exception as e:
            messagebox.showerror("Error", f"No pude generar el gráfico:\n{e}")

    
    def _refresh(self):
        """Recarga la lista de turnos según los filtros seleccionados"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        filtro_fecha = self.filtro_fecha_var.get()
        filtro_estado = self.filtro_estado_var.get()
        
        turnos = self.ctrl.obtener_turnos_con_doble_filtro(filtro_fecha, filtro_estado)
        
        for t in turnos:
            # Verificar si el turno ya pasó (fecha anterior a hoy)
            try:
                fecha_turno = date.fromisoformat(str(t['fecha']))
                turno_pasado = fecha_turno < date.today()
            except:
                turno_pasado = False
            
            # Determinar texto de acciones según estado y si ya pasó
            if turno_pasado or t['estado'] in ['Atendido', 'Cancelado', 'Inasistencia']:
                # Turnos pasados, atendidos, cancelados o inasistencia: sin acciones
                acciones = "— | — | —"
            elif t['estado'] == 'Programado':
                acciones = "✓ Atender | ✕ Cancelar | ⚠ No Asistió"
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