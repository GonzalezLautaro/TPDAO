from tkinter import ttk

def setup_theme():
    style = ttk.Style()
    try:
        style.theme_use("clam")
    except:
        pass

    style.configure("TButton", padding=6)
    style.configure("TLabel", padding=4)
    style.configure("Treeview", rowheight=26)
