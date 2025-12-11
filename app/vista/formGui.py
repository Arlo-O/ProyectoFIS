import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from .config import *


def create_base_step(master, step_number, title_text, nav_commands):
    """Crea la estructura base para cada paso del formulario."""
    step_frame = tk.Frame(master, bg="#ffffff")
    
    # Header
    header_frame = tk.Frame(step_frame, bg=COLOR_HEADER_PRE, height=80)
    header_frame.pack(fill="x", side="top")
    header_frame.pack_propagate(False)
    tk.Button(
        header_frame, 
        text="← Volver al Inicio", 
        bg=COLOR_HEADER_PRE, 
        fg=COLOR_TEXT_PRE, 
        font=FONT_P_BOLD,
        bd=0, 
        highlightthickness=0, 
        command=nav_commands['home']
    ).pack(side="left", padx=20)
    tk.Label(
        header_frame, 
        text="Formulario de Preinscripción - Colegio Pequeño", 
        bg=COLOR_HEADER_PRE, 
        fg=COLOR_TEXT_PRE, 
        font=FONT_H1
    ).pack(side="left", padx=50)
    
    # Step info
    step_info_frame = tk.Frame(step_frame, bg="#ffffff", pady=20)
    step_info_frame.pack(fill="x")
    tk.Label(
        step_info_frame, 
        text=f"Paso {step_number} de 4", 
        bg="#ffffff", 
        fg=COLOR_TEXT_DARK, 
        font=FONT_H2
    ).pack(side="left", padx=20)
    tk.Label(
        step_info_frame, 
        text="Proceso de Preinscripción", 
        bg="#ffffff", 
        fg=COLOR_TEXT_MUTED, 
        font=FONT_P
    ).pack(side="right", padx=20)

    # Progress bar
    progress_bar = tk.Canvas(step_frame, height=5, bg="#ffffff", highlightthickness=0)
    progress_bar.pack(fill="x", padx=20, pady=(0, 20))
    progress_width_ratio = step_number / 4 
    
    def update_progress_bar(event):
        width = event.width
        progress_bar.coords(
            progress_bar.find_all()[0], 
            20, 0, 
            (width - 40) * progress_width_ratio + 20, 5
        )

    progress_bar.create_rectangle(20, 0, 20, 5, fill=COLOR_HEADER_PRE, outline="")
    progress_bar.bind('<Configure>', update_progress_bar)
    
    # Scroll container
    scroll_container = tk.Frame(step_frame)
    scroll_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))
    
    scrollbar = ttk.Scrollbar(scroll_container, orient="vertical")
    scrollbar.pack(side="right", fill="y")
    
    canvas = tk.Canvas(scroll_container, yscrollcommand=scrollbar.set, bg="#ffffff", highlightthickness=0)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.config(command=canvas.yview)
    
    fields_frame_container = tk.Frame(canvas, bg="#ffffff")
    canvas_window = canvas.create_window((0, 0), window=fields_frame_container, anchor="nw")
    
    def on_frame_configure(event):
        canvas.config(scrollregion=canvas.bbox("all"))
        canvas.itemconfig(canvas_window, width=canvas.winfo_width())

    def on_canvas_configure(event):
        canvas.itemconfig(canvas_window, width=event.width)

    fields_frame_container.bind("<Configure>", on_frame_configure)
    canvas.bind("<Configure>", on_canvas_configure)

    # Form box
    form_box = tk.Frame(fields_frame_container, bg="#ffffff", highlightbackground=COLOR_TEST_BORDER, highlightthickness=1)
    form_box.pack(pady=20, padx=20, fill="x")
    
    master.update_idletasks()
    tk.Label(
        form_box, 
        text=f"Paso {step_number}: {title_text}", 
        bg="#fcf0e5", 
        fg=COLOR_HEADER_PRE, 
        font=FONT_P_BOLD, 
        anchor="w"
    ).pack(fill="x", ipady=10)
    
    # Fields frame
    fields_frame = tk.Frame(form_box, bg="#ffffff", padx=30, pady=30)
    fields_frame.pack(fill="x")
    fields_frame.grid_columnconfigure(0, weight=1)
    fields_frame.grid_columnconfigure(1, weight=1)

    # Navigation
    nav_frame = tk.Frame(step_frame, bg="#ffffff", padx=50, pady=20)
    nav_frame.pack(fill="x", side="bottom")

    if step_number > 1:
        ttk.Button(nav_frame, text="Anterior", command=nav_commands['prev']).pack(side="left")
    
    if step_number < 4:
        ttk.Button(nav_frame, text="Siguiente", style="Pre.TButton", command=nav_commands['next']).pack(side="right")
    elif step_number == 4:
        def on_submit():
            try:
                from .dialogs import show_confirmation_dialog
                def redirect_home():
                    nav_commands['home']()
                show_confirmation_dialog(
                    step_frame,
                    "Preinscripción Enviada",
                    "Su formulario de preinscripción ha sido enviado exitosamente. Nos pondremos en contacto pronto.",
                    on_confirm=redirect_home
                )
            except ImportError:
                messagebox.showinfo("Éxito", "Preinscripción enviada correctamente")
        
        ttk.Button(nav_frame, text="Enviar Preinscripción", style="Login.TButton", command=on_submit).pack(side="right")

    return step_frame, fields_frame, canvas, fields_frame_container


