import tkinter as tk
import tkinter.ttk as ttk
from ..config import *
from sqlalchemy import text

# ✅ NUEVO: Importar decorador RBAC
from app.services.rbac_service import require_permission

# ✅ NUEVO: Importar servicios de usuario
from app.ui.components.crear_usuario_form import crear_ventana_formulario
from app.services.usuario_service import ServicioUsuario
from app.data.db import SessionLocal
from app.ui.components.session import get_user_info

try:
    from app.services.gestion_academica import ServicioGestionAcademica
    from app.services.reportes import ServicioReportes
except ImportError:
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    from app.services.gestion_academica import ServicioGestionAcademica
    from app.services.reportes import ServicioReportes


def create_sidebar_button(parent, text, icon, module_name, nav_commands, is_active=False):
    bg_color = COLOR_ACCENT_DARK if is_active else COLOR_SIDEBAR_ADMIN
    hover_color = COLOR_ACCENT_DARK
    
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
        fg=COLOR_HEADER_PRE if is_active else COLOR_TEXT_LIGHT,
        font=FONT_P_BOLD,
        command=lambda: nav_commands['show_frame'](module_name) if module_name else None
    )
    btn.pack(fill="x")
    
    # Hover effects
    def on_enter(e):
        btn.config(bg=hover_color)
    def on_leave(e):
        btn.config(bg=bg_color)
    
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    
    return btn


def create_info_card(parent, title, value, icon, color):
    """Crea tarjeta de información con icono y estadísticas."""
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
    
    # Icono
    icon_label = tk.Label(
        card,
        text=icon,
        font=("Segoe UI Emoji", 24, "bold"),
        fg=color,
        bg="#ffffff"
    )
    icon_label.pack(side="left")
    
    # Contenido texto
    text_frame = tk.Frame(card, bg="#ffffff")
    text_frame.pack(side="right", fill="both", expand=True, padx=(15, 0))
    
    tk.Label(
        text_frame,
        text=value,
        font=FONT_H2,
        fg=color,
        bg="#ffffff"
    ).pack(anchor="w")
    tk.Label(
        text_frame,
        text=title,
        font=FONT_P,
        fg=COLOR_TEXT_MUTED,
        bg="#ffffff"
    ).pack(anchor="w")
    
    return card


