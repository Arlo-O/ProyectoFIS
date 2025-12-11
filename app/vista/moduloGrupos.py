import tkinter as tk
import tkinter.ttk as ttk
from .config import *


def create_groups_manager(master, nav_commands):
    """Gestión completa de grupos académicos con sidebar y tarjetas interactivas."""
    
    groups_frame = tk.Frame(master)
    groups_frame.grid_columnconfigure(0, weight=0)
    groups_frame.grid_columnconfigure(1, weight=1)
    groups_frame.grid_rowconfigure(0, weight=1)
    
    # 1. SIDEBAR
    sidebar = tk.Frame(groups_frame, bg=COLOR_SIDEBAR_ADMIN, width=260)
    sidebar.grid(row=0, column=0, sticky="nsew")
    sidebar.pack_propagate(False)
    
    # Header sidebar
    header_sid = tk.Frame(sidebar, bg=COLOR_SIDEBAR_ADMIN)
    header_sid.pack(fill="x", pady=(20, 25))
    
    tk.Label(
        header_sid,
        text="👥 Gestión de Grupos",
        bg=COLOR_SIDEBAR_ADMIN,
        fg=COLOR_TEXT_LIGHT,
        font=FONT_H2
    ).pack()
    
    tk.Label(
        header_sid,
        text="Administrador de Grupos",
        bg=COLOR_SIDEBAR_ADMIN,
        fg=COLOR_HEADER_PRE,
        font=FONT_P
    ).pack(pady=(5, 20))
    
    # Separador
    tk.Frame(sidebar, height=1, bg="#444").pack(fill="x", padx=20, pady=(0, 20))
    
    # Función para botones de navegación
    def create_nav_btn(parent, text, icon, module_name=None, is_active=False):
        btn_frame = tk.Frame(
            parent,
            bg=COLOR_ACCENT_DARK if is_active else COLOR_SIDEBAR_ADMIN
        )
        btn_frame.pack(fill="x", pady=(0, 8), padx=20)
        
        def on_click():
            if module_name:
                nav_commands['show_frame'](module_name)
        
        btn = tk.Button(
            btn_frame,
            text=f"{icon}  {text}",
            anchor="w",
            bd=0,
            padx=25,
            pady=15,
            highlightthickness=0,
            bg=COLOR_ACCENT_DARK if is_active else COLOR_SIDEBAR_ADMIN,
            fg=COLOR_TEXT_LIGHT,
            font=FONT_P_BOLD,
            relief="flat",
            command=on_click
        )
        btn.pack(fill="x")
        
        # Hover effects
        def on_enter(e):
            btn.config(bg=COLOR_ACCENT_DARK)
        def on_leave(e):
            btn.config(bg=COLOR_ACCENT_DARK if is_active else COLOR_SIDEBAR_ADMIN)
        
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        
        return btn
    
    # Navegación activa
    create_nav_btn(sidebar, "📋 Lista de Grupos", None, is_active=True)
    create_nav_btn(sidebar, "👨‍🎓 Asignar Estudiantes", "assign_students")
    create_nav_btn(sidebar, "📊 Estadísticas", "group_stats")
    
    # Separador footer
    tk.Frame(sidebar, height=1, bg="#444").pack(fill="x", pady=20, padx=20)
    
    # Botón volver (corregido)
    tk.Button(
        sidebar,
        text="🏠 Volver al Dashboard",
        bg=COLOR_ACCENT_ADMIN,
        fg=COLOR_TEXT_LIGHT,
        font=FONT_P_BOLD,
        bd=0,
        highlightthickness=0,
        relief="flat",
        command=nav_commands['director_home']
    ).pack(fill="x", pady=20, padx=20)
    
    # 2. CONTENIDO PRINCIPAL
    main_content = tk.Frame(groups_frame, bg="#f8f9fa")
    main_content.grid(row=0, column=1, sticky="nsew", padx=(20, 40), pady=30)
    main_content.grid_columnconfigure(0, weight=1)
    
    # Header contenido
    header_content = tk.Frame(main_content, bg="#f8f9fa")
    header_content.pack(fill="x", pady=(0, 30))
    
    tk.Label(
        header_content,
        text="👥 Gestión de Grupos Académicos",
        font=FONT_H1,
        bg="#f8f9fa",
        fg=COLOR_TEXT_DARK
    ).pack(side="left")
    
    tk.Label(
        header_content,
        text="Colegio Pequeño - 12 grupos activos | Período Nov-Dic 2025",
        font=FONT_P,
        bg="#f8f9fa",
        fg=COLOR_TEXT_MUTED
    ).pack(side="right")
    
    # Barra de búsqueda y controles
    search_frame = tk.Frame(main_content, bg="#f8f9fa")
    search_frame.pack(fill="x", pady=(0, 30))
    
    search_var = tk.StringVar()
    tk.Label(
        search_frame,
        text="🔍 Buscar grupo:",
        bg="#f8f9fa",
        font=FONT_P_BOLD
    ).pack(side="left", padx=(0, 10))
    
    tk.Entry(
        search_frame,
        textvariable=search_var,
        width=35,
        font=FONT_P,
        relief="solid",
        bd=1
    ).pack(side="left", padx=(0, 20))
    
    tk.Label(
        search_frame,
        text="🎓 Grado:",
        bg="#f8f9fa",
        font=FONT_P_BOLD
    ).pack(side="left", padx=(0, 5))
    
    grade_combo = ttk.Combobox(
        search_frame,
        values=["Todos", "Preescolar", "Transición", "Primero"],
        width=15,
        state="readonly"
    )
    grade_combo.set("Todos")
    grade_combo.pack(side="left", padx=(0, 20))
    
    # Botón crear grupo
    tk.Button(
        search_frame,
        text="➕ Crear Nuevo Grupo",
        bg=COLOR_ACCENT_ADMIN,
        fg=COLOR_TEXT_LIGHT,
        font=FONT_P_BOLD,
        bd=0,
        relief="flat",
        padx=30,
        pady=12,
        command=lambda: print("Abrir modal crear grupo")
    ).pack(side="right")
    
    # Grid de grupos (responsive 3 columnas)
    groups_grid = tk.Frame(main_content, bg="#f8f9fa")
    groups_grid.pack(fill="both", expand=True)
    
    # Configurar grid responsive
    for i in range(3):
        groups_grid.grid_columnconfigure(i, weight=1)
    groups_grid.grid_rowconfigure(0, weight=1)
    groups_grid.grid_rowconfigure(1, weight=1)
    
    # Función para crear tarjeta de grupo
    def create_group_card(parent, title, professor, age_range, capacity, color, row, col):
        card = tk.Frame(
            parent,
            bg="#ffffff",
            padx=25,
            pady=25,
            relief="solid",
            bd=2,
            highlightbackground=COLOR_TEST_BORDER,
            highlightthickness=2
        )
        card.grid(row=row, column=col, sticky="nsew", padx=15, pady=15)
        
        # Header con título y capacidad
        header_frame = tk.Frame(card, bg="#ffffff")
        header_frame.pack(fill="x")
        
        tk.Label(
            header_frame,
            text=f"👨‍🎓 {title}",
            font=FONT_H2,
            bg="#ffffff",
            fg=COLOR_TEXT_DARK
        ).pack(side="left")
        
        capacity_label = tk.Label(
            header_frame,
            text=capacity,
            font=FONT_H3,
            bg=color,
            fg=COLOR_TEXT_LIGHT,
            padx=20,
            pady=8,
            relief="solid",
            bd=1
        )
        capacity_label.pack(side="right")
        
        # Detalles del grupo
        details_frame = tk.Frame(card, bg="#ffffff")
        details_frame.pack(fill="x", pady=(15, 0))
        
        tk.Label(
            details_frame,
            text=f"👶 Rango de edad: {age_range}",
            font=FONT_P,
            bg="#ffffff",
            fg=COLOR_TEXT_MUTED
        ).pack(anchor="w")
        
        tk.Label(
            details_frame,
            text=f"👩‍🏫 Profesor: {professor}",
            font=FONT_P,
            bg="#ffffff",
            fg=COLOR_HEADER_PRE
        ).pack(anchor="w")
        
        tk.Label(
            details_frame,
            text="📅 Horario: Lunes a Viernes 7:00-12:00",
            font=FONT_P,
            bg="#ffffff",
            fg=COLOR_TEXT_MUTED
        ).pack(anchor="w")
        
        # Barra de progreso simulada
        progress_frame = tk.Frame(details_frame, bg="#f0f0f0", height=8, relief="solid", bd=1)
        progress_frame.pack(fill="x", pady=(15, 20))
        progress_frame.pack_propagate(False)
        
        progress_bar = tk.Frame(progress_frame, bg=color, height=6, relief="solid", bd=1)
        progress_bar.pack(fill="x", padx=2, pady=1)
        progress_bar.place(width=240, relx=0.8)  # 80% lleno
        
        # Botones de acción
        btn_frame = tk.Frame(card, bg="#ffffff")
        btn_frame.pack(fill="x")
        
        ttk.Button(
            btn_frame,
            text="✏️ Editar Grupo",
            style="AdminBlue.TButton"
        ).pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        ttk.Button(
            btn_frame,
            text="👥 Asignar Estudiantes",
            style="Pre.TButton"
        ).pack(side="left", fill="x", expand=True)
        
        ttk.Button(
            btn_frame,
            text="📊 Ver Estadísticas",
            style="AdminGreen.TButton"
        ).pack(side="left", fill="x")
    
    # Crear 6 grupos de ejemplo (grid 3x2)
    groups_data = [
        ("Párvulos A", "María García", "3-4 años", "10/12 cupos", "#e74c3c"),
        ("Párvulos B", "Laura Pérez", "3-4 años", "8/12 cupos", "#f39c12"),
        ("Caminadores A", "Carlos Martínez", "2-3 años", "9/10 cupos", "#27ae60"),
        ("Caminadores B", "Ana Rodríguez", "2-3 años", "7/10 cupos", "#3498db"),
        ("Transición A", "Juan López", "4-5 años", "11/14 cupos", "#9b59b6"),
        ("Transición B", "Sofía Torres", "4-5 años", "10/14 cupos", "#1abc9c")
    ]
    
    for i, (title, professor, age_range, capacity, color) in enumerate(groups_data):
        row = i // 3
        col = i % 3
        create_group_card(groups_grid, title, professor, age_range, capacity, color, row, col)
    
    return groups_frame
