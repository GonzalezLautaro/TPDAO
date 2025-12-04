import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date, time
import sys, os

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if BASE not in sys.path:
    sys.path.insert(0, BASE)

from data.database import Database


class CrearMedicoDialog:
    def __init__(self, parent, controller):
        self.controller = controller
        self.window = tk.Toplevel(parent)
        self.window.title("Crear Nuevo Médico")
        self.window.geometry("580x570")
        self.window.resizable(False, False)
        
        # Container principal SIN scroll
        container = ttk.Frame(self.window, padding=12)
        container.pack(fill="both", expand=True)
        
        # Título
        ttk.Label(container, text="Registrar Nuevo Médico", font=("Arial", 13, "bold")).pack(pady=(0, 8))
        
        # === DATOS BÁSICOS ===
        datos_frame = ttk.LabelFrame(container, text="Datos Básicos", padding=8)
        datos_frame.pack(fill="x", pady=(0, 6))
        
        # Fila 1
        row1 = ttk.Frame(datos_frame)
        row1.pack(fill="x", pady=2)
        ttk.Label(row1, text="Matrícula:", width=10).pack(side="left")
        self.entry_matricula = ttk.Entry(row1, width=14)
        self.entry_matricula.pack(side="left", padx=(0, 12))
        ttk.Label(row1, text="Nombre:", width=9).pack(side="left")
        self.entry_nombre = ttk.Entry(row1, width=18)
        self.entry_nombre.pack(side="left")
        
        # Fila 2
        row2 = ttk.Frame(datos_frame)
        row2.pack(fill="x", pady=2)
        ttk.Label(row2, text="Apellido:", width=10).pack(side="left")
        self.entry_apellido = ttk.Entry(row2, width=14)
        self.entry_apellido.pack(side="left", padx=(0, 12))
        ttk.Label(row2, text="Teléfono:", width=9).pack(side="left")
        self.entry_telefono = ttk.Entry(row2, width=18)
        self.entry_telefono.pack(side="left")
        
        # Fila 3
        row3 = ttk.Frame(datos_frame)
        row3.pack(fill="x", pady=2)
        ttk.Label(row3, text="Email:", width=10).pack(side="left")
        self.entry_email = ttk.Entry(row3, width=14)
        self.entry_email.pack(side="left", padx=(0, 12))
        ttk.Label(row3, text="Fecha Alta:", width=9).pack(side="left")
        self.entry_fecha_alta = ttk.Entry(row3, width=18)
        self.entry_fecha_alta.insert(0, str(date.today()))
        self.entry_fecha_alta.pack(side="left")
        
        # === ESPECIALIDADES ===
        esp_frame = ttk.LabelFrame(container, text="Especialidades", padding=6)
        esp_frame.pack(fill="x", pady=(0, 6))
        
        self.especialidades = self._cargar_especialidades()
        self.var_especialidades = {}
        
        # 4 columnas compactas
        if self.especialidades:
            num_cols = 4
            esp_container = ttk.Frame(esp_frame)
            esp_container.pack()
            
            for i, esp in enumerate(self.especialidades):
                var = tk.BooleanVar()
                self.var_especialidades[esp['id']] = var
                row = i // num_cols
                col = i % num_cols
                ttk.Checkbutton(esp_container, text=esp['nombre'], variable=var, width=13).grid(
                    row=row, column=col, sticky="w", padx=3, pady=1
                )
        
        # === AGENDA ===
        agenda_frame = ttk.LabelFrame(container, text="Programar Agenda", padding=8)
        agenda_frame.pack(fill="x", pady=(0, 6))
        
        # Consultorio
        cons_row = ttk.Frame(agenda_frame)
        cons_row.pack(fill="x", pady=(0, 4))
        ttk.Label(cons_row, text="Consultorio:", width=10).pack(side="left")
        self.combo_consultorio = ttk.Combobox(cons_row, state="readonly", width=15)
        self.combo_consultorio.pack(side="left")
        self._cargar_consultorios()
        
        # Header de columnas
        header = ttk.Frame(agenda_frame)
        header.pack(fill="x", pady=(0, 2))
        ttk.Label(header, text="Día", width=10, font=("Arial", 8, "bold")).pack(side="left")
        ttk.Label(header, text="De:", width=5, font=("Arial", 8, "bold")).pack(side="left")
        ttk.Label(header, text="", width=7).pack(side="left")
        ttk.Label(header, text="a:", width=4, font=("Arial", 8, "bold")).pack(side="left")
        ttk.Label(header, text="", width=7).pack(side="left")
        ttk.Label(header, text="Día", width=10, font=("Arial", 8, "bold")).pack(side="left")
        ttk.Label(header, text="De:", width=5, font=("Arial", 8, "bold")).pack(side="left")
        ttk.Label(header, text="", width=7).pack(side="left")
        ttk.Label(header, text="a:", width=4, font=("Arial", 8, "bold")).pack(side="left")
        
        self.var_dias = {}
        self.entry_hora_inicio = {}
        self.entry_hora_fin = {}
        
        dias_semana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        
        # 2 columnas con días
        for i in range(0, len(dias_semana), 2):
            dia_row = ttk.Frame(agenda_frame)
            dia_row.pack(fill="x", pady=1)
            
            # Columna izquierda
            dia1 = dias_semana[i]
            var1 = tk.BooleanVar()
            self.var_dias[dia1] = var1
            
            ttk.Checkbutton(dia_row, text=dia1, variable=var1, width=10).pack(side="left")
            ttk.Label(dia_row, text="De:", width=3).pack(side="left")
            entry_inicio1 = ttk.Entry(dia_row, width=6)
            entry_inicio1.insert(0, "08:00")
            entry_inicio1.pack(side="left")
            self.entry_hora_inicio[dia1] = entry_inicio1
            
            ttk.Label(dia_row, text="a:", width=3).pack(side="left")
            entry_fin1 = ttk.Entry(dia_row, width=6)
            entry_fin1.insert(0, "12:00")
            entry_fin1.pack(side="left", padx=(0, 10))
            self.entry_hora_fin[dia1] = entry_fin1
            
            # Columna derecha (si existe)
            if i + 1 < len(dias_semana):
                dia2 = dias_semana[i + 1]
                var2 = tk.BooleanVar()
                self.var_dias[dia2] = var2
                
                ttk.Checkbutton(dia_row, text=dia2, variable=var2, width=10).pack(side="left")
                ttk.Label(dia_row, text="De:", width=3).pack(side="left")
                entry_inicio2 = ttk.Entry(dia_row, width=6)
                entry_inicio2.insert(0, "08:00")
                entry_inicio2.pack(side="left")
                self.entry_hora_inicio[dia2] = entry_inicio2
                
                ttk.Label(dia_row, text="a:", width=3).pack(side="left")
                entry_fin2 = ttk.Entry(dia_row, width=6)
                entry_fin2.insert(0, "12:00")
                entry_fin2.pack(side="left")
                self.entry_hora_fin[dia2] = entry_fin2
        
        # Botones
        btn_frame = ttk.Frame(container)
        btn_frame.pack(fill="x", pady=(8, 0))
        
        ttk.Frame(btn_frame).pack(side="left", expand=True)
        ttk.Button(btn_frame, text="Cancelar", command=self.window.destroy, width=10).pack(side="left", padx=3)
        ttk.Button(btn_frame, text="✓ Crear", command=self._crear_medico, width=10).pack(side="left", padx=3)
    
    def _cargar_especialidades(self):
        db = Database()
        if not db.conectar("127.0.0.1:3306/hospital_db"):
            return []
        try:
            especialidades = db.obtener_registros("SELECT id_especialidad as id, nombre FROM Especialidad ORDER BY nombre")
            db.desconectar()
            return especialidades if especialidades else []
        except:
            db.desconectar()
            return []
    
    def _cargar_consultorios(self):
        db = Database()
        if not db.conectar("127.0.0.1:3306/hospital_db"):
            return
        try:
            consultorios = db.obtener_registros("SELECT id_consultorio, numero FROM Consultorio ORDER BY numero")
            db.desconectar()
            if consultorios:
                self.combo_consultorio['values'] = [f"Consultorio {c['numero']}" for c in consultorios]
                self.consultorios_data = consultorios
                if consultorios:
                    self.combo_consultorio.current(0)
        except:
            db.desconectar()
    
    def _crear_medico(self):
        matricula = self.entry_matricula.get().strip()
        nombre = self.entry_nombre.get().strip()
        apellido = self.entry_apellido.get().strip()
        telefono = self.entry_telefono.get().strip()
        email = self.entry_email.get().strip()
        fecha_alta = self.entry_fecha_alta.get().strip()
        
        if not matricula or not nombre or not apellido or not email:
            messagebox.showwarning("Advertencia", "Matrícula, nombre, apellido y email son obligatorios")
            return
        
        if "@" not in email:
            messagebox.showwarning("Advertencia", "El email no es válido")
            return
        
        especialidades_ids = [esp_id for esp_id, var in self.var_especialidades.items() if var.get()]
        
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
        
        ok, msg = self.controller.crear(
            matricula, nombre, apellido, telefono, email, fecha_alta, 
            especialidades_ids, agenda_data
        )
        
        if ok:
            messagebox.showinfo("Éxito", "✓ Médico creado exitosamente\n✓ Agenda programada\n✓ Turnos generados automáticamente")
            self.window.destroy()
        else:
            messagebox.showerror("Error", msg)
