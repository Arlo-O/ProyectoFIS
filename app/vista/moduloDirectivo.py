

import tkinter as tk
import tkinter.ttk as ttk
from config import *

def create_dashboard_button(parent, text, icon, module_name, nav_commands):
    frame = tk.Frame(parent, bg="#ffffff", padx=20, pady=20, relief="solid", bd=1, highlightbackground=COLOR_TEST_BORDER, highlightthickness=1)
    
    tk.Label(frame, text=icon, font=("Helvetica", 36), bg="#ffffff").pack(pady=(0, 10))
    tk.Label(frame, text=text, font=FONT_H3, bg="#ffffff", fg=COLOR_TEXT_DARK).pack(pady=(0, 10))
    
    show_module_command = lambda: nav_commands['show_frame'](module_name) 

    if module_name in ['groups_manager', 'citation_generator', 'achievements_manager']:
        style = "AdminBlue.TButton"
        btn_text = "→ Gestionar"
    else:
        style = "AdminGreen.TButton"
        btn_text = "→ Abrir Módulo"
        
    ttk.Button(frame, text=btn_text, style=style, command=show_module_command).pack(pady=(10, 0))
    
    return frame

def create_director_dashboard(master, nav_commands):
    
    dashboard_frame = tk.Frame(master)
    dashboard_frame.grid_columnconfigure(0, weight=0) 
    dashboard_frame.grid_columnconfigure(1, weight=1) 
    dashboard_frame.grid_rowconfigure(0, weight=1)
    
    # 1. BARRA LATERAL (SIDEBAR)
    sidebar = tk.Frame(dashboard_frame, bg=COLOR_DARK_BG, width=220)
    sidebar.grid(row=0, column=0, sticky="nsew")
    sidebar.pack_propagate(False)

    # Header de la Sidebar
    tk.Label(sidebar, text="Directivo Panel", bg=COLOR_DARK_BG, fg=COLOR_TEXT_LIGHT, font=FONT_H1, pady=15).pack(fill="x")
    tk.Label(sidebar, text="Navegación", bg=COLOR_DARK_BG, fg=COLOR_HEADER_PRE, font=FONT_P_BOLD).pack(fill="x", padx=10, pady=(5, 0), anchor="w")
    tk.Frame(sidebar, height=1, bg="#444a57").pack(fill="x", pady=10, padx=10)

    # ... (Botones de navegación de la sidebar inalterados) ...
    def create_side_nav_button(parent, text, icon, is_active=False):
        btn_frame = tk.Frame(parent, bg=COLOR_ACCENT_DARK if is_active else COLOR_DARK_BG)
        btn = tk.Button(btn_frame, text=f"{icon}   {text}", anchor="w", bd=0, padx=10, pady=8, highlightthickness=0,
                        bg=COLOR_ACCENT_DARK if is_active else COLOR_DARK_BG, 
                        fg=COLOR_HEADER_PRE if is_active else COLOR_TEXT_LIGHT,
                        font=FONT_P_BOLD)
        btn.pack(fill="x")
        btn_frame.pack(fill="x", pady=(0, 2))
        return btn

    create_side_nav_button(sidebar, "Dashboard", "🏠", is_active=True)
    
    # TODO: Implementar módulo de reportes
    # create_side_nav_button(sidebar, "Reportes", "📈")
    
    # Footer (Cerrar Sesión)
    tk.Frame(sidebar, height=1, bg="#444a57").pack(fill="x", pady=10, padx=10, side="bottom")
    # 🛑 CORRECCIÓN: Este botón SIEMPRE debe ir a 'home'
    tk.Button(sidebar, text="❌ Cerrar Sesión", bg=COLOR_DARK_BG, fg="#ff5555", font=FONT_P_BOLD, bd=0, 
              highlightthickness=0, command=nav_commands['home']).pack(fill="x", side="bottom", pady=10, padx=10)


    # 2. CONTENIDO PRINCIPAL (Se mantiene)
    main_content = tk.Frame(dashboard_frame, bg="#f5f7fa")
    main_content.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
    
    # Header del contenido
    header_content = tk.Frame(main_content, bg="#f5f7fa")
    header_content.pack(fill="x", pady=(0, 20))
    
    tk.Label(header_content, text="Panel Directivo", font=FONT_H1, bg="#f5f7fa", fg=COLOR_TEXT_DARK).pack(side="left", anchor="w")
    tk.Label(header_content, text="Rol: Directivo", font=FONT_P, bg="#f5f7fa", fg=COLOR_TEXT_MUTED).pack(side="right", anchor="e")

    # --- Grid de Módulos (Se mantiene) ---
    modules_grid = tk.Frame(main_content, bg="#f5f7fa")
    modules_grid.pack(fill="both", expand=True)
    
    modules_grid.grid_columnconfigure(0, weight=1)
    modules_grid.grid_columnconfigure(1, weight=1)
    modules_grid.grid_columnconfigure(2, weight=1)

    # Fila 1 (Módulos de gestión académica)
    create_dashboard_button(modules_grid, "Gestión de Logros", "⭐", "achievements_manager", nav_commands).grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
    create_dashboard_button(modules_grid, "Gestión de Estudiantes", "‍🎓", "student_manager", nav_commands).grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
    create_dashboard_button(modules_grid, "Gestión de Grupos", "👥", "groups_manager", nav_commands).grid(row=0, column=2, sticky="nsew", padx=10, pady=10)
    
    # Fila 2 (Módulos de comunicación y seguimiento)
    create_dashboard_button(modules_grid, "Citaciones y Entrevistas", "📝", "citation_generator", nav_commands).grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
    
    # TODO: Implementar módulo de notificaciones
    # create_dashboard_button(modules_grid, "Gestión de Notificaciones", "📧", "notifications_manager", nav_commands).grid(row=1, column=1, sticky="nsew", padx=10, pady=10)
    
    # TODO: Implementar módulo de reportes
    # create_dashboard_button(modules_grid, "Reportes y Estadísticas", "📈", "reports", nav_commands).grid(row=1, column=2, sticky="nsew", padx=10, pady=10)
    
    return dashboard_frame