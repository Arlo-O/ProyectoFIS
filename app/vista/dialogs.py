import tkinter as tk
from typing import Optional, Callable


def show_confirmation_dialog(
    parent: tk.Tk | tk.Toplevel,
    title: str = "Confirmación",
    message: str = "Operación completada con éxito",
    on_confirm: Optional[Callable[[], None]] = None
) -> None:
    """Muestra un diálogo de confirmación centrado."""
    
    d = tk.Toplevel(parent)
    d.title(title)
    d.transient(parent)
    d.grab_set()
    d.resizable(False, False)
    
    # Centrar ventana
    d.geometry("400x200")
    d.update_idletasks()
    w = d.winfo_width()
    h = d.winfo_height()
    x = (d.winfo_screenwidth() // 2) - (w // 2)
    y = (d.winfo_screenheight() // 2) - (h // 2)
    d.geometry(f"{w}x{h}+{x}+{y}")
    
    # Contenido
    tk.Label(
        d, 
        text=message, 
        wraplength=350, 
        pady=30,
        font=("Helvetica", 11)
    ).pack(expand=True)
    
    def cerrar():
        d.destroy()
        if on_confirm:
            on_confirm()
    
    tk.Button(
        d,
        text="Aceptar",
        command=cerrar,
        width=12,
        font=("Helvetica", 10, "bold"),
        bg="#4a90e2",
        fg="white",
        relief="flat",
        padx=20,
        pady=8
    ).pack(pady=20)
    
    d.wait_window()


def show_error_dialog(
    parent: tk.Tk | tk.Toplevel,
    title: str = "Error",
    message: str = "Ocurrió un error inesperado"
) -> None:
    """Muestra un diálogo de error."""
    show_confirmation_dialog(parent, title, message, bg="#dc3545", fg="white")


def show_success_dialog(
    parent: tk.Tk | tk.Toplevel,
    title: str = "Éxito",
    message: str = "Operación completada correctamente"
) -> None:
    """Muestra un diálogo de éxito."""
    show_confirmation_dialog(parent, title, message)
