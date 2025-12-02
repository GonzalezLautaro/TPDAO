import tkinter as tk
from tkinter import ttk, messagebox

from ..controllers.especialidades_controller import EspecialidadesController
from ..dialogs.crear_especialidad_dialog import CrearEspecialidadDialog
from ..dialogs.modificar_especialidad_dialog import ModificarEspecialidadDialog


class EspecialidadesView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=12)
        self.ctrl = EspecialidadesController()
        
        # Frame superior con botones
        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill="x", pady=(0, 10))
        
        ttk.Button(btn_frame, text="➕ Crear Nueva Especialidad", command=self._crear_especialidad).pack(side="left")
        ttk.Button(btn_frame, text="🔄 Refrescar", command=self._refresh).pack(side="left", padx=5)
        
        # Frame de búsqueda
        search_frame = ttk.LabelFrame(self, text="Buscar Especialidad", padding=10)
        search_frame.pack(fill="x", pady=(0, 10))
        
        ttk.Label(search_frame, text="Buscar por nombre:").pack(side="left")
        
        self.entry_busqueda = ttk.Entry(search_frame, width=30)
        self.entry_busqueda.pack(side="left", padx=(10, 0))
        self.entry_busqueda.bind("<KeyRelease>", lambda e: self._filtrar_especialidades())
        
        ttk.Button(search_frame, text="✕ Limpiar", command=self._limpiar_busqueda).pack(side="left", padx=10)
        
        # Tabla de especialidades
        tabla_frame = ttk.LabelFrame(self, text="Especialidades Registradas")
        tabla_frame.pack(fill="both", expand=True)
        
        # Crear Treeview
        self.tree = ttk.Treeview(
            tabla_frame,
            columns=("id", "nombre", "descripcion", "acciones"),
            show="headings",
            height=14
        )
        
        headers = [
            ("id", "ID", 50),
            ("nombre", "Nombre", 150),
            ("descripcion", "Descripción", 350),
            ("acciones", "Acciones", 200)
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
        
        # Almacenar todas las especialidades
        self.todas_especialidades = []
        self.especialidades_filtradas = []
        
        self._refresh()
    
    def _crear_especialidad(self):
        """Abre el diálogo para crear una nueva especialidad"""
        dialog = CrearEspecialidadDialog(self.winfo_toplevel(), self.ctrl)
        self.winfo_toplevel().wait_window(dialog.window)
        self._refresh()
    
    def _limpiar_busqueda(self):
        """Limpia el campo de búsqueda"""
        self.entry_busqueda.delete(0, tk.END)
        self._refresh()
    
    def _filtrar_especialidades(self):
        """Filtra las especialidades según el texto de búsqueda"""
        texto_busqueda = self.entry_busqueda.get().lower().strip()
        
        if not texto_busqueda:
            self.especialidades_filtradas = self.todas_especialidades
        else:
            self.especialidades_filtradas = [
                e for e in self.todas_especialidades
                if texto_busqueda in e['nombre'].lower()
            ]
        
        self._repoblar_tabla()
    
    def _repoblar_tabla(self):
        """Repuebla la tabla con las especialidades filtradas"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for e in self.especialidades_filtradas:
            self.tree.insert("", "end", values=(
                e["id"],
                e["nombre"],
                e["descripcion"],
                "✏️ Modificar | 🗑️ Eliminar"
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
            
            for i, col in enumerate(["id", "nombre", "descripcion", "acciones"]):
                col_width = self.tree.column(col, "width")
                if event.x < col_x + col_width:
                    col_num = i
                    break
                col_x += col_width
            
            # Si es la columna de acciones (columna 3)
            if col_num == 3:
                valores = self.tree.item(item)["values"]
                id_especialidad = valores[0]
                nombre = valores[1]
                descripcion = valores[2]
                
                # Determinar si se clickeó en "Modificar" o "Eliminar"
                acciones_col_width = self.tree.column("acciones", "width")
                acciones_col_x = col_x
                
                # Dividir en dos mitades
                mitad = acciones_col_x + (acciones_col_width / 2)
                
                if event.x < mitad:
                    # Modificar
                    especialidad_data = {
                        "id": id_especialidad,
                        "nombre": nombre,
                        "descripcion": descripcion
                    }
                    
                    dialog = ModificarEspecialidadDialog(self.winfo_toplevel(), self.ctrl, especialidad_data)
                    self.winfo_toplevel().wait_window(dialog.window)
                    self._refresh()
                else:
                    # Eliminar
                    self._eliminar_especialidad(id_especialidad, nombre)
        
        except Exception as e:
            print(f"[ERROR] Error en click: {str(e)}")
            import traceback
            traceback.print_exc()
    
    def _eliminar_especialidad(self, id_especialidad, nombre):
        """Elimina una especialidad"""
        respuesta = messagebox.askyesno(
            "Confirmar",
            f"¿Deseas eliminar la especialidad '{nombre}'?"
        )
        
        if respuesta:
            ok, msg = self.ctrl.eliminar(id_especialidad)
            if ok:
                messagebox.showinfo("Éxito", f"✓ Especialidad '{nombre}' eliminada correctamente")
                self._refresh()
            else:
                messagebox.showerror("Error", msg)
    
    def _refresh(self):
        """Recarga la lista de especialidades"""
        self.todas_especialidades = self.ctrl.listar()
        self.especialidades_filtradas = self.todas_especialidades
        self.entry_busqueda.delete(0, tk.END)
        self._repoblar_tabla()
