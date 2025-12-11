import tkinter as tk
import tkinter.ttk as ttk
from .config import *


def create_dashboard_button(parent, text, icon, module_name, nav_commands):
    """Crea botón modular para dashboard directivo con estilos diferenciados."""
    frame = tk.Frame(
        parent,
        bg="#ffffff",
        padx=25,
        pady=25,
        relief="solid",
        bd=2,
        highlightbackground=COLOR_TEST_BORDER,
        highlightthickness=2
    )
    
    # Icono grande
    tk.Label(
        frame,
        text=icon,
        font=("Segoe UI Emoji", 40, "bold"),
        bg="#ffffff",
        fg=COLOR_HEADER_PRE
    ).pack(pady=(0, 15))
    
    # Título del módulo
    tk.Label(
        frame,
        text=text,
        font=FONT_H3,
        bg="#ffffff",
        fg=COLOR_TEXT_DARK
    ).pack(pady=(0, 15))
    
    # Texto descriptivo
    description_map = {
        'achievements_manager': 'Gestión completa de logros CRE',
        'student_manager': 'Registro y seguimiento de estudiantes',
        'groups_manager': 'Administración de grupos y asignaciones',
        'citation_generator': 'Generador de citaciones GCR'
    }
    
    tk.Label(
        frame,
        text=description_map.get(module_name, "Abrir módulo"),
        font=FONT_P,
        bg="#ffffff",
        fg=COLOR_TEXT_MUTED,
        wraplength=200
    ).pack(pady=(0, 20))
    
    # Comando de navegación
    show_module_command = lambda: nav_commands['show_frame'](module_name)
    
    # Estilo condicional del botón
    if module_name in ['groups_manager', 'citation_generator', 'achievements_manager']:
        style = "AdminBlue.TButton"
        btn_text = "→ Gestionar"
    else:
        style = "AdminGreen.TButton"
        btn_text = "→ Abrir Módulo"
    
    ttk.Button(
        frame,
        text=btn_text,
        style=style,
        command=show_module_command
    ).pack(pady=(0, 0))
    
    return frame