def create_step1(master, nav_commands):
    """Paso 1: Datos del Estudiante"""
    step_frame, parent, canvas, fields_frame_container = create_base_step(master, 1, "Datos del Estudiante", nav_commands)
    
    # Nombre
    tk.Label(parent, text="Nombre Completo del Estudiante *", bg="#ffffff", anchor="w", font=FONT_P_BOLD).grid(row=0, column=0, sticky="w", pady=(0, 5))
    ttk.Entry(parent, width=35).grid(row=1, column=0, sticky="ew", padx=(0, 20), ipady=5)
    
    # Fecha nacimiento
    tk.Label(parent, text="Fecha de Nacimiento *", bg="#ffffff", anchor="w", font=FONT_P_BOLD).grid(row=0, column=1, sticky="w", pady=(0, 5))
    ttk.Entry(parent, width=35).grid(row=1, column=1, sticky="ew", ipady=5)
    
    # Edad y género
    tk.Label(parent, text="Edad Actual", bg="#ffffff", anchor="w", font=FONT_P_BOLD).grid(row=2, column=0, sticky="w", pady=(20, 5))
    ttk.Entry(parent, width=35, state="readonly").grid(row=3, column=0, sticky="ew", padx=(0, 20), ipady=5)
    tk.Label(parent, text="Género *", bg="#ffffff", anchor="w", font=FONT_P_BOLD).grid(row=2, column=1, sticky="w", pady=(20, 5))
    ttk.Combobox(parent, width=35, values=["Masculino", "Femenino"]).grid(row=3, column=1, sticky="ew", ipady=5)
    
    # Grupo
    tk.Label(parent, text="Grupo Deseado *", bg="#ffffff", anchor="w", font=FONT_P_BOLD).grid(row=4, column=0, sticky="w", pady=(20, 5))
    ttk.Combobox(parent, width=35, values=["Grupo 1", "Grupo 2", "Grupo 3"]).grid(row=5, column=0, sticky="ew", padx=(0, 20), ipady=5)

    return step_frame, parent, canvas, fields_frame_container


