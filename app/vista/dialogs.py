"""
Archivo: dialogs.py
Diálogos personalizados y modales para la interfaz gráfica.

Este módulo proporciona funciones para crear ventanas emergentes (diálogos)
personalizadas que se pueden usar en toda la aplicación para mostrar mensajes,
confirmaciones o solicitar información al usuario.

Ventajas de estos diálogos personalizados vs messagebox estándar:
- Mayor control sobre el diseño visual
- Posibilidad de agregar callbacks personalizados
- Consistencia con el tema de la aplicación
"""

import tkinter as tk
from tkinter import messagebox

def show_confirmation_dialog(parent, title="Confirmación", message="Operación completada con éxito", on_confirm=None):
    """
    Muestra un diálogo modal personalizado para mostrar mensajes al usuario.
    
    El diálogo es modal (bloquea la interacción con otras ventanas hasta que se cierre)
    y está centrado en la pantalla. Es útil para confirmar operaciones exitosas o
    solicitar confirmación del usuario antes de realizar una acción importante.
    
    Parámetros:
        parent (tk.Tk|tk.Toplevel): Ventana padre del diálogo
        title (str): Título que aparecerá en la barra superior del diálogo
        message (str): Mensaje principal a mostrar al usuario
        on_confirm (function|None): Función opcional a ejecutar después de que
                                    el usuario confirme (presiona "Aceptar")
    
    Ejemplo de uso:
        show_confirmation_dialog(
            root,
            title="Éxito",
            message="El estudiante ha sido agregado correctamente",
            on_confirm=lambda: print("Usuario confirmó")
        )
    """
    # Crear ventana emergente (Toplevel = ventana secundaria)
    dialog = tk.Toplevel(parent)
    dialog.title(title)
    dialog.transient(parent)  # Mantener el diálogo sobre la ventana padre
    dialog.grab_set()  # Hacer el diálogo modal (bloquear interacción con otras ventanas)
    
    # ------------------------------------------------------------------
    # CONFIGURAR TAMAÑO Y POSICIÓN
    # ------------------------------------------------------------------
    # Tamaño fijo del diálogo
    dialog.geometry("400x200")
    
    # Calcular posición para centrar en la pantalla
    window_width = dialog.winfo_reqwidth()
    window_height = dialog.winfo_reqheight()
    position_right = int(parent.winfo_screenwidth()/2 - window_width/2)
    position_down = int(parent.winfo_screenheight()/2 - window_height/2)
    dialog.geometry(f"+{position_right}+{position_down}")
    
    # ------------------------------------------------------------------
    # CONTENIDO DEL DIÁLOGO
    # ------------------------------------------------------------------
    # Label con el mensaje, wraplength permite que el texto se ajuste al ancho
    tk.Label(
        dialog,
        text=message,
        wraplength=350,  # Ancho máximo antes de hacer salto de línea
        pady=20          # Padding vertical
    ).pack(expand=True)
    
    def on_accept():
        """Maneja el evento de confirmación (botón Aceptar)."""
        dialog.destroy()  # Cerrar el diálogo
        if on_confirm:    # Si hay callback definido, ejecutarlo
            on_confirm()
    
    # Botón de confirmación
    tk.Button(
        dialog,
        text="Aceptar",
        command=on_accept,
        width=15
    ).pack(pady=20)
    
    # ------------------------------------------------------------------
    # HACER EL DIÁLOGO MODAL
    # ------------------------------------------------------------------
    dialog.focus_set()     # Dar foco al diálogo
    dialog.wait_window()   # Bloquear ejecución hasta que se cierre el diálogo