#!/usr/bin/env python3
"""
Punto de entrada simple para ejecutar la aplicación directamente.
"""

import sys
import os

# Configurar el path para imports
current_dir = os.path.dirname(os.path.abspath(__file__))
app_dir = os.path.join(current_dir, 'app')
vista_dir = os.path.join(app_dir, 'vista')

sys.path.insert(0, current_dir)
sys.path.insert(0, app_dir)
sys.path.insert(0, vista_dir)

# Importar y ejecutar
import tkinter as tk
from app_gui import initialize_app

if __name__ == "__main__":
    root = tk.Tk()
    initialize_app(root)
    root.mainloop()
