import tkinter as tk
import tkinter.ttk as ttk
from config import *


def create_citation_generator(master, nav_commands):
    """Generador de Citaciones para administradores."""
    
    citation_frame = tk.Frame(master, bg="#f8f9fa")
    citation_frame.grid(row=0, column=0, sticky="nsew")
    
    # Header
    header_frame = tk.Frame(citation_frame, bg=COLOR_ACCENT_ADMIN, height=70)
    header_frame.pack(fill="x")
    header_frame.pack_propagate(False)
    
    tk.Button(
        header_frame,
        text="← Volver al Dashboard",
        bg=COLOR_ACCENT_ADMIN,
        fg=COLOR_TEXT_LIGHT,
        font=FONT_P_BOLD,
        bd=0,
        highlightthickness=0,
        relief="flat",
        command=lambda: nav_commands.get('admin_home', lambda: None)()
    ).pack(side="left", padx=25, pady=20)
    
    tk.Label(
        header_frame,
        text="📋 Generación de Citación (GCR)",
        bg=COLOR_ACCENT_ADMIN,
        fg=COLOR_TEXT_LIGHT,
        font=FONT_H1
    ).pack(side="left", padx=30, pady=20)
    
    # Contenido principal (2 columnas)
    content_area = tk.Frame(citation_frame, bg="#ffffff", padx=40, pady=40)
    content_area.pack(fill="both", expand=True, pady=20)
    content_area.grid_columnconfigure(0, weight=1)
    content_area.grid_columnconfigure(1, weight=1)
    content_area.grid_rowconfigure(0, weight=1)
    
    # Columna 1: Campos de la Citación
    col1 = tk.LabelFrame(
        content_area,
        text="📝 Campos Obligatorios de la Citación",
        bg="#ffffff",
        fg=COLOR_ACCENT_ADMIN,
        font=FONT_H2,
        padx=25,
        pady=25,
        relief="solid",
        bd=2,
        highlightbackground=COLOR_TEST_BORDER
    )
    col1.grid(row=0, column=0, sticky="nsew", padx=(0, 20))
    
    # Fecha y Hora
    date_time_frame = tk.Frame(col1, bg="#ffffff")
    date_time_frame.pack(fill="x", pady=(0, 20))
    
    tk.Label(
        date_time_frame,
        text="📅 Fecha *:",
        bg="#ffffff",
        font=FONT_P_BOLD
    ).grid(row=0, column=0, sticky="w", padx=(0, 15), pady=5)
    
    date_entry = tk.Entry(
        date_time_frame,
        font=FONT_P,
        width=15,
        relief="solid"
    )
    date_entry.grid(row=0, column=1, sticky="w", pady=5)
    
    tk.Label(
        date_time_frame,
        text="🕐 Hora *:",
        bg="#ffffff",
        font=FONT_P_BOLD
    ).grid(row=1, column=0, sticky="w", padx=(0, 15), pady=(10, 5))
    
    time_entry = tk.Entry(
        date_time_frame,
        font=FONT_P,
        width=15,
        relief="solid"
    )
    time_entry.grid(row=1, column=1, sticky="w", pady=(10, 5))
    
    tk.Label(
        col1,
        text="📍 Lugar *:",
        bg="#ffffff",
        font=FONT_P_BOLD
    ).pack(anchor="w", pady=(0, 8))
    
    place_entry = tk.Entry(
        col1,
        font=FONT_P,
        relief="solid"
    )
    place_entry.pack(fill="x", ipady=8, pady=(0, 15))
    
    tk.Label(
        col1,
        text="🎯 Motivo *:",
        bg="#ffffff",
        font=FONT_P_BOLD
    ).pack(anchor="w", pady=(0, 8))
    
    reason_entry = tk.Entry(
        col1,
        font=FONT_P,
        relief="solid"
    )
    reason_entry.pack(fill="x", ipady=8, pady=(0, 15))
    
    tk.Label(
        col1,
        text="📄 Descripción Detallada:",
        bg="#ffffff",
        font=FONT_P_BOLD
    ).pack(anchor="w", pady=(0, 8))
    
    desc_text = tk.Text(
        col1,
        font=FONT_P,
        height=6,
        relief="solid",
        wrap="word"
    )
    desc_text.pack(fill="x", pady=(0, 20))
    
    col2 = tk.LabelFrame(
        content_area,
        text="👥 Selector de Destinatarios",
        bg="#ffffff",
        fg=COLOR_ACCENT_ADMIN,
        font=FONT_H2,
        padx=25,
        pady=25,
        relief="solid",
        bd=2,
        highlightbackground=COLOR_TEST_BORDER
    )
    col2.grid(row=0, column=1, sticky="nsew", padx=20)
    
    send_type = tk.StringVar(value="individual")
    
    tk.Radiobutton(
        col2,
        text="👪 Enviar a Grupos Completos",
        variable=send_type,
        value="grupos",
        bg="#ffffff",
        font=FONT_P_BOLD,
        selectcolor="#e3f2fd"
    ).pack(anchor="w", pady=(0, 5))
    
    tk.Label(
        col2,
        text="Seleccionar grupos enteros de estudiantes",
        bg="#ffffff",
        fg=COLOR_TEXT_MUTED,
        font=FONT_SMALL
    ).pack(anchor="w", padx=25)
    
    group_frame = tk.Frame(col2, bg="#ffffff")
    group_frame.pack(fill="x", pady=(10, 20))
    
    ttk.Combobox(
        group_frame,
        values=["Párvulos A", "Párvulos B", "Transición A", "Transición B"],
        width=20,
        state="readonly"
    ).pack(side="left")
    
    tk.Radiobutton(
        col2,
        text="👤 Enviar a Acudientes Individuales",
        variable=send_type,
        value="individual",
        bg="#ffffff",
        font=FONT_P_BOLD,
        selectcolor="#e3f2fd"
    ).pack(anchor="w", pady=(0, 5))
    
    tk.Label(
        col2,
        text="Seleccionar acudientes específicos",
        bg="#ffffff",
        fg=COLOR_TEXT_MUTED,
        font=FONT_SMALL
    ).pack(anchor="w", padx=25)
    
    # Listbox con scrollbar
    list_frame = tk.Frame(col2, bg="#ffffff")
    list_frame.pack(fill="x", pady=(10, 0))
    
    list_scroll = ttk.Scrollbar(list_frame)
    list_scroll.pack(side="right", fill="y")
    
    listbox = tk.Listbox(
        list_frame,
        height=8,
        selectmode=tk.MULTIPLE,
        font=FONT_P,
        yscrollcommand=list_scroll.set,
        relief="solid"
    )
    list_scroll.config(command=listbox.yview)
    listbox.pack(side="left", fill="both", expand=True)
    
    # Datos de ejemplo
    acudientes = [
        "María González - Párvulos A (Emma)",
        "Carlos Martínez - Párvulos A (Lucas)",
        "Ana Rodríguez - Párvulos A (Sofía)",
        "Luis Pérez - Párvulos B (Diego)",
        "Laura Gómez - Transición A (Valentina)",
        "Miguel Torres - Párvulos A (Mateo)"
    ]
    
    for acudiente in acudientes:
        listbox.insert(tk.END, acudiente)
    
    # Contador seleccionados
    count_var = tk.StringVar(value="0")
    count_label = tk.Label(
        col2,
        textvariable=count_var,
        bg="#ffffff",
        fg=COLOR_ACCENT_ADMIN,
        font=FONT_P_BOLD
    )
    count_label.pack(anchor="w", pady=(10, 0))
    
    def update_count(*args):
        count = len(listbox.curselection())
        count_var.set(f"Seleccionados: {count}")
    
    listbox.bind("<<ListboxSelect>>", update_count)
    
    # Botón principal
    btn_frame = tk.Frame(citation_frame, bg="#f8f9fa")
    btn_frame.pack(fill="x", pady=30)
    
    ttk.Button(
        btn_frame,
        text="🚀 Generar y Enviar Citación",
        style="AdminBlue.TButton",
        command=lambda: print("Generando citación...")
    ).pack(pady=15)
    
    # Vista previa simulada
    preview_btn = tk.Button(
        btn_frame,
        text="👁️ Vista Previa",
        bg=COLOR_HEADER_PRE,
        fg=COLOR_TEXT_LIGHT,
        font=FONT_P_BOLD,
        bd=0,
        relief="flat"
    )
    preview_btn.pack()
    
    return citation_frame
