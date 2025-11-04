# Archivo: parent_module.py

import tkinter as tk
import tkinter.ttk as ttk
from config import *
from session_manager import get_dashboard_command

# --- FUNCIÓN AUXILIAR DE WIDGETS ---
def create_sidebar_button_parent(parent, text, icon, module_name, nav_commands, is_active=False):
    """Crea un botón de navegación lateral para el acudiente."""
    bg_color = COLOR_ACCENT_DARK if is_active else COLOR_SIDEBAR_PARENT
    active_color = COLOR_ACCENT_DARK
    
    btn_frame = tk.Frame(parent, bg=bg_color)
    
    btn = tk.Button(btn_frame, text=f"{icon}   {text}", anchor="w", bd=0, padx=10, pady=8, highlightthickness=0,
                    bg=bg_color, 
                    fg=COLOR_TEXT_LIGHT if is_active else COLOR_TEXT_LIGHT,
                    font=FONT_P_BOLD,
                    command=lambda: nav_commands['show_frame'](module_name) if module_name else None)
    btn.pack(fill="x")
    btn_frame.pack(fill="x", pady=(0, 2))
    
    return btn

def create_parent_card(parent, title, text, action_text, color, command):
    """Crea una tarjeta de módulo en el dashboard del acudiente."""
    card = tk.Frame(parent, bg="#ffffff", padx=15, pady=15, relief="solid", bd=1, highlightbackground=COLOR_TEST_BORDER, highlightthickness=1)
    
    tk.Label(card, text=title, font=FONT_H3, fg=color, bg="#ffffff").pack(anchor="w", pady=(0, 5))
    tk.Label(card, text=text, font=FONT_P, fg=COLOR_TEXT_MUTED, bg="#ffffff", wraplength=250, justify="left").pack(anchor="w", pady=(0, 15))
    
    if action_text == "Descargar":
        btn = ttk.Button(card, text=action_text, style="Pre.TButton", command=command)
    else:
        btn = tk.Button(card, text=action_text, bg=color, fg=COLOR_TEXT_LIGHT, font=FONT_P_BOLD, bd=0, command=command)
        
    btn.pack(anchor="w", ipady=5)
    
    return card

