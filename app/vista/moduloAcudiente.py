import tkinter as tk
import tkinter.ttk as ttk
from .config import *


def create_sidebar_button_parent(parent, text, icon, module_name, nav_commands, is_active=False):
    bg_color = COLOR_ACCENT_DARK if is_active else COLOR_SIDEBAR_PARENT
    
    btn_frame = tk.Frame(parent, bg=bg_color)
    btn_frame.pack(fill="x", pady=(0, 2))
    
    btn = tk.Button(
        btn_frame, 
        text=f"{icon}  {text}", 
        anchor="w", 
        bd=0, 
        padx=15, 
        pady=12, 
        highlightthickness=0,
        bg=bg_color, 
        fg=COLOR_TEXT_LIGHT,
        font=FONT_P_BOLD,
        command=lambda: nav_commands['show_frame'](module_name) if module_name else None
    )
    btn.pack(fill="x")
    
    return btn


def create_parent_card(parent, title, text, action_text, color, command):
    card = tk.Frame(
        parent, 
        bg="#ffffff", 
        padx=20, 
        pady=20, 
        relief="solid", 
        bd=1, 
        highlightbackground=COLOR_TEST_BORDER, 
        highlightthickness=1
    )
    
    tk.Label(card, text=title, font=FONT_H3, fg=color, bg="#ffffff").pack(anchor="w", pady=(0, 8))
    tk.Label(card, text=text, font=FONT_P, fg=COLOR_TEXT_MUTED, bg="#ffffff", 
             wraplength=280, justify="left").pack(anchor="w", pady=(0, 20))
    
    if action_text == "Descargar":
        btn = ttk.Button(card, text=action_text, style="Pre.TButton", command=command)
    else:
        btn = tk.Button(
            card, 
            text=action_text, 
            bg=color, 
            fg=COLOR_TEXT_LIGHT, 
            font=FONT_P_BOLD, 
            bd=0, 
            relief="flat",
            command=command
        )
    
    btn.pack(anchor="w", ipady=8, ipadx=20)
    return card


