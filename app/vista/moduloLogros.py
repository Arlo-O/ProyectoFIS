import tkinter as tk
import tkinter.ttk as ttk
from .config import *


def create_category_box(parent, title, subcategories):
    """Crea caja de categoría con header y lista de subcategorías expandible."""
    # Contenedor principal de categoría
    category_container = tk.Frame(parent, bg="#ffffff")
    
    # Header de categoría
    header_frame = tk.Frame(
        category_container,
        bg="#ffffff",
        padx=25,
        pady=20,
        relief="solid",
        bd=2,
        highlightbackground=COLOR_TEST_BORDER,
        highlightthickness=2
    )
    header_frame.pack(fill="x")
    
    tk.Label(
        header_frame,
        text=f"⭐ {title}",
        font=FONT_H2,
        bg="#ffffff",
        fg=COLOR_TEXT_DARK
    ).pack(side="left")
    
    # Contador de subcategorías
    count_label = tk.Label(
        header_frame,
        text=f"({len(subcategories)} subcategorías)",
        bg="#ffffff",
        fg=COLOR_TEXT_MUTED,
        font=FONT_P
    )
    count_label.pack(side="left", padx=(10, 0))
    
    # Botones de acción header
    btn_frame = tk.Frame(header_frame, bg="#ffffff")
    btn_frame.pack(side="right")
    
    ttk.Button(
        btn_frame,
        text="➕ Nueva Subcategoría",
        style="AdminBlue.TButton"
    ).pack(side="right", padx=(5, 0))
    
    ttk.Button(
        btn_frame,
        text="✏️ Editar Categoría",
        style="AdminGreen.TButton"
    ).pack(side="right")
    
    # Lista de subcategorías
    list_frame = tk.Frame(
        category_container,
        bg="#f8f9fa",
        padx=25,
        pady=20,
        relief="solid",
        bd=1
    )
    list_frame.pack(fill="both", expand=True, pady=(0, 20))
    
    # Scrollbar para subcategorías
    list_scroll = ttk.Scrollbar(list_frame)
    list_scroll.pack(side="right", fill="y")
    
    listbox = tk.Listbox(
        list_frame,
        yscrollcommand=list_scroll.set,
        font=FONT_P,
        selectmode=tk.MULTIPLE,
        height=6,
        relief="solid"
    )
    list_scroll.config(command=listbox.yview)
    listbox.pack(side="left", fill="both", expand=True)
    
    # Poblar subcategorías
    for sub in subcategories:
        listbox.insert(tk.END, f"• {sub}")
    
    return category_container