# ======================================================================
# --- DASHBOARD ACUDIENTE ---
# ======================================================================
def create_parent_dashboard(master, nav_commands):
    """Crea la interfaz del Panel del Acudiente."""
    
    dashboard_frame = tk.Frame(master)
    dashboard_frame.grid_columnconfigure(0, weight=0) 
    dashboard_frame.grid_columnconfigure(1, weight=1) 
    dashboard_frame.grid_rowconfigure(0, weight=1)
    
    # 1. BARRA LATERAL (SIDEBAR)
    sidebar = tk.Frame(dashboard_frame, bg=COLOR_SIDEBAR_PARENT, width=220)
    sidebar.grid(row=0, column=0, sticky="nsew")
    sidebar.pack_propagate(False)

    # Header de la Sidebar
    tk.Label(sidebar, text="Panel Acudiente", bg=COLOR_SIDEBAR_PARENT, fg=COLOR_TEXT_LIGHT, font=FONT_H1).pack(fill="x", ipady=10)
    tk.Label(sidebar, text="Emma Rodríguez", bg=COLOR_SIDEBAR_PARENT, fg=COLOR_TEXT_LIGHT, font=FONT_H3).pack(fill="x")
    tk.Label(sidebar, text="Consulta de Logros", bg=COLOR_SIDEBAR_PARENT, fg=COLOR_HEADER_PRE, font=FONT_P).pack(fill="x", pady=(0, 10))

    # Nav Buttons
    create_sidebar_button_parent(sidebar, "Mi Dashboard", "🏠", "parent_dashboard", nav_commands, is_active=True)
    
    tk.Label(sidebar, text="CONSULTAS", bg=COLOR_SIDEBAR_PARENT, fg="#f5f5f5", font=FONT_SMALL).pack(fill="x", padx=10, pady=(15, 5), anchor="w")
    create_sidebar_button_parent(sidebar, "Consultar Logros (CRE)", "⭐", "consult_parent", nav_commands)
    create_sidebar_button_parent(sidebar, "Descargar Boletines", "📄", "download_bulletins_parent", nav_commands)

    tk.Label(sidebar, text="INFORMACIÓN", bg=COLOR_SIDEBAR_PARENT, fg="#f5f5f5", font=FONT_SMALL).pack(fill="x", padx=10, pady=(15, 5), anchor="w")
    create_sidebar_button_parent(sidebar, "Horarios y Eventos", "📅", "events_parent", nav_commands)
    create_sidebar_button_parent(sidebar, "Comunicaciones", "📧", "comms_parent", nav_commands)
    create_sidebar_button_parent(sidebar, "Asistencia", "✔️", "attendance_parent", nav_commands)
    
    # Footer (Cerrar Sesión)
    tk.Frame(sidebar, height=1, bg="#a0a0a0").pack(fill="x", pady=10, padx=10, side="bottom")
    tk.Button(sidebar, text="❌ Cerrar Sesión", bg=COLOR_SIDEBAR_PARENT, fg="#ff5555", font=FONT_P_BOLD, bd=0, 
              highlightthickness=0, command=nav_commands['home']).pack(fill="x", side="bottom", pady=10, padx=10)


    # 2. CONTENIDO PRINCIPAL
    main_content = tk.Frame(dashboard_frame, bg="#f5f7fa")
    main_content.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
    main_content.grid_columnconfigure(0, weight=1)
    
    # Header del contenido
    header_content = tk.Frame(main_content, bg="#f5f7fa")
    header_content.pack(fill="x", pady=(0, 20))
    
    tk.Label(header_content, text="Panel del Acudiente - Emma Rodríguez", font=FONT_H1, bg="#f5f7fa", fg=COLOR_TEXT_DARK).pack(side="left", anchor="w")
    tk.Label(header_content, text="Periodo Actual: Noviembre - Diciembre 2024", font=FONT_P, bg="#f5f7fa", fg=COLOR_TEXT_MUTED).pack(side="right", anchor="e")

    # Info Estudiante
    student_info = tk.Frame(main_content, bg="#ffffff", padx=15, pady=15, relief="solid", bd=1, highlightbackground=COLOR_TEST_BORDER, highlightthickness=1)
    student_info.pack(fill="x", pady=(0, 20))
    tk.Label(student_info, text="Emma Rodríguez González", font=FONT_H3, bg="#ffffff", fg=COLOR_TEXT_DARK).pack(anchor="w")
    tk.Label(student_info, text="Párvulos A - 4 años | Prof. Ana María Rodríguez", font=FONT_P, bg="#ffffff", fg=COLOR_TEXT_MUTED).pack(anchor="w")
    tk.Label(student_info, text="Asistencia: 98% | Rendimiento: Excelente", font=FONT_P_BOLD, bg="#ffffff", fg="#28a745").pack(anchor="w", pady=(5, 0))

    # --- Tarjetas de Módulos (Mid Row) ---
    management_row = tk.Frame(main_content, bg="#f5f7fa")
    management_row.pack(fill="x", pady=(0, 20))
    management_row.grid_columnconfigure(0, weight=1)
    management_row.grid_columnconfigure(1, weight=1)
    management_row.grid_columnconfigure(2, weight=1)
    
    # Card 1: Consultar Logros
    create_parent_card(management_row, "Consultar Logros (CRE)", 
                       "Ver progreso académico y psicosocial de Emma.", "Abrir Módulo", 
                       COLOR_HEADER_PRE, lambda: nav_commands['show_frame']("consult_parent")).grid(row=0, column=0, sticky="nsew", padx=10)
    
    # Card 2: Boletines PDF
    create_parent_card(management_row, "Boletines PDF", 
                       "Descargar boletines de períodos anteriores.", "Descargar", 
                       COLOR_HEADER_PRE, lambda: nav_commands['show_frame']("generate_reports")).grid(row=0, column=1, sticky="nsew", padx=10)
    
    # Card 3: Comunicaciones
    card_comms = create_parent_card(management_row, "Comunicaciones", 
                       "Mensajes y citaciones del colegio.", "Ver", 
                       COLOR_HEADER_PRE, lambda: nav_commands['show_frame']("student_observer"))
    card_comms.grid(row=0, column=2, sticky="nsew", padx=10)
    tk.Label(card_comms, text="2 nuevos", bg="#ffffff", fg="red", font=FONT_SMALL).place(relx=0.9, rely=0.1, anchor="ne")

    # --- Logros Recientes y Eventos (Bottom Row) ---
    bottom_row = tk.Frame(main_content, bg="#f5f7fa")
    bottom_row.pack(fill="x", pady=(20, 0))
    bottom_row.grid_columnconfigure(0, weight=1)
    bottom_row.grid_columnconfigure(1, weight=1)

    # Card 4: Logros Recientes
    card_logros = tk.Frame(bottom_row, bg="#ffffff", padx=15, pady=15, relief="solid", bd=1, highlightbackground=COLOR_TEST_BORDER, highlightthickness=1)
    card_logros.grid(row=0, column=0, sticky="nsew", padx=10)
    tk.Label(card_logros, text="Logros Recientes", font=FONT_H3, fg=COLOR_TEXT_DARK, bg="#ffffff").pack(anchor="w", pady=(0, 10))
    
    # Lista simulada
    def create_logro_item(parent, category, description, date, color):
        item = tk.Frame(parent, bg="#ffffff", pady=5)
        item.pack(fill="x")
        tk.Label(item, text=f"• Logro {category}", font=FONT_P_BOLD, fg=color, bg="#ffffff").pack(anchor="w")
        tk.Label(item, text=description, font=FONT_P, bg="#ffffff", fg=COLOR_TEXT_DARK).pack(anchor="w")
        tk.Label(item, text=date, font=FONT_SMALL, bg="#ffffff", fg=COLOR_TEXT_MUTED).pack(anchor="w")
    
    create_logro_item(card_logros, "Cognitivo", "Reconocimiento números 1 - 10", "25 Nov", "#4a90e2")
    create_logro_item(card_logros, "Psicosocial", "Trabajo colaborativo", "23 Nov", "#28a745")
    create_logro_item(card_logros, "Desarrollo Motor", "Coordinación y equilibrio", "20 Nov", COLOR_HEADER_PRE)
    
    # Card 5: Próximos Eventos
    card_events = tk.Frame(bottom_row, bg="#ffffff", padx=15, pady=15, relief="solid", bd=1, highlightbackground=COLOR_TEST_BORDER, highlightthickness=1)
    card_events.grid(row=0, column=1, sticky="nsew", padx=10)
    tk.Label(card_events, text="Próximos Eventos", font=FONT_H3, fg=COLOR_TEXT_DARK, bg="#ffffff").pack(anchor="w", pady=(0, 10))
    
    def create_event_item(parent, event_name, date):
        item = tk.Frame(parent, bg="#e8f9e8", padx=10, pady=5)
        item.pack(fill="x", pady=2)
        tk.Label(item, text=event_name, font=FONT_P, bg="#e8f9e8", fg=COLOR_TEXT_DARK).pack(side="left", anchor="w")
        tk.Label(item, text=date, font=FONT_P_BOLD, bg="#e8f9e8", fg="#28a745").pack(side="right", anchor="e")

    create_event_item(card_events, "Entrega Boletines", "29 Nov")
    create_event_item(card_events, "Festival Navideño", "15 Dic")
    create_event_item(card_events, "Clausura del Año", "20 Dic")
    
    return dashboard_frame