def create_parent_dashboard(master, nav_commands):
    dashboard_frame = tk.Frame(master)
    dashboard_frame.grid_columnconfigure(0, weight=0) 
    dashboard_frame.grid_columnconfigure(1, weight=1) 
    dashboard_frame.grid_rowconfigure(0, weight=1)
    
    sidebar = tk.Frame(dashboard_frame, bg=COLOR_SIDEBAR_PARENT, width=240)
    sidebar.grid(row=0, column=0, sticky="nsew")
    sidebar.pack_propagate(False)

    header_sid = tk.Frame(sidebar, bg=COLOR_SIDEBAR_PARENT)
    header_sid.pack(fill="x", pady=(10, 20))
    tk.Label(header_sid, text="Panel Acudiente", bg=COLOR_SIDEBAR_PARENT, 
             fg=COLOR_TEXT_LIGHT, font=FONT_H2).pack(pady=5)
    tk.Label(header_sid, text="Emma Rodríguez", bg=COLOR_SIDEBAR_PARENT, 
             fg=COLOR_TEXT_LIGHT, font=FONT_H3).pack()
    tk.Label(header_sid, text="Consulta de Logros", bg=COLOR_SIDEBAR_PARENT, 
             fg=COLOR_HEADER_PRE, font=FONT_P).pack(pady=(5, 15))

    create_sidebar_button_parent(sidebar, "Mi Dashboard", "🏠", "parent_dashboard", nav_commands, is_active=True)
    
    tk.Label(sidebar, text="CONSULTAS", bg=COLOR_SIDEBAR_PARENT, fg="#cccccc", 
             font=FONT_SMALL_BOLD).pack(fill="x", padx=20, pady=(20, 8), anchor="w")
    create_sidebar_button_parent(sidebar, "Consultar Logros (CRE)", "⭐", "consult_parent", nav_commands)

    footer_sid = tk.Frame(sidebar, bg=COLOR_SIDEBAR_PARENT)
    footer_sid.pack(fill="x", side="bottom", pady=20)
    tk.Frame(footer_sid, height=1, bg="#444").pack(fill="x", pady=(0, 10))
    tk.Button(
        footer_sid, 
        text="❌ Cerrar Sesión", 
        bg=COLOR_SIDEBAR_PARENT, 
        fg="#ff6b6b", 
        font=FONT_P_BOLD, 
        bd=0, 
        highlightthickness=0, 
        command=nav_commands['home']
    ).pack(fill="x", padx=15, pady=5)

    main_content = tk.Frame(dashboard_frame, bg="#f8f9fa")
    main_content.grid(row=0, column=1, sticky="nsew", padx=(10, 20), pady=20)
    main_content.grid_columnconfigure(0, weight=1)
    
    header_content = tk.Frame(main_content, bg="#f8f9fa")
    header_content.pack(fill="x", pady=(0, 25))
    tk.Label(header_content, text="Panel del Acudiente", font=FONT_H1, 
             bg="#f8f9fa", fg=COLOR_TEXT_DARK).pack(side="left")

    student_info = tk.Frame(main_content, bg="#ffffff", padx=25, pady=25, 
                           relief="solid", bd=1, highlightbackground=COLOR_TEST_BORDER)
    student_info.pack(fill="x", pady=(0, 25))
    tk.Label(student_info, text="Estudiante", font=FONT_H2, 
             bg="#ffffff", fg=COLOR_TEXT_DARK).pack(anchor="w")
    info_line = tk.Frame(student_info, bg="#ffffff")
    info_line.pack(fill="x", pady=10)

    cards_container = tk.Frame(main_content, bg="#f8f9fa")
    cards_container.pack(fill="x", pady=(0, 25))
    cards_container.grid_columnconfigure(0, weight=1)
    
    create_parent_card(
        cards_container, 
        "Consultar Logros (CRE)", 
        "Acceda al detalle completo de los logros académicos y psicosociales de Emma en el período actual.", 
        "Abrir Módulo", 
        COLOR_HEADER_PRE, 
        lambda: nav_commands['show_frame']("consult_parent")
    ).pack(fill="x", pady=(0, 15))

    bottom_row = tk.Frame(main_content, bg="#f8f9fa")
    bottom_row.pack(fill="x")
    bottom_row.grid_columnconfigure(0, weight=1)
    bottom_row.grid_columnconfigure(1, weight=1)
    bottom_row.grid_rowconfigure(0, weight=1)

    card_logros = tk.Frame(bottom_row, bg="#ffffff", padx=20, pady=20, 
                          relief="solid", bd=1, highlightbackground=COLOR_TEST_BORDER)
    card_logros.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=10)
    
    tk.Label(card_logros, text="⭐ Logros Recientes", font=FONT_H3, 
             fg=COLOR_TEXT_DARK, bg="#ffffff").pack(anchor="w", pady=(0, 15))
    
    def create_logro_item(parent, category, description, date, color):
        item_frame = tk.Frame(parent, bg="#ffffff")
        item_frame.pack(fill="x", pady=3)
        tk.Label(item_frame, text=f"• {category}", font=FONT_P_BOLD, 
                fg=color, bg="#ffffff").pack(anchor="w")
        tk.Label(item_frame, text=description, font=FONT_P, 
                bg="#ffffff", fg=COLOR_TEXT_DARK).pack(anchor="w")
        tk.Label(item_frame, text=date, font=FONT_SMALL, 
                bg="#ffffff", fg=COLOR_TEXT_MUTED).pack(anchor="w")
    
    create_logro_item(card_logros, "Cognitivo", "Reconocimiento números 1-10", "25 Nov", "#4a90e2")
    create_logro_item(card_logros, "Psicosocial", "Trabajo colaborativo", "23 Nov", "#28a745")
    create_logro_item(card_logros, "Motor", "Coordinación y equilibrio", "20 Nov", COLOR_HEADER_PRE)

    card_events = tk.Frame(bottom_row, bg="#ffffff", padx=20, pady=20, 
                          relief="solid", bd=1, highlightbackground=COLOR_TEST_BORDER)
    card_events.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
    
    tk.Label(card_events, text="📅 Próximos Eventos", font=FONT_H3, 
             fg=COLOR_TEXT_DARK, bg="#ffffff").pack(anchor="w", pady=(0, 15))
    
    def create_event_item(parent, event_name, date):
        item = tk.Frame(parent, bg="#e8f9e8", padx=15, pady=8, relief="solid", bd=1)
        item.pack(fill="x", pady=3)
        tk.Label(item, text=event_name, font=FONT_P, bg="#e8f9e8", 
                fg=COLOR_TEXT_DARK).pack(side="left")
        tk.Label(item, text=date, font=FONT_P_BOLD, bg="#e8f9e8", 
                fg="#28a745").pack(side="right")
    
    create_event_item(card_events, "Entrega Boletines", "29 Nov")
    create_event_item(card_events, "Festival Navideño", "15 Dic")
    create_event_item(card_events, "Clausura del Año", "20 Dic")
    
    return dashboard_frame


