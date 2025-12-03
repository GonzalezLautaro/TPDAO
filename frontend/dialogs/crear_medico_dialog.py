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
        self.window.geometry("620x620")
        self.window.resizable(False, False)
        
        # Container principal con padding
        container = ttk.Frame(self.window, padding=20)
        container.pack(fill="both", expand=True)
        
        # Título
        titulo = ttk.Label(container, text="Registrar Nuevo Médico", font=("Arial", 14, "bold"))
        titulo.pack(pady=(0, 15))
        
        # Form frame
        form_frame = ttk.Frame(container)
        form_frame.pack(fill="both", expand=True, pady=(0, 15))
        
        # Matrícula
        ttk.Label(form_frame, text="Matrícula:").grid(row=0, column=0, sticky="w", pady=8, padx=(0, 15))
        self.entry_matricula = ttk.Entry(form_frame, width=35, font=("Arial", 9))
        self.entry_matricula.grid(row=0, column=1, sticky="ew", pady=8)
        
        # Nombre
        ttk.Label(form_frame, text="Nombre:").grid(row=1, column=0, sticky="w", pady=8, padx=(0, 15))
        self.entry_nombre = ttk.Entry(form_frame, width=35, font=("Arial", 9))
        self.entry_nombre.grid(row=1, column=1, sticky="ew", pady=8)
        
        # Apellido
        ttk.Label(form_frame, text="Apellido:").grid(row=2, column=0, sticky="w", pady=8, padx=(0, 15))
        self.entry_apellido = ttk.Entry(form_frame, width=35, font=("Arial", 9))
        self.entry_apellido.grid(row=2, column=1, sticky="ew", pady=8)
        
        # Teléfono
        ttk.Label(form_frame, text="Teléfono:").grid(row=3, column=0, sticky="w", pady=8, padx=(0, 15))
        self.entry_telefono = ttk.Entry(form_frame, width=35, font=("Arial", 9))
        self.entry_telefono.grid(row=3, column=1, sticky="ew", pady=8)
        
        # Email
        ttk.Label(form_frame, text="Email:").grid(row=4, column=0, sticky="w", pady=8, padx=(0, 15))
        self.entry_email = ttk.Entry(form_frame, width=35, font=("Arial", 9))
        self.entry_email.grid(row=4, column=1, sticky="ew", pady=8)
        
        # Fecha de Ingreso
        ttk.Label(form_frame, text="Fecha Ingreso (YYYY-MM-DD):", font=("Arial", 9)).grid(row=5, column=0, sticky="w", pady=10, padx=(0, 15))
        
        self.entry_fecha_ingreso = ttk.Entry(form_frame, width=30, font=("Arial", 9))
        self.entry_fecha_ingreso.insert(0, str(date.today()))
        self.entry_fecha_ingreso.grid(row=5, column=1, sticky="ew", padx=(0, 0), pady=10)
        
        form_frame.columnconfigure(1, weight=1)
        
        # Frame de botones (separado del container principal)
        btn_frame = ttk.Frame(container)
        btn_frame.pack(fill="x", side="bottom", pady=(15, 0))
        
        # Espaciador a la izquierda
        ttk.Frame(btn_frame).pack(side="left", expand=True)
        
        # Botones a la derecha
        ttk.Button(btn_frame, text="Cancelar", command=self.window.destroy, width=12).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="✓ Crear", command=self._crear_medico, width=12).pack(side="left", padx=5)
    
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
        try:
            matricula = int(self.entry_matricula.get().strip())
            nombre = self.entry_nombre.get().strip()
            apellido = self.entry_apellido.get().strip()
            telefono = self.entry_telefono.get().strip()
            email = self.entry_email.get().strip()
            fecha_ingreso = self.entry_fecha_ingreso.get().strip()
            
            if not all([nombre, apellido, email, fecha_ingreso]):
                messagebox.showwarning("Advertencia", "Todos los campos son obligatorios")
                return
            
            # Crear médico
            if self.controller.crear_medico(matricula, nombre, apellido, telefono, email, fecha_ingreso):
                messagebox.showinfo("Éxito", "Médico creado correctamente")
                self.window.destroy()
            else:
                messagebox.showerror("Error", "No se pudo crear el médico")
        
        except ValueError:
            messagebox.showerror("Error", "La matrícula debe ser un número")
        except Exception as e:
            messagebox.showerror("Error", f"Error: {str(e)}")
