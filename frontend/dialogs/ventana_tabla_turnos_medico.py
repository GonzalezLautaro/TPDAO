import tkinter as tk
from tkinter import ttk


class VentanaTablaTurnosMedico(tk.Toplevel):
    def __init__(self, parent, datos, fecha_inicio, fecha_fin):
        super().__init__(parent)
        self.title("Listado de turnos por médico")
        self.geometry("1200x600")

        # Título
        titulo = ttk.Label(
            self,
            text=f"Listado de turnos por médico — {fecha_inicio} a {fecha_fin}",
            font=("Arial", 15, "bold")
        )
        titulo.pack(pady=15)

        # Frame para la tabla
        frame = ttk.Frame(self)
        frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        # Definir columnas
        cols = ("medico", "especialidad", "fecha", "horario", "paciente", "estado")
        tree = ttk.Treeview(frame, columns=cols, show="headings", height=20)

        # Configurar encabezados y anchos
        headers = [
            ("medico", "Médico", 200),
            ("especialidad", "Especialidad", 180),
            ("fecha", "Fecha", 100),
            ("horario", "Horario", 130),
            ("paciente", "Paciente", 200),
            ("estado", "Estado", 120)
        ]

        for col, text, width in headers:
            tree.heading(col, text=text)
            tree.column(col, width=width, anchor="center" if col != "medico" else "w")

        # Scrollbar
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Cargar datos y calcular totales
        total_turnos = 0
        totales_por_estado = {
            'Programado': 0,
            'Atendido': 0,
            'Cancelado': 0,
            'Inasistencia': 0
        }

        for fila in datos:
            horario = f"{str(fila['hora_inicio'])[:5]} - {str(fila['hora_fin'])[:5]}"
            
            tree.insert("", "end", values=(
                fila["medico"],
                fila["especialidad"],
                fila["fecha"],
                horario,
                fila["paciente"],
                fila["estado"]
            ))
            
            total_turnos += 1
            estado = fila["estado"]
            if estado in totales_por_estado:
                totales_por_estado[estado] += 1

        # Frame de totales
        footer = ttk.Frame(self)
        footer.pack(fill="x", padx=10, pady=(0, 10))

        # Texto de totales
        texto_totales = (
            f"Total de turnos: {total_turnos}  |  "
            f"Atendidos: {totales_por_estado['Atendido']}  |  "
            f"Programados: {totales_por_estado['Programado']}  |  "
            f"Cancelados: {totales_por_estado['Cancelado']}  |  "
            f"Inasistencias: {totales_por_estado['Inasistencia']}"
        )

        ttk.Label(
            footer,
            text=texto_totales,
            font=("Arial", 10, "bold")
        ).pack(side="left")

        # Botón cerrar
        ttk.Button(footer, text="Cerrar", command=self.destroy).pack(side="right")