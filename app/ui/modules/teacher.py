# Archivo: teacher_module.py

import tkinter as tk
import tkinter.ttk as ttk
from ..config import *
from ..components.session import get_dashboard_command

# ✅ NUEVO: Importar decorador RBAC
from app.services.rbac_service import require_permission


def create_sidebar_button_teacher(parent, text, icon, module_name, nav_commands, is_active=False):
    bg_color = COLOR_ACCENT_DARK if is_active else COLOR_SIDEBAR_TEACHER
    
    btn_frame = tk.Frame(parent, bg=bg_color)
    btn = tk.Button(
        btn_frame, text=f"{icon}   {text}", anchor="w", bd=0, padx=10, pady=8,
        highlightthickness=0, bg=bg_color,
        fg=COLOR_HEADER_PRE if is_active else COLOR_TEXT_LIGHT, font=FONT_P_BOLD,
        command=lambda: nav_commands['show_frame'](module_name) if module_name else None
    )
    btn.pack(fill="x")
    btn_frame.pack(fill="x", pady=(0, 2))
    return btn


def create_info_pill(parent, value, title, icon, color):
    card = tk.Frame(parent, bg="#ffffff", padx=10, pady=10, relief="solid", bd=1,
                    highlightbackground=COLOR_TEST_BORDER, highlightthickness=1)
    tk.Label(card, text=icon, font=("Helvetica", 24), fg=color, bg="#ffffff").pack(side="right")
    text_frame = tk.Frame(card, bg="#ffffff")
    text_frame.pack(side="left", padx=(0, 10))
    tk.Label(text_frame, text=title, font=FONT_P, fg=COLOR_TEXT_MUTED, bg="#ffffff").pack(anchor="w")
    tk.Label(text_frame, text=value, font=FONT_H1, fg=color, bg="#ffffff").pack(anchor="w")
    return card

