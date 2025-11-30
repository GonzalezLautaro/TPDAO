import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
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
        self.window.geometry("600x550")
        self.window.resizable(False, False)
        
        # Container principal con padding
        container = ttk.Frame(self.window, padding=15)
        container.pack(fill="both", expand=True)
        
        # Título
        titulo = ttk.Label(container, text="Registrar Nuevo Médico", font=("Arial", 14, "bold"))
        titulo.pack(pady=(0, 20))
        
        # Form frame
        form_frame = ttk.Frame(container)
        form_frame.pack(fill="both", expand=True, pady=(0, 20))
        
        # Matrícula
        ttk.Label(form_frame, text="Matrícula:").grid(row=0, column=0, sticky="w", pady=8, padx=(0, 15))
        self.entry_matricula = ttk.Entry(form_frame, width=30, font=("Arial", 9))
        self.entry_matricula.grid(row=0, column=1, sticky="ew", pady=8)
        
        # Nombre
        ttk.Label(form_frame, text="Nombre:").grid(row=1, column=0, sticky="w", pady=8, padx=(0, 15))
        self.entry_nombre = ttk.Entry(form_frame, width=30, font=("Arial", 9))
        self.entry_nombre.grid(row=1, column=1, sticky="ew", pady=8)
        
        # Apellido
        ttk.Label(form_frame, text="Apellido:").grid(row=2, column=0, sticky="w", pady=8, padx=(0, 15))
        self.entry_apellido = ttk.Entry(form_frame, width=30, font=("Arial", 9))
        self.entry_apellido.grid(row=2, column=1, sticky="ew", pady=8)
        
        # Teléfono
        ttk.Label(form_frame, text="Teléfono:").grid(row=3, column=0, sticky="w", pady=8, padx=(0, 15))
        self.entry_telefono = ttk.Entry(form_frame, width=30, font=("Arial", 9))
        self.entry_telefono.grid(row=3, column=1, sticky="ew", pady=8)
        
        # Email
        ttk.Label(form_frame, text="Email:").grid(row=4, column=0, sticky="w", pady=8, padx=(0, 15))
        self.entry_email = ttk.Entry(form_frame, width=30, font=("Arial", 9))
        self.entry_email.grid(row=4, column=1, sticky="ew", pady=8)
        
        # Fecha de Alta
        ttk.Label(form_frame, text="Fecha Alta (YYYY-MM-DD):").grid(row=5, column=0, sticky="w", pady=8, padx=(0, 15))
        self.entry_fecha_alta = ttk.Entry(form_frame, width=30, font=("Arial", 9))
        self.entry_fecha_alta.insert(0, str(date.today()))
        self.entry_fecha_alta.grid(row=5, column=1, sticky="ew", pady=8)
        
        # Especialidades - Cambiar a Listbox con scroll
        ttk.Label(form_frame, text="Especialidades:").grid(row=6, column=0, sticky="nw", pady=(8, 0), padx=(0, 15))
        
        # Frame para especialidades con Listbox
        esp_frame = ttk.LabelFrame(form_frame, text="Selecciona una o más (Ctrl+Click)", padding=10)
        esp_frame.grid(row=6, column=1, sticky="ew", pady=8)
        
        # Scrollbar para el Listbox
        scrollbar_esp = ttk.Scrollbar(esp_frame, orient="vertical")
        scrollbar_esp.pack(side="right", fill="y")
        
        # Listbox con selección múltiple
        self.listbox_especialidades = tk.Listbox(
            esp_frame, 
            selectmode="multiple",
            yscrollcommand=scrollbar_esp.set,
            height=6,
            font=("Arial", 9)
        )
        self.listbox_especialidades.pack(side="left", fill="both", expand=True)
        scrollbar_esp.config(command=self.listbox_especialidades.yview)
        
        # Cargar especialidades
        self.especialidades = self._cargar_especialidades()
        
        if self.especialidades:
            for esp in self.especialidades:
                texto = f"{esp['nombre']} - {esp['descripcion']}"
                self.listbox_especialidades.insert(tk.END, texto)
        else:
            self.listbox_especialidades.insert(tk.END, "No hay especialidades disponibles")
            self.listbox_especialidades.config(state="disabled")
        
        form_frame.columnconfigure(1, weight=1)
        
        # Frame de botones
        btn_frame = ttk.Frame(container)
        btn_frame.pack(fill="x", side="bottom", expand=False, pady=(10, 0))
        
        btn_frame.columnconfigure(0, weight=1)
        
        ttk.Button(btn_frame, text="Cancelar", command=self.window.destroy).grid(row=0, column=1, padx=5, sticky="e")
        ttk.Button(btn_frame, text="✓ Crear", command=self._crear_medico).grid(row=0, column=2, padx=5, sticky="e")
    
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
    
    def _crear_medico(self):
        """Valida y crea el médico"""
        matricula = self.entry_matricula.get().strip()
        nombre = self.entry_nombre.get().strip()
        apellido = self.entry_apellido.get().strip()
        telefono = self.entry_telefono.get().strip()
        email = self.entry_email.get().strip()
        fecha_alta = self.entry_fecha_alta.get().strip()
        
        # Validaciones
        if not matricula:
            messagebox.showwarning("Advertencia", "La matrícula es obligatoria")
            return
        
        if not nombre:
            messagebox.showwarning("Advertencia", "El nombre es obligatorio")
            return
        
        if not apellido:
            messagebox.showwarning("Advertencia", "El apellido es obligatorio")
            return
        
        if not email:
            messagebox.showwarning("Advertencia", "El email es obligatorio")
            return
        
        if "@" not in email:
            messagebox.showwarning("Advertencia", "El email no es válido")
            return
        
        if not fecha_alta:
            messagebox.showwarning("Advertencia", "La fecha de alta es obligatoria")
            return
        
        # Obtener especialidades seleccionadas desde el Listbox
        especialidades_ids = []
        seleccionados = self.listbox_especialidades.curselection()
        
        for idx in seleccionados:
            if idx < len(self.especialidades):
                especialidades_ids.append(self.especialidades[idx]['id'])
        
        # Crear médico
        ok, msg = self.controller.crear(
            matricula,
            nombre,
            apellido,
            telefono,
            email,
            fecha_alta,
            especialidades_ids
        )
        
        if ok:
            messagebox.showinfo("Éxito", "✓ Médico creado exitosamente")
            self.window.destroy()
        else:
            messagebox.showerror("Error", msg)
