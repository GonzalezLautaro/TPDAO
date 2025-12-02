import tkinter as tk
from tkinter import ttk

class ValidatedEntry(ttk.Entry):
    def __init__(self, parent, only_int=False, **kwargs):
        super().__init__(parent, **kwargs)
        self.only_int = only_int
        vcmd = (self.register(self._validate), "%P")
        self.config(validate="key", validatecommand=vcmd)

    def _validate(self, value):
        if self.only_int and value:
            return value.isdigit()
        return True
