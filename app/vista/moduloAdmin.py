# Archivo: admin_module.py

import tkinter as tk
import tkinter.ttk as ttk
from config import *

# --- FUNCIÓN AUXILIAR DE WIDGETS ---
def create_sidebar_button(parent, text, icon, module_name, nav_commands, is_active=False):
    """Crea un botón de navegación lateral."""
    bg_color = COLOR_ACCENT_DARK if is_active else COLOR_SIDEBAR_ADMIN
    active_color = COLOR_ACCENT_DARK
    
    btn_frame = tk.Frame(parent, bg=bg_color)
    
    btn = tk.Button(btn_frame, text=f"{icon}   {text}", anchor="w", bd=0, padx=10, pady=8, highlightthickness=0,
                    bg=bg_color, 
                    fg=COLOR_HEADER_PRE if is_active else COLOR_TEXT_LIGHT,
                    font=FONT_P_BOLD,
                    command=lambda: nav_commands['show_frame'](module_name) if module_name else None)
    btn.pack(fill="x")
    btn_frame.pack(fill="x", pady=(0, 2))
    
    # Manejo de Hover simple para Tkinter
    btn.bind("<Enter>", lambda e: btn.config(bg=active_color))
    btn.bind("<Leave>", lambda e: btn.config(bg=bg_color))
    
    return btn

def create_info_card(parent, title, value, icon, color):
    """Crea una tarjeta de información clave (Estudiantes, Profesores, etc.)."""
    card = tk.Frame(parent, bg="#ffffff", padx=15, pady=15, relief="solid", bd=1, highlightbackground=COLOR_TEST_BORDER, highlightthickness=1)
    
    icon_label = tk.Label(card, text=icon, font=("Helvetica", 24), fg=color, bg="#ffffff")
    icon_label.pack(side="left")
    
    text_frame = tk.Frame(card, bg="#ffffff")
    text_frame.pack(side="right", padx=(10, 0))
    
    tk.Label(text_frame, text=value, font=FONT_H1, fg=color, bg="#ffffff").pack(anchor="w")
    tk.Label(text_frame, text=title, font=FONT_P, fg=COLOR_TEXT_MUTED, bg="#ffffff").pack(anchor="w")
    
    return card