def create_achievements_manager(master, nav_commands):
    """Gestión completa de categorías y logros (GLE) con sidebar profesional."""
    
    achievements_frame = tk.Frame(master)
    achievements_frame.grid_columnconfigure(0, weight=0)  # Sidebar
    achievements_frame.grid_columnconfigure(1, weight=1)  # Contenido
    achievements_frame.grid_rowconfigure(0, weight=1)
    
    # 1. SIDEBAR
    sidebar = tk.Frame(achievements_frame, bg=COLOR_DARK_BG, width=260)
    sidebar.grid(row=0, column=0, sticky="nsew")
    sidebar.pack_propagate(False)
    
    # Header sidebar
    header_sid = tk.Frame(sidebar, bg=COLOR_DARK_BG)
    header_sid.pack(fill="x", pady=(25, 30))
    
    tk.Label(
        header_sid,
        text="⭐ Gestión de Logros (GLE)",
        bg=COLOR_DARK_BG,
        fg=COLOR_TEXT_LIGHT,
        font=FONT_H2
    ).pack()
    
    tk.Label(
        header_sid,
        text="Configuración de Evaluación CRE",
        bg=COLOR_DARK_BG,
        fg=COLOR_HEADER_PRE,
        font=FONT_P
    ).pack(pady=(5, 20))
    
    # Separador
    tk.Frame(sidebar, height=1, bg="#444a57").pack(fill="x", padx=20, pady=(0, 20))
    
    # Función para botones de navegación
    def create_side_nav_button(parent, text, icon, module_name=None, is_active=False):
        btn_frame = tk.Frame(
            parent,
            bg=COLOR_ACCENT_DARK if is_active else COLOR_DARK_BG
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
            bg=COLOR_ACCENT_DARK if is_active else COLOR_DARK_BG,
            fg=COLOR_HEADER_PRE if is_active else COLOR_TEXT_LIGHT,
            font=FONT_P_BOLD,
            relief="flat",
            command=on_click
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
    
    # Navegación activa
    create_side_nav_button(sidebar, "📋 Gestión de Categorías", None, is_active=True)
    create_side_nav_button(sidebar, "📈 Reportes de Logros", "achievements_reports")
    create_side_nav_button(sidebar, "👥 Asignar por Estudiante", "student_achievements")
    
    # Separador footer
    tk.Frame(sidebar, height=1, bg="#444a57").pack(fill="x", pady=25, padx=20)
    
    # Botón volver corregido
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
    main_content = tk.Frame(achievements_frame, bg="#f8f9fa")
    main_content.grid(row=0, column=1, sticky="nsew", padx=(20, 40), pady=30)
    main_content.grid_columnconfigure(0, weight=1)
    
    # Header contenido
    header_content = tk.Frame(main_content, bg="#f8f9fa")
    header_content.pack(fill="x", pady=(0, 30))
    
    tk.Label(
        header_content,
        text="⭐ Gestión de Categorías y Logros (GLE)",
        font=FONT_H1,
        bg="#f8f9fa",
        fg=COLOR_TEXT_DARK
    ).pack(side="left")
    
    tk.Label(
        header_content,
        text="Colegio Pequeño | 28 categorías activas | Período Nov-Dic 2025",
        font=FONT_P,
        bg="#f8f9fa",
        fg=COLOR_TEXT_MUTED
    ).pack(side="right")
    
    # Controles de búsqueda y creación
    controls_frame = tk.Frame(main_content, bg="#f8f9fa")
    controls_frame.pack(fill="x", pady=(0, 30))
    
    # Placeholder de búsqueda mejorado
    search_container = tk.Frame(controls_frame, bg="#ffffff", relief="solid", bd=1)
    search_container.pack(side="left")
    
    search_var = tk.StringVar()
    tk.Entry(
        search_container,
        textvariable=search_var,
        width=40,
        font=FONT_P,
        relief="flat",
        bd=0,
        bg="#f8f9fa"
    ).pack(side="left", padx=20, pady=12, ipady=5)
    
    tk.Label(
        search_container,
        text="🔍 Buscar categoría...",
        bg="#f8f9fa",
        fg=COLOR_TEXT_MUTED,
        font=FONT_P
    ).pack(side="left", padx=(0, 20), pady=14)
    
    # Botón crear categoría
    ttk.Button(
        controls_frame,
        text="➕ Crear Nueva Categoría",
        style="AdminBlue.TButton",
        command=lambda: print("Abrir modal nueva categoría")
    ).pack(side="right", padx=20)
    
    # Grid de categorías (responsive 2 columnas)
    categories_grid = tk.Frame(main_content, bg="#f8f9fa")
    categories_grid.pack(fill="both", expand=True)
    
    categories_grid.grid_columnconfigure(0, weight=1)
    categories_grid.grid_columnconfigure(1, weight=1)
    categories_grid.grid_rowconfigure(0, weight=1)
    categories_grid.grid_rowconfigure(1, weight=1)
    
    # Datos de categorías realistas
    categories_data = [
        {
            "title": "Desarrollo del Lenguaje (12 Subcategorías)",
            "subs": [
                "Identificación letras A-J", "Reconocimiento números 1-10",
                "Vocabulario básico (20 palabras)", "Comunicación verbal simple",
                "Secuencias simples", "Rimas y canciones"
            ]
        },
        {
            "title": "Desarrollo Físico (8 Subcategorías)",
            "subs": [
                "Motricidad fina (pinza)", "Motricidad gruesa (equilibrio)",
                "Coordinación ojo-mano", "Corte con tijeras seguras",
                "Lanzar y atrapar", "Dibujo con crayones"
            ]
        },
        {
            "title": "Desarrollo Socioemocional (10 Subcategorías)",
            "subs": [
                "Interacción con pares", "Regulación emocional",
                "Compartir juguetes", "Seguir instrucciones grupales",
                "Expresar emociones", "Trabajo colaborativo"
            ]
        },
        {
            "title": "Desarrollo Cognitivo (9 Subcategorías)",
            "subs": [
                "Clasificación por color", "Series simples",
                "Concepto grande-pequeño", "Formas geométricas básicas",
                "Secuencias temporales", "Comparaciones"
            ]
        }
    ]
    
    # Crear categorías en grid 2x2
    for i, cat_data in enumerate(categories_data):
        row = i // 2
        col = i % 2
        category_box = create_category_box(categories_grid, cat_data["title"], cat_data["subs"])
        category_box.grid(row=row, column=col, sticky="nsew", padx=20, pady=20)
    
    return achievements_frame
