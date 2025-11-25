import tkinter as tk
from tkinter import ttk, messagebox

# imports RELATIVOS al paquete frontend
from ..controllers.pacientes_controller import PacientesController
from ..widgets.validated_entry import ValidatedEntry


class PacientesView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=12)
        self.ctrl = PacientesController()

        # --- Formulario alta ---
        form = ttk.LabelFrame(self, text="Nuevo paciente")
        form.pack(fill="x", pady=10)

        ttk.Label(form, text="ID:").grid(row=0, column=0, sticky="w")
        self.ent_id = ValidatedEntry(form, only_int=True, width=10)
        self.ent_id.grid(row=0, column=1)

        ttk.Label(form, text="Nombre:").grid(row=0, column=2, sticky="w", padx=(10,0))
        self.ent_nom = ValidatedEntry(form, width=18)
        self.ent_nom.grid(row=0, column=3)

        ttk.Label(form, text="Apellido:").grid(row=0, column=4, sticky="w", padx=(10,0))
        self.ent_ape = ValidatedEntry(form, width=18)
        self.ent_ape.grid(row=0, column=5)

        ttk.Label(form, text="Tel:").grid(row=1, column=0, sticky="w", pady=(8,0))
        self.ent_tel = ValidatedEntry(form, width=14)
        self.ent_tel.grid(row=1, column=1, pady=(8,0))

        ttk.Label(form, text="Nac (YYYY-MM-DD):").grid(row=1, column=2, sticky="w", pady=(8,0))
        self.ent_nac = ValidatedEntry(form, width=14)
        self.ent_nac.grid(row=1, column=3, pady=(8,0))

        ttk.Label(form, text="Dirección:").grid(row=1, column=4, sticky="w", pady=(8,0))
        self.ent_dir = ValidatedEntry(form, width=22)
        self.ent_dir.grid(row=1, column=5, pady=(8,0))

        ttk.Button(form, text="Crear", command=self._crear).grid(row=1, column=6, padx=(12,0))

        # --- Tabla ---
        self.tree = ttk.Treeview(
            self,
            columns=("id","nombre","apellido","telefono","direccion","nacimiento"),
            show="headings",
            height=14
        )
        for c, txt, w in [
            ("id","ID",80),
            ("nombre","Nombre",160),
            ("apellido","Apellido",160),
            ("telefono","Teléfono",120),
            ("direccion","Dirección",220),
            ("nacimiento","Nacimiento",120)
        ]:
            self.tree.heading(c, text=txt)
            self.tree.column(c, width=w)
        self.tree.pack(fill="both", expand=True, pady=10)

        ttk.Button(self, text="Refrescar", command=self._refresh).pack(anchor="e")
        self._refresh()

    def _crear(self):
        ok, msg = self.ctrl.crear(
            self.ent_id.get(),
            self.ent_nom.get(),
            self.ent_ape.get(),
            self.ent_tel.get(),
            self.ent_nac.get(),
            self.ent_dir.get()
        )
        if not ok:
            messagebox.showerror("Error", msg)
        self._refresh()

    def _refresh(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for p in self.ctrl.listar():
            self.tree.insert(
                "",
                "end",
                values=(p["id"], p["nombre"], p["apellido"], p["telefono"], p["direccion"], p["nacimiento"])
            )