def create_director_dashboard(master, nav_commands):
    """Dashboard completo para rol DIRECTIVO con navegación lateral."""
    
    dashboard_frame = tk.Frame(master)
    dashboard_frame.grid_columnconfigure(0, weight=0)
    dashboard_frame.grid_columnconfigure(1, weight=1)
    dashboard_frame.grid_rowconfigure(0, weight=1)
    
    # 1. BARRA LATERAL (SIDEBAR)
    sidebar = tk.Frame(dashboard_frame, bg=COLOR_DARK_BG, width=260)
    sidebar.grid(row=0, column=0, sticky="nsew")
    sidebar.pack_propagate(False)
    
    # Header de la Sidebar
    header_sid = tk.Frame(sidebar, bg=COLOR_DARK_BG)
    header_sid.pack(fill="x", pady=(20, 25))
    
    tk.Label(
        header_sid,
        text="👑 Panel Directivo",
        bg=COLOR_DARK_BG,
        fg=COLOR_TEXT_LIGHT,
        font=FONT_H1
    ).pack()
    
    tk.Label(
        header_sid,
        text="Directora General",
        bg=COLOR_DARK_BG,
        fg=COLOR_HEADER_PRE,
        font=FONT_H3
    ).pack(pady=(5, 15))
    
    # Separador
    tk.Frame(sidebar, height=1, bg="#444a57").pack(fill="x", padx=20, pady=(0, 20))
    
    # Función para botones de navegación lateral
    def create_side_nav_button(parent, text, icon, module_name=None, is_active=False):
        btn_frame = tk.Frame(
            parent,
            bg=COLOR_ACCENT_DARK if is_active else COLOR_DARK_BG
        )
        btn_frame.pack(fill="x", pady=(0, 5), padx=20)
        
        def on_click():
            if module_name:
                nav_commands['show_frame'](module_name)
        
        btn = tk.Button(
            btn_frame,
            text=f"{icon}  {text}",
            anchor="w",
            bd=0,
            padx=20,
            pady=15,
            highlightthickness=0,
            bg=COLOR_ACCENT_DARK if is_active else COLOR_DARK_BG,
            fg=COLOR_HEADER_PRE if is_active else COLOR_TEXT_LIGHT,
            font=FONT_P_BOLD,
            command=on_click,
            relief="flat"
        )
        btn.pack(fill="x")
        
        # Hover effects
        def on_enter(e):
            btn.config(bg=COLOR_ACCENT_DARK)
        def on_leave(e):
            btn.config(bg=COLOR_ACCENT_DARK if is_active else COLOR_DARK_BG)
        
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        
        return btn
    
    # Navegación principal (activa Dashboard)
    create_side_nav_button(sidebar, "Dashboard Principal", "🏠", None, is_active=True)
    create_side_nav_button(sidebar, "Gestión de Logros", "⭐", "achievements_manager")
    create_side_nav_button(sidebar, "Estudiantes", "👨‍🎓", "student_manager")
    create_side_nav_button(sidebar, "Grupos", "👥", "groups_manager")
    create_side_nav_button(sidebar, "Citaciones", "📝", "citation_generator")
    
    # Separador antes del footer
    tk.Frame(sidebar, height=1, bg="#444a57").pack(fill="x", pady=20, padx=20)
    
    # Footer (Cerrar Sesión)
    footer_sid = tk.Frame(sidebar, bg=COLOR_DARK_BG)
    footer_sid.pack(fill="x", side="bottom", pady=20, padx=20)
    
    tk.Button(
        footer_sid,
        text="❌ Cerrar Sesión",
        bg=COLOR_DARK_BG,
        fg="#ff6b6b",
        font=FONT_P_BOLD,
        bd=0,
        highlightthickness=0,
        relief="flat",
        command=nav_commands['home']
    ).pack(fill="x", pady=10)
    
    # 2. CONTENIDO PRINCIPAL
    main_content = tk.Frame(dashboard_frame, bg="#f8f9fa")
    main_content.grid(row=0, column=1, sticky="nsew", padx=(15, 30), pady=30)
    main_content.grid_columnconfigure(0, weight=1)
    
    # Header del contenido
    header_content = tk.Frame(main_content, bg="#f8f9fa")
    header_content.pack(fill="x", pady=(0, 30))
    
    tk.Label(
        header_content,
        text="👑 Panel Directivo - Dashboard Principal",
        font=FONT_H1,
        bg="#f8f9fa",
        fg=COLOR_TEXT_DARK
    ).pack(side="left")
    
    tk.Label(
        header_content,
        text="Rol: Directora General | Período: Nov-Dic 2025",
        font=FONT_P,
        bg="#f8f9fa",
        fg=COLOR_TEXT_MUTED
    ).pack(side="right")
    
    # Estadísticas rápidas
    stats_row = tk.Frame(main_content, bg="#f8f9fa")
    stats_row.pack(fill="x", pady=(0, 30))
    stats_row.grid_columnconfigure(0, weight=1)
    stats_row.grid_columnconfigure(1, weight=1)
    stats_row.grid_columnconfigure(2, weight=1)
    
    # Cards de estadísticas
    stat_cards = [
        ("👥 Total Estudiantes", "156", "#28a745"),
        ("⭐ Logros Registrados", "847", COLOR_HEADER_PRE),
        ("📝 Citaciones Pendientes", "12", "#f39c12"),
        ("👥 Grupos Activos", "18", "#3498db")
    ]
    
    for i, (title, value, color) in enumerate(stat_cards):
        col = i % 3
        row = i // 3
        card = tk.Frame(
            stats_row,
            bg="#ffffff",
            padx=25,
            pady=25,
            relief="solid",
            bd=2,
            highlightbackground=COLOR_TEST_BORDER
        )
        card.grid(row=row, column=col, sticky="nsew", padx=10, pady=10)
        
        tk.Label(card, text=title, font=FONT_P_BOLD, fg=color, bg="#ffffff").pack(anchor="w")
        tk.Label(card, text=value, font=FONT_H1, fg=color, bg="#ffffff").pack(anchor="w")
    
    # Grid de Módulos (3x2)
    modules_grid = tk.Frame(main_content, bg="#f8f9fa")
    modules_grid.pack(fill="both", expand=True)
    
    modules_grid.grid_columnconfigure(0, weight=1)
    modules_grid.grid_columnconfigure(1, weight=1)
    modules_grid.grid_columnconfigure(2, weight=1)
    modules_grid.grid_rowconfigure(0, weight=1)
    modules_grid.grid_rowconfigure(1, weight=1)
    
    # Fila 1: Gestión Académica
    create_dashboard_button(
        modules_grid, "Gestión de Logros (CRE)", "⭐", "achievements_manager", nav_commands
    ).grid(row=0, column=0, sticky="nsew", padx=15, pady=15)
    
    create_dashboard_button(
        modules_grid, "Gestión de Estudiantes", "👨‍🎓", "student_manager", nav_commands
    ).grid(row=0, column=1, sticky="nsew", padx=15, pady=15)
    
    create_dashboard_button(
        modules_grid, "Gestión de Grupos", "👥", "groups_manager", nav_commands
    ).grid(row=0, column=2, sticky="nsew", padx=15, pady=15)
    
    # Fila 2: Comunicación y Reportes
    create_dashboard_button(
        modules_grid, "Citaciones (GCR)", "📝", "citation_generator", nav_commands
    ).grid(row=1, column=0, sticky="nsew", padx=15, pady=15)
    
    create_dashboard_button(
        modules_grid, "Reportes y Estadísticas", "📈", "reports_manager", nav_commands
    ).grid(row=1, column=1, sticky="nsew", padx=15, pady=15)
    
    create_dashboard_button(
        modules_grid, "Notificaciones", "📧", "notifications_manager", nav_commands
    ).grid(row=1, column=2, sticky="nsew", padx=15, pady=15)
    
    return dashboard_frame
