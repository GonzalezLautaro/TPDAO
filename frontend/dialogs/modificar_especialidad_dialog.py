import tkinter as tk
from tkinter import ttk, messagebox


class ModificarEspecialidadDialog:
    def __init__(self, parent, controller, especialidad_data):
        self.controller = controller
        self.especialidad_data = especialidad_data
        self.window = tk.Toplevel(parent)
        self.window.title("Modificar Especialidad")
        self.window.geometry("550x450")
        self.window.resizable(False, False)
        
        # Container principal con padding
        container = ttk.Frame(self.window, padding=15)
        container.pack(fill="both", expand=True)
        
        # Título
        titulo = ttk.Label(
            container,
            text=f"Modificar Especialidad: {especialidad_data['nombre']}",
            font=("Arial", 13, "bold")
        )
        titulo.pack(pady=(0, 20))
        
        # Form frame
        form_frame = ttk.LabelFrame(container, text="Datos de la Especialidad", padding=15)
        form_frame.pack(fill="both", expand=True, pady=(0, 15))
        
        # ID (NO EDITABLE)
        ttk.Label(form_frame, text="ID Especialidad:", font=("Arial", 9, "bold")).grid(row=0, column=0, sticky="w", pady=10, padx=(0, 15))
        id_label = ttk.Label(form_frame, text=str(especialidad_data['id_especialidad']), font=("Arial", 10))
        id_label.grid(row=0, column=1, sticky="w", pady=10, padx=(0, 0))
        
        # Nombre
        ttk.Label(form_frame, text="Nombre:", font=("Arial", 9)).grid(row=1, column=0, sticky="w", pady=10, padx=(0, 15))
        self.entry_nombre = ttk.Entry(form_frame, width=30, font=("Arial", 9))
        self.entry_nombre.insert(0, especialidad_data['nombre'])
        self.entry_nombre.grid(row=1, column=1, sticky="ew", padx=(0, 0), pady=10)
        
        # Descripción
        ttk.Label(form_frame, text="Descripción:", font=("Arial", 9)).grid(row=2, column=0, sticky="nw", pady=10, padx=(0, 15))
        self.text_descripcion = tk.Text(form_frame, height=6, width=30, font=("Arial", 9))
        self.text_descripcion.insert("1.0", especialidad_data['descripcion'])
        self.text_descripcion.grid(row=2, column=1, sticky="ew", padx=(0, 0), pady=10)
        
        form_frame.columnconfigure(1, weight=1)
        
        # Frame de botones
        btn_frame = ttk.Frame(container)
        btn_frame.pack(fill="x", side="bottom", expand=False, pady=(10, 0))
        
        ttk.Button(btn_frame, text="Guardar", command=self._modificar_especialidad).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Cancelar", command=self.window.destroy).pack(side="left", padx=5)
    
    def _modificar_especialidad(self):
        """Valida y modifica la especialidad"""
        nombre = self.entry_nombre.get().strip()
        descripcion = self.text_descripcion.get("1.0", tk.END).strip()
        
        if not nombre:
            messagebox.showwarning("Advertencia", "El nombre es obligatorio")
            return
        
        if not descripcion:
            messagebox.showwarning("Advertencia", "La descripción es obligatoria")
            return
        
        # ✅ CAMBIAR: self.controller.modificar → self.controller.actualizar_especialidad
        if self.controller.actualizar_especialidad(self.especialidad_data['id_especialidad'], nombre, descripcion):
            messagebox.showinfo("Éxito", "✓ Especialidad modificada exitosamente")
            self.window.destroy()
        else:
            messagebox.showerror("Error", "No se pudo modificar la especialidad")
