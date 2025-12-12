#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de prueba para verificar que el scroll funciona en el formulario de preinscripción
Prueba: Abre el formulario y verifica que el scroll con rueda del mouse funciona
"""

import tkinter as tk
from tkinter import messagebox
import sys
from pathlib import Path

# Agregar la ruta del proyecto al path
sys.path.insert(0, str(Path(__file__).parent))

def test_form_scroll():
    """Abre el formulario y proporciona instrucciones de prueba"""
    root = tk.Tk()
    root.title("Prueba de Scroll - Formulario de Preinscripción")
    root.geometry("900x600")
    
    # Frame de instrucciones
    instructions_frame = tk.Frame(root, bg="#f0f0f0", pady=20)
    instructions_frame.pack(fill="x")
    
    tk.Label(
        instructions_frame,
        text="📋 PRUEBA DE SCROLL - FORMULARIO DE PREINSCRIPCIÓN",
        font=("Arial", 14, "bold"),
        bg="#f0f0f0"
    ).pack()
    
    tk.Label(
        instructions_frame,
        text="Instrucciones:",
        font=("Arial", 12, "bold"),
        bg="#f0f0f0"
    ).pack(pady=(10, 5))
    
    instructions = """
    1. Pasa el mouse sobre el formulario (las áreas de entrada)
    2. Usa la rueda del mouse para desplazarte ARRIBA y ABAJO
    3. Verifica que el contenido se desplace suavemente
    4. El scroll NO debe funcionar cuando el mouse está fuera del formulario
    5. El scroll SÍ debe funcionar en los campos de texto y dropdowns
    
    ✓ Scroll funciona: El formulario se desplaza
    ✗ Scroll no funciona: Nada sucede
    """
    
    tk.Label(
        instructions_frame,
        text=instructions,
        font=("Courier", 10),
        bg="#f0f0f0",
        justify="left"
    ).pack(padx=20)
    
    # Frame para cargar el formulario
    form_container = tk.Frame(root)
    form_container.pack(fill="both", expand=True, padx=10, pady=10)
    
    try:
        # Importar y crear el formulario
        from app.ui.components.form import create_unified_form
        
        # Simulación de nav_commands
        nav_commands = {
            'home': lambda: root.quit(),
            'dashboard': lambda: None
        }
        
        # Crear el formulario
        form = create_unified_form(form_container, nav_commands)
        
        # Mostrar mensaje de éxito
        messagebox.showinfo(
            "Prueba Lista",
            "Formulario cargado exitosamente.\n\n"
            "Ahora prueba el scroll con la rueda del mouse.\n"
            "Recuerda pasar el mouse sobre el formulario primero."
        )
        
    except Exception as e:
        messagebox.showerror(
            "Error",
            f"No se pudo cargar el formulario:\n\n{type(e).__name__}: {e}"
        )
        import traceback
        traceback.print_exc()
    
    root.mainloop()

if __name__ == "__main__":
    print("[INFO] Iniciando prueba de scroll...")
    test_form_scroll()
    print("[INFO] Prueba finalizada")
