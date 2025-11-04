import tkinter as tk
from tkinter import messagebox

def show_confirmation_dialog(parent, title="Confirmación", message="Operación completada con éxito", on_confirm=None):
    """
    Muestra un diálogo de confirmación personalizado.
    
    Args:
        parent: Ventana padre del diálogo
        title: Título del diálogo
        message: Mensaje a mostrar
        on_confirm: Función a ejecutar al confirmar
    """
    dialog = tk.Toplevel(parent)
    dialog.title(title)
    dialog.transient(parent)
    dialog.grab_set()
    
    # Centrar el diálogo
    dialog.geometry("400x200")
    window_width = dialog.winfo_reqwidth()
    window_height = dialog.winfo_reqheight()
    position_right = int(parent.winfo_screenwidth()/2 - window_width/2)
    position_down = int(parent.winfo_screenheight()/2 - window_height/2)
    dialog.geometry(f"+{position_right}+{position_down}")
    
    # Contenido
    tk.Label(dialog, text=message, wraplength=350, pady=20).pack(expand=True)
    
    def on_accept():
        dialog.destroy()
        if on_confirm:
            on_confirm()
    
    tk.Button(dialog, text="Aceptar", command=on_accept, width=15).pack(pady=20)
    
    # Hacer el diálogo modal
    dialog.focus_set()
    dialog.wait_window()