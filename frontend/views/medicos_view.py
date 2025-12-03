import tkinter as tk
from tkinter import ttk, messagebox
import sys, os

# Agregar TPDAO al path
BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if BASE not in sys.path:
    sys.path.insert(0, BASE)

from ..controllers.medicos_controller import MedicosController
from ..dialogs.crear_medico_dialog import CrearMedicoDialog
from ..dialogs.modificar_medico_dialog import ModificarMedicoDialog
from data.database import Database


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
        
        # Fila 1: Búsqueda por texto
        ttk.Label(search_frame, text="Buscar por nombre o matrícula:").grid(row=0, column=0, sticky="w", pady=(0, 5))
        
        self.entry_busqueda = ttk.Entry(search_frame, width=30)
        self.entry_busqueda.grid(row=0, column=1, sticky="ew", padx=(10, 5), pady=(0, 5))
        self.entry_busqueda.bind("<KeyRelease>", lambda e: self._filtrar_medicos())
        
        ttk.Button(search_frame, text="✕ Limpiar", command=self._limpiar_busqueda).grid(row=0, column=2, padx=(0, 0), pady=(0, 5))
        
        # Fila 2: Filtro por especialidad
        ttk.Label(search_frame, text="Filtrar por especialidad:").grid(row=1, column=0, sticky="w", pady=(5, 0))
        
        self.especialidad_var = tk.StringVar(value="Todas")
        
        self.combo_especialidad = ttk.Combobox(
            search_frame,
            textvariable=self.especialidad_var,
            values=["Todas"],
            state="readonly",
            width=27
        )
        self.combo_especialidad.grid(row=1, column=1, sticky="ew", padx=(10, 5), pady=(5, 0))
        self.combo_especialidad.bind("<<ComboboxSelected>>", lambda e: self._filtrar_medicos())
        
        ttk.Button(search_frame, text="↻ Todas", command=self._resetear_especialidad).grid(row=1, column=2, padx=(0, 0), pady=(5, 0))
        
        search_frame.columnconfigure(1, weight=1)
        
        # Tabla de médicos
        tabla_frame = ttk.LabelFrame(self, text="Médicos Registrados")
        tabla_frame.pack(fill="both", expand=True)
        
        # Label contador
        self.label_contador = ttk.Label(tabla_frame, text="", font=("Arial", 9))
        self.label_contador.pack(anchor="w", padx=10, pady=(5, 0))
        
        # Crear Treeview
        self.tree = ttk.Treeview(
            tabla_frame,
            columns=("matricula", "nombre", "apellido", "telefono", "email", "fecha_alta", "especialidades", "acciones"),
            show="headings",
            height=12
        )
        
        headers = [
            ("matricula", "Matrícula", 70),
            ("nombre", "Nombre", 100),
            ("apellido", "Apellido", 100),
            ("telefono", "Teléfono", 90),
            ("email", "Email", 140),
            ("fecha_alta", "Fecha Alta", 90),
            ("especialidades", "Especialidades", 180),
            ("acciones", "Acciones", 180)
        ]
        
        for col, text, width in headers:
            self.tree.heading(col, text=text)
            self.tree.column(col, width=width)
        
        scrollbar = ttk.Scrollbar(tabla_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=(5, 10))
        scrollbar.pack(side="right", fill="y", pady=(5, 10))
        
        # Bind para detectar clicks en la columna de acciones
        self.tree.bind("<Button-1>", self._on_tree_click)
        
        # Almacenar todos los médicos
        self.todos_medicos = []
        self.medicos_filtrados = []
        self.especialidades_disponibles = []
        
        self._cargar_especialidades()
        self._refresh()
    
    def _cargar_especialidades(self):
        """Carga las especialidades desde la BD"""
        db = Database()
        if not db.conectar("127.0.0.1:3306/hospital_db"):
            return
        
        try:
            query = "SELECT id_especialidad, nombre FROM Especialidad ORDER BY nombre"
            especialidades = db.obtener_registros(query)
            db.desconectar()
            
            if especialidades:
                self.especialidades_disponibles = especialidades
                nombres = ["Todas"] + [esp['nombre'] for esp in especialidades]
                self.combo_especialidad['values'] = nombres
        except Exception as e:
            print(f"[ERROR] Error al cargar especialidades: {str(e)}")
            db.desconectar()
    
    def _crear_medico(self):
        """Abre el diálogo para crear un nuevo médico"""
        dialog = CrearMedicoDialog(self.winfo_toplevel(), self.ctrl)
        self.winfo_toplevel().wait_window(dialog.window)
        self._refresh()
    
    def _limpiar_busqueda(self):
        """Limpia el campo de búsqueda"""
        self.entry_busqueda.delete(0, tk.END)
        self._filtrar_medicos()
    
    def _resetear_especialidad(self):
        """Resetea el filtro de especialidad a 'Todas'"""
        self.especialidad_var.set("Todas")
        self._filtrar_medicos()
    
    def _filtrar_medicos(self):
        """Filtra los médicos según el texto de búsqueda y especialidad"""
        texto_busqueda = self.entry_busqueda.get().lower().strip()
        especialidad_seleccionada = self.especialidad_var.get()
        
        self.medicos_filtrados = []
        
        for m in self.todos_medicos:
            # Filtro por texto (nombre, apellido o matrícula)
            nombre_completo = f"{m['nombre']} {m['apellido']}".lower()
            matricula_str = str(m['matricula'])
            
            coincide_texto = True
            if texto_busqueda:
                coincide_texto = (texto_busqueda in nombre_completo or texto_busqueda in matricula_str)
            
            # Filtro por especialidad
            coincide_especialidad = True
            if especialidad_seleccionada != "Todas":
                especialidades_medico = m.get('especialidades', '').split(', ')
                coincide_especialidad = especialidad_seleccionada in especialidades_medico
            
            # Agregar si cumple ambos filtros
            if coincide_texto and coincide_especialidad:
                self.medicos_filtrados.append(m)
        
        self._repoblar_tabla()
    
    def _repoblar_tabla(self):
        """Repuebla la tabla con los médicos filtrados"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for m in self.medicos_filtrados:
            especialidades_str = m.get('especialidades', 'Sin especialidad')
            
            self.tree.insert("", "end", values=(
                m["matricula"],
                m["nombre"],
                m["apellido"],
                m["telefono"],
                m["email"],
                m["fecha_alta"],
                especialidades_str,
                "✏️ Modificar | 🗑️ Dar de Baja"
            ))
        
        # Actualizar contador
        total = len(self.todos_medicos)
        mostrados = len(self.medicos_filtrados)
        
        if mostrados == total:
            self.label_contador.config(text=f"Mostrando {mostrados} médico(s)")
        else:
            self.label_contador.config(text=f"Mostrando {mostrados} de {total} médico(s)")
    
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
            for i, col in enumerate(["matricula", "nombre", "apellido", "telefono", "email", "fecha_alta", "especialidades", "acciones"]):
                col_width = self.tree.column(col, "width")
                if event.x < col_x + col_width:
                    col_num = i
                    break
                col_x += col_width
            
            # Si es la columna de acciones (columna 7)
            if col_num == 7:
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
        """Recarga la lista de médicos con sus especialidades"""
        db = Database()
        if not db.conectar("127.0.0.1:3306/hospital_db"):
            self.todos_medicos = []
            self.medicos_filtrados = []
            self._repoblar_tabla()
            return
        
        try:
            query = """
            SELECT m.matricula, m.nombre, m.apellido, m.telefono, m.email, m.fecha_ingreso,
                   GROUP_CONCAT(DISTINCT e.nombre SEPARATOR ', ') as especialidades
            FROM Medico m
            LEFT JOIN Medico_especialidad me ON m.matricula = me.matricula
            LEFT JOIN Especialidad e ON me.id_especialidad = e.id_especialidad
            WHERE m.activo = 1
            GROUP BY m.matricula, m.nombre, m.apellido, m.telefono, m.email, m.fecha_ingreso
            ORDER BY m.nombre, m.apellido
            """
            
            medicos = db.obtener_registros(query)
            db.desconectar()
            
            if medicos:
                self.todos_medicos = []
                for m in medicos:
                    self.todos_medicos.append({
                        "matricula": m["matricula"],
                        "nombre": m["nombre"],
                        "apellido": m["apellido"],
                        "telefono": m["telefono"],
                        "email": m["email"],
                        "fecha_alta": str(m["fecha_ingreso"]),
                        "especialidades": m["especialidades"] or "Sin especialidad"
                    })
            else:
                self.todos_medicos = []
            
            self.medicos_filtrados = self.todos_medicos
            self.entry_busqueda.delete(0, tk.END)
            self.especialidad_var.set("Todas")
            self._repoblar_tabla()
            
        except Exception as e:
            print(f"[ERROR] Error al listar médicos: {str(e)}")
            db.desconectar()
            self.todos_medicos = []
            self.medicos_filtrados = []
            self._repoblar_tabla()