# Dashboard de Profesor
def create_teacher_dashboard(master, nav_commands):
    """Crea la interfaz del Panel del Profesor."""
    dashboard_frame = tk.Frame(master)
    dashboard_frame.grid_columnconfigure(0, weight=0)
    dashboard_frame.grid_columnconfigure(1, weight=1)
    dashboard_frame.grid_rowconfigure(0, weight=1)

    # SIDEBAR
    sidebar = tk.Frame(dashboard_frame, bg=COLOR_SIDEBAR_TEACHER, width=220)
    sidebar.grid(row=0, column=0, sticky="nsew")
    sidebar.pack_propagate(False)

    tk.Label(sidebar, text="Panel Profesor", bg=COLOR_SIDEBAR_TEACHER, fg=COLOR_TEXT_LIGHT,
             font=FONT_H1).pack(fill="x", ipady=10)
    tk.Label(sidebar, text="Carlos Martínez - Párvulos A", bg=COLOR_SIDEBAR_TEACHER,
             fg=COLOR_HEADER_PRE, font=FONT_H3).pack(fill="x", pady=(0, 10))

    create_sidebar_button_teacher(sidebar, "Mi Dashboard", "🏠", "teacher_dashboard",
                                  nav_commands, is_active=True)

    tk.Label(sidebar, text="EVALUACIÓN", bg=COLOR_SIDEBAR_TEACHER, fg="#a0a0a0",
             font=FONT_SMALL).pack(fill="x", padx=10, pady=(15, 5), anchor="w")
    create_sidebar_button_teacher(sidebar, "Asignar Logros (GLE)", "📝", "assignment_teacher",
                                  nav_commands)
    create_sidebar_button_teacher(sidebar, "Observador Estudiantes", "🔎", "observer_teacher",
                                  nav_commands)
    create_sidebar_button_teacher(sidebar, "Generar Boletines (CRE)", "📄", "teacher_reports",
                                  nav_commands)

    tk.Label(sidebar, text="MI GRUPO", bg=COLOR_SIDEBAR_TEACHER, fg="#a0a0a0",
             font=FONT_SMALL).pack(fill="x", padx=10, pady=(15, 5), anchor="w")

    tk.Frame(sidebar, height=1, bg="#444a57").pack(fill="x", pady=10, padx=10, side="bottom")
    tk.Button(sidebar, text="❌ Cerrar Sesión", bg=COLOR_SIDEBAR_TEACHER, fg="#ff5555",
              font=FONT_P_BOLD, bd=0, highlightthickness=0,
              command=nav_commands['home']).pack(fill="x", side="bottom", pady=10, padx=10)

    # CONTENIDO PRINCIPAL
    main_content = tk.Frame(dashboard_frame, bg="#f5f7fa")
    main_content.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
    main_content.grid_columnconfigure(0, weight=1)

    header_content = tk.Frame(main_content, bg="#f5f7fa")
    header_content.pack(fill="x", pady=(0, 20))
    tk.Label(header_content, text="Panel del Profesor - Párvulos A", font=FONT_H1,
             bg="#f5f7fa", fg=COLOR_TEXT_DARK).pack(side="left", anchor="w")
    tk.Label(header_content, text="Periodo Actual: Noviembre - Diciembre 2024",
             font=FONT_P, bg="#f5f7fa", fg=COLOR_TEXT_MUTED).pack(side="right", anchor="e")

    # Pastillas Resumen
    summary_row = tk.Frame(main_content, bg="#f5f7fa")
    summary_row.pack(fill="x", pady=(0, 20))
    for i in range(4):
        summary_row.grid_columnconfigure(i, weight=1)

    create_info_pill(summary_row, "8", "Mis Estudiantes", "🧑🏻‍🎓", "#007bff").grid(
        row=0, column=0, sticky="ew", padx=5)
    create_info_pill(summary_row, "100%", "Asistencia Hoy", "📅", "#28a745").grid(
        row=0, column=1, sticky="ew", padx=5)
    create_info_pill(summary_row, "3", "Logros Pendientes", "🗒️", COLOR_HEADER_PRE).grid(
        row=0, column=2, sticky="ew", padx=5)
    create_info_pill(summary_row, "6", "Boletines", "🗂️", "#9343FF").grid(
        row=0, column=3, sticky="ew", padx=5)

    # Módulos Principales
    management_row = tk.Frame(main_content, bg="#f5f7fa")
    management_row.pack(fill="x", pady=(0, 20))
    for i in range(3):
        management_row.grid_columnconfigure(i, weight=1)

    # Card Logros
    card_logros = tk.Frame(management_row, bg="#ffffff", padx=15, pady=15, relief="solid", bd=1,
                           highlightbackground=COLOR_TEST_BORDER, highlightthickness=1)
    card_logros.grid(row=0, column=0, sticky="nsew", padx=10)
    tk.Label(card_logros, text="Asignación de Logros (GLE)", font=FONT_H3,
             fg=COLOR_ACCENT_TEACHER, bg="#ffffff").pack(anchor="w", pady=(0, 5))
    tk.Label(card_logros, text="Evaluar logros académicos y psicosociales de estudiantes.",
             font=FONT_P, fg=COLOR_TEXT_MUTED, bg="#ffffff", wraplength=200,
             justify="left").pack(anchor="w", pady=(0, 15))
    ttk.Button(card_logros, text="Abrir Módulo", style="AdminGreen.TButton",
               command=lambda: nav_commands['show_frame']("assignment_teacher")).pack(
                   fill="x", ipady=5)

    # Card Observador
    card_obs = tk.Frame(management_row, bg="#ffffff", padx=15, pady=15, relief="solid", bd=1,
                        highlightbackground=COLOR_TEST_BORDER, highlightthickness=1)
    card_obs.grid(row=0, column=1, sticky="nsew", padx=10)
    tk.Label(card_obs, text="Observador de Estudiantes", font=FONT_H3,
             fg=COLOR_ACCENT_TEACHER, bg="#ffffff").pack(anchor="w", pady=(0, 5))
    tk.Label(card_obs, text="Registrar observaciones de comportamiento y desarrollo.",
             font=FONT_P, fg=COLOR_TEXT_MUTED, bg="#ffffff", wraplength=200,
             justify="left").pack(anchor="w", pady=(0, 15))
    ttk.Button(card_obs, text="Abrir", style="AdminGreen.TButton",
               command=lambda: nav_commands['show_frame']("observer_teacher")).pack(
                   fill="x", ipady=5)

    # Card Boletines
    card_boletines = tk.Frame(management_row, bg="#ffffff", padx=15, pady=15, relief="solid", bd=1,
                              highlightbackground=COLOR_TEST_BORDER, highlightthickness=1)
    card_boletines.grid(row=0, column=2, sticky="nsew", padx=10)
    tk.Label(card_boletines, text="Generar Boletines (CRE)", font=FONT_H3,
             fg=COLOR_ACCENT_ADMIN, bg="#ffffff").pack(anchor="w", pady=(0, 5))
    tk.Label(card_boletines, text="Crear boletines semestrales con progreso de estudiantes.",
             font=FONT_P, fg=COLOR_TEXT_MUTED, bg="#ffffff", wraplength=200,
             justify="left").pack(anchor="w", pady=(0, 15))
    ttk.Button(card_boletines, text="Generar", style="AdminBlue.TButton",
               command=lambda: nav_commands['show_frame']("teacher_reports")).pack(
                   fill="x", ipady=5)

    # Bottom Row
    bottom_row = tk.Frame(main_content, bg="#f5f7fa")
    bottom_row.pack(fill="x", pady=(20, 0))
    bottom_row.grid_columnconfigure(0, weight=1)
    bottom_row.grid_columnconfigure(1, weight=1)

    # Card Estudiantes
    card_students = tk.Frame(bottom_row, bg="#ffffff", padx=15, pady=15, relief="solid", bd=1,
                             highlightbackground=COLOR_TEST_BORDER, highlightthickness=1)
    card_students.grid(row=0, column=0, sticky="nsew", padx=10)
    tk.Label(card_students, text="Mis Estudiantes - Párvulos A", font=FONT_H3,
             fg=COLOR_TEXT_DARK, bg="#ffffff").pack(anchor="w", pady=(0, 10))

    def create_student_item(parent, name, eval_text, eval_color):
        item = tk.Frame(parent, bg="#ffffff", pady=5)
        item.pack(fill="x")
        tk.Label(item, text="•", font=FONT_P_BOLD, fg=eval_color,
                 bg="#ffffff").pack(side="left", padx=(0, 5))
        tk.Label(item, text=name, font=FONT_P, bg="#ffffff",
                 fg=COLOR_TEXT_DARK).pack(side="left", anchor="w")
        tk.Label(item, text=eval_text, font=FONT_SMALL, bg=eval_color,
                 fg=COLOR_TEXT_LIGHT, padx=5).pack(side="right")

    create_student_item(card_students, "Emma Rodríguez", "Excelente", "#28a745")
    create_student_item(card_students, "Lucas Martínez", "Bueno", "#4a90e2")
    create_student_item(card_students, "Sofía García", "Excelente", "#28a745")
    create_student_item(card_students, "Diego López", "Regular", COLOR_HEADER_PRE)

    # Card Actividades
    card_activities = tk.Frame(bottom_row, bg="#ffffff", padx=15, pady=15, relief="solid", bd=1,
                               highlightbackground=COLOR_TEST_BORDER, highlightthickness=1)
    card_activities.grid(row=0, column=1, sticky="nsew", padx=10)
    tk.Label(card_activities, text="Actividades Pendientes", font=FONT_H3,
             fg=COLOR_TEXT_DARK, bg="#ffffff").pack(anchor="w", pady=(0, 10))

    def create_activity_item(parent, activity, status):
        item = tk.Frame(parent, bg="#ffffff", pady=5)
        item.pack(fill="x")
        tk.Label(item, text=activity, font=FONT_P, bg="#ffffff",
                 fg=COLOR_TEXT_DARK).pack(anchor="w")
        tk.Label(item, text=status, font=FONT_SMALL, bg="#ffffff",
                 fg=COLOR_TEXT_MUTED).pack(anchor="w")

    create_activity_item(card_activities, "Evaluación Logros Cognitivos",
                        "Matemáticas básicos - reconocimiento")
    create_activity_item(card_activities, "Actividad Psicosocial", "Trabajo en equipo - Completado")
    create_activity_item(card_activities, "Reunión Acudientes",
                        "Entrega boletín periodo - Viernes 15:00")

    return dashboard_frame


