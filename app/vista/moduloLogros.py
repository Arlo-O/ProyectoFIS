import tkinter as tk
import tkinter.ttk as ttk
from config import *
from session_manager import get_dashboard_command

def create_category_box(parent, title, subcategories):
    box = tk.Frame(parent, bg="#ffffff", padx=15, pady=15, relief="solid", bd=1, highlightbackground=COLOR_TEST_BORDER, highlightthickness=1)
    
    tk.Label(box, text="⭐ " + title, font=FONT_H3, bg="#ffffff", fg=COLOR_TEXT_DARK).pack(side="left", anchor="w")
    
    btn_frame = tk.Frame(box, bg="#ffffff")
    btn_frame.pack(side="right", fill="x")
    
    ttk.Button(btn_frame, text="➕ Subcategoría", style="TButton", width=12).pack(side="right", padx=(5, 0))
    ttk.Button(btn_frame, text="✏️ Editar", style="TButton", width=8).pack(side="right")
    
    list_frame = tk.Frame(parent, bg="#ffffff", padx=15, pady=10, relief="solid", bd=1, highlightbackground=COLOR_TEST_BORDER, highlightthickness=1)
    
    for sub in subcategories:
        sub_item = tk.Frame(list_frame, bg="#f9f9f9", padx=10, pady=5, bd=1, relief="flat")
        sub_item.pack(fill="x", pady=2)
        tk.Label(sub_item, text=sub, bg="#f9f9f9", font=FONT_P).pack(side="left", anchor="w")
        ttk.Button(sub_item, text="X Eliminar", style="TButton", width=8).pack(side="right")
        
    return box, list_frame

def create_achievements_manager(master, nav_commands):
    
    achievements_frame = tk.Frame(master, bg="#f5f7fa")
    achievements_frame.grid_columnconfigure(0, weight=0) # Sidebar
    achievements_frame.grid_columnconfigure(1, weight=1) # Contenido principal
    achievements_frame.grid_rowconfigure(0, weight=1)

    sidebar = tk.Frame(achievements_frame, bg=COLOR_DARK_BG, width=220)
    sidebar.grid(row=0, column=0, sticky="nsew")
    sidebar.pack_propagate(False)

    tk.Label(sidebar, text="Gestión de Logros", bg=COLOR_DARK_BG, fg=COLOR_TEXT_LIGHT, font=FONT_H2, pady=15).pack(fill="x")
    tk.Label(sidebar, text="Administración", bg=COLOR_DARK_BG, fg=COLOR_HEADER_PRE, font=FONT_P_BOLD).pack(fill="x", padx=10, pady=(5, 0), anchor="w")
    tk.Frame(sidebar, height=1, bg="#444a57").pack(fill="x", pady=10, padx=10)
    def create_side_nav_button(parent, text, icon, is_active=False):
        btn_frame = tk.Frame(parent, bg=COLOR_ACCENT_DARK if is_active else COLOR_DARK_BG)
        btn = tk.Button(btn_frame, text=f"{icon}   {text}", anchor="w", bd=0, padx=10, pady=8, highlightthickness=0,
                        bg=COLOR_ACCENT_DARK if is_active else COLOR_DARK_BG, 
                        fg=COLOR_HEADER_PRE if is_active else COLOR_TEXT_LIGHT,
                        font=FONT_P_BOLD)
        btn.pack(fill="x")
        btn_frame.pack(fill="x", pady=(0, 2))
        return btn

    create_side_nav_button(sidebar, "Gestión de Categorías", "📋", is_active=True)
    create_side_nav_button(sidebar, "Reportes de Logros", "📈")

    tk.Frame(sidebar, height=1, bg="#444a57").pack(fill="x", pady=10, padx=10, side="bottom")
    tk.Button(sidebar, text="← Volver al Dashboard", bg=COLOR_DARK_BG, fg="#ff5555", font=FONT_P_BOLD, bd=0, 
              highlightthickness=0, command=lambda: get_dashboard_command(nav_commands)()).pack(fill="x", side="bottom", pady=10, padx=10)


    main_content = tk.Frame(achievements_frame, bg="#f5f7fa")
    main_content.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
    
    # Header del contenido
    header_content = tk.Frame(main_content, bg="#f5f7fa")
    header_content.pack(fill="x")
    
    tk.Label(header_content, text="Gestión de Categorías y Logros (GLE)", font=FONT_H1, bg="#f5f7fa", fg=COLOR_TEXT_DARK).pack(side="left", anchor="w")
    tk.Label(header_content, text="Colegio Pequeño - Configuración de Evaluación", font=FONT_P, bg="#f5f7fa", fg=COLOR_TEXT_MUTED).pack(side="right", anchor="e")

    # Búsqueda y Creación
    controls_frame = tk.Frame(main_content, bg="#f5f7fa", pady=15)
    controls_frame.pack(fill="x")
    
    ttk.Entry(controls_frame, width=30).pack(side="left", ipady=5)
    tk.Label(controls_frame, text="🔍 Buscar categoría...", bg="#f5f7fa", fg=COLOR_TEXT_MUTED).place(x=5, y=10)
    
    ttk.Button(controls_frame, text="➕ Crear Nueva Categoría", style="AdminGreen.TButton").pack(side="right")
    
    # --- Grid de Categorías ---
    categories_grid = tk.Frame(main_content, bg="#f5f7fa")
    categories_grid.pack(fill="both", expand=True, pady=10)
    
    categories_grid.grid_columnconfigure(0, weight=1)
    categories_grid.grid_columnconfigure(1, weight=1)

    # Datos simulados
    cat1_subs = ["Identificación de letras y números", "Uso de vocabulario básico", "Comunicación verbal"]
    cat2_subs = ["Motricidad fina (pinza)", "Motricidad gruesa (equilibrio)", "Coordinación ojo-mano"]

    # Fila 1
    box1, list1 = create_category_box(categories_grid, "Desarrollo del Lenguaje (12 Subcategorías)", cat1_subs)
    box1.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 0))
    list1.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
    
    box2, list2 = create_category_box(categories_grid, "Desarrollo Físico (8 Subcategorías)", cat2_subs)
    box2.grid(row=0, column=1, sticky="ew", padx=10, pady=(10, 0))
    list2.grid(row=1, column=1, sticky="nsew", padx=10, pady=(0, 10))
    
    # Fila 2 (ejemplo)
    box3, list3 = create_category_box(categories_grid, "Desarrollo Socioemocional (10 Subcategorías)", ["Interacción con pares", "Regulación emocional"])
    box3.grid(row=2, column=0, sticky="ew", padx=10, pady=(10, 0))
    list3.grid(row=3, column=0, sticky="nsew", padx=10, pady=(0, 10))

    return achievements_frame