# Dashboard de Administrador
def create_admin_dashboard(master, nav_commands):
    """Interfaz exclusiva para gestión de usuarios - Dashboard Admin."""
    
    # Inicializar servicios
    reportes = ServicioReportes()
    gestion_academica = ServicioGestionAcademica(reportes)
    
    dashboard_frame = tk.Frame(master)
    dashboard_frame.grid_columnconfigure(0, weight=0)
    dashboard_frame.grid_columnconfigure(1, weight=1)
    dashboard_frame.grid_rowconfigure(0, weight=1)
    
    # SIDEBAR
    sidebar = tk.Frame(dashboard_frame, bg=COLOR_SIDEBAR_ADMIN, width=240)
    sidebar.grid(row=0, column=0, sticky="nsew")
    sidebar.pack_propagate(False)
    
    # Header sidebar
    header_sid = tk.Frame(sidebar, bg=COLOR_SIDEBAR_ADMIN)
    header_sid.pack(fill="x", pady=(15, 20))
    tk.Label(
        header_sid,
        text="Gestión Usuarios",
        bg=COLOR_SIDEBAR_ADMIN,
        fg=COLOR_TEXT_LIGHT,
        font=FONT_H2
    ).pack(pady=5)
    tk.Label(
        header_sid,
        text="Administrador",
        bg=COLOR_SIDEBAR_ADMIN,
        fg=COLOR_HEADER_PRE,
        font=FONT_H3
    ).pack()
    tk.Label(
        header_sid,
        text="Panel: Gestión de Usuarios",
        bg=COLOR_SIDEBAR_ADMIN,
        fg=COLOR_TEXT_LIGHT,
        font=FONT_P
    ).pack(pady=(5, 20))
    
    # Navegación
    tk.Label(
        sidebar,
        text="USUARIOS",
        bg=COLOR_SIDEBAR_ADMIN,
        fg="#a0a0a0",
        font=FONT_SMALL_BOLD
    ).pack(fill="x", padx=20, pady=(10, 8), anchor="w")
    
    create_sidebar_button(
        sidebar,
        "Gestión de Usuarios",
        "👤",
        "users_manager",
        nav_commands,
        is_active=True
    )
    
    # Footer sidebar
    footer_sid = tk.Frame(sidebar, bg=COLOR_SIDEBAR_ADMIN)
    footer_sid.pack(fill="x", side="bottom", pady=20)
    tk.Frame(footer_sid, height=1, bg="#444a57").pack(fill="x", pady=(0, 15), padx=15)
    tk.Button(
        footer_sid,
        text="❌ Cerrar Sesión",
        bg=COLOR_SIDEBAR_ADMIN,
        fg="#ff6b6b",
        font=FONT_P_BOLD,
        bd=0,
        highlightthickness=0,
        command=nav_commands['home']
    ).pack(fill="x", padx=20)
    
    # CONTENIDO PRINCIPAL
    main_content = tk.Frame(dashboard_frame, bg="#f8f9fa")
    main_content.grid(row=0, column=1, sticky="nsew", padx=(10, 25), pady=25)
    main_content.grid_columnconfigure(0, weight=1)
    
    # Header contenido
    header_content = tk.Frame(main_content, bg="#f8f9fa")
    header_content.pack(fill="x", pady=(0, 25))
    tk.Label(
        header_content,
        text="👥 Gestión de Usuarios",
        font=FONT_H1,
        bg="#f8f9fa",
        fg=COLOR_TEXT_DARK
    ).pack(side="left")
    tk.Label(
        header_content,
        text="Crear, editar y eliminar usuarios del sistema",
        font=FONT_P,
        bg="#f8f9fa",
        fg=COLOR_TEXT_MUTED
    ).pack(side="right")
    
    # Estadísticas rápidas
    stats_row = tk.Frame(main_content, bg="#f8f9fa")
    stats_row.pack(fill="x", pady=(0, 25))
    stats_row.grid_columnconfigure(0, weight=1)
    stats_row.grid_columnconfigure(1, weight=1)
    stats_row.grid_columnconfigure(2, weight=1)
    
    create_info_card(stats_row, "Total Usuarios", "63", "👥", COLOR_ACCENT_ADMIN).grid(
        row=0, column=0, sticky="ew", padx=8, pady=8
    )
    create_info_card(stats_row, "Administradores", "3", "🛡️", COLOR_HEADER_PRE).grid(
        row=0, column=1, sticky="ew", padx=8, pady=8
    )
    create_info_card(stats_row, "Profesores", "20", "📚", COLOR_ACCENT_TEACHER).grid(
        row=0, column=2, sticky="ew", padx=8, pady=8
    )
    
    # Contenedor principal de tabla
    content_card = tk.Frame(
        main_content,
        bg="#ffffff",
        padx=25,
        pady=25,
        relief="solid",
        bd=1,
        highlightbackground=COLOR_TEST_BORDER,
        highlightthickness=1
    )
    content_card.pack(fill="both", expand=True)
    
    # Toolbar
    toolbar = tk.Frame(content_card, bg="#ffffff")
    toolbar.pack(fill="x", pady=(0, 15))
    
    # Búsqueda
    search_frame = tk.Frame(toolbar, bg="#ffffff")
    search_frame.pack(side="left")
    tk.Label(search_frame, text="🔍 Buscar:", font=FONT_P_BOLD, bg="#ffffff").pack(side="left", padx=(0, 5))
    search_var = tk.StringVar()
    search_entry = tk.Entry(
        search_frame,
        textvariable=search_var,
        font=FONT_P,
        width=25,
        relief="solid",
        bd=1
    )
    search_entry.pack(side="left")
    
    # Botones CRUD
    btn_frame = tk.Frame(toolbar, bg="#ffffff")
    btn_frame.pack(side="right")
    
    def abrir_formulario_crear_usuario():
        """Abre el formulario para crear nuevo usuario"""
        try:
            # Obtener info del usuario actual
            user_info = get_user_info()
            
            # Crear servicio con sesión
            session = SessionLocal()
            servicio = ServicioUsuario(session)
            
            # Obtener roles disponibles según el rol del usuario actual
            roles_disponibles = servicio.obtener_roles_disponibles(user_info.get("role", "Administrador"))
            
            # Colores
            config_colors = {
                "BG": "#f5f5f5",
                "ACCENT": COLOR_ACCENT_ADMIN,
                "ERROR": "#f44336",
                "SUCCESS": "#4caf50",
                "TEXT": COLOR_TEXT_DARK
            }
            
            # Crear ventana con formulario
            ventana, formulario = crear_ventana_formulario(
                roles_disponibles,
                lambda datos: procesar_creacion_usuario(datos, servicio, session, ventana),
                config_colors
            )
        
        except Exception as e:
            from tkinter import messagebox
            messagebox.showerror("Error", f"Error al abrir formulario: {str(e)}")
            print(f"[ERROR] abrir_formulario_crear_usuario: {e}")
            import traceback
            traceback.print_exc()
    
    def procesar_creacion_usuario(datos: dict, servicio: ServicioUsuario, session, ventana):
        """Procesa la creación del usuario desde el formulario"""
        from tkinter import messagebox
        
        try:
            # Obtener info del usuario actual
            user_info = get_user_info()
            
            # Agregar información de contexto
            datos["rol_usuario_actual"] = user_info.get("role", "Administrador")
            
            # Llamar al servicio
            exito, mensaje, datos_usuario = servicio.crear_usuario(datos, user_info.get("id"))
            
            if exito:
                messagebox.showinfo("✅ Éxito", mensaje)
                # Cerrar ventana del formulario
                ventana.destroy()
                # Recargar tabla de usuarios
                recargar_tabla_usuarios()
            else:
                messagebox.showerror("❌ Error", mensaje)
        
        except Exception as e:
            from tkinter import messagebox
            messagebox.showerror("Error", f"Error al crear usuario: {str(e)}")
            print(f"[ERROR] procesar_creacion_usuario: {e}")
            import traceback
            traceback.print_exc()
        finally:
            try:
                session.close()
            except:
                pass
    
    def recargar_tabla_usuarios():
        """Recarga la tabla de usuarios"""
        try:
            # Limpiar items actuales
            for item in tree.get_children():
                tree.delete(item)
            
            # Cargar usuarios desde BD
            session = SessionLocal()
            try:
                usuarios = session.execute(text("""
                    SELECT 
                        u.id_usuario,
                        p.primer_nombre || ' ' || p.primer_apellido as nombre,
                        r.nombre_rol,
                        u.correo_electronico,
                        CASE WHEN u.activo THEN '✓ Activo' ELSE '✗ Inactivo' END as estado,
                        COALESCE(TO_CHAR(u.ultimo_ingreso, 'DD/MM/YYYY'), 'N/A') as ultimo_ingreso
                    FROM usuario u
                    JOIN rol r ON u.id_rol = r.id_rol
                    LEFT JOIN persona p ON (
                        u.id_profesor = p.id_persona OR 
                        u.id_acudiente = p.id_persona OR 
                        u.id_directivo = p.id_persona OR 
                        u.id_administrador = p.id_persona
                    )
                    ORDER BY u.fecha_creacion DESC
                """)).fetchall()
                
                for usuario in usuarios:
                    tree.insert('', 'end', values=usuario)
            
            finally:
                session.close()
        except Exception as e:
            print(f"[ERROR] recargar_tabla_usuarios: {e}")
            import traceback
            traceback.print_exc()
    
    ttk.Button(
        btn_frame,
        text="➕ Nuevo Usuario",
        style="AdminBlue.TButton",
        command=abrir_formulario_crear_usuario
    ).pack(side="left", padx=(0, 8))
    
    ttk.Button(
        btn_frame,
        text="✏️ Editar",
        style="AdminBlue.TButton",
        command=lambda: open_edit_user_modal(content_card, tree)
    ).pack(side="left", padx=(0, 8))
    
    ttk.Button(
        btn_frame,
        text="🗑️ Eliminar",
        style="AdminGreen.TButton",  # Cambiado a verde para menos agresivo
        command=lambda: delete_selected_user(tree)
    ).pack(side="left")
    
    # Treeview con scrollbar
    tree_container = tk.Frame(content_card)
    tree_container.pack(fill="both", expand=True)
    
    tree_scroll = ttk.Scrollbar(tree_container)
    tree_scroll.pack(side="right", fill="y")
    
    columns = ("id", "name", "role", "email", "status", "last_login")
    tree = ttk.Treeview(
        tree_container,
        columns=columns,
        show="headings",
        selectmode="browse",
        yscrollcommand=tree_scroll.set,
        height=12
    )
    tree_scroll.config(command=tree.yview)
    tree.pack(side="left", fill="both", expand=True)
    
    # Configurar columnas
    tree.heading("id", text="ID")
    tree.heading("name", text="Nombre Completo")
    tree.heading("role", text="Rol")
    tree.heading("email", text="Correo Electrónico")
    tree.heading("status", text="Estado")
    tree.heading("last_login", text="Último Acceso")
    
    tree.column("id", width=60, anchor="center")
    tree.column("name", width=220)
    tree.column("role", width=130, anchor="center")
    tree.column("email", width=250)
    tree.column("status", width=100, anchor="center")
    tree.column("last_login", width=140, anchor="center")
    
    # Datos de ejemplo
    sample_users = [
        (1, "María Pérez González", "Administrador", "maria.perez@colegio.edu", "Activo", "08/12/2025"),
        (2, "Juan Gómez López", "Profesor", "juan.gomez@colegio.edu", "Activo", "07/12/2025"),
        (3, "Lucía Martínez", "Estudiante", "lucia.m@colegio.edu", "Inactivo", "N/A"),
        (4, "Carlos Rodríguez", "Profesor", "carlos.rodriguez@colegio.edu", "Activo", "09/12/2025"),
        (5, "Ana Torres", "Administrador", "ana.torres@colegio.edu", "Activo", "06/12/2025"),
    ]
    
    for user in sample_users:
        tree.insert("", "end", values=user)
    
    # FUNCIONES CRUD (UI simulada)
    def open_add_user_modal(parent, treeview):
        modal = tk.Toplevel(parent)
        modal.title("➕ Crear Nuevo Usuario")
        modal.geometry("400x300")
        modal.transient(parent.winfo_toplevel())
        modal.grab_set()
        modal.resizable(False, False)
        
        tk.Label(modal, text="Crear Nuevo Usuario", font=FONT_H2).pack(pady=20)
        
        frm = tk.Frame(modal, padx=30, pady=20)
        frm.pack()
        frm.grid_columnconfigure(1, weight=1)
        
        tk.Label(frm, text="Nombre Completo:", font=FONT_P_BOLD).grid(row=0, column=0, sticky="e", pady=8)
        name_e = tk.Entry(frm, width=30, font=FONT_P)
        name_e.grid(row=0, column=1, sticky="ew", pady=8)
        
        tk.Label(frm, text="Email:", font=FONT_P_BOLD).grid(row=1, column=0, sticky="e", pady=8)
        email_e = tk.Entry(frm, width=30, font=FONT_P)
        email_e.grid(row=1, column=1, sticky="ew", pady=8)
        
        tk.Label(frm, text="Rol:", font=FONT_P_BOLD).grid(row=2, column=0, sticky="e", pady=8)
        role_combo = ttk.Combobox(frm, values=["Administrador", "Profesor", "Estudiante", "Acudiente"], state="readonly", width=27)
        role_combo.current(2)
        role_combo.grid(row=2, column=1, sticky="ew", pady=8)
        
        def save_new():
            new_id = len(treeview.get_children()) + 1
            treeview.insert("", "end", values=(
                new_id,
                name_e.get() or "Sin nombre",
                role_combo.get(),
                email_e.get() or "sin@email.com",
                "Activo",
                "Hoy"
            ))
            modal.destroy()
        
        btn_frame = tk.Frame(modal)
        btn_frame.pack(pady=20)
        tk.Button(
            btn_frame,
            text="💾 Guardar",
            bg=COLOR_ACCENT_ADMIN,
            fg=COLOR_TEXT_LIGHT,
            font=FONT_P_BOLD,
            bd=0,
            width=12,
            command=save_new
        ).pack(side="left", padx=10)
        tk.Button(
            btn_frame,
            text="❌ Cancelar",
            bg="#6c757d",
            fg="white",
            font=FONT_P_BOLD,
            bd=0,
            width=12,
            command=modal.destroy
        ).pack(side="left")
    
    def open_edit_user_modal(parent, treeview):
        sel = treeview.selection()
        if not sel:
            tk.messagebox.showwarning("Advertencia", "Seleccione un usuario para editar")
            return
        
        item = treeview.item(sel[0])
        vals = item['values']
        
        modal = tk.Toplevel(parent)
        modal.title("✏️ Editar Usuario")
        modal.geometry("400x300")
        modal.transient(parent.winfo_toplevel())
        modal.grab_set()
        modal.resizable(False, False)
        
        tk.Label(modal, text="Editar Usuario", font=FONT_H2).pack(pady=20)
        
        frm = tk.Frame(modal, padx=30, pady=20)
        frm.pack()
        frm.grid_columnconfigure(1, weight=1)
        
        tk.Label(frm, text="Nombre Completo:", font=FONT_P_BOLD).grid(row=0, column=0, sticky="e", pady=8)
        name_e = tk.Entry(frm, width=30, font=FONT_P)
        name_e.insert(0, vals[1])
        name_e.grid(row=0, column=1, sticky="ew", pady=8)
        
        tk.Label(frm, text="Email:", font=FONT_P_BOLD).grid(row=1, column=0, sticky="e", pady=8)
        email_e = tk.Entry(frm, width=30, font=FONT_P)
        email_e.insert(0, vals[3])
        email_e.grid(row=1, column=1, sticky="ew", pady=8)
        
        tk.Label(frm, text="Rol:", font=FONT_P_BOLD).grid(row=2, column=0, sticky="e", pady=8)
        role_combo = ttk.Combobox(frm, values=["Administrador", "Profesor", "Estudiante", "Acudiente"], state="readonly", width=27)
        role_combo.set(vals[2])
        role_combo.grid(row=2, column=1, sticky="ew", pady=8)
        
        def save_edit():
            treeview.item(sel[0], values=(
                vals[0],
                name_e.get() or vals[1],
                role_combo.get(),
                email_e.get() or vals[3],
                vals[4],
                vals[5]
            ))
            modal.destroy()
        
        btn_frame = tk.Frame(modal)
        btn_frame.pack(pady=20)
        tk.Button(
            btn_frame,
            text="💾 Actualizar",
            bg=COLOR_ACCENT_ADMIN,
            fg=COLOR_TEXT_LIGHT,
            font=FONT_P_BOLD,
            bd=0,
            width=12,
            command=save_edit
        ).pack(side="left", padx=10)
        tk.Button(
            btn_frame,
            text="❌ Cancelar",
            bg="#6c757d",
            fg="white",
            font=FONT_P_BOLD,
            bd=0,
            width=12,
            command=modal.destroy
        ).pack(side="left")
    
    def delete_selected_user(treeview):
        sel = treeview.selection()
        if not sel:
            tk.messagebox.showwarning("Advertencia", "Seleccione un usuario para eliminar")
            return
        
        if tk.messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este usuario?"):
            treeview.delete(sel[0])
    
    return dashboard_frame