def create_assignment_teacher(master, nav_commands):
    """Crea la interfaz de Asignación de Logros (Matriz de Evaluación)."""
    assignment_frame = tk.Frame(master, bg="#f5f7fa")

    # Header
    header_frame = tk.Frame(assignment_frame, bg=COLOR_SIDEBAR_TEACHER, height=50)
    header_frame.pack(fill="x", side="top")
    header_frame.pack_propagate(False)

    tk.Button(header_frame, text="← Volver al Dashboard", bg=COLOR_SIDEBAR_TEACHER,
              fg=COLOR_TEXT_LIGHT, font=FONT_P_BOLD, bd=0, highlightthickness=0,
              command=lambda: get_dashboard_command(nav_commands)()).pack(side="left", padx=20)

    tk.Label(header_frame, text="Asignación de Logros/Notas",
             bg=COLOR_SIDEBAR_TEACHER, fg=COLOR_TEXT_LIGHT, font=FONT_H1).pack(side="left", padx=50)

    # Contenido
    content_area = tk.Frame(assignment_frame, bg="#ffffff", padx=30, pady=30)
    content_area.pack(fill="both", expand=True)

    controls_frame = tk.Frame(content_area, bg="#ffffff")
    controls_frame.pack(fill="x", pady=(0, 20))

    tk.Label(controls_frame, text="Grado/Grupo:", bg="#ffffff",
             font=FONT_P_BOLD).pack(side="left", padx=(0, 5))
    ttk.Combobox(controls_frame, values=["Párvulos A"], width=15).pack(side="left", padx=10)

    tk.Label(controls_frame, text="Periodo Académico:", bg="#ffffff",
             font=FONT_P_BOLD).pack(side="left", padx=(10, 5))
    ttk.Combobox(controls_frame, values=["Noviembre - Diciembre"], width=20).pack(side="left", padx=10)

    tk.Button(controls_frame, text="Guardar Evaluación del Periodo",
              bg=COLOR_ACCENT_TEACHER, fg=COLOR_TEXT_LIGHT, font=FONT_P_BOLD, bd=0).pack(
                  side="right", ipady=5)

    tk.Label(content_area, text="Matriz de Evaluación - Párvulos A", font=FONT_H3,
             bg="#ffffff", fg=COLOR_TEXT_DARK).pack(anchor="w", pady=(10, 5))

    tree_frame = tk.Frame(content_area)
    tree_frame.pack(fill="both", expand=True, pady=(0, 10))

    tree = ttk.Treeview(tree_frame, columns=("c1", "c2", "c3", "c4", "c5", "c6", "c7", "c8", "c9"),
                        show='headings')

    tree.heading("c1", text="Estudiante")
    tree.heading("c2", text="Desarrollo Cognitivo")
    tree.heading("c3", text="Memoria")
    tree.heading("c4", text="Atención")
    tree.heading("c5", text="Percepción")
    tree.heading("c6", text="Desarrollo Psicomotor")
    tree.heading("c7", text="Motricidad Gruesa")
    tree.heading("c8", text="Motricidad Fina")
    tree.heading("c9", text="Desarrollo Socioafectivo")

    tree.column("c1", width=120)

    students = ["A. Emma Rodríguez", "B. Lucas Martínez", "C. Sofia García"]
    for student in students:
        tree.insert("", "end", values=(student, "Cognitivo", "1-5", "1-5", "1-5", "Psicomotor",
                                       "1-5", "1-5", "Socioafectivo"))

    tree.pack(fill="both", expand=True)

    return assignment_frame


