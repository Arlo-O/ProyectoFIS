"""
Configuración de estilos personalizados TTK para la interfaz gráfica.
"""

import tkinter.ttk as ttk
from .config import (
    COLOR_BTN_LOGIN, COLOR_BTN_LOGIN_HOVER, COLOR_TEXT_LOGIN,
    COLOR_BTN_PRE, COLOR_BTN_PRE_HOVER, COLOR_TEXT_PRE,
    FONT_P_BOLD, COLOR_TEXT_LIGHT
)


def configure_styles(root):
    """Configura todos los estilos TTK personalizados."""
    style = ttk.Style(root)
    style.theme_use('clam')  # Mejor soporte para colores personalizados
    
    # Login.TButton - Botón azul principal
    style.configure(
        "Login.TButton",
        background=COLOR_BTN_LOGIN,
        foreground=COLOR_TEXT_LOGIN,
        font=FONT_P_BOLD,
        borderwidth=0,
        relief="flat",
        padding=[15, 12]
    )
    style.map(
        "Login.TButton",
        background=[('active', COLOR_BTN_LOGIN_HOVER)],
        foreground=[('active', COLOR_TEXT_LOGIN)]
    )
    
    # Pre.TButton - Botón naranja para preinscripción
    style.configure(
        "Pre.TButton",
        background=COLOR_BTN_PRE,
        foreground=COLOR_TEXT_PRE,
        font=FONT_P_BOLD,
        borderwidth=0,
        relief="flat",
        padding=[15, 12]
    )
    style.map(
        "Pre.TButton",
        background=[('active', COLOR_BTN_PRE_HOVER)],
        foreground=[('active', COLOR_TEXT_PRE)]
    )
    
    # AdminBlue.TButton - Botones azules de dashboard
    style.configure(
        "AdminBlue.TButton",
        background="#007bff",
        foreground=COLOR_TEXT_LIGHT,
        font=FONT_P_BOLD,
        borderwidth=0,
        relief="flat",
        padding=[12, 10]
    )
    style.map(
        "AdminBlue.TButton",
        background=[('active', '#0056b3')]
    )
    
    # AdminGreen.TButton - Botones verdes secundarios
    style.configure(
        "AdminGreen.TButton",
        background="#28a745",
        foreground=COLOR_TEXT_LIGHT,
        font=FONT_P_BOLD,
        borderwidth=0,
        relief="flat",
        padding=[12, 10]
    )
    style.map(
        "AdminGreen.TButton",
        background=[('active', '#1e7e34')]
    )
    
    print("[OK] Estilos TTK configurados correctamente")
