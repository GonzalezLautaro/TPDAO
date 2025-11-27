import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date


class CrearMedicoDialog:
    def __init__(self, parent, controller):
        self.controller = controller
        self.window = tk.Toplevel(parent)
        self.window.title("Crear Nuevo Médico")
        self.window.geometry("550x500")
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
        ttk.Label(form_frame, text="Matrícula:").grid(row=0, column=0, sticky="w", pady=10, padx=(0, 15))
        self.entry_matricula = ttk.Entry(form_frame, width=30, font=("Arial", 9))
        self.entry_matricula.grid(row=0, column=1, sticky="ew", padx=(0, 0), pady=10)
        
        # Nombre
        ttk.Label(form_frame, text="Nombre:").grid(row=1, column=0, sticky="w", pady=10, padx=(0, 15))
        self.entry_nombre = ttk.Entry(form_frame, width=30, font=("Arial", 9))
        self.entry_nombre.grid(row=1, column=1, sticky="ew", padx=(0, 0), pady=10)
        
        # Apellido
        ttk.Label(form_frame, text="Apellido:").grid(row=2, column=0, sticky="w", pady=10, padx=(0, 15))
        self.entry_apellido = ttk.Entry(form_frame, width=30, font=("Arial", 9))
        self.entry_apellido.grid(row=2, column=1, sticky="ew", padx=(0, 0), pady=10)
        
        # Teléfono
        ttk.Label(form_frame, text="Teléfono:").grid(row=3, column=0, sticky="w", pady=10, padx=(0, 15))
        self.entry_telefono = ttk.Entry(form_frame, width=30, font=("Arial", 9))
        self.entry_telefono.grid(row=3, column=1, sticky="ew", padx=(0, 0), pady=10)
        
        # Email
        ttk.Label(form_frame, text="Email:").grid(row=4, column=0, sticky="w", pady=10, padx=(0, 15))
        self.entry_email = ttk.Entry(form_frame, width=30, font=("Arial", 9))
        self.entry_email.grid(row=4, column=1, sticky="ew", padx=(0, 0), pady=10)
        
        # Fecha de Alta → cambiar label a "Fecha de Ingreso"
        ttk.Label(form_frame, text="Fecha Ingreso (YYYY-MM-DD):", font=("Arial", 9)).grid(row=5, column=0, sticky="w", pady=10, padx=(0, 15))
        
        # Cambiar nombre de variable para claridad
        self.entry_fecha_ingreso = ttk.Entry(form_frame, width=30, font=("Arial", 9))
        self.entry_fecha_ingreso.insert(0, str(date.today()))
        self.entry_fecha_ingreso.grid(row=5, column=1, sticky="ew", padx=(0, 0), pady=10)
        
        form_frame.columnconfigure(1, weight=1)
        
        # Frame de botones
        btn_frame = ttk.Frame(container)
        btn_frame.pack(fill="x", side="bottom", expand=False, pady=(10, 0))
        
        btn_frame.columnconfigure(0, weight=1)
        
        ttk.Button(btn_frame, text="Cancelar", command=self.window.destroy).grid(row=0, column=1, padx=5, sticky="e")
        ttk.Button(btn_frame, text="✓ Crear", command=self._crear_medico).grid(row=0, column=2, padx=5, sticky="e")
    
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
            
            # ✅ CAMBIAR: self.controller.crear → self.controller.crear_medico
            if self.controller.crear_medico(matricula, nombre, apellido, telefono, email, fecha_ingreso):
                messagebox.showinfo("Éxito", "Médico creado correctamente")
                self.window.destroy()
            else:
                messagebox.showerror("Error", "No se pudo crear el médico")
        
        except ValueError:
            messagebox.showerror("Error", "La matrícula debe ser un número")
        except Exception as e:
            messagebox.showerror("Error", f"Error: {str(e)}")
