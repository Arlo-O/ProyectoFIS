# Archivo: gui_styles.py

import tkinter.ttk as ttk
from config import (COLOR_BTN_LOGIN, COLOR_BTN_LOGIN_HOVER, COLOR_TEXT_LOGIN, 
                    COLOR_BTN_PRE, COLOR_BTN_PRE_HOVER, COLOR_TEXT_PRE, 
                    FONT_P_BOLD, COLOR_TEXT_LIGHT)

def configure_styles(root):
    """Configura y aplica los estilos TTK necesarios para la interfaz."""
    # Necesita el root para obtener el objeto Style
    style = ttk.Style(root) 
    
    # Asegura que el tema base sea compatible con colores (clam o alt)
    style.theme_use('clam') 

    # --- 1. Estilo para el Botón de Login (Azul) ---
    style.configure("Login.TButton",
                    background=COLOR_BTN_LOGIN,  # Color de fondo (normal)
                    foreground=COLOR_TEXT_LOGIN, # Color del texto
                    font=FONT_P_BOLD,
                    borderwidth=0,               # Quitar el borde 3D estándar
                    relief="flat",
                    padding=[15, 12])            # Padding [horizontal, vertical]

    # Mapeo para el efecto hover/activo
    style.map("Login.TButton",
              background=[('active', COLOR_BTN_LOGIN_HOVER)], # Color al presionar/hover
              foreground=[('active', COLOR_TEXT_LOGIN)])


    # --- 2. Estilo para el Botón de Preinscripción (Naranja) ---
    style.configure("Pre.TButton",
                    background=COLOR_BTN_PRE,
                    foreground=COLOR_TEXT_PRE,
                    font=FONT_P_BOLD,
                    borderwidth=0,
                    relief="flat",
                    padding=[15, 12])

    # Mapeo para el efecto hover/activo
    style.map("Pre.TButton",
              background=[('active', COLOR_BTN_PRE_HOVER)],
              foreground=[('active', COLOR_TEXT_PRE)])
    
    # --- 3. Estilos Generales de Dashboard (manteniendo los anteriores para módulos) ---
    # Estos estilos son necesarios para los módulos Admin/Directivo
    style.configure("AdminBlue.TButton", background="#007bff", foreground=COLOR_TEXT_LIGHT, font=FONT_P_BOLD)
    style.map("AdminBlue.TButton", background=[('active', '#0056b3')])
    
    style.configure("AdminGreen.TButton", background="#28a745", foreground=COLOR_TEXT_LIGHT, font=FONT_P_BOLD)
    style.map("AdminGreen.TButton", background=[('active', '#1e7e34')])