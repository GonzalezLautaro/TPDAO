import tkinter as tk
from tkinter import ttk, messagebox
from ..controllers.turno_controller import TurnoController
from ..widgets.validated_entry import ValidatedEntry


class TurnosView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=12)
        self.ctrl = TurnoController()

        form = ttk.LabelFrame(self, text="Nuevo turno")
        form.pack(fill="x", pady=10)

        ttk.Label(form, text="ID Paciente:").grid(row=0, column=0, sticky="w")
        self.ent_dni = ValidatedEntry(form, only_int=True, width=15)
        self.ent_dni.grid(row=0, column=1)

        ttk.Label(form, text="Matrícula médico:").grid(row=0, column=2, sticky="w", padx=(20,0))
        self.ent_mat = ValidatedEntry(form, only_int=True, width=15)
        self.ent_mat.grid(row=0, column=3)

        ttk.Label(form, text="Fecha (YYYY-MM-DD HH:MM):").grid(row=1, column=0, sticky="w", pady=(8,0))
        self.ent_fecha = ValidatedEntry(form, width=22)
        self.ent_fecha.grid(row=1, column=1, pady=(8,0))
        ttk.Button(form, text="Programar", command=self._programar).grid(row=1, column=3, padx=(12,0))

        self.tree = ttk.Treeview(self, columns=("dni","mat","fecha","estado"), show="headings")
        for col, txt, w in [("dni","ID Paciente",120),("mat","Matrícula",120),("fecha","Fecha",240),("estado","Estado",120)]:
            self.tree.heading(col, text=txt); self.tree.column(col, width=w)
        self.tree.pack(fill="both", expand=True, pady=10)

        btns = ttk.Frame(self); btns.pack(fill="x")
        ttk.Button(btns, text="Atender", command=lambda: self._cambiar("atendido")).pack(side="left")
        ttk.Button(btns, text="Cancelar", command=lambda: self._cambiar("cancelado")).pack(side="left", padx=10)
        ttk.Button(btns, text="No asistió", command=lambda: self._cambiar("inasistencia")).pack(side="left")
        ttk.Button(btns, text="Refrescar", command=self._refresh).pack(side="right")

        self._refresh()

    def _programar(self):
        ok, msg = self.ctrl.programar(self.ent_dni.get(), self.ent_mat.get(), self.ent_fecha.get())
        if not ok: messagebox.showerror("Error", msg)
        self._refresh()

    def _cambiar(self, estado):
        sel = self.tree.selection()
        if not sel: return
        vals = self.tree.item(sel[0])["values"]
        ok, msg = self.ctrl.cambiar_estado(vals[0], vals[1], vals[2], estado)
        if not ok: messagebox.showerror("Error", msg)
        self._refresh()

    def _refresh(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        for t in self.ctrl.listar():
            self.tree.insert("", "end", values=(t["dni"], t["mat"], t["fecha"], t["estado"]))
