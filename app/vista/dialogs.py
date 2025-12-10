import tkinter as tk

def show_confirmation_dialog(parent, title="Confirmación", message="Operación completada con éxito", on_confirm=None):
    d = tk.Toplevel(parent)
    d.title(title)
    d.transient(parent)
    d.grab_set()
    
    d.geometry("400x200")
    w = d.winfo_reqwidth()
    h = d.winfo_reqheight()
    x = (d.winfo_screenwidth() // 2) - (w // 2)
    y = (d.winfo_screenheight() // 2) - (h // 2)
    d.geometry(f"+{x}+{y}")
    
    tk.Label(d, text=message, wraplength=350, pady=20).pack(expand=True)
    
    def cerrar():
        d.destroy()
        if on_confirm:
            on_confirm()
    
    tk.Button(
        d,
        text="Aceptar",
        command=cerrar,
        width=15
    ).pack(pady=20)
   
    dialog.wait_window()