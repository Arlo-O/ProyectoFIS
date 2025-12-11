#!/usr/bin/env python3
"""
Punto de entrada principal para la aplicación.
Ejecuta la GUI del sistema de gestión académica.
"""

import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Importar y ejecutar la aplicación
from app.vista.app_gui import initialize_app
import tkinter as tk

if __name__ == "__main__":
    root_window = tk.Tk()
    initialize_app(root_window)
    root_window.mainloop()