def create_observer_teacher(master, nav_commands):
    """Crea la interfaz del Observador del Estudiante."""
    observer_frame = tk.Frame(master, bg="#f5f7fa")

    header_frame = tk.Frame(observer_frame, bg="#ffffff", height=50)
    header_frame.pack(fill="x", side="top", padx=20, pady=10)
    header_frame.pack_propagate(False)

    main_content = tk.Frame(observer_frame, bg="#f5f7fa")
    main_content.pack(fill="both", expand=True)
    main_content.grid_columnconfigure(0, weight=0)
    main_content.grid_columnconfigure(1, weight=1)
    main_content.grid_rowconfigure(0, weight=1)

    # Sidebar Estudiantes
    student_sidebar = tk.Frame(main_content, bg="#f5f7fa", width=250)
    student_sidebar.grid(row=0, column=0, sticky="nsew", padx=(20, 10), pady=(0, 20))
    student_sidebar.pack_propagate(False)

    tk.Label(student_sidebar, text="Buscar Estudiante", font=FONT_H3, bg="#f5f7fa",
             fg=COLOR_TEXT_DARK).pack(anchor="w", pady=(0, 10))
    ttk.Entry(student_sidebar, width=30).pack(fill="x", pady=(0, 15))

    students = [("Lucía Fernández Gómez", "Párvulos A"),
                ("Santiago Díaz Martínez", "Párvulos A", True),
                ("Valentina Castro López", "Caminadores A"),
                ("Mateo Vargas Silva", "Prejardín B")]

    for name, group, *active in students:
        bg_color = "#ffffff" if not active else "#007bff"
        fg_color = COLOR_TEXT_DARK if not active else COLOR_TEXT_LIGHT

        btn_frame = tk.Frame(student_sidebar, bg=bg_color, pady=5)
        btn_frame.pack(fill="x", pady=(0, 5))

        tk.Label(btn_frame, text=name, font=FONT_P_BOLD, bg=bg_color,
                 fg=fg_color).pack(anchor="w", padx=10)
        tk.Label(btn_frame, text=group, font=FONT_SMALL, bg=bg_color,
                 fg=fg_color).pack(anchor="w", padx=10)

    tk.Button(student_sidebar, text="← Volver al Dashboard", bg=COLOR_ACCENT_ADMIN,
              fg=COLOR_TEXT_LIGHT, font=FONT_P_BOLD, bd=0, highlightthickness=0,
              command=lambda: get_dashboard_command(nav_commands)()).pack(
                  fill="x", side="bottom", pady=(20, 0))

    # Área Detalle
    detail_area = tk.Frame(main_content, bg="#ffffff", padx=30, pady=30, relief="solid", bd=1,
                           highlightbackground=COLOR_TEST_BORDER, highlightthickness=1)
    detail_area.grid(row=0, column=1, sticky="nsew", padx=(0, 20), pady=(0, 20))

    info_frame = tk.Frame(detail_area, bg="#ffffff")
    info_frame.pack(fill="x", pady=(0, 20))

    tk.Label(info_frame, text="Observador del Estudiante", font=FONT_H1, bg="#ffffff",
             fg=COLOR_TEXT_DARK).pack(side="left", anchor="w")
    tk.Button(info_frame, text="+ Nueva Observación", bg="#007bff", fg=COLOR_TEXT_LIGHT,
              font=FONT_P_BOLD, bd=0).pack(side="right", ipady=5)

    tk.Label(detail_area, text="Historial de Observaciones", font=FONT_H3, bg="#ffffff",
             fg=COLOR_TEXT_DARK).pack(anchor="w", pady=(10, 5))

    obs_neg = tk.Frame(detail_area, bg="#f9e8e8", padx=15, pady=15, relief="solid", bd=1,
                       highlightbackground="#d39e9e", highlightthickness=1)
    obs_neg.pack(fill="x", pady=(5, 10))
    tk.Label(obs_neg, text="🔴 Negativa | Comportamental", font=FONT_P_BOLD, fg="#cc0000",
             bg="#f9e8e8").pack(anchor="w")
    tk.Label(obs_neg, text="", font=FONT_P,
             bg="#f9e8e8", wraplength=500, justify="left").pack(anchor="w", pady=(5, 5))

    obs_pos = tk.Frame(detail_area, bg="#e8f9e8", padx=15, pady=15, relief="solid", bd=1,
                       highlightbackground="#9ed39e", highlightthickness=1)
    obs_pos.pack(fill="x", pady=(5, 10))
    tk.Label(obs_pos, text="🟢 Positiva | Académico", font=FONT_P_BOLD, fg="#00cc00",
             bg="#e8f9e8").pack(anchor="w")
    tk.Label(obs_pos, text="", font=FONT_P,
             bg="#e8f9e8", wraplength=500, justify="left").pack(anchor="w", pady=(5, 5))

    return observer_frame
