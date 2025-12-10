

import tkinter as tk
import tkinter.ttk as ttk
from config import *


def create_sidebar_button(parent, text, icon, module_name, nav_commands, is_active=False):
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

    btn.bind("<Enter>", lambda e: btn.config(bg=active_color))
    btn.bind("<Leave>", lambda e: btn.config(bg=bg_color))

    return btn

def create_info_card(parent, title, value, icon, color):
    card = tk.Frame(parent, bg="#ffffff", padx=12, pady=12, relief="solid", bd=1, highlightbackground=COLOR_TEST_BORDER, highlightthickness=1)

    icon_label = tk.Label(card, text=icon, font=("Helvetica", 22), fg=color, bg="#ffffff")
    icon_label.pack(side="left")

    text_frame = tk.Frame(card, bg="#ffffff")
    text_frame.pack(side="right", padx=(8, 0))

    tk.Label(text_frame, text=value, font=FONT_H1, fg=color, bg="#ffffff").pack(anchor="w")
    tk.Label(text_frame, text=title, font=FONT_P, fg=COLOR_TEXT_MUTED, bg="#ffffff").pack(anchor="w")

    return card

def create_admin_dashboard(master, nav_commands):
    """Interfaz exclusiva para gestión de usuarios. Mantiene la estética original."""

    dashboard_frame = tk.Frame(master)
    dashboard_frame.grid_columnconfigure(0, weight=0)
    dashboard_frame.grid_columnconfigure(1, weight=1)
    dashboard_frame.grid_rowconfigure(0, weight=1)

    # SIDEBAR
    sidebar = tk.Frame(dashboard_frame, bg=COLOR_SIDEBAR_ADMIN, width=220)
    sidebar.grid(row=0, column=0, sticky="nsew")
    sidebar.pack_propagate(False)

    tk.Label(sidebar, text="Gestión Usuarios", bg=COLOR_DARK_BG, fg=COLOR_TEXT_LIGHT, font=FONT_H1).pack(fill="x", ipady=10)
    tk.Label(sidebar, text="Administrador", bg=COLOR_SIDEBAR_ADMIN, fg=COLOR_HEADER_PRE, font=FONT_H3).pack(fill="x")
    tk.Label(sidebar, text="Panel: Gestión de Usuarios", bg=COLOR_SIDEBAR_ADMIN, fg=COLOR_TEXT_LIGHT, font=FONT_P).pack(fill="x", pady=(0, 10))

    # Sólo opciones relacionadas con usuarios
    tk.Label(sidebar, text="USUARIOS", bg=COLOR_SIDEBAR_ADMIN, fg="#a0a0a0", font=FONT_SMALL).pack(fill="x", padx=10, pady=(10, 5), anchor="w")
    create_sidebar_button(sidebar, "Gestión de Usuarios", "👤", "users_manager", nav_commands, is_active=True)

    tk.Frame(sidebar, height=1, bg="#444a57").pack(fill="x", pady=10, padx=10, side="bottom")
    tk.Button(sidebar, text="❌ Cerrar Sesión", bg=COLOR_SIDEBAR_ADMIN, fg="#ff5555", font=FONT_P_BOLD, bd=0,
              highlightthickness=0, command=nav_commands['home']).pack(fill="x", side="bottom", pady=10, padx=10)

    # CONTENIDO PRINCIPAL
    main_content = tk.Frame(dashboard_frame, bg="#f5f7fa")
    main_content.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
    main_content.grid_columnconfigure(0, weight=1)

    # Header
    header_content = tk.Frame(main_content, bg="#f5f7fa")
    header_content.pack(fill="x", pady=(0, 12))
    tk.Label(header_content, text="Gestión de Usuarios", font=FONT_H1, bg="#f5f7fa", fg=COLOR_TEXT_DARK).pack(side="left", anchor="w")
    tk.Label(header_content, text="Usuarios del sistema: crear, editar y eliminar", font=FONT_P, bg="#f5f7fa", fg=COLOR_TEXT_MUTED).pack(side="right", anchor="e")

    # Resumen rápido
    summary_row = tk.Frame(main_content, bg="#f5f7fa")
    summary_row.pack(fill="x", pady=(0, 12))
    summary_row.grid_columnconfigure(0, weight=1)
    summary_row.grid_columnconfigure(1, weight=1)
    summary_row.grid_columnconfigure(2, weight=1)

    create_info_card(summary_row, "Total Usuarios", "63", "👥", COLOR_ACCENT_ADMIN).grid(row=0, column=0, sticky="ew", padx=4)
    create_info_card(summary_row, "Administradores", "3", "🛡️", COLOR_HEADER_PRE).grid(row=0, column=1, sticky="ew", padx=4)
    create_info_card(summary_row, "Profesores", "20", "📚", COLOR_ACCENT_TEACHER).grid(row=0, column=2, sticky="ew", padx=4)

    # Área de lista y acciones
    content_card = tk.Frame(main_content, bg="#ffffff", padx=12, pady=12, relief="solid", bd=1, highlightbackground=COLOR_TEST_BORDER, highlightthickness=1)
    content_card.pack(fill="both", expand=True)

    # Toolbar superior (buscar, botones)
    toolbar = tk.Frame(content_card, bg="#ffffff")
    toolbar.pack(fill="x", pady=(0, 8))

    search_var = tk.StringVar()
    tk.Entry(toolbar, textvariable=search_var, font=FONT_P, width=30).pack(side="left", padx=(0, 8))
    tk.Button(toolbar, text="Buscar", bg=COLOR_ACCENT_ADMIN, fg=COLOR_TEXT_LIGHT, font=FONT_P_BOLD, bd=0).pack(side="left")

    # Botones CRUD
    btn_frame = tk.Frame(toolbar, bg="#ffffff")
    btn_frame.pack(side="right")
    ttk.Button(btn_frame, text="Nuevo Usuario", style="AdminBlue.TButton", command=lambda: open_add_user_modal(content_card, tree)).pack(side="left", padx=6)
    ttk.Button(btn_frame, text="Editar", style="AdminBlue.TButton", command=lambda: open_edit_user_modal(content_card, tree)).pack(side="left", padx=6)
    ttk.Button(btn_frame, text="Eliminar", style="Danger.TButton", command=lambda: delete_selected_user(tree)).pack(side="left", padx=6)

    # Treeview de usuarios
    columns = ("id", "name", "role", "email", "status")
    tree = ttk.Treeview(content_card, columns=columns, show="headings", selectmode="browse")
    tree.heading("id", text="ID")
    tree.heading("name", text="Nombre")
    tree.heading("role", text="Rol")
    tree.heading("email", text="Email")
    tree.heading("status", text="Estado")

    tree.column("id", width=50, anchor="center")
    tree.column("name", width=200)
    tree.column("role", width=120, anchor="center")
    tree.column("email", width=200)
    tree.column("status", width=100, anchor="center")

    tree.pack(fill="both", expand=True)

    # Datos de ejemplo (simulados)
    sample_users = [
        (1, "María Pérez", "Administrador", "maria.perez@colegio.edu", "Activo"),
        (2, "Juan Gómez", "Profesor", "juan.gomez@colegio.edu", "Activo"),
        (3, "Lucía Martínez", "Estudiante", "lucia.m@colegio.edu", "Inactivo"),
    ]

    for u in sample_users:
        tree.insert("", "end", values=u)

    # --- Funciones auxiliares CRUD (simuladas, UI only) ---
    def open_add_user_modal(parent, treeview):
        modal = tk.Toplevel(parent)
        modal.transient(parent)
        modal.grab_set()
        modal.title("Crear Usuario")

        tk.Label(modal, text="Crear Nuevo Usuario", font=FONT_H3).pack(pady=(10, 6))

        frm = tk.Frame(modal)
        frm.pack(padx=12, pady=8)

        tk.Label(frm, text="Nombre:").grid(row=0, column=0, sticky="e")
        name_e = tk.Entry(frm, width=30)
        name_e.grid(row=0, column=1, pady=4)

        tk.Label(frm, text="Email:").grid(row=1, column=0, sticky="e")
        email_e = tk.Entry(frm, width=30)
        email_e.grid(row=1, column=1, pady=4)

        tk.Label(frm, text="Rol:").grid(row=2, column=0, sticky="e")
        role_e = ttk.Combobox(frm, values=["Administrador", "Profesor", "Estudiante"], state="readonly")
        role_e.grid(row=2, column=1, pady=4)
        role_e.current(2)

        def save_new():
            # Inserción simulada en la vista
            new_id = len(treeview.get_children()) + 1
            treeview.insert("", "end", values=(new_id, name_e.get() or "-", role_e.get() or "Estudiante", email_e.get() or "-", "Activo"))
            modal.destroy()

        tk.Button(modal, text="Guardar", bg=COLOR_ACCENT_ADMIN, fg=COLOR_TEXT_LIGHT, bd=0, command=save_new).pack(pady=(8, 12))

    def open_edit_user_modal(parent, treeview):
        sel = treeview.selection()
        if not sel:
            return
        item = treeview.item(sel)
        vals = item.get("values", ())

        modal = tk.Toplevel(parent)
        modal.transient(parent)
        modal.grab_set()
        modal.title("Editar Usuario")

        tk.Label(modal, text="Editar Usuario", font=FONT_H3).pack(pady=(10, 6))
        frm = tk.Frame(modal)
        frm.pack(padx=12, pady=8)

        tk.Label(frm, text="Nombre:").grid(row=0, column=0, sticky="e")
        name_e = tk.Entry(frm, width=30)
        name_e.insert(0, vals[1])
        name_e.grid(row=0, column=1, pady=4)

        tk.Label(frm, text="Email:").grid(row=1, column=0, sticky="e")
        email_e = tk.Entry(frm, width=30)
        email_e.insert(0, vals[3])
        email_e.grid(row=1, column=1, pady=4)

        tk.Label(frm, text="Rol:").grid(row=2, column=0, sticky="e")
        role_e = ttk.Combobox(frm, values=["Administrador", "Profesor", "Estudiante"], state="readonly")
        role_e.grid(row=2, column=1, pady=4)
        try:
            role_e.current(["Administrador", "Profesor", "Estudiante"].index(vals[2]))
        except Exception:
            role_e.current(2)

        def save_edit():
            treeview.item(sel, values=(vals[0], name_e.get() or vals[1], role_e.get() or vals[2], email_e.get() or vals[3], vals[4]))
            modal.destroy()

        tk.Button(modal, text="Guardar cambios", bg=COLOR_ACCENT_ADMIN, fg=COLOR_TEXT_LIGHT, bd=0, command=save_edit).pack(pady=(8, 12))

    def delete_selected_user(treeview):
        sel = treeview.selection()
        if not sel:
            return
        treeview.delete(sel)

    return dashboard_frame