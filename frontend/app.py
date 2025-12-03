"""Punto de entrada de la aplicación Tkinter"""

from .main_window import run_app
from typing import List, Dict
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


def obtener_turnos_por_especialidad(self, fecha_desde: str, fecha_hasta: str) -> List[Dict]:
    """Obtiene cantidad de turnos por especialidad en rango de fechas"""
    if not self.__db.conectar("127.0.0.1:3306/hospital_db"):
        return []
    
    try:
        query = """
        SELECT e.nombre AS especialidad, COUNT(t.id_turno) AS cantidad
        FROM Turno t
        JOIN Medico m ON t.matricula = m.matricula
        JOIN Especialidad e ON m.id_especialidad = e.id_especialidad
        WHERE t.fecha BETWEEN %s AND %s
        AND t.estado = 'Atendido'
        GROUP BY e.nombre
        ORDER BY cantidad DESC
        """
        
        resultados = self.__db.obtener_registros(query, (fecha_desde, fecha_hasta))
        return resultados if resultados else []
    
    except Exception as e:
        print(f"[ERROR] obtener_turnos_por_especialidad: {e}")
        return []
    finally:
        self.__db.desconectar()


def mostrar_reporte_pacientes_rango(self):
    """Muestra ventana mejorada de pacientes atendidos por rango de fechas"""
    ventana = tk.Toplevel(self.frame)
    ventana.title("📅 Pacientes Atendidos por Rango de Fechas")
    ventana.geometry("900x700")
    ventana.resizable(True, True)
    
    # ═══════════════════════════════════════════════════════════════
    # FRAME PRINCIPAL CON PADDING
    # ═══════════════════════════════════════════════════════════════
    main_frame = ttk.Frame(ventana, padding=20)
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    # ═══════════════════════════════════════════════════════════════
    # TÍTULO
    # ═══════════════════════════════════════════════════════════════
    titulo = ttk.Label(
        main_frame,
        text="📊 Reporte de Pacientes Atendidos",
        font=("Arial", 16, "bold")
    )
    titulo.pack(pady=(0, 20))
    
    # ═══════════════════════════════════════════════════════════════
    # FILTROS DE FECHA
    # ═══════════════════════════════════════════════════════════════
    filtros_frame = ttk.LabelFrame(main_frame, text="🔍 Seleccionar Rango de Fechas", padding=15)
    filtros_frame.pack(fill=tk.X, pady=(0, 15))
    
    # Contenedor horizontal para fechas
    fechas_container = ttk.Frame(filtros_frame)
    fechas_container.pack()
    
    # Fecha desde
    ttk.Label(fechas_container, text="Desde:", font=("Arial", 10)).grid(row=0, column=0, padx=(0, 5), sticky="e")
    fecha_desde = ttk.Entry(fechas_container, width=15, font=("Arial", 10))
    fecha_desde.grid(row=0, column=1, padx=(0, 20))
    fecha_desde.insert(0, "AAAA-MM-DD")
    
    # Fecha hasta
    ttk.Label(fechas_container, text="Hasta:", font=("Arial", 10)).grid(row=0, column=2, padx=(0, 5), sticky="e")
    fecha_hasta = ttk.Entry(fechas_container, width=15, font=("Arial", 10))
    fecha_hasta.grid(row=0, column=3, padx=(0, 20))
    fecha_hasta.insert(0, "AAAA-MM-DD")
    
    # Botón buscar
    btn_buscar = ttk.Button(
        fechas_container,
        text="🔎 Buscar",
        command=lambda: self._ejecutar_busqueda_mejorada(
            fecha_desde.get(),
            fecha_hasta.get(),
            tree_pacientes,
            tree_especialidades,
            lbl_total_pacientes,
            lbl_total_turnos
        )
    )
    btn_buscar.grid(row=0, column=4, padx=10)
    
    # ═══════════════════════════════════════════════════════════════
    # SECCIÓN 1: LISTA DE PACIENTES
    # ═══════════════════════════════════════════════════════════════
    pacientes_frame = ttk.LabelFrame(main_frame, text="👥 Pacientes Atendidos", padding=10)
    pacientes_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
    
    # Tabla de pacientes
    tree_frame_pac = ttk.Frame(pacientes_frame)
    tree_frame_pac.pack(fill=tk.BOTH, expand=True)
    
    tree_pacientes = ttk.Treeview(
        tree_frame_pac,
        columns=("paciente", "fecha", "medico", "especialidad"),
        height=10,
        show="headings"
    )
    
    tree_pacientes.heading("paciente", text="Paciente")
    tree_pacientes.heading("fecha", text="Fecha")
    tree_pacientes.heading("medico", text="Médico")
    tree_pacientes.heading("especialidad", text="Especialidad")
    
    tree_pacientes.column("paciente", width=200)
    tree_pacientes.column("fecha", width=100, anchor=tk.CENTER)
    tree_pacientes.column("medico", width=200)
    tree_pacientes.column("especialidad", width=150)
    
    scrollbar_pac = ttk.Scrollbar(tree_frame_pac, orient="vertical", command=tree_pacientes.yview)
    tree_pacientes.configure(yscroll=scrollbar_pac.set)
    
    tree_pacientes.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar_pac.pack(side=tk.RIGHT, fill=tk.Y)
    
    # Label resumen de pacientes
    lbl_total_pacientes = ttk.Label(pacientes_frame, text="Total: 0 pacientes", font=("Arial", 10, "bold"))
    lbl_total_pacientes.pack(pady=(5, 0))
    
    # ═══════════════════════════════════════════════════════════════
    # SECCIÓN 2: TURNOS POR ESPECIALIDAD
    # ═══════════════════════════════════════════════════════════════
    especialidades_frame = ttk.LabelFrame(main_frame, text="📊 Turnos por Especialidad", padding=10)
    especialidades_frame.pack(fill=tk.BOTH, expand=True)
    
    # Tabla de especialidades
    tree_frame_esp = ttk.Frame(especialidades_frame)
    tree_frame_esp.pack(fill=tk.BOTH, expand=True)
    
    tree_especialidades = ttk.Treeview(
        tree_frame_esp,
        columns=("especialidad", "cantidad"),
        height=6,
        show="headings"
    )
    
    tree_especialidades.heading("especialidad", text="Especialidad")
    tree_especialidades.heading("cantidad", text="Cantidad de Turnos")
    
    tree_especialidades.column("especialidad", width=400)
    tree_especialidades.column("cantidad", width=150, anchor=tk.CENTER)
    
    scrollbar_esp = ttk.Scrollbar(tree_frame_esp, orient="vertical", command=tree_especialidades.yview)
    tree_especialidades.configure(yscroll=scrollbar_esp.set)
    
    tree_especialidades.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar_esp.pack(side=tk.RIGHT, fill=tk.Y)
    
    # Label resumen de turnos
    lbl_total_turnos = ttk.Label(especialidades_frame, text="Total: 0 turnos", font=("Arial", 10, "bold"))
    lbl_total_turnos.pack(pady=(5, 0))
    
    # ═══════════════════════════════════════════════════════════════
    # BOTÓN CERRAR
    # ═══════════════════════════════════════════════════════════════
    ttk.Button(
        main_frame,
        text="❌ Cerrar",
        command=ventana.destroy
    ).pack(pady=(10, 0))
    
    def _ejecutar_busqueda_mejorada(self, fecha_desde, fecha_hasta, tree_pacientes, tree_especialidades, lbl_pacientes, lbl_turnos):
        """Ejecuta la búsqueda y actualiza ambas tablas"""
        # Validar fechas
        if fecha_desde == "AAAA-MM-DD" or fecha_hasta == "AAAA-MM-DD":
            messagebox.showwarning("Advertencia", "Por favor ingrese las fechas en formato AAAA-MM-DD")
            return
        
        try:
            # ═══════════════════════════════════════════════════════════
            # BUSCAR PACIENTES
            # ═══════════════════════════════════════════════════════════
            pacientes = self.controller.obtener_pacientes_rango(fecha_desde, fecha_hasta)
            
            # Limpiar tabla
            for item in tree_pacientes.get_children():
                tree_pacientes.delete(item)
            
            # Llenar tabla
            if pacientes:
                for p in pacientes:
                    tree_pacientes.insert("", "end", values=(
                        p.get('nombre_paciente', 'N/A'),
                        p.get('fecha', 'N/A'),
                        p.get('nombre_medico', 'N/A'),
                        p.get('especialidad', 'N/A')
                    ))
            
            lbl_pacientes.config(text=f"Total: {len(pacientes) if pacientes else 0} pacientes")
            
            # ═══════════════════════════════════════════════════════════
            # BUSCAR TURNOS POR ESPECIALIDAD
            # ═══════════════════════════════════════════════════════════
            especialidades = self.controller.obtener_turnos_por_especialidad(fecha_desde, fecha_hasta)
            
            # Limpiar tabla
            for item in tree_especialidades.get_children():
                tree_especialidades.delete(item)
            
            # Llenar tabla
            total_turnos = 0
            if especialidades:
                for esp in especialidades:
                    cantidad = esp.get('cantidad', 0)
                    total_turnos += cantidad
                    tree_especialidades.insert("", "end", values=(
                        esp.get('especialidad', 'N/A'),
                        cantidad
                    ))
            
            lbl_turnos.config(text=f"Total: {total_turnos} turnos")
            
            # Mensaje de éxito
            messagebox.showinfo(
                "✓ Búsqueda Completada",
                f"Se encontraron:\n\n"
                f"  • {len(pacientes) if pacientes else 0} pacientes atendidos\n"
                f"  • {total_turnos} turnos totales\n"
                f"  • {len(especialidades) if especialidades else 0} especialidades"
            )
        
        except Exception as e:
            messagebox.showerror("Error", f"Error al buscar:\n{str(e)}")
            import traceback
            traceback.print_exc()