# ======================================================================
# --- SUBMÓDULO: CONSULTA DE LOGROS (CRE) ---
# ======================================================================

def create_consult_parent(master, nav_commands):
    """Crea la interfaz de Consulta de Logros del Acudiente."""
    
    consult_frame = tk.Frame(master, bg="#f5f7fa")
    
    # 1. HEADER FIJO
    header_frame = tk.Frame(consult_frame, bg=COLOR_HEADER_PRE, height=50)
    header_frame.pack(fill="x", side="top")
    header_frame.pack_propagate(False)

    # Evaluar el comando al hacer click para que tome el rol actual
    tk.Button(header_frame, text="← Volver al Dashboard", bg=COLOR_HEADER_PRE, fg=COLOR_TEXT_LIGHT, 
              font=FONT_P_BOLD, bd=0, highlightthickness=0, 
              command=lambda: get_dashboard_command(nav_commands)()).pack(side="left", padx=20)

    tk.Label(header_frame, text="Panel de Consulta de Acudiente (CRE) - Caso de Uso 33", 
             bg=COLOR_HEADER_PRE, fg=COLOR_TEXT_LIGHT, font=FONT_H1).pack(side="left", padx=50)
    
    # 2. CONTENIDO PRINCIPAL
    content_area = tk.Frame(consult_frame, bg="#ffffff", padx=30, pady=30)
    content_area.pack(fill="both", expand=True)

    # Info Estudiante y Botón Descargar
    info_frame = tk.Frame(content_area, bg="#ffffff")
    info_frame.pack(fill="x", pady=(0, 20))
    
    tk.Label(info_frame, text="Emma Rodríguez González", font=FONT_H3, bg="#ffffff", fg=COLOR_TEXT_DARK).pack(side="left", anchor="w")
    tk.Button(info_frame, text="Descargar Logros Académicos en PDF", bg=COLOR_HEADER_PRE, fg=COLOR_TEXT_LIGHT, font=FONT_P_BOLD, bd=0).pack(side="right", ipady=5)
    tk.Label(info_frame, text="Párvulos A - 4 años | Prof. Ana María Rodríguez", font=FONT_P, bg="#ffffff", fg=COLOR_TEXT_MUTED).pack(anchor="w", padx=10, side="left")
    tk.Label(info_frame, text="Asistencia: 98% | Rendimiento: Excelente", font=FONT_P_BOLD, bg="#ffffff", fg="#28a745").pack(anchor="w", padx=10, side="left")
    
    # Filtro de Período
    filter_frame = tk.Frame(content_area, bg="#ffffff")
    filter_frame.pack(fill="x", pady=(0, 10))
    tk.Label(filter_frame, text="Periodo Académico:", bg="#ffffff", font=FONT_P_BOLD).pack(side="left", padx=(0, 5))
    ttk.Combobox(filter_frame, values=["Noviembre - Diciembre 2024"], width=20).pack(side="left", padx=10)
    tk.Label(filter_frame, text="Mostrando 7 logros del período seleccionado", bg="#ffffff", fg=COLOR_TEXT_MUTED, font=FONT_SMALL).pack(side="left", padx=20)

    # Tabla de Logros (Simulación)
    tk.Label(content_area, text="⭐ Logros Académicos | Noviembre | Diciembre 2024", font=FONT_H3, bg="#ffffff", fg=COLOR_TEXT_DARK).pack(anchor="w", pady=(10, 5))
    
    # Simulación de la tabla de logros con Treeview
    tree_frame = tk.Frame(content_area)
    tree_frame.pack(fill="both", expand=True, pady=(0, 10))

    tree = ttk.Treeview(tree_frame, columns=("c1", "c2", "c3", "c4"), show='headings')
    
    # Definición de encabezados
    tree.heading("c1", text="Fecha")
    tree.heading("c2", text="Categoría")
    tree.heading("c3", text="Descripción del Logro")
    tree.heading("c4", text="Evaluación")
    
    # Insertar filas de ejemplo
    logros = [
        ("24/11/2024", "Desarrollo Cognitivo", "Reconoce y recuerda secuencias de números del 1 al 10", "Excelente"),
        ("21/11/2024", "Desarrollo Cognitivo", "Mantiene concentración en actividades por 15 minutos", "Bueno"),
        ("17/11/2024", "Desarrollo Psicomotor", "Corre, salta y mantiene equilibrio en un pie", "Excelente"),
    ]
    
    for fecha, cat, desc, eval_text in logros:
        tree.insert("", "end", values=(fecha, cat, desc, eval_text))

    tree.pack(fill="both", expand=True)
    
    return consult_frame