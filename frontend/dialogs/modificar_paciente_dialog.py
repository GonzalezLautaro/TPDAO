import tkinter as tk
from tkinter import ttk, messagebox


class ModificarPacienteDialog:
    def __init__(self, parent, controller, paciente_data):
        self.controller = controller
        self.paciente_data = paciente_data
        
        self.window = tk.Toplevel(parent)
        self.window.title(f"Modificar Paciente: {paciente_data['nombre_completo']}")
        self.window.geometry("400x350")
        
        # Frame principal
        main_frame = ttk.Frame(self.window, padding=15)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Campos
        ttk.Label(main_frame, text="Nombre:", font=("Arial", 9, "bold")).grid(row=0, column=0, sticky="w", pady=10)
        self.entry_nombre = ttk.Entry(main_frame, width=30, font=("Arial", 9))
        self.entry_nombre.insert(0, paciente_data.get('nombre_completo', '').split()[0])
        self.entry_nombre.grid(row=0, column=1, sticky="ew", pady=10)
        
        ttk.Label(main_frame, text="Apellido:", font=("Arial", 9, "bold")).grid(row=1, column=0, sticky="w", pady=10)
        self.entry_apellido = ttk.Entry(main_frame, width=30, font=("Arial", 9))
        # ✅ Extraer apellido correctamente
        nombres_split = paciente_data.get('nombre_completo', '').split()
        apellido = nombres_split[1] if len(nombres_split) > 1 else ''
        self.entry_apellido.insert(0, apellido)
        self.entry_apellido.grid(row=1, column=1, sticky="ew", pady=10)
        
        ttk.Label(main_frame, text="Teléfono:", font=("Arial", 9, "bold")).grid(row=2, column=0, sticky="w", pady=10)
        self.entry_telefono = ttk.Entry(main_frame, width=30, font=("Arial", 9))
        self.entry_telefono.insert(0, paciente_data.get('telefono', ''))
        self.entry_telefono.grid(row=2, column=1, sticky="ew", pady=10)
        
        ttk.Label(main_frame, text="Dirección:", font=("Arial", 9, "bold")).grid(row=3, column=0, sticky="w", pady=10)
        self.text_direccion = tk.Text(main_frame, width=30, height=3, font=("Arial", 9))
        self.text_direccion.insert("1.0", paciente_data.get('direccion', ''))
        self.text_direccion.grid(row=3, column=1, sticky="ew", pady=10)
        
        # Botones
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=4, column=0, columnspan=2, sticky="ew", pady=20)
        
        ttk.Button(btn_frame, text="Guardar", command=self._guardar).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancelar", command=self.window.destroy).pack(side=tk.LEFT, padx=5)
    
    def _guardar(self):
        """Guarda los cambios del paciente"""
        try:
            nombre = self.entry_nombre.get().strip()
            apellido = self.entry_apellido.get().strip()
            telefono = self.entry_telefono.get().strip()
            direccion = self.text_direccion.get("1.0", tk.END).strip()
            
            if not all([nombre, apellido, direccion]):
                messagebox.showerror("Error", "Todos los campos son obligatorios")
                return
            
            # ✅ USAR id_paciente, NO id
            if self.controller.actualizar_paciente(
                self.paciente_data['id_paciente'],
                nombre,
                apellido,
                telefono,
                direccion
            ):
                messagebox.showinfo("Éxito", "Paciente actualizado correctamente")
                self.window.destroy()
            else:
                messagebox.showerror("Error", "No se pudo actualizar el paciente")
        
        except Exception as e:
            messagebox.showerror("Error", f"Error: {str(e)}")