def create_step2(master, nav_commands):
    """Paso 2: Datos de los Acudientes"""
    step_frame, parent, canvas, fields_frame_container = create_base_step(master, 2, "Datos de los Acudientes", nav_commands)
    
    # Acudiente Principal
    tk.Label(parent, text="Acudiente Principal *", bg="#ffffff", font=FONT_H3).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 10))
    tk.Label(parent, text="Nombre Completo *", bg="#ffffff", anchor="w", font=FONT_P_BOLD).grid(row=1, column=0, sticky="w", pady=(0, 5))
    ttk.Entry(parent, width=35).grid(row=2, column=0, sticky="ew", padx=(0, 20), ipady=5)
    tk.Label(parent, text="Cédula de Ciudadanía *", bg="#ffffff", anchor="w", font=FONT_P_BOLD).grid(row=1, column=1, sticky="w", pady=(0, 5))
    ttk.Entry(parent, width=35).grid(row=2, column=1, sticky="ew", ipady=5)

    tk.Label(parent, text="Teléfono/Celular *", bg="#ffffff", anchor="w", font=FONT_P_BOLD).grid(row=3, column=0, sticky="w", pady=(20, 5))
    ttk.Entry(parent, width=35).grid(row=4, column=0, sticky="ew", padx=(0, 20), ipady=5)
    tk.Label(parent, text="Correo Electrónico *", bg="#ffffff", anchor="w", font=FONT_P_BOLD).grid(row=3, column=1, sticky="w", pady=(20, 5))
    ttk.Entry(parent, width=35).grid(row=4, column=1, sticky="ew", ipady=5)

    tk.Label(parent, text="Dirección de Residencia *", bg="#ffffff", anchor="w", font=FONT_P_BOLD).grid(row=5, column=0, sticky="w", pady=(20, 5))
    ttk.Entry(parent, width=35).grid(row=6, column=0, sticky="ew", padx=(0, 20), ipady=5)
    tk.Label(parent, text="Parentesco *", bg="#ffffff", anchor="w", font=FONT_P_BOLD).grid(row=5, column=1, sticky="w", pady=(20, 5))
    ttk.Combobox(parent, width=35, values=["Padre", "Madre", "Tutor Legal", "Otro"]).grid(row=6, column=1, sticky="ew", ipady=5)

    # Acudiente Secundario
    tk.Label(parent, text="Acudiente Secundario (Opcional)", bg="#ffffff", font=FONT_H3).grid(row=7, column=0, columnspan=2, sticky="w", pady=(30, 10))
    tk.Label(parent, text="Nombre Completo", bg="#ffffff", anchor="w", font=FONT_P_BOLD).grid(row=8, column=0, sticky="w", pady=(0, 5))
    ttk.Entry(parent, width=35).grid(row=9, column=0, sticky="ew", padx=(0, 20), ipady=5)
    tk.Label(parent, text="Teléfono/Celular", bg="#ffffff", anchor="w", font=FONT_P_BOLD).grid(row=8, column=1, sticky="w", pady=(0, 5))
    ttk.Entry(parent, width=35).grid(row=9, column=1, sticky="ew", ipady=5)

    tk.Label(parent, text="Correo Electrónico", bg="#ffffff", anchor="w", font=FONT_P_BOLD).grid(row=10, column=0, sticky="w", pady=(20, 5))
    ttk.Entry(parent, width=35).grid(row=11, column=0, sticky="ew", padx=(0, 20), ipady=5)
    tk.Label(parent, text="Parentesco", bg="#ffffff", anchor="w", font=FONT_P_BOLD).grid(row=10, column=1, sticky="w", pady=(20, 5))
    ttk.Combobox(parent, width=35, values=["Padre", "Madre", "Tutor Legal", "Otro"]).grid(row=11, column=1, sticky="ew", ipady=5)
    
    return step_frame, parent, canvas, fields_frame_container


def create_step3(master, nav_commands):
    """Paso 3: Información Médica y Emergencia"""
    step_frame, parent, canvas, fields_frame_container = create_base_step(master, 3, "Información Médica y de Emergencia", nav_commands)
    
    # Información médica
    tk.Label(parent, text="Alergias Conocidas", bg="#ffffff", anchor="w", font=FONT_P_BOLD).grid(row=0, column=0, sticky="w", pady=(0, 5))
    tk.Text(parent, height=3, width=35).grid(row=1, column=0, sticky="ew", padx=(0, 20), pady=(0, 20))
    tk.Label(parent, text="Medicamentos Actuales", bg="#ffffff", anchor="w", font=FONT_P_BOLD).grid(row=0, column=1, sticky="w", pady=(0, 5))
    tk.Text(parent, height=3, width=35).grid(row=1, column=1, sticky="ew", pady=(0, 20))

    # Emergencia
    tk.Label(parent, text="Contacto de Emergencia *", bg="#ffffff", anchor="w", font=FONT_P_BOLD).grid(row=2, column=0, sticky="w", pady=(0, 5))
    ttk.Entry(parent, width=35).grid(row=3, column=0, sticky="ew", padx=(0, 20), ipady=5)
    tk.Label(parent, text="Teléfono de Emergencia *", bg="#ffffff", anchor="w", font=FONT_P_BOLD).grid(row=2, column=1, sticky="w", pady=(0, 5))
    ttk.Entry(parent, width=35).grid(row=3, column=1, sticky="ew", ipady=5)

    tk.Label(parent, text="Colegio o Jardín Anterior (si aplica)", bg="#ffffff", anchor="w", font=FONT_P_BOLD).grid(row=4, column=0, sticky="w", pady=(20, 5))
    ttk.Entry(parent, width=35).grid(row=5, column=0, sticky="ew", padx=(0, 20), ipady=5)

    # Observaciones
    tk.Label(parent, text="Observaciones Adicionales", bg="#ffffff", anchor="w", font=FONT_P_BOLD).grid(row=6, column=0, columnspan=2, sticky="w", pady=(20, 5))
    tk.Text(parent, height=4, width=70).grid(row=7, column=0, columnspan=2, sticky="ew", pady=10)
    
    return step_frame, parent, canvas, fields_frame_container


