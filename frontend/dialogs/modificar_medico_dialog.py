import tkinter as tk
from tkinter import ttk, messagebox


class ModificarMedicoDialog:
    def __init__(self, parent, controller, medico_data):
        self.controller = controller
        self.medico_data = medico_data
        self.window = tk.Toplevel(parent)
        self.window.title("Modificar Médico")
        self.window.geometry("600x550")
        self.window.resizable(False, False)
        
        # Container principal con padding
        container = ttk.Frame(self.window, padding=15)
        container.pack(fill="both", expand=True)
        
        # Título
        titulo = ttk.Label(
            container,
            text=f"Modificar Médico: {medico_data['nombre']} {medico_data['apellido']}",
            font=("Arial", 13, "bold")
        )
        titulo.pack(pady=(0, 20))
        
        # Form frame con LabelFrame
        form_frame = ttk.LabelFrame(container, text="Datos del Médico", padding=15)
        form_frame.pack(fill="both", expand=True, pady=(0, 15))
        
        # Matrícula (NO EDITABLE)
        matric_label_title = ttk.Label(form_frame, text="Matrícula:", font=("Arial", 9, "bold"))
        matric_label_title.grid(row=0, column=0, sticky="w", pady=10, padx=(0, 15))
        
        matric_value_label = ttk.Label(form_frame, text=str(medico_data['matricula']), font=("Arial", 10))
        matric_value_label.grid(row=0, column=1, sticky="w", pady=10, padx=(0, 0))
        
        # Nombre
        ttk.Label(form_frame, text="Nombre:", font=("Arial", 9)).grid(row=1, column=0, sticky="w", pady=10, padx=(0, 15))
        self.entry_nombre = ttk.Entry(form_frame, width=30, font=("Arial", 9))
        self.entry_nombre.insert(0, medico_data['nombre'])
        self.entry_nombre.grid(row=1, column=1, sticky="ew", padx=(0, 0), pady=10)
        
        # Apellido
        ttk.Label(form_frame, text="Apellido:", font=("Arial", 9)).grid(row=2, column=0, sticky="w", pady=10, padx=(0, 15))
        self.entry_apellido = ttk.Entry(form_frame, width=30, font=("Arial", 9))
        self.entry_apellido.insert(0, medico_data['apellido'])
        self.entry_apellido.grid(row=2, column=1, sticky="ew", padx=(0, 0), pady=10)
        
        # Teléfono
        ttk.Label(form_frame, text="Teléfono:", font=("Arial", 9)).grid(row=3, column=0, sticky="w", pady=10, padx=(0, 15))
        self.entry_telefono = ttk.Entry(form_frame, width=30, font=("Arial", 9))
        self.entry_telefono.insert(0, medico_data['telefono'])
        self.entry_telefono.grid(row=3, column=1, sticky="ew", padx=(0, 0), pady=10)
        
        # Email
        ttk.Label(form_frame, text="Email:", font=("Arial", 9)).grid(row=4, column=0, sticky="w", pady=10, padx=(0, 15))
        self.entry_email = ttk.Entry(form_frame, width=30, font=("Arial", 9))
        self.entry_email.insert(0, medico_data['email'])
        self.entry_email.grid(row=4, column=1, sticky="ew", padx=(0, 0), pady=10)
        
        # ✅ CAMBIAR: Label de "Fecha de Alta" a "Fecha de Ingreso"
        ttk.Label(form_frame, text="Fecha Ingreso (YYYY-MM-DD):", font=("Arial", 9)).grid(row=5, column=0, sticky="w", pady=10, padx=(0, 15))
        
        # ✅ Cambiar nombre de variable y acceso al campo correcto
        self.entry_fecha_ingreso = ttk.Entry(form_frame, width=30, font=("Arial", 9), state="readonly")
        # ✅ CAMBIAR: fecha_alta → fecha_ingreso
        self.entry_fecha_ingreso.insert(0, str(medico_data.get('fecha_ingreso', '')))
        self.entry_fecha_ingreso.grid(row=5, column=1, sticky="ew", padx=(0, 0), pady=10)
        
        form_frame.columnconfigure(1, weight=1)
        
        # Frame de botones
        btn_frame = ttk.Frame(container)
        btn_frame.pack(fill="x", side="bottom", expand=False, pady=(10, 0))
        
        btn_frame.columnconfigure(0, weight=1)
        
        ttk.Button(btn_frame, text="Cancelar", command=self.window.destroy).grid(row=0, column=1, padx=5, sticky="e")
        ttk.Button(btn_frame, text="✓ Guardar Cambios", command=self._guardar).grid(row=0, column=2, padx=5, sticky="e")
    
    def _guardar(self):
        """Guarda los cambios del médico"""
        try:
            nombre = self.entry_nombre.get().strip()
            apellido = self.entry_apellido.get().strip()
            telefono = self.entry_telefono.get().strip()
            email = self.entry_email.get().strip()
            
            if not all([nombre, apellido, email]):
                messagebox.showerror("Error", "Todos los campos son obligatorios")
                return
            
            if self.controller.actualizar_medico(self.medico_data['matricula'], nombre, apellido, telefono, email):
                messagebox.showinfo("Éxito", "Médico actualizado correctamente")
                self.window.destroy()
            else:
                messagebox.showerror("Error", "No se pudo actualizar el médico")
        
        except Exception as e:
            messagebox.showerror("Error", f"Error: {str(e)}")
