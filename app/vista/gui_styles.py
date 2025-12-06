"""
Archivo: gui_styles.py
Configuración de estilos personalizados usando TTK (Themed Tkinter).

Este módulo define y aplica estilos visuales para los widgets TTK de la aplicación,
principalmente botones con colores y efectos hover personalizados.

Los estilos TTK permiten:
- Botones con colores de fondo personalizados
- Efectos hover (cambio de color al pasar el mouse)
- Consistencia visual en toda la aplicación
- Separación de diseño y lógica

Estilos definidos:
- Login.TButton: Botón azul para login
- Pre.TButton: Botón naranja para preinscripción  
- AdminBlue.TButton: Botones para módulos de admin
- AdminGreen.TButton: Botones secundarios de admin
"""

import tkinter.ttk as ttk
from config import (
    COLOR_BTN_LOGIN, COLOR_BTN_LOGIN_HOVER, COLOR_TEXT_LOGIN,
    COLOR_BTN_PRE, COLOR_BTN_PRE_HOVER, COLOR_TEXT_PRE,
    FONT_P_BOLD, COLOR_TEXT_LIGHT
)

# ======================================================================
# CONFIGURACIÓN PRINCIPAL DE ESTILOS
# ======================================================================

def configure_styles(root):
    """
    Configura y registra todos los estilos TTK necesarios para la interfaz.
    
    Esta función debe llamarse UNA VEZ durante la inicialización de la aplicación,
    antes de crear cualquier widget que use estos estilos.
    
    Parámetros:
        root (tk.Tk): La ventana principal de Tkinter (necesaria para crear Style)
    
    Proceso:
    1. Crea el objeto Style de TTK
    2. Establece el tema base ('clam' para mejor soporte de colores)
    3. Configura cada estilo personalizado con sus colores y fuentes
    4. Define mapeos de estados (normal, hover, pressed)
    """
    # Crear objeto de estilos TTK vinculado a la ventana principal
    style = ttk.Style(root)
    
    # Usar tema 'clam' para mejor compatibilidad con colores personalizados
    # Otros temas: 'default', 'alt', 'classic'
    style.theme_use('clam')

    # ------------------------------------------------------------------
    # ESTILO: Login.TButton (Botón Azul)
    # ------------------------------------------------------------------
    # Usado en la pantalla de login para el botón "Ingresar al Sistema"
    
    style.configure("Login.TButton",
                    background=COLOR_BTN_LOGIN,    # Color de fondo normal
                    foreground=COLOR_TEXT_LOGIN,   # Color del texto
                    font=FONT_P_BOLD,              # Fuente en negrita
                    borderwidth=0,                 # Sin borde 3D estándar
                    relief="flat",                 # Apariencia plana
                    padding=[15, 12])              # Padding interno [horiz, vert]

    # Mapeo de estados: define cómo cambia el botón en diferentes estados
    style.map("Login.TButton",
              background=[('active', COLOR_BTN_LOGIN_HOVER)],  # Color al hover/click
              foreground=[('active', COLOR_TEXT_LOGIN)])

    # ------------------------------------------------------------------
    # ESTILO: Pre.TButton (Botón Naranja)
    # ------------------------------------------------------------------
    # Usado en la sección de preinscripción
    
    style.configure("Pre.TButton",
                    background=COLOR_BTN_PRE,
                    foreground=COLOR_TEXT_PRE,
                    font=FONT_P_BOLD,
                    borderwidth=0,
                    relief="flat",
                    padding=[15, 12])

    style.map("Pre.TButton",
              background=[('active', COLOR_BTN_PRE_HOVER)],
              foreground=[('active', COLOR_TEXT_PRE)])
    
    # ------------------------------------------------------------------
    # ESTILOS DE DASHBOARD
    # ------------------------------------------------------------------
    # Estos estilos son usados por los módulos de admin/directivo
    
    # Botón azul principal para acciones importantes
    style.configure("AdminBlue.TButton",
                    background="#007bff",
                    foreground=COLOR_TEXT_LIGHT,
                    font=FONT_P_BOLD)
    style.map("AdminBlue.TButton",
              background=[('active', '#0056b3')])  # Azul más oscuro al hover
    
    # Botón verde para acciones secundarias/confirmación
    style.configure("AdminGreen.TButton",
                    background="#28a745",
                    foreground=COLOR_TEXT_LIGHT,
                    font=FONT_P_BOLD)
    style.map("AdminGreen.TButton",
              background=[('active', '#1e7e34')])  # Verde más oscuro al hover

# Nota: Para agregar más estilos, seguir el mismo patrón:
# 1. style.configure("NombreEstilo.TButton", ...) para configuración base
# 2. style.map("NombreEstilo.TButton", ...) para estados interactivos