def create_step4(master, nav_commands):
    """Paso 4: Confirmación y Términos"""
    step_frame, parent, canvas, fields_frame_container = create_base_step(master, 4, "Confirmación y Términos", nav_commands)
    
    # Resumen
    summary_frame = tk.Frame(parent, bg="#ffffff")
    summary_frame.pack(fill="x", pady=20)
    summary_frame.grid_columnconfigure(0, weight=1)
    summary_frame.grid_columnconfigure(1, weight=1)

    tk.Label(summary_frame, text="Resumen de la Preinscripción:", bg="#ffffff", font=FONT_H3).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 15))
    tk.Label(summary_frame, text="Estudiante:", bg="#ffffff", anchor="w", font=FONT_P_BOLD).grid(row=1, column=0, sticky="w", pady=5)
    tk.Label(summary_frame, text="[Nombre del estudiante]", bg="#ffffff", anchor="w").grid(row=1, column=1, sticky="w", pady=5)
    tk.Label(summary_frame, text="Grupo:", bg="#ffffff", anchor="w", font=FONT_P_BOLD).grid(row=2, column=0, sticky="w", pady=5)
    tk.Label(summary_frame, text="[Grupo seleccionado]", bg="#ffffff", anchor="w").grid(row=2, column=1, sticky="w", pady=5)
    tk.Label(summary_frame, text="Acudiente Principal:", bg="#ffffff", anchor="w", font=FONT_P_BOLD).grid(row=3, column=0, sticky="w", pady=5)
    tk.Label(summary_frame, text="[Nombre acudiente]", bg="#ffffff", anchor="w").grid(row=3, column=1, sticky="w", pady=5)
    tk.Label(summary_frame, text="Contacto Emergencia:", bg="#ffffff", anchor="w", font=FONT_P_BOLD).grid(row=4, column=0, sticky="w", pady=5)
    tk.Label(summary_frame, text="[Contacto emergencia]", bg="#ffffff", anchor="w").grid(row=4, column=1, sticky="w", pady=5)

    # Términos
    terms_frame = tk.Frame(parent, bg="#ffffff")
    terms_frame.pack(fill="x", pady=(30, 0))
    tk.Label(terms_frame, text="Términos y Condiciones:", bg="#ffffff", font=FONT_H3).pack(anchor="w", pady=(0, 10))

    terms_text = tk.Text(terms_frame, height=8, wrap="word", borderwidth=1, relief="solid")
    terms_content = """• La preinscripción no garantiza el cupo en el colegio.
• Se requiere completar el proceso de documentación en las fechas asignadas.
• Los datos proporcionados serán verificados durante el proceso de matrícula.
• El colegio se reserva el derecho de solicitar documentación adicional.
• La información médica es confidencial y será usada solo para el cuidado del estudiante.
• Autorizo el tratamiento de datos personales según la ley 1581 de 2012."""
    terms_text.insert("1.0", terms_content)
    terms_text.config(state="disabled")
    terms_text.pack(fill="x")

    # Checkbox aceptación
    check_var = tk.BooleanVar()
    ttk.Checkbutton(
        parent, 
        text="Acepto los términos y condiciones, y autorizo el tratamiento de datos personales *", 
        variable=check_var
    ).pack(anchor="w", pady=20)
    
    return step_frame, parent, canvas, fields_frame_container
