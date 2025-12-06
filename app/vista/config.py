"""
Archivo: config.py
Configuración centralizada de constantes para la interfaz gráfica.

Este archivo define todos los colores, fuentes y valores constantes utilizados
en la aplicación GUI. Centralizar estas configuraciones facilita el mantenimiento
y permite cambios rápidos en el tema visual.

Secciones:
- Colores base: Fondos, textos, bordes generales
- Colores de botones: Login (azul) y Preinscripción (naranja)
- Colores por rol: Admin, Profesor, Acudiente
- Fuentes: Títulos, párrafos, textos pequeños
"""

# ======================================================================
# COLORES BASE
# ======================================================================

# Colores de fondo principales
COLOR_DARK_BG = "#2b313d"          # Fondo oscuro para headers
COLOR_BG_LOGIN = "#f5f7fa"         # Fondo claro para sección de login
COLOR_BG_PRE = "#ffffff"           # Fondo blanco para preinscripción

# Colores de texto
COLOR_TEXT_LIGHT = "#ffffff"       # Texto blanco (sobre fondos oscuros)
COLOR_TEXT_DARK = "#333333"        # Texto oscuro (sobre fondos claros)
COLOR_TEXT_MUTED = "#666666"       # Texto atenuado para información secundaria
COLOR_TEXT_PLACEHOLDER = "#aaaaaa" # Color para placeholders en campos de entrada

# Colores de acento y bordes
COLOR_HEADER_PRE = "#ff7733"       # Color naranja para header de preinscripción
COLOR_ACCENT_DARK = "#3e4655"      # Acento oscuro
COLOR_TEST_BORDER = "#dddddd"      # Bordes sutiles

# ======================================================================
# COLORES DE BOTONES
# ======================================================================

# Botón de Login (Azul)
COLOR_BTN_LOGIN = "#4a90e2"        # Fondo normal
COLOR_BTN_LOGIN_HOVER = "#3a7fd1"  # Fondo al pasar el mouse
COLOR_TEXT_LOGIN = "#ffffff"       # Texto del botón

# Botón de Preinscripción (Naranja)
COLOR_BTN_PRE = "#ff7733"          # Fondo normal
COLOR_BTN_PRE_HOVER = "#e66627"    # Fondo al pasar el mouse
COLOR_TEXT_PRE = "#ffffff"         # Texto del botón

# ======================================================================
# COLORES POR ROL DE USUARIO
# ======================================================================

# Administrador (Azul)
COLOR_ACCENT_ADMIN = "#007bff"     # Color de acento principal
COLOR_SIDEBAR_ADMIN = "#343a40"    # Color de sidebar/menú lateral

# Profesor (Verde)
COLOR_ACCENT_TEACHER = "#28a745"   # Color de acento principal
COLOR_SIDEBAR_TEACHER = "#1e7e34"  # Color de sidebar/menú lateral

# Acudiente/Padre (Naranja)
COLOR_ACCENT_PARENT = "#ff7733"    # Color de acento principal
COLOR_SIDEBAR_PARENT = "#cc5c26"   # Color de sidebar/menú lateral

# ======================================================================
# FUENTES
# ======================================================================
# Formato: (familia, tamaño, peso)

FONT_H1 = ("Helvetica", 16, "bold")      # Títulos principales
FONT_H2 = ("Helvetica", 14, "bold")      # Subtítulos
FONT_H3 = ("Helvetica", 12, "bold")      # Encabezados de sección
FONT_P = ("Helvetica", 10)               # Texto de párrafo normal
FONT_P_BOLD = ("Helvetica", 10, "bold")  # Texto de párrafo en negrita
FONT_SMALL = ("Helvetica", 8)            # Texto pequeño para notas