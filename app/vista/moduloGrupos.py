# Archivo: groups_module.py

import tkinter as tk
import tkinter.ttk as ttk
from config import *
from session_manager import get_dashboard_command

def create_groups_manager(master, nav_commands):
    """Crea la interfaz de Gestión de Grupos Académicos."""
    
    groups_frame = tk.Frame(master, bg="#f5f7fa")
    groups_frame.grid_columnconfigure(0, weight=0)
    groups_frame.grid_columnconfigure(1, weight=1)
    groups_frame.grid_rowconfigure(0, weight=1)

    # 1. SIDEBAR DE NAVEGACIÓN
    sidebar = tk.Frame(groups_frame, bg=COLOR_SIDEBAR_ADMIN, width=200)
    sidebar.grid(row=0, column=0, sticky="nsew")
    sidebar.pack_propagate(False)

    tk.Label(sidebar, text="Gestión de Grupos", bg=COLOR_DARK_BG, fg=COLOR_TEXT_LIGHT, font=FONT_H1).pack(fill="x", ipady=10)
    tk.Label(sidebar, text="Administración", bg=COLOR_SIDEBAR_ADMIN, fg=COLOR_HEADER_PRE, font=FONT_P).pack(fill="x", pady=(0, 10))
    
    # Botones de navegación interna
    def create_nav_btn(parent, text, icon, is_active=False):
        btn_bg = COLOR_ACCENT_DARK if is_active else COLOR_SIDEBAR_ADMIN
        btn = tk.Button(parent, text=f"{icon}  {text}", anchor="w", bd=0, padx=10, pady=10, highlightthickness=0,
                        bg=btn_bg, fg=COLOR_TEXT_LIGHT, font=FONT_P_BOLD)
        btn.pack(fill="x", pady=(1, 1))
        return btn

    create_nav_btn(sidebar, "Lista de Grupos", "📋", is_active=True)
    create_nav_btn(sidebar, "Asignar Estudiantes", "🧑🏻‍🎓")

    # Botón Volver al Dashboard — evaluar al click para tomar rol actual
    tk.Button(sidebar, text="← Volver al Dashboard", bg=COLOR_ACCENT_ADMIN, fg=COLOR_TEXT_LIGHT, font=FONT_P_BOLD, bd=0, 
              highlightthickness=0, command=lambda: get_dashboard_command(nav_commands)()).pack(fill="x", side="bottom", pady=20, padx=10)


    # 2. CONTENIDO PRINCIPAL
    main_content = tk.Frame(groups_frame, bg="#f5f7fa", padx=30, pady=30)
    main_content.grid(row=0, column=1, sticky="nsew")
    main_content.grid_columnconfigure(0, weight=1)
    
    # Header del contenido
    header_content = tk.Frame(main_content, bg="#f5f7fa")
    header_content.pack(fill="x", pady=(0, 20))
    
    tk.Label(header_content, text="Gestión de Grupos Académicos", font=FONT_H1, bg="#f5f7fa", fg=COLOR_TEXT_DARK).pack(side="left", anchor="w")
    tk.Label(header_content, text="Colegio Pequeño - 6 grupos activos", font=FONT_P, bg="#f5f7fa", fg=COLOR_TEXT_MUTED).pack(side="right", anchor="e")

    # Barra de búsqueda y botón Crear Grupo
    search_frame = tk.Frame(main_content, bg="#f5f7fa")
    search_frame.pack(fill="x", pady=(0, 20))
    ttk.Entry(search_frame, width=40).pack(side="left", ipady=5, padx=(0, 20))
    tk.Button(search_frame, text="+ Crear Nuevo Grupo", bg=COLOR_ACCENT_ADMIN, fg=COLOR_TEXT_LIGHT, font=FONT_P_BOLD, bd=0).pack(side="right", ipady=5)

    # --- Grid de Grupos ---
    groups_grid = tk.Frame(main_content, bg="#f5f7fa")
    groups_grid.pack(fill="both", expand=True)
    groups_grid.grid_columnconfigure(0, weight=1)
    groups_grid.grid_columnconfigure(1, weight=1)

    # Función para crear tarjeta de grupo
    def create_group_card(parent, title, professor, range, capacity, color):
        card = tk.Frame(parent, bg="#ffffff", padx=15, pady=15, relief="solid", bd=1, highlightbackground=COLOR_TEST_BORDER, highlightthickness=1)
        
        # Título y Capacidad
        title_frame = tk.Frame(card, bg="#ffffff")
        title_frame.pack(fill="x")
        tk.Label(title_frame, text=f"🧑🏻‍🎓 {title}", font=FONT_H2, bg="#ffffff", fg=COLOR_TEXT_DARK).pack(side="left", anchor="w")
        tk.Label(title_frame, text=capacity, font=FONT_P_BOLD, bg="#f0f0f0", fg=color, padx=5).pack(side="right", anchor="e")
        
        # Detalles
        tk.Label(card, text=f"Rango de edad: {range}", font=FONT_P, bg="#ffffff", fg=COLOR_TEXT_MUTED).pack(anchor="w", pady=(10, 2))
        tk.Label(card, text=f"Profesor: {professor}", font=FONT_P, bg="#ffffff", fg=COLOR_TEXT_MUTED).pack(anchor="w", pady=2)
        tk.Label(card, text=f"Horario: Lunes a Viernes 7:00-12:00", font=FONT_P, bg="#ffffff", fg=COLOR_TEXT_MUTED).pack(anchor="w", pady=2)
        
        # Barra de progreso (simulada)
        bar = tk.Frame(card, bg=color, height=5)
        bar.pack(fill="x", pady=(10, 15))
        
        # Botones de Acción
        btn_frame = tk.Frame(card, bg="#ffffff")
        btn_frame.pack(fill="x")
        
        tk.Button(btn_frame, text="📝 Editar", bg="#f0f0f0", fg=COLOR_TEXT_DARK, font=FONT_P_BOLD, bd=0).pack(side="left", fill="x", expand=True, padx=(0, 5))
        tk.Button(btn_frame, text="→ Asignar", bg=COLOR_ACCENT_ADMIN, fg=COLOR_TEXT_LIGHT, font=FONT_P_BOLD, bd=0).pack(side="left", fill="x", expand=True, padx=(5, 0))
        
        return card

    # Grupos (Fila 1)
    create_group_card(groups_grid, "Párvulos A", "Maria García", "3-4 años", "10/10 cupos", "red").grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
    create_group_card(groups_grid, "Párvulos B", "Laura Pérez", "3-4 años", "8/10 cupos", "orange").grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
    
    # Grupos (Fila 2)
    create_group_card(groups_grid, "Caminadores A", "Carlos Martínez", "2-3 años", "7/8 cupos", "green").grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
    create_group_card(groups_grid, "Caminadores B", "Ana Rodríguez", "2-3 años", "6/8 cupos", "#007bff").grid(row=1, column=1, sticky="nsew", padx=10, pady=10)
    
    return groups_frame