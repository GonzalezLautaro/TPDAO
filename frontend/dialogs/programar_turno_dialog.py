import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import sys
import os

# Agregar path
BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if BASE not in sys.path:
    sys.path.insert(0, BASE)

from data.database import Database


class ProgramarTurnoDialog:
    def __init__(self, parent, controller):
        self.controller = controller
        self.window = tk.Toplevel(parent)
        self.window.title("Programar Nuevo Turno")
        self.window.geometry("750x700")
        self.window.resizable(False, False)
        
        # Variables de estado
        self.paso_actual = 1
        self.medico_seleccionado = None
        self.turno_seleccionado = None
        self.paciente_seleccionado = None
        
        # Container principal
        self.container = ttk.Frame(self.window)
        self.container.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Título
        self.titulo = ttk.Label(self.container, text="", font=("Arial", 12, "bold"))
        self.titulo.pack(pady=(0, 10))
        
        # Contenedor de pasos
        self.frame_paso = ttk.Frame(self.container)
        self.frame_paso.pack(fill="both", expand=True, pady=(0, 10))
        
        # Frame de botones (IMPORTANTE: debe estar fuera del frame_paso)
        self.frame_botones = ttk.Frame(self.container)
        self.frame_botones.pack(fill="x", pady=(10, 0), side="bottom")
        
        self._mostrar_paso_1()
    
    def _limpiar_frame(self):
        """Limpia el frame de pasos"""
        for widget in self.frame_paso.winfo_children():
            widget.destroy()
    
    def _obtener_medicos_directo(self):
        """Obtiene médicos directamente de la BD sin pasar por controlador"""
        db = Database()
        if not db.conectar("127.0.0.1:3306/hospital_db"):
            print("[ERROR] No se pudo conectar a BD")
            return []
        
        try:
            query = "SELECT matricula, nombre, apellido FROM Medico"
            medicos = db.obtener_registros(query)
            print(f"[DEBUG] Médicos obtenidos: {len(medicos) if medicos else 0}")
            if medicos:
                for m in medicos:
                    print(f"[DEBUG]   - {m}")
            db.desconectar()
            return medicos if medicos else []
        except Exception as e:
            print(f"[ERROR] Error al obtener médicos: {str(e)}")
            db.desconectar()
            return []
    
    def _mostrar_paso_1(self):
        """Paso 1: Seleccionar médico"""
        self.paso_actual = 1
        self.titulo.config(text="PASO 1/3: Seleccionar Médico")
        self._limpiar_frame()
        
        # Cargar médicos directamente
        medicos = self._obtener_medicos_directo()
        
        if not medicos:
            messagebox.showerror("Error", "No hay médicos disponibles")
            self.window.destroy()
            return
        
        # Crear listbox con scroll
        frame_lista = ttk.Frame(self.frame_paso)
        frame_lista.pack(fill="both", expand=True)
        
        ttk.Label(frame_lista, text=f"Médicos disponibles ({len(medicos)}):", font=("Arial", 10)).pack(anchor="w", pady=(0, 5))
        
        scrollbar = ttk.Scrollbar(frame_lista)
        scrollbar.pack(side="right", fill="y")
        
        self.listbox_medicos = tk.Listbox(frame_lista, yscrollcommand=scrollbar.set, height=15, font=("Arial", 9))
        scrollbar.config(command=self.listbox_medicos.yview)
        self.listbox_medicos.pack(fill="both", expand=True, pady=5)
        
        for i, med in enumerate(medicos):
            label = f"Dr/Dra. {med['nombre']} {med['apellido']} (Mat: {med['matricula']})"
            self.listbox_medicos.insert(tk.END, label)
        
        # Si hay solo 1, seleccionar automáticamente
        if len(medicos) == 1:
            self.listbox_medicos.selection_set(0)
        
        # Guardar médicos para referencia
        self.medicos_paso1 = medicos
        
        # Botones
        self._actualizar_botones(
            btn_siguiente=lambda: self._seleccionar_medico(),
            btn_cancelar=True
        )
    
    def _seleccionar_medico(self):
        """Valida y pasa al paso 2"""
        sel = self.listbox_medicos.curselection()
        if not sel:
            messagebox.showwarning("Advertencia", "Selecciona un médico")
            return
        
        self.medico_seleccionado = self.medicos_paso1[sel[0]]
        print(f"[DEBUG] Médico seleccionado: {self.medico_seleccionado}")
        self._mostrar_paso_2()
    
    def _mostrar_paso_2(self):
        """Paso 2: Seleccionar turno disponible agrupado por día"""
        self.paso_actual = 2
        self.titulo.config(text=f"PASO 2/3: Seleccionar Turno - Dr/Dra. {self.medico_seleccionado['nombre']} {self.medico_seleccionado['apellido']}")
        self._limpiar_frame()
        
        # Cargar turnos libres
        turnos = self.controller.obtener_turnos_libres_medico(self.medico_seleccionado['matricula'])
        
        if not turnos:
            messagebox.showwarning("Advertencia", "Este médico no tiene turnos disponibles")
            self._mostrar_paso_1()
            return
        
        # Agrupar turnos por fecha
        turnos_por_dia = {}
        for t in turnos:
            fecha = str(t['fecha'])
            if fecha not in turnos_por_dia:
                turnos_por_dia[fecha] = []
            turnos_por_dia[fecha].append(t)
        
        # Crear Treeview con dos niveles
        self.tree_turnos = ttk.Treeview(self.frame_paso, columns=("horario", "consultorio"), show="tree headings", height=15)
        self.tree_turnos.heading("#0", text="Fecha")
        self.tree_turnos.heading("horario", text="Horario")
        self.tree_turnos.heading("consultorio", text="Consultorio")
        
        self.tree_turnos.column("#0", width=150)
        self.tree_turnos.column("horario", width=150)
        self.tree_turnos.column("consultorio", width=80)
        
        scrollbar = ttk.Scrollbar(self.frame_paso, orient="vertical", command=self.tree_turnos.yview)
        self.tree_turnos.configure(yscroll=scrollbar.set)
        
        self.tree_turnos.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Poblar árbol
        self.turnos_dict = {}
        for fecha in sorted(turnos_por_dia.keys()):
            fecha_item = self.tree_turnos.insert("", "end", text=fecha, open=True)
            
            for turno in turnos_por_dia[fecha]:
                horario = f"{turno['hora_inicio']} - {turno['hora_fin']}"
                item_id = self.tree_turnos.insert(fecha_item, "end", text="", values=(
                    horario,
                    f"#{turno['consultorio_numero']}"
                ))
                self.turnos_dict[item_id] = turno
        
        # Botones
        self._actualizar_botones(
            btn_siguiente=lambda: self._seleccionar_turno(),
            btn_anterior=lambda: self._mostrar_paso_1(),
            btn_cancelar=True
        )
    
    def _seleccionar_turno(self):
        """Valida y pasa al paso 3"""
        sel = self.tree_turnos.selection()
        if not sel:
            messagebox.showwarning("Advertencia", "Selecciona un turno")
            return
        
        item_id = sel[0]
        if item_id not in self.turnos_dict:
            messagebox.showwarning("Advertencia", "Debes seleccionar un turno (no una fecha)")
            return
        
        self.turno_seleccionado = self.turnos_dict[item_id]
        self._mostrar_paso_3()
    
    def _mostrar_paso_3(self):
        """Paso 3: Seleccionar paciente e ingresar observaciones"""
        self.paso_actual = 3
        self.titulo.config(text="PASO 3/3: Seleccionar Paciente y Observaciones")
        self._limpiar_frame()
        
        # Cargar pacientes
        pacientes = self.controller.obtener_pacientes()
        
        if not pacientes:
            messagebox.showerror("Error", "No hay pacientes disponibles")
            self._mostrar_paso_2()
            return
        
        # Frame para búsqueda
        frame_busqueda = ttk.LabelFrame(self.frame_paso, text="Buscar Paciente", padding=10)
        frame_busqueda.pack(fill="x", pady=(0, 10))
        
        ttk.Label(frame_busqueda, text="Buscar por nombre o ID:", font=("Arial", 9)).grid(row=0, column=0, sticky="w", pady=(0, 5))
        
        self.entry_busqueda = ttk.Entry(frame_busqueda, width=40)
        self.entry_busqueda.grid(row=0, column=1, sticky="ew", padx=(10, 0))
        self.entry_busqueda.bind("<KeyRelease>", lambda e: self._filtrar_pacientes())
        
        frame_busqueda.columnconfigure(1, weight=1)
        
        # Frame para pacientes
        frame_paciente = ttk.LabelFrame(self.frame_paso, text="Pacientes", padding=10)
        frame_paciente.pack(fill="both", expand=True, pady=(0, 10))
        
        ttk.Label(frame_paciente, text="Selecciona paciente:", font=("Arial", 9)).pack(anchor="w")
        
        scrollbar_pac = ttk.Scrollbar(frame_paciente)
        scrollbar_pac.pack(side="right", fill="y")
        
        self.listbox_pacientes = tk.Listbox(frame_paciente, yscrollcommand=scrollbar_pac.set, height=8, font=("Arial", 9))
        scrollbar_pac.config(command=self.listbox_pacientes.yview)
        self.listbox_pacientes.pack(fill="both", expand=True, pady=5)
        self.listbox_pacientes.bind("<<ListboxSelect>>", lambda e: self._seleccionar_paciente_listbox())
        
        # Guardar todos los pacientes y crear mapping
        self.todos_los_pacientes = pacientes
        self.pacientes_filtrados = pacientes
        self.pacientes_dict = {}
        
        for pac in pacientes:
            self.pacientes_dict[pac['id_paciente']] = pac
        
        self._repoblar_listbox()
        
        # Frame para observaciones
        frame_obs = ttk.LabelFrame(self.frame_paso, text="Observaciones", padding=10)
        frame_obs.pack(fill="both", expand=True, pady=(0, 10))
        
        ttk.Label(frame_obs, text="Observaciones (opcional):", font=("Arial", 9)).pack(anchor="w")
        
        self.text_observaciones = tk.Text(frame_obs, height=4, width=50, font=("Arial", 9))
        self.text_observaciones.pack(fill="both", expand=True)
        
        # Resumen
        frame_resumen = ttk.LabelFrame(self.frame_paso, text="Resumen", padding=10)
        frame_resumen.pack(fill="x")
        
        resumen_text = f"""Médico: Dr/Dra. {self.medico_seleccionado['nombre']} {self.medico_seleccionado['apellido']}
Fecha: {self.turno_seleccionado['fecha']}
Horario: {self.turno_seleccionado['hora_inicio']} - {self.turno_seleccionado['hora_fin']}
Consultorio: #{self.turno_seleccionado['consultorio_numero']}"""
        
        ttk.Label(frame_resumen, text=resumen_text, font=("Arial", 9), justify="left").pack(anchor="w")
        
        # Botones
        self._actualizar_botones(
            btn_siguiente=lambda: self._confirmar_programacion(),
            btn_anterior=lambda: self._mostrar_paso_2(),
            btn_cancelar=True,
            texto_siguiente="✓ Aceptar"
        )
    
    def _filtrar_pacientes(self):
        """Filtra los pacientes según el texto de búsqueda"""
        texto_busqueda = self.entry_busqueda.get().lower().strip()
        
        if not texto_busqueda:
            self.pacientes_filtrados = self.todos_los_pacientes
        else:
            self.pacientes_filtrados = [
                p for p in self.todos_los_pacientes
                if (texto_busqueda in f"{p['nombre']} {p['apellido']}".lower() or
                    texto_busqueda in str(p['id_paciente']))
            ]
        
        self._repoblar_listbox()
    
    def _repoblar_listbox(self):
        """Repuebla el listbox con los pacientes filtrados"""
        self.listbox_pacientes.delete(0, tk.END)
        
        for pac in self.pacientes_filtrados:
            label = f"{pac['nombre']} {pac['apellido']} (ID: {pac['id_paciente']})"
            self.listbox_pacientes.insert(tk.END, label)
    
    def _seleccionar_paciente_listbox(self):
        """Selecciona un paciente del listbox"""
        sel = self.listbox_pacientes.curselection()
        if sel:
            self.paciente_seleccionado = self.pacientes_filtrados[sel[0]]
    
    def _confirmar_programacion(self):
        """Valida y confirma la programación"""
        if not self.paciente_seleccionado:
            messagebox.showwarning("Advertencia", "Selecciona un paciente")
            return
        
        observaciones = self.text_observaciones.get("1.0", tk.END).strip()
        
        # Programar turno
        ok, msg = self.controller.programar_turno(
            id_paciente=self.paciente_seleccionado['id_paciente'],
            matricula=self.medico_seleccionado['matricula'],
            id_turno=self.turno_seleccionado['id_turno'],
            observaciones=observaciones
        )
        
        if ok:
            messagebox.showinfo("Éxito", f"✓ Turno programado exitosamente")
            self.window.destroy()
        else:
            messagebox.showerror("Error", msg)
    
    def _actualizar_botones(self, btn_siguiente=None, btn_anterior=None, btn_cancelar=False, texto_siguiente="Siguiente"):
        """Actualiza los botones según el paso"""
        # Limpiar botones anteriores
        for widget in self.frame_botones.winfo_children():
            widget.destroy()
        
        # Crear frame para botones con separación
        btn_frame = ttk.Frame(self.frame_botones)
        btn_frame.pack(fill="x", expand=True)
        
        # Botón izquierdo (Anterior)
        if btn_anterior:
            ttk.Button(btn_frame, text="← Anterior", command=btn_anterior).pack(side="left", padx=5)
        else:
            ttk.Frame(btn_frame, width=80).pack(side="left")  # Espaciador
        
        # Botones derechos
        right_frame = ttk.Frame(btn_frame)
        right_frame.pack(side="right")
        
        if btn_cancelar:
            ttk.Button(right_frame, text="Cancelar", command=self.window.destroy).pack(side="left", padx=5)
        
        if btn_siguiente:
            ttk.Button(right_frame, text=texto_siguiente + " →", command=btn_siguiente).pack(side="left", padx=5)
