import tkinter as tk
from tkinter import ttk, messagebox

from ..controllers.medicos_controller import MedicosController
from ..dialogs.crear_medico_dialog import CrearMedicoDialog
from ..dialogs.modificar_medico_dialog import ModificarMedicoDialog


class MedicosView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=12)
        self.ctrl = MedicosController()
        
        # Frame superior con botones
        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill="x", pady=(0, 10))
        
        ttk.Button(btn_frame, text="➕ Crear Nuevo Médico", command=self._crear_medico).pack(side="left")
        ttk.Button(btn_frame, text="🔄 Refrescar", command=self._refresh).pack(side="left", padx=5)
        
        # Frame de búsqueda
        search_frame = ttk.LabelFrame(self, text="Buscar Médico", padding=10)
        search_frame.pack(fill="x", pady=(0, 10))
        
        ttk.Label(search_frame, text="Buscar por nombre o matrícula:").pack(side="left")
        
        self.entry_busqueda = ttk.Entry(search_frame, width=30)
        self.entry_busqueda.pack(side="left", padx=(10, 0))
        self.entry_busqueda.bind("<KeyRelease>", lambda e: self._filtrar_medicos())
        
        ttk.Button(search_frame, text="✕ Limpiar", command=self._limpiar_busqueda).pack(side="left", padx=10)
        
        # Tabla de médicos
        tabla_frame = ttk.LabelFrame(self, text="Médicos Registrados")
        tabla_frame.pack(fill="both", expand=True)
        
        # Crear Treeview
        self.tree = ttk.Treeview(
            tabla_frame,
            columns=("matricula", "nombre", "apellido", "telefono", "email", "fecha_alta", "acciones"),
            show="headings",
            height=14
        )
        
        headers = [
            ("matricula", "Matrícula", 70),
            ("nombre", "Nombre", 120),
            ("apellido", "Apellido", 120),
            ("telefono", "Teléfono", 100),
            ("email", "Email", 160),
            ("fecha_alta", "Fecha Alta", 100),
            ("acciones", "Acciones", 180)
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
        
        # Almacenar todos los médicos
        self.todos_medicos = []
        self.medicos_filtrados = []
        
        self._refresh()
    
    def _crear_medico(self):
        """Abre el diálogo para crear un nuevo médico"""
        dialog = CrearMedicoDialog(self.winfo_toplevel(), self.ctrl)
        self.winfo_toplevel().wait_window(dialog.window)
        self._refresh()
    
    def _limpiar_busqueda(self):
        """Limpia el campo de búsqueda"""
        self.entry_busqueda.delete(0, tk.END)
        self._refresh()
    
    def _filtrar_medicos(self):
        """Filtra los médicos según el texto de búsqueda"""
        texto_busqueda = self.entry_busqueda.get().lower().strip()
        
        if not texto_busqueda:
            self.medicos_filtrados = self.todos_medicos
        else:
            self.medicos_filtrados = [
                m for m in self.todos_medicos
                if (texto_busqueda in f"{m['nombre']} {m['apellido']}".lower() or
                    texto_busqueda in str(m['matricula']))
            ]
        
        self._repoblar_tabla()
    
    def _repoblar_tabla(self):
        """Repuebla la tabla con los médicos filtrados"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for m in self.medicos_filtrados:
            self.tree.insert("", "end", values=(
                m["matricula"],
                m["nombre"],
                m["apellido"],
                m["telefono"],
                m["email"],
                m["fecha_alta"],
                "✏️ Modificar | 🗑️ Dar de Baja"
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
            
            for i, col in enumerate(["matricula", "nombre", "apellido", "telefono", "email", "fecha_alta", "acciones"]):
                col_width = self.tree.column(col, "width")
                if event.x < col_x + col_width:
                    col_num = i
                    break
                col_x += col_width
            
            # Si es la columna de acciones (columna 6)
            if col_num == 6:
                valores = self.tree.item(item)["values"]
                matricula = valores[0]
                nombre = valores[1]
                apellido = valores[2]
                telefono = valores[3]
                email = valores[4]
                fecha_alta = valores[5]
                
                # Determinar si se clickeó en "Modificar" o "Dar de Baja"
                # Obtener el ancho relativo de la columna de acciones
                acciones_col_width = self.tree.column("acciones", "width")
                acciones_col_x = col_x
                
                # Dividir en dos mitades
                mitad = acciones_col_x + (acciones_col_width / 2)
                
                if event.x < mitad:
                    # Modificar
                    medico_data = {
                        "matricula": matricula,
                        "nombre": nombre,
                        "apellido": apellido,
                        "telefono": telefono,
                        "email": email,
                        "fecha_alta": fecha_alta
                    }
                    
                    dialog = ModificarMedicoDialog(self.winfo_toplevel(), self.ctrl, medico_data)
                    self.winfo_toplevel().wait_window(dialog.window)
                    self._refresh()
                else:
                    # Dar de Baja
                    self._dar_de_baja_medico(matricula, nombre, apellido)
        
        except Exception as e:
            print(f"[ERROR] Error en click: {str(e)}")
            import traceback
            traceback.print_exc()
    
    def _dar_de_baja_medico(self, matricula, nombre, apellido):
        """Da de baja un médico"""
        respuesta = messagebox.askyesno(
            "Confirmar",
            f"¿Deseas dar de baja a {nombre} {apellido}?"
        )
        
        if respuesta:
            ok, msg = self.ctrl.dar_de_baja(matricula)
            if ok:
                messagebox.showinfo("Éxito", f"✓ {nombre} {apellido} dado de baja correctamente")
                self._refresh()
            else:
                messagebox.showerror("Error", msg)
    
    def _refresh(self):
        """Recarga la lista de médicos"""
        try:
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            medicos = self.ctrl.listar()
            
            for medico in medicos:
                # ✅ CAMBIAR: medico['id'] → medico['matricula']
                self.tree.insert("", "end", values=(
                    medico['matricula'],  # ← CAMBIAR AQUÍ
                    f"{medico['nombre']} {medico['apellido']}",
                    medico['telefono'],
                    medico['email'],
                    medico['fecha_ingreso']
                ))
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar médicos: {str(e)}")