def create_consult_parent(master, nav_commands):
    consult_frame = tk.Frame(master, bg="#f8f9fa")
    
    header_frame = tk.Frame(consult_frame, bg=COLOR_HEADER_PRE, height=70)
    header_frame.pack(fill="x")
    header_frame.pack_propagate(False)
    
    tk.Button(
        header_frame, 
        text="← Volver al Dashboard", 
        bg=COLOR_HEADER_PRE, 
        fg=COLOR_TEXT_LIGHT, 
        font=FONT_P_BOLD, 
        bd=0, 
        highlightthickness=0, 
        command=nav_commands.get('parent_home', nav_commands['home'])
    ).pack(side="left", padx=20, pady=15)
    
    tk.Label(
        header_frame, 
        text="Consulta de Logros", 
        bg=COLOR_HEADER_PRE, 
        fg=COLOR_TEXT_LIGHT, 
        font=FONT_H1
    ).pack(side="left", padx=30, pady=15)
    
    content_area = tk.Frame(consult_frame, bg="#ffffff", padx=40, pady=40)
    content_area.pack(fill="both", expand=True, pady=(20, 0))
    
    info_frame = tk.Frame(content_area, bg="#ffffff")
    info_frame.pack(fill="x", pady=(0, 25))
    
    tk.Label(info_frame, text="Estudiante", font=FONT_H2, 
             bg="#ffffff", fg=COLOR_TEXT_DARK).pack(side="left")
    
    tk.Button(
        info_frame, 
        text="📥 Descargar Logros en PDF", 
        bg=COLOR_HEADER_PRE, 
        fg=COLOR_TEXT_LIGHT, 
        font=FONT_P_BOLD, 
        bd=0, 
        relief="flat",
        command=lambda: print("Descargando PDF...")
    ).pack(side="right", padx=(20, 0), ipady=8)
    
    filter_frame = tk.Frame(content_area, bg="#f0f4f8", padx=20, pady=15, relief="solid", bd=1)
    filter_frame.pack(fill="x", pady=(0, 20))
    
    tk.Label(filter_frame, text="📅 Período Académico:", font=FONT_P_BOLD, 
             bg="#f0f4f8").pack(side="left", padx=(10, 5))
    period_combo = ttk.Combobox(filter_frame, values=["Noviembre - Diciembre 2025", "Septiembre - Octubre 2025"], 
                               width=20, state="readonly")
    period_combo.set("Noviembre - Diciembre 2025")
    period_combo.pack(side="left", padx=10)
    tk.Label(filter_frame, text="Mostrando 12 logros", font=FONT_P, 
             bg="#f0f4f8", fg=COLOR_TEXT_MUTED).pack(side="left", padx=20)
    
    tk.Label(content_area, text="⭐ Logros Académicos y Psicosociales", 
             font=FONT_H2, bg="#ffffff", fg=COLOR_TEXT_DARK).pack(anchor="w", pady=(0, 15))
    
    tree_container = tk.Frame(content_area)
    tree_container.pack(fill="both", expand=True)
    
    tree_scroll = ttk.Scrollbar(tree_container)
    tree_scroll.pack(side="right", fill="y")
    
    tree = ttk.Treeview(
        tree_container, 
        columns=("Fecha", "Categoría", "Descripción", "Evaluación"), 
        show='headings',
        yscrollcommand=tree_scroll.set,
        height=12
    )
    tree_scroll.config(command=tree.yview)
    tree.pack(side="left", fill="both", expand=True)
    
    tree.heading("Fecha", text="Fecha")
    tree.heading("Categoría", text="Categoría")
    tree.heading("Descripción", text="Descripción del Logro")
    tree.heading("Evaluación", text="Evaluación")
    
    tree.column("Fecha", width=100)
    tree.column("Categoría", width=150)
    tree.column("Descripción", width=400)
    tree.column("Evaluación", width=120)
    
    return consult_frame
