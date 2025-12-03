import tkinter as tk
from tkinter import ttk, messagebox

from ..controllers.pacientes_controller import PacientesController
from ..dialogs.crear_paciente_dialog import CrearPacienteDialog
from ..dialogs.modificar_paciente_dialog import ModificarPacienteDialog
from ..dialogs.ver_historial_dialog import VerHistorialDialog


class PacientesView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=12)
        self.ctrl = PacientesController()
        
        # Frame superior con botones
        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill="x", pady=(0, 10))
        
        ttk.Button(btn_frame, text="➕ Crear Nuevo Paciente", command=self._crear_paciente).pack(side="left")
        ttk.Button(btn_frame, text="🔄 Refrescar", command=self._refresh).pack(side="left", padx=5)
        
        # Frame de búsqueda
        search_frame = ttk.LabelFrame(self, text="Buscar Paciente", padding=10)
        search_frame.pack(fill="x", pady=(0, 10))
        
        ttk.Label(search_frame, text="Buscar por nombre o ID:").pack(side="left")
        
        self.entry_busqueda = ttk.Entry(search_frame, width=30)
        self.entry_busqueda.pack(side="left", padx=(10, 0))
        self.entry_busqueda.bind("<KeyRelease>", lambda e: self._filtrar_pacientes())
        
        ttk.Button(search_frame, text="✕ Limpiar", command=self._limpiar_busqueda).pack(side="left", padx=10)
        
        # Tabla de pacientes
        tabla_frame = ttk.LabelFrame(self, text="Pacientes Registrados")
        tabla_frame.pack(fill="both", expand=True)
        
        # Crear Treeview
        self.tree = ttk.Treeview(
            tabla_frame,
            columns=("id", "nombre", "apellido", "telefono", "nacimiento", "direccion", "acciones"),
            show="headings",
            height=14
        )
        
        headers = [
            ("id", "ID", 50),
            ("nombre", "Nombre", 120),
            ("apellido", "Apellido", 120),
            ("telefono", "Teléfono", 100),
            ("nacimiento", "Nacimiento", 100),
            ("direccion", "Dirección", 150),
            ("acciones", "Acciones", 230)
        ]
        
        for col, text, width in headers:
            self.tree.heading(col, text=text)
            self.tree.column(col, width=width)
        
        scrollbar = ttk.Scrollbar(tabla_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind para detectar clicks en la columna de acciones
        self.tree.bind("<Button-1>", self._on_tree_click)
        
        # Almacenar todos los pacientes
        self.todos_pacientes = []
        self.pacientes_filtrados = []
        
        self._refresh()
    
    def _crear_paciente(self):
        """Abre el diálogo para crear un nuevo paciente"""
        dialog = CrearPacienteDialog(self.winfo_toplevel(), self.ctrl)
        self.winfo_toplevel().wait_window(dialog.window)
        self._refresh()
    
    def _limpiar_busqueda(self):
        """Limpia el campo de búsqueda"""
        self.entry_busqueda.delete(0, tk.END)
        self._refresh()
    
    def _filtrar_pacientes(self):
        """Filtra los pacientes según el texto de búsqueda"""
        texto_busqueda = self.entry_busqueda.get().lower().strip()
        
        if not texto_busqueda:
            self.pacientes_filtrados = self.todos_pacientes
        else:
            self.pacientes_filtrados = [
                p for p in self.todos_pacientes
                if (texto_busqueda in f"{p['nombre']} {p['apellido']}".lower() or
                    texto_busqueda in str(p['id']))
            ]
        
        self._repoblar_tabla()
    
    def _repoblar_tabla(self):
        """Repuebla la tabla con los pacientes filtrados"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for p in self.pacientes_filtrados:
            self.tree.insert("", "end", values=(
                p["id"],
                p["nombre"],
                p["apellido"],
                p["telefono"],
                p["nacimiento"],
                p["direccion"],
                "✏️ Modificar | 👁️ Historial | 🗑️ Baja"
            ))
    
    def _on_tree_click(self, event):
        """Maneja clicks en la tabla"""
        try:
            item = self.tree.identify("item", event.x, event.y)
            if not item:
                return
            
            # Obtener el ancho de cada columna para detectar qué columna se clickeó
            col_num = 0
            col_x = 0
            
            # Usar los IDs de columna definidos en el Treeview
            for i, col in enumerate(["id", "nombre", "apellido", "telefono", "nacimiento", "direccion", "acciones"]):
                col_width = self.tree.column(col, "width")
                if event.x < col_x + col_width:
                    col_num = i
                    break
                col_x += col_width
            
            # Si es la columna de acciones (columna 6)
            if col_num == 6:
                valores = self.tree.item(item)["values"]
                id_paciente = valores[0]
                nombre = valores[1]
                apellido = valores[2]
                telefono = valores[3]
                nacimiento = valores[4]
                direccion = valores[5]
                
                # Obtener el ancho relativo de la columna de acciones
                acciones_col_width = self.tree.column("acciones", "width")
                acciones_col_x = col_x
                
                # Dividir en tres secciones
                sec1 = acciones_col_x + (acciones_col_width / 3)
                sec2 = acciones_col_x + (acciones_col_width * 2 / 3)
                
                if event.x < sec1:
                    # Modificar
                    paciente_data = {
                        "id_paciente": id_paciente,
                        "nombre": nombre,
                        "apellido": apellido,
                        "telefono": telefono,
                        "nacimiento": nacimiento,
                        "direccion": direccion
                    }
                    
                    dialog = ModificarPacienteDialog(self.winfo_toplevel(), self.ctrl, paciente_data)
                    self.winfo_toplevel().wait_window(dialog.window)
                    self._refresh()
                
                elif event.x < sec2:
                    # Ver Historial
                    self._ver_historial_paciente(id_paciente, nombre, apellido)
                
                else:
                    # Dar de Baja
                    self._dar_de_baja_paciente(id_paciente, nombre, apellido)
        
        except Exception as e:
            print(f"[ERROR] Error en click: {str(e)}")
            import traceback
            traceback.print_exc()
    
    def _ver_historial_paciente(self, id_paciente, nombre, apellido):
        """Abre el diálogo para ver el historial del paciente"""
        historial = self.ctrl.obtener_historial(id_paciente)
        
        if not historial:
            messagebox.showinfo("Historial Clínico", f"{nombre} {apellido}\n\nNo tiene historial médico registrado")
            return
        
        dialog = VerHistorialDialog(self.winfo_toplevel(), nombre, apellido, historial)
        self.winfo_toplevel().wait_window(dialog.window)
    
    def _dar_de_baja_paciente(self, id_paciente, nombre, apellido):
        """Da de baja un paciente"""
        respuesta = messagebox.askyesno(
            "Confirmar",
            f"¿Deseas dar de baja a {nombre} {apellido}?"
        )
        
        if respuesta:
            try:
                self.ctrl.dar_de_baja_paciente(id_paciente)
                messagebox.showinfo("Éxito", f"{nombre} {apellido} ha sido dado de baja")
                self._refresh()
            except Exception as e:
                messagebox.showerror("Error", f"Error al dar de baja: {str(e)}")
    
    def _refresh(self):
        """Recarga la lista de pacientes"""
        try:
            self.todos_pacientes = self.ctrl.obtener_pacientes()
            self._filtrar_pacientes()
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar pacientes: {str(e)}")
