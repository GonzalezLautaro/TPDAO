import tkinter as tk
from tkinter import ttk, messagebox


class CrearEspecialidadDialog:
    def __init__(self, parent, controller):
        self.controller = controller
        self.window = tk.Toplevel(parent)
        self.window.title("Crear Nueva Especialidad")
        self.window.geometry("550x450")
        self.window.resizable(False, False)
        
        # Container principal con padding
        container = ttk.Frame(self.window, padding=15)
        container.pack(fill="both", expand=True)
        
        # Título
        titulo = ttk.Label(container, text="Registrar Nueva Especialidad", font=("Arial", 14, "bold"))
        titulo.pack(pady=(0, 20))
        
        # Form frame
        form_frame = ttk.Frame(container)
        form_frame.pack(fill="both", expand=True, pady=(0, 20))
        
        # ID Especialidad
        ttk.Label(form_frame, text="ID Especialidad:").grid(row=0, column=0, sticky="w", pady=10, padx=(0, 15))
        self.entry_id = ttk.Entry(form_frame, width=30, font=("Arial", 9))
        self.entry_id.grid(row=0, column=1, sticky="ew", padx=(0, 0), pady=10)
        
        # Nombre
        ttk.Label(form_frame, text="Nombre:").grid(row=1, column=0, sticky="w", pady=10, padx=(0, 15))
        self.entry_nombre = ttk.Entry(form_frame, width=30, font=("Arial", 9))
        self.entry_nombre.grid(row=1, column=1, sticky="ew", padx=(0, 0), pady=10)
        
        # Descripción
        ttk.Label(form_frame, text="Descripción:").grid(row=2, column=0, sticky="nw", pady=10, padx=(0, 15))
        self.text_descripcion = tk.Text(form_frame, height=6, width=30, font=("Arial", 9))
        self.text_descripcion.grid(row=2, column=1, sticky="ew", padx=(0, 0), pady=10)
        
        form_frame.columnconfigure(1, weight=1)
        
        # Frame de botones
        btn_frame = ttk.Frame(container)
        btn_frame.pack(fill="x", side="bottom", expand=False, pady=(10, 0))
        
        btn_frame.columnconfigure(0, weight=1)
        
        ttk.Button(btn_frame, text="Cancelar", command=self.window.destroy).grid(row=0, column=1, padx=5, sticky="e")
        ttk.Button(btn_frame, text="✓ Crear", command=self._crear_especialidad).grid(row=0, column=2, padx=5, sticky="e")
    
    def _crear_especialidad(self):
        """Valida y crea la especialidad"""
        try:
            nombre = self.entry_nombre.get().strip()
            descripcion = self.text_descripcion.get("1.0", tk.END).strip()
            
            if not nombre:
                messagebox.showwarning("Advertencia", "El nombre es obligatorio")
                return
            
            if not descripcion:
                messagebox.showwarning("Advertencia", "La descripción es obligatoria")
                return
            
            # ✅ CAMBIAR: self.controller.crear → self.controller.crear_especialidad
            if self.controller.crear_especialidad(nombre, descripcion):
                messagebox.showinfo("Éxito", "Especialidad creada correctamente")
                self.window.destroy()
            else:
                messagebox.showerror("Error", "No se pudo crear la especialidad")
        
        except Exception as e:
            messagebox.showerror("Error", f"Error: {str(e)}")
