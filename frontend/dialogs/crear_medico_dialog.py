import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date, time
import sys, os

# Agregar TPDAO al path
BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if BASE not in sys.path:
    sys.path.insert(0, BASE)

from data.database import Database


class CrearMedicoDialog:
    def __init__(self, parent, controller):
        self.controller = controller
        self.window = tk.Toplevel(parent)
        self.window.title("Crear Nuevo Médico")
        self.window.geometry("700x750")
        self.window.resizable(False, False)
        
        # Container principal con scroll
        main_frame = ttk.Frame(self.window)
        main_frame.pack(fill="both", expand=True)
        
        canvas = tk.Canvas(main_frame, highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas, padding=20)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Título
        titulo = ttk.Label(scrollable_frame, text="Registrar Nuevo Médico", font=("Arial", 14, "bold"))
        titulo.pack(pady=(0, 15))
        
        # === DATOS BÁSICOS ===
        datos_frame = ttk.LabelFrame(scrollable_frame, text="Datos Básicos", padding=15)
        datos_frame.pack(fill="x", pady=(0, 10))
        
        # Matrícula
        ttk.Label(datos_frame, text="Matrícula:").grid(row=0, column=0, sticky="w", pady=5, padx=(0, 10))
        self.entry_matricula = ttk.Entry(datos_frame, width=40)
        self.entry_matricula.grid(row=0, column=1, sticky="ew", pady=5)
        
        # Nombre
        ttk.Label(datos_frame, text="Nombre:").grid(row=1, column=0, sticky="w", pady=5, padx=(0, 10))
        self.entry_nombre = ttk.Entry(datos_frame, width=40)
        self.entry_nombre.grid(row=1, column=1, sticky="ew", pady=5)
        
        # Apellido
        ttk.Label(datos_frame, text="Apellido:").grid(row=2, column=0, sticky="w", pady=5, padx=(0, 10))
        self.entry_apellido = ttk.Entry(datos_frame, width=40)
        self.entry_apellido.grid(row=2, column=1, sticky="ew", pady=5)
        
        # Teléfono
        ttk.Label(datos_frame, text="Teléfono:").grid(row=3, column=0, sticky="w", pady=5, padx=(0, 10))
        self.entry_telefono = ttk.Entry(datos_frame, width=40)
        self.entry_telefono.grid(row=3, column=1, sticky="ew", pady=5)
        
        # Email
        ttk.Label(datos_frame, text="Email:").grid(row=4, column=0, sticky="w", pady=5, padx=(0, 10))
        self.entry_email = ttk.Entry(datos_frame, width=40)
        self.entry_email.grid(row=4, column=1, sticky="ew", pady=5)
        
        # Fecha de Alta
        ttk.Label(datos_frame, text="Fecha Alta:").grid(row=5, column=0, sticky="w", pady=5, padx=(0, 10))
        self.entry_fecha_alta = ttk.Entry(datos_frame, width=40)
        self.entry_fecha_alta.insert(0, str(date.today()))
        self.entry_fecha_alta.grid(row=5, column=1, sticky="ew", pady=5)
        
        datos_frame.columnconfigure(1, weight=1)
        
        # === ESPECIALIDADES ===
        esp_frame = ttk.LabelFrame(scrollable_frame, text="Especialidades", padding=10)
        esp_frame.pack(fill="x", pady=(0, 10))
        
        canvas_esp = tk.Canvas(esp_frame, height=100, highlightthickness=0)
        scrollbar_esp = ttk.Scrollbar(esp_frame, orient="vertical", command=canvas_esp.yview)
        self.esp_frame_scroll = ttk.Frame(canvas_esp)
        
        self.esp_frame_scroll.bind("<Configure>", lambda e: canvas_esp.configure(scrollregion=canvas_esp.bbox("all")))
        canvas_esp.create_window((0, 0), window=self.esp_frame_scroll, anchor="nw")
        canvas_esp.configure(yscrollcommand=scrollbar_esp.set)
        
        canvas_esp.pack(side="left", fill="both", expand=True)
        scrollbar_esp.pack(side="right", fill="y")
        
        self.especialidades = self._cargar_especialidades()
        self.var_especialidades = {}
        
        if self.especialidades:
            for esp in self.especialidades:
                var = tk.BooleanVar()
                self.var_especialidades[esp['id']] = var
                ttk.Checkbutton(self.esp_frame_scroll, text=f"{esp['nombre']}", variable=var).pack(anchor="w", pady=2)
        
        # === AGENDA (DÍAS Y HORARIOS) ===
        agenda_frame = ttk.LabelFrame(scrollable_frame, text="Programar Agenda", padding=15)
        agenda_frame.pack(fill="x", pady=(0, 10))
        
        ttk.Label(agenda_frame, text="Selecciona los días y horarios de atención:", font=("Arial", 9, "italic")).pack(anchor="w", pady=(0, 10))
        
        # Consultorio
        cons_frame = ttk.Frame(agenda_frame)
        cons_frame.pack(fill="x", pady=(0, 10))
        
        ttk.Label(cons_frame, text="Consultorio:").pack(side="left", padx=(0, 10))
        self.combo_consultorio = ttk.Combobox(cons_frame, state="readonly", width=25)
        self.combo_consultorio.pack(side="left")
        self._cargar_consultorios()
        
        # Días de semana con horarios
        self.var_dias = {}
        self.entry_hora_inicio = {}
        self.entry_hora_fin = {}
        
        dias_semana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        
        for i, dia in enumerate(dias_semana):
            dia_frame = ttk.Frame(agenda_frame)
            dia_frame.pack(fill="x", pady=3)
            
            var = tk.BooleanVar()
            self.var_dias[dia] = var
            
            check = ttk.Checkbutton(dia_frame, text=dia, variable=var, width=12)
            check.pack(side="left", padx=(0, 10))
            
            ttk.Label(dia_frame, text="Desde:").pack(side="left", padx=(10, 5))
            entry_inicio = ttk.Entry(dia_frame, width=8)
            entry_inicio.insert(0, "08:00")
            entry_inicio.pack(side="left", padx=(0, 10))
            self.entry_hora_inicio[dia] = entry_inicio
            
            ttk.Label(dia_frame, text="Hasta:").pack(side="left", padx=(0, 5))
            entry_fin = ttk.Entry(dia_frame, width=8)
            entry_fin.insert(0, "12:00")
            entry_fin.pack(side="left")
            self.entry_hora_fin[dia] = entry_fin
        
        # Botones
        btn_frame = ttk.Frame(scrollable_frame)
        btn_frame.pack(fill="x", side="bottom", pady=(15, 0))
        
        ttk.Frame(btn_frame).pack(side="left", expand=True)
        ttk.Button(btn_frame, text="Cancelar", command=self.window.destroy, width=12).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="✓ Crear", command=self._crear_medico, width=12).pack(side="left", padx=5)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def _cargar_especialidades(self):
        """Carga las especialidades desde la BD"""
        db = Database()
        if not db.conectar("127.0.0.1:3306/hospital_db"):
            return []
        
        try:
            query = "SELECT id_especialidad as id, nombre, descripcion FROM Especialidad ORDER BY nombre"
            especialidades = db.obtener_registros(query)
            db.desconectar()
            return especialidades if especialidades else []
        except Exception as e:
            print(f"[ERROR] Error al cargar especialidades: {str(e)}")
            db.desconectar()
            return []
    
    def _cargar_consultorios(self):
        """Carga los consultorios desde la BD"""
        db = Database()
        if not db.conectar("127.0.0.1:3306/hospital_db"):
            return
        
        try:
            query = "SELECT id_consultorio, numero FROM Consultorio ORDER BY numero"
            consultorios = db.obtener_registros(query)
            db.desconectar()
            
            if consultorios:
                self.combo_consultorio['values'] = [f"Consultorio {c['numero']}" for c in consultorios]
                self.consultorios_data = consultorios
                
                if consultorios:
                    self.combo_consultorio.current(0)
        except Exception as e:
            print(f"[ERROR] Error al cargar consultorios: {str(e)}")
            db.desconectar()
    
    def _crear_medico(self):
        """Valida y crea el médico con su agenda"""
        matricula = self.entry_matricula.get().strip()
        nombre = self.entry_nombre.get().strip()
        apellido = self.entry_apellido.get().strip()
        telefono = self.entry_telefono.get().strip()
        email = self.entry_email.get().strip()
        fecha_alta = self.entry_fecha_alta.get().strip()
        
        # Validaciones básicas
        if not matricula or not nombre or not apellido or not email:
            messagebox.showwarning("Advertencia", "Matrícula, nombre, apellido y email son obligatorios")
            return
        
        if "@" not in email:
            messagebox.showwarning("Advertencia", "El email no es válido")
            return
        
        # Obtener especialidades seleccionadas desde checkboxes
        especialidades_ids = [
            esp_id for esp_id, var in self.var_especialidades.items() if var.get()
        ]
        
        # Agenda (días seleccionados con horarios)
        agenda_data = []
        dias_seleccionados = [dia for dia, var in self.var_dias.items() if var.get()]
        
        if dias_seleccionados:
            if not self.combo_consultorio.get():
                messagebox.showwarning("Advertencia", "Selecciona un consultorio para la agenda")
                return
            
            idx_consultorio = self.combo_consultorio.current()
            id_consultorio = self.consultorios_data[idx_consultorio]['id_consultorio']
            
            for dia in dias_seleccionados:
                hora_inicio_str = self.entry_hora_inicio[dia].get().strip()
                hora_fin_str = self.entry_hora_fin[dia].get().strip()
                
                try:
                    hora_inicio = time.fromisoformat(hora_inicio_str)
                    hora_fin = time.fromisoformat(hora_fin_str)
                    
                    if hora_fin <= hora_inicio:
                        messagebox.showerror("Error", f"{dia}: La hora de fin debe ser mayor a la de inicio")
                        return
                    
                    agenda_data.append({
                        'dia': dia,
                        'hora_inicio': hora_inicio,
                        'hora_fin': hora_fin,
                        'id_consultorio': id_consultorio
                    })
                except ValueError:
                    messagebox.showerror("Error", f"{dia}: Formato de hora inválido (usa HH:MM)")
                    return
        
        # Crear médico con agenda
        ok, msg = self.controller.crear(
            matricula, nombre, apellido, telefono, email, fecha_alta, 
            especialidades_ids, agenda_data
        )
        
        if ok:
            messagebox.showinfo("Éxito", "✓ Médico creado exitosamente\n✓ Agenda programada\n✓ Turnos generados automáticamente")
            self.window.destroy()
        else:
            messagebox.showerror("Error", msg)