# --- FUNCIÓN PRINCIPAL: DASHBOARD ADMINISTRADOR ---
def create_admin_dashboard(master, nav_commands):
    """Crea la interfaz del Dashboard Administrador."""
    
    dashboard_frame = tk.Frame(master)
    dashboard_frame.grid_columnconfigure(0, weight=0) 
    dashboard_frame.grid_columnconfigure(1, weight=1) 
    dashboard_frame.grid_rowconfigure(0, weight=1)
    
    # 1. BARRA LATERAL (SIDEBAR)
    sidebar = tk.Frame(dashboard_frame, bg=COLOR_SIDEBAR_ADMIN, width=220)
    sidebar.grid(row=0, column=0, sticky="nsew")
    sidebar.pack_propagate(False)

    # Header de la Sidebar
    tk.Label(sidebar, text="Gestión Académica", bg=COLOR_DARK_BG, fg=COLOR_TEXT_LIGHT, font=FONT_H1).pack(fill="x", ipady=10)
    tk.Label(sidebar, text="Administrador", bg=COLOR_SIDEBAR_ADMIN, fg=COLOR_HEADER_PRE, font=FONT_H3).pack(fill="x")
    tk.Label(sidebar, text="Bienvenido, Administrador Principal", bg=COLOR_SIDEBAR_ADMIN, fg=COLOR_TEXT_LIGHT, font=FONT_P).pack(fill="x", pady=(0, 10))

    # Nav Buttons
    tk.Label(sidebar, text="GESTIÓN PRINCIPAL", bg=COLOR_SIDEBAR_ADMIN, fg="#a0a0a0", font=FONT_SMALL).pack(fill="x", padx=10, pady=(15, 5), anchor="w")
    create_sidebar_button(sidebar, "Dashboard Principal", "🏠", "dashboard", nav_commands, is_active=True)
    create_sidebar_button(sidebar, "Generar Citaciones", "📝", "citation_generator", nav_commands)
    create_sidebar_button(sidebar, "Gestión de Grupos", "👥", "groups_manager", nav_commands)
    create_sidebar_button(sidebar, "Categorías/Logros", "⭐", "achievements_manager", nav_commands)
    
    tk.Label(sidebar, text="REPORTES", bg=COLOR_SIDEBAR_ADMIN, fg="#a0a0a0", font=FONT_SMALL).pack(fill="x", padx=10, pady=(15, 5), anchor="w")
    create_sidebar_button(sidebar, "Reportes Académicos", "📈", "reports_admin", nav_commands)
    
    tk.Label(sidebar, text="SISTEMA", bg=COLOR_SIDEBAR_ADMIN, fg="#a0a0a0", font=FONT_SMALL).pack(fill="x", padx=10, pady=(15, 5), anchor="w")
    create_sidebar_button(sidebar, "Configuración", "⚙️", "config_admin", nav_commands)
    create_sidebar_button(sidebar, "Notificaciones", "🔔", "notifications_admin", nav_commands)
    
    # Footer (Cerrar Sesión)
    tk.Frame(sidebar, height=1, bg="#444a57").pack(fill="x", pady=10, padx=10, side="bottom")
    tk.Button(sidebar, text="❌ Cerrar Sesión", bg=COLOR_SIDEBAR_ADMIN, fg="#ff5555", font=FONT_P_BOLD, bd=0, 
              highlightthickness=0, command=nav_commands['home']).pack(fill="x", side="bottom", pady=10, padx=10)


    # 2. CONTENIDO PRINCIPAL
    main_content = tk.Frame(dashboard_frame, bg="#f5f7fa")
    main_content.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
    main_content.grid_columnconfigure(0, weight=1)
    
    # Header del contenido
    header_content = tk.Frame(main_content, bg="#f5f7fa")
    header_content.pack(fill="x", pady=(0, 20))
    tk.Label(header_content, text="Panel Administrativo", font=FONT_H1, bg="#f5f7fa", fg=COLOR_TEXT_DARK).pack(side="left", anchor="w")
    tk.Label(header_content, text="Colegio Pequeño - Sistema de Gestión Académica", font=FONT_P, bg="#f5f7fa", fg=COLOR_TEXT_MUTED).pack(side="right", anchor="e")

    # --- Tarjetas de Resumen (Top Row) ---
    summary_row = tk.Frame(main_content, bg="#f5f7fa")
    summary_row.pack(fill="x", pady=(0, 20))
    
    summary_row.grid_columnconfigure(0, weight=1)
    summary_row.grid_columnconfigure(1, weight=1)
    summary_row.grid_columnconfigure(2, weight=1)
    summary_row.grid_columnconfigure(3, weight=1)
    summary_row.grid_columnconfigure(4, weight=1)
    
    create_info_card(summary_row, "Total Estudiantes", "47", "🧑🏻‍🎓", "#007bff").grid(row=0, column=0, sticky="ew", padx=5)
    create_info_card(summary_row, "Profesores", "8", "🧑🏻‍🏫", "#28a745").grid(row=0, column=1, sticky="ew", padx=5)
    create_info_card(summary_row, "Grupos Activos", "6", "🧡", COLOR_HEADER_PRE).grid(row=0, column=2, sticky="ew", padx=5)
    create_info_card(summary_row, "Cupos Disponibles", "13", "🗒️", "#808080").grid(row=0, column=3, sticky="ew", padx=5)
    
    # --- Gestión Principal (Mid Row) ---
    management_row = tk.Frame(main_content, bg="#f5f7fa")
    management_row.pack(fill="x", pady=(0, 20))
    
    management_row.grid_columnconfigure(0, weight=1)
    management_row.grid_columnconfigure(1, weight=1)
    management_row.grid_columnconfigure(2, weight=1)

    # Card 1: Gestión de Citaciones
    card_cita = tk.Frame(management_row, bg="#ffffff", padx=15, pady=15, relief="solid", bd=1, highlightbackground=COLOR_TEST_BORDER, highlightthickness=1)
    card_cita.grid(row=0, column=0, sticky="nsew", padx=10)
    tk.Label(card_cita, text="Gestion de Citaciones (GCR)", font=FONT_H3, fg=COLOR_ACCENT_ADMIN, bg="#ffffff").pack(anchor="w", pady=(0, 5))
    tk.Label(card_cita, text="Generar citaciones grupales o individuales a acudientes.", font=FONT_P, fg=COLOR_TEXT_MUTED, bg="#ffffff", wraplength=200, justify="left").pack(anchor="w", pady=(0, 15))
    ttk.Button(card_cita, text="Abrir Módulo", style="AdminBlue.TButton", command=lambda: nav_commands['show_frame']("citation_generator")).pack(fill="x", ipady=5)

    # Card 2: Gestión de Grupos
    card_grupos = tk.Frame(management_row, bg="#ffffff", padx=15, pady=15, relief="solid", bd=1, highlightbackground=COLOR_TEST_BORDER, highlightthickness=1)
    card_grupos.grid(row=0, column=1, sticky="nsew", padx=10)
    tk.Label(card_grupos, text="Gestión de Grupos", font=FONT_H3, fg=COLOR_ACCENT_ADMIN, bg="#ffffff").pack(anchor="w", pady=(0, 5))
    tk.Label(card_grupos, text="Administrar grupos, cupos y asignación de estudiantes.", font=FONT_P, fg=COLOR_TEXT_MUTED, bg="#ffffff", wraplength=200, justify="left").pack(anchor="w", pady=(0, 15))
    ttk.Button(card_grupos, text="Gestionar", style="AdminBlue.TButton", command=lambda: nav_commands['show_frame']("groups_manager")).pack(fill="x", ipady=5)

    # Card 3: Categorías/Logros
    card_logros = tk.Frame(management_row, bg="#ffffff", padx=15, pady=15, relief="solid", bd=1, highlightbackground=COLOR_TEST_BORDER, highlightthickness=1)
    card_logros.grid(row=0, column=2, sticky="nsew", padx=10)
    tk.Label(card_logros, text="Categorías de Logros (GLE)", font=FONT_H3, fg=COLOR_ACCENT_TEACHER, bg="#ffffff").pack(anchor="w", pady=(0, 5))
    tk.Label(card_logros, text="Crear y gestionar categorías y subcategorías de evaluación.", font=FONT_P, fg=COLOR_TEXT_MUTED, bg="#ffffff", wraplength=200, justify="left").pack(anchor="w", pady=(0, 15))
    ttk.Button(card_logros, text="Gestionar", style="AdminGreen.TButton", command=lambda: nav_commands['show_frame']("achievements_manager")).pack(fill="x", ipady=5)

    # --- Tareas Pendientes (Bottom Row) ---
    bottom_row = tk.Frame(main_content, bg="#f5f7fa")
    bottom_row.pack(fill="x")
    bottom_row.grid_columnconfigure(0, weight=1)
    bottom_row.grid_columnconfigure(1, weight=1)

    # Card 4: Preinscripciones Pendientes
    card_pre = tk.Frame(bottom_row, bg="#ffffff", padx=15, pady=15, relief="solid", bd=1, highlightbackground=COLOR_TEST_BORDER, highlightthickness=1)
    card_pre.grid(row=0, column=0, sticky="nsew", padx=10)
    tk.Label(card_pre, text="Preinscripciones Pendientes de Revisión", font=FONT_H3, fg=COLOR_HEADER_PRE, bg="#ffffff").pack(anchor="w", pady=(0, 10))
    
    # Lista simulada
    def create_pre_item(parent, name, group, status_color, status_text):
        item = tk.Frame(parent, bg="#ffffff", pady=5)
        item.pack(fill="x")
        tk.Label(item, text=name, font=FONT_P_BOLD, bg="#ffffff", fg=COLOR_TEXT_DARK).pack(anchor="w")
        tk.Label(item, text=f"{group} - 3 años", font=FONT_SMALL, bg="#ffffff", fg=COLOR_TEXT_MUTED).pack(anchor="w")
        tk.Label(item, text=status_text, font=FONT_SMALL, bg=status_color, fg=COLOR_TEXT_LIGHT, padx=5).pack(side="right")
    
    create_pre_item(card_pre, "Sofia Ramirez Torres", "Párvulos", "orange", "Nueva")
    create_pre_item(card_pre, "Mateo Vargas López", "Caminadores", "orange", "Nueva")
    create_pre_item(card_pre, "Isabella Moreno Cruz", "Prejardín", "red", "En Revisión")
    
    tk.Button(card_pre, text="Ver todas (5 pendientes)", bg=COLOR_HEADER_PRE, fg=COLOR_TEXT_LIGHT, font=FONT_P_BOLD, bd=0).pack(fill="x", ipady=5, pady=(15, 0))

    # Card 5: Citaciones Programadas (Simplificado)
    card_cita_prog = tk.Frame(bottom_row, bg="#ffffff", padx=15, pady=15, relief="solid", bd=1, highlightbackground=COLOR_TEST_BORDER, highlightthickness=1)
    card_cita_prog.grid(row=0, column=1, sticky="nsew", padx=10)
    tk.Label(card_cita_prog, text="Citaciones Programadas", font=FONT_H3, fg=COLOR_ACCENT_ADMIN, bg="#ffffff").pack(anchor="w", pady=(0, 10))
    
    # Lista simulada
    def create_cita_item(parent, reason, date, status_color, status_text):
        item = tk.Frame(parent, bg="#ffffff", pady=5)
        item.pack(fill="x")
        tk.Label(item, text=reason, font=FONT_P_BOLD, bg="#ffffff", fg=COLOR_TEXT_DARK).pack(anchor="w")
        tk.Label(item, text=date, font=FONT_SMALL, bg="#ffffff", fg=COLOR_TEXT_MUTED).pack(anchor="w")
        tk.Label(item, text=status_text, font=FONT_SMALL, bg=status_color, fg=COLOR_TEXT_LIGHT, padx=5).pack(side="right")
    
    create_cita_item(card_cita_prog, "Reunión Padres - Prejardín B", "15 Oct 2025 - 3:00 PM", "#28a745", "Confirmada")
    create_cita_item(card_cita_prog, "Citación individual - Acudiente Silva", "18 Oct 2025 - 4:30 PM", "orange", "Pendiente")
    create_cita_item(card_cita_prog, "Entrega Boletines - Caminadores A", "20 Oct 2025 - 2:00 PM", "orange", "Pendiente")

    tk.Button(card_cita_prog, text="Crear nueva citación", bg=COLOR_ACCENT_ADMIN, fg=COLOR_TEXT_LIGHT, font=FONT_P_BOLD, bd=0).pack(fill="x", ipady=5, pady=(15, 0))
    
    return dashboard_frame