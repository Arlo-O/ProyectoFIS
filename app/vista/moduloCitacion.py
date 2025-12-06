"""
Archivo: moduloCitacion.py
Generación de Citaciones a Acudientes (Caso de Uso 42).

Módulo funcional para directivos que permite generar citaciones
formales para reuniones con acudientes/padres.

Funcionalidades:
- Formulario completo de citación (fecha, hora, lugar, motivo)
- Selección de destinatarios (grupos completos o individuales)
- Envío masivo o selectivo
- Generación de documento formal
- Registro de citaciones enviadas

Acceso: Directivo (director)
Caso de Uso: CU-42 (Generar citación a reunión)
"""

import tkinter as tk
import tkinter.ttk as ttk
from config import *
from session_manager import get_dashboard_command

def create_citation_generator(master, nav_commands):
    """Crea la interfaz del Generador de Citaciones."""
    
    citation_frame = tk.Frame(master, bg="#f5f7fa")
    
    # 1. HEADER FIJO (Usando color del Admin/Citación)
    header_frame = tk.Frame(citation_frame, bg=COLOR_ACCENT_ADMIN, height=50)
    header_frame.pack(fill="x", side="top")
    header_frame.pack_propagate(False)

    # Evaluar al click para usar el rol actual
    tk.Button(header_frame, text="← Volver al Dashboard", bg=COLOR_ACCENT_ADMIN, fg=COLOR_TEXT_LIGHT, 
              font=FONT_P_BOLD, bd=0, highlightthickness=0, 
              command=lambda: get_dashboard_command(nav_commands)()).pack(side="left", padx=20)

    tk.Label(header_frame, text="Generación de Citación (GCR) - Caso de Uso 42", 
             bg=COLOR_ACCENT_ADMIN, fg=COLOR_TEXT_LIGHT, font=FONT_H1).pack(side="left", padx=50)
    
    # 2. CONTENIDO PRINCIPAL
    content_area = tk.Frame(citation_frame, bg="#ffffff", padx=30, pady=30)
    content_area.pack(fill="both", expand=True, padx=20, pady=20)
    content_area.grid_columnconfigure(0, weight=1)
    content_area.grid_columnconfigure(1, weight=1)

    # --- Columna 1: Campos Obligatorios ---
    col1 = tk.Frame(content_area, bg="#ffffff")
    col1.grid(row=0, column=0, sticky="nsew", padx=10)
    
    tk.Label(col1, text="🗓️ Campos Obligatorios de la Citación", font=FONT_H3, bg="#ffffff", fg=COLOR_ACCENT_ADMIN).pack(anchor="w", pady=(0, 15))
    
    # Fecha y Hora
    date_time_frame = tk.Frame(col1, bg="#ffffff")
    date_time_frame.pack(fill="x")
    
    tk.Label(date_time_frame, text="Fecha *", bg="#ffffff", font=FONT_P_BOLD).grid(row=0, column=0, sticky="w", padx=5, pady=(5, 0))
    tk.Entry(date_time_frame, font=FONT_P, width=20).grid(row=1, column=0, sticky="w", padx=5, ipady=5)
    
    tk.Label(date_time_frame, text="Hora *", bg="#ffffff", font=FONT_P_BOLD).grid(row=0, column=1, sticky="w", padx=5, pady=(5, 0))
    tk.Entry(date_time_frame, font=FONT_P, width=20).grid(row=1, column=1, sticky="w", padx=5, ipady=5)
    
    # Lugar
    tk.Label(col1, text="Lugar *", bg="#ffffff", font=FONT_P_BOLD).pack(anchor="w", pady=(15, 5))
    tk.Entry(col1, font=FONT_P).pack(fill="x", ipady=5)
    
    # Motivo
    tk.Label(col1, text="Motivo *", bg="#ffffff", font=FONT_P_BOLD).pack(anchor="w", pady=(15, 5))
    tk.Entry(col1, font=FONT_P).pack(fill="x", ipady=5)

    # Descripción Detallada
    tk.Label(col1, text="Descripción Detallada", bg="#ffffff", font=FONT_P_BOLD).pack(anchor="w", pady=(15, 5))
    tk.Text(col1, font=FONT_P, height=5).pack(fill="x")

    # --- Columna 2: Selector de Destinatarios ---
    col2 = tk.Frame(content_area, bg="#e8f0f7", padx=15, pady=15, relief="solid", bd=1, highlightbackground=COLOR_TEST_BORDER, highlightthickness=1)
    col2.grid(row=0, column=1, sticky="nsew", padx=10)
    
    tk.Label(col2, text="👤 Selector de Destinatarios", font=FONT_H3, bg="#e8f0f7", fg=COLOR_ACCENT_ADMIN).pack(anchor="w", pady=(0, 15))

    # Tipo de Envío (Radio Buttons)
    send_type = tk.StringVar(value="grupos")
    
    tk.Radiobutton(col2, text="Enviar a Grupos Seleccionados", variable=send_type, value="grupos", bg="#e8f0f7", font=FONT_P_BOLD).pack(anchor="w")
    tk.Label(col2, text="Seleccionar grupos completos", bg="#e8f0f7", fg=COLOR_TEXT_MUTED, font=FONT_SMALL).pack(anchor="w", padx=20)
    
    tk.Radiobutton(col2, text="Enviar a Acudientes Individuales", variable=send_type, value="individual", bg="#e8f0f7", font=FONT_P_BOLD).pack(anchor="w", pady=(15, 0))
    tk.Label(col2, text="Lista seleccionable de nombres", bg="#e8f0f7", fg=COLOR_TEXT_MUTED, font=FONT_SMALL).pack(anchor="w", padx=20)

    # Lista de Nombres (ListBox simulado)
    tk.Label(col2, text="Lista Seleccionable de Nombres (0):", bg="#e8f0f7", font=FONT_P_BOLD).pack(anchor="w", pady=(15, 5))
    
    listbox = tk.Listbox(col2, height=10, selectmode=tk.MULTIPLE, font=FONT_P)
    listbox.insert(tk.END, "Maria González - Párvulos A")
    listbox.insert(tk.END, "Emma Rodríguez - Párvulos A")
    listbox.insert(tk.END, "Carlos Martínez - Párvulos A")
    listbox.pack(fill="x")

    # Botón de Enviar (Pie de página)
    tk.Button(citation_frame, text="Generar y Enviar Citación", bg=COLOR_ACCENT_ADMIN, fg=COLOR_TEXT_LIGHT, font=FONT_H3, bd=0).pack(pady=20, ipady=10)
    
    return citation_frame