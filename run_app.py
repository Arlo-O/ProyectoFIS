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
from dotenv import load_dotenv
load_dotenv()

# Inicializar mapeos del ORM (necesario antes de importar módulos que usen el ORM)
try:
    from app.data.mappers import start_mappers
    start_mappers()
except Exception as e:
    print(f"Warning: no se pudieron inicializar los mapeos: {e}")

from app.ui.main import initialize_app
import tkinter as tk

if __name__ == "__main__":
    root_window = tk.Tk()
    try:
        initialize_app(root_window)
        root_window.mainloop()
    except Exception as e:
        import traceback
        print("Error al inicializar la aplicación GUI:")
        traceback.print_exc()
