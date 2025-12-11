import tkinter as tk
import tkinter.ttk as ttk
from config import * # Asegúrate de que config.py tiene las constantes

# ======================================================================
# --- FUNCIÓN PRINCIPAL: Formulario Completo con Scroll ---
# ======================================================================

def create_complete_form(master, nav_commands):
    """Crea un formulario completo en una sola pantalla con scroll vertical"""
    
    form_frame = tk.Frame(master, bg="#ffffff")
    
    # --- HEADER ---
    header_frame = tk.Frame(form_frame, bg=COLOR_HEADER_PRE, height=80)
    header_frame.pack(fill="x", side="top")
    header_frame.pack_propagate(False)
    tk.Button(header_frame, text="← Volver al Inicio", bg=COLOR_HEADER_PRE, fg=COLOR_TEXT_PRE, font=FONT_P_BOLD, 
              bd=0, highlightthickness=0, command=nav_commands['home']).pack(side="left", padx=20)
    tk.Label(header_frame, text="Formulario de Preinscripción - Colegio Pequeño", bg=COLOR_HEADER_PRE, fg=COLOR_TEXT_PRE, font=FONT_H1).pack(side="left", padx=50)
    
    # --- BARRA DE PROGRESO ---
    progress_bar = tk.Canvas(form_frame, height=5, bg="#ffffff", highlightthickness=0)
    progress_bar.pack(fill="x", padx=20, pady=(20, 20))
    
    # La barra de progreso estará al 100% ya que se ve todo de una vez
    progress_bar.create_rectangle(20, 0, 0, 5, fill=COLOR_HEADER_PRE, outline="", tags="progress_fill")
    
    def update_progress_bar(event):
        width = event.width
        progress_bar.coords("progress_fill", 20, 0, width - 20, 5)
    
    progress_bar.bind('<Configure>', update_progress_bar)
    
    # --- CONTENEDOR CON SCROLL ---
    scroll_container = tk.Frame(form_frame)
    scroll_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))
    
    scrollbar = ttk.Scrollbar(scroll_container, orient="vertical")
    scrollbar.pack(side="right", fill="y")
    
    canvas = tk.Canvas(scroll_container, yscrollcommand=scrollbar.set, bg="#ffffff", highlightthickness=0)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.config(command=canvas.yview)
    
    # Habilitar scroll con rueda del ratón
    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    canvas.bind_all("<MouseWheel>", _on_mousewheel)
    
    fields_frame_container = tk.Frame(canvas, bg="#ffffff")
    canvas_window = canvas.create_window((0, 0), window=fields_frame_container, anchor="nw", tags="fields_frame")
    
    def on_frame_configure(event):
        canvas.config(scrollregion=canvas.bbox("all"))
        canvas.itemconfig(canvas_window, width=canvas.winfo_width())

    def on_canvas_configure(event):
        canvas.itemconfig(canvas_window, width=event.width)

    fields_frame_container.bind("<Configure>", on_frame_configure)
    canvas.bind("<Configure>", on_canvas_configure)
    
    # --- AGREGAMOS TODOS LOS PASOS COMO SECCIONES ---
    _add_step1_section(fields_frame_container)
    _add_step2_section(fields_frame_container)
    _add_step3_section(fields_frame_container)
    _add_step4_section(fields_frame_container)
    
    # --- BOTÓN DE ENVÍO (Fijo al pie) ---
    nav_frame = tk.Frame(form_frame, bg="#ffffff", padx=50, pady=20)
    nav_frame.pack(fill="x", side="bottom")
    
    def on_submit():
        from dialogs import show_confirmation_dialog
        def redirect_home():
            nav_commands['home']()
        show_confirmation_dialog(
            form_frame,
            "Preinscripción Enviada",
            "Su formulario de preinscripción ha sido enviado exitosamente. Nos pondremos en contacto pronto.",
            on_confirm=redirect_home
        )
    ttk.Button(nav_frame, text="Enviar Preinscripción", style="Login.TButton", command=on_submit).pack(side="right")
    
    return form_frame, canvas


# ======================================================================
# --- FUNCIÓN AUXILIAR PARA CREAR SECCIONES DE PASOS ---
# ======================================================================

def _create_step_section(parent, step_number, title_text):
    """Crea una sección de paso dentro del formulario único"""
    
    form_box = tk.Frame(parent, bg="#ffffff", highlightbackground=COLOR_TEST_BORDER, highlightthickness=1)
    form_box.pack(pady=20, padx=0, fill="x")
    
    # Encabezado del paso
    tk.Label(form_box, text=f" Paso {step_number}: {title_text}", bg="#fcf0e5", fg=COLOR_HEADER_PRE, font=FONT_P_BOLD, anchor="w").pack(fill="x", ipady=10, padx=0)
    
    # Marco para los campos
    fields_frame = tk.Frame(form_box, bg="#ffffff", padx=30, pady=30)
    fields_frame.pack(fill="x")
    fields_frame.grid_columnconfigure(0, weight=1)
    fields_frame.grid_columnconfigure(1, weight=1)
    
    return fields_frame 

# ======================================================================
# --- PASO 1: Datos del Estudiante ---
# ======================================================================
def _add_step1_section(parent):
    """Añade la sección del Paso 1 al formulario único"""
    fields_frame = _create_step_section(parent, 1, "Datos del Estudiante")
    
    tk.Label(fields_frame, text="Nombre Completo del Estudiante *", bg="#ffffff", anchor="w", font=FONT_P_BOLD).grid(row=0, column=0, sticky="w", pady=(0, 5))
    ttk.Entry(fields_frame, width=35).grid(row=1, column=0, sticky="ew", padx=(0, 20), ipady=5)
    tk.Label(fields_frame, text="Fecha de Nacimiento *", bg="#ffffff", anchor="w", font=FONT_P_BOLD).grid(row=0, column=1, sticky="w", pady=(0, 5))
    ttk.Entry(fields_frame, width=35).grid(row=1, column=1, sticky="ew", ipady=5)
    tk.Label(fields_frame, text="Edad Actual", bg="#ffffff", anchor="w", font=FONT_P_BOLD).grid(row=2, column=0, sticky="w", pady=(20, 5))
    ttk.Entry(fields_frame, width=35, state="readonly").grid(row=3, column=0, sticky="ew", padx=(0, 20), ipady=5)
    tk.Label(fields_frame, text="Género *", bg="#ffffff", anchor="w", font=FONT_P_BOLD).grid(row=2, column=1, sticky="w", pady=(20, 5))
    ttk.Combobox(fields_frame, width=35, values=["Masculino", "Femenino"]).grid(row=3, column=1, sticky="ew", ipady=5)
    tk.Label(fields_frame, text="Grupo Deseado *", bg="#ffffff", anchor="w", font=FONT_P_BOLD).grid(row=4, column=0, sticky="w", pady=(20, 5))
    ttk.Combobox(fields_frame, width=35, values=["Grupo 1", "Grupo 2"]).grid(row=5, column=0, sticky="ew", padx=(0, 20), ipady=5)


# ======================================================================
# --- PASO 2: Datos de los Acudientes ---
# ======================================================================
def _add_step2_section(parent):
    """Añade la sección del Paso 2 al formulario único"""
    fields_frame = _create_step_section(parent, 2, "Datos de los Acudientes")
    
    tk.Label(fields_frame, text="Acudiente Principal *", bg="#ffffff", font=FONT_H3).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 10))
    tk.Label(fields_frame, text="Nombre Completo *", bg="#ffffff", anchor="w", font=FONT_P_BOLD).grid(row=1, column=0, sticky="w", pady=(0, 5))
    ttk.Entry(fields_frame, width=35).grid(row=2, column=0, sticky="ew", padx=(0, 20), ipady=5)
    tk.Label(fields_frame, text="Cédula de Ciudadanía *", bg="#ffffff", anchor="w", font=FONT_P_BOLD).grid(row=1, column=1, sticky="w", pady=(0, 5))
    ttk.Entry(fields_frame, width=35).grid(row=2, column=1, sticky="ew", ipady=5)

    tk.Label(fields_frame, text="Teléfono/Celular *", bg="#ffffff", anchor="w", font=FONT_P_BOLD).grid(row=3, column=0, sticky="w", pady=(20, 5))
    ttk.Entry(fields_frame, width=35).grid(row=4, column=0, sticky="ew", padx=(0, 20), ipady=5)
    tk.Label(fields_frame, text="Correo Electrónico *", bg="#ffffff", anchor="w", font=FONT_P_BOLD).grid(row=3, column=1, sticky="w", pady=(20, 5))
    ttk.Entry(fields_frame, width=35).grid(row=4, column=1, sticky="ew", ipady=5)

    tk.Label(fields_frame, text="Dirección de Residencia *", bg="#ffffff", anchor="w", font=FONT_P_BOLD).grid(row=5, column=0, sticky="w", pady=(20, 5))
    ttk.Entry(fields_frame, width=35).grid(row=6, column=0, sticky="ew", padx=(0, 20), ipady=5)
    tk.Label(fields_frame, text="Parentesco *", bg="#ffffff", anchor="w", font=FONT_P_BOLD).grid(row=5, column=1, sticky="w", pady=(20, 5))
    ttk.Combobox(fields_frame, width=35, values=["Padre", "Madre", "Otro"]).grid(row=6, column=1, sticky="ew", ipady=5)

    tk.Label(fields_frame, text="Acudiente Secundario (Opcional)", bg="#ffffff", font=FONT_H3).grid(row=7, column=0, columnspan=2, sticky="w", pady=(30, 10))

    tk.Label(fields_frame, text="Nombre Completo", bg="#ffffff", anchor="w", font=FONT_P_BOLD).grid(row=8, column=0, sticky="w", pady=(0, 5))
    ttk.Entry(fields_frame, width=35).grid(row=9, column=0, sticky="ew", padx=(0, 20), ipady=5)
    tk.Label(fields_frame, text="Teléfono/Celular", bg="#ffffff", anchor="w", font=FONT_P_BOLD).grid(row=8, column=1, sticky="w", pady=(0, 5))
    ttk.Entry(fields_frame, width=35).grid(row=9, column=1, sticky="ew", ipady=5)

    tk.Label(fields_frame, text="Correo Electrónico", bg="#ffffff", anchor="w", font=FONT_P_BOLD).grid(row=10, column=0, sticky="w", pady=(20, 5))
    ttk.Entry(fields_frame, width=35).grid(row=11, column=0, sticky="ew", padx=(0, 20), ipady=5)
    tk.Label(fields_frame, text="Parentesco", bg="#ffffff", anchor="w", font=FONT_P_BOLD).grid(row=10, column=1, sticky="w", pady=(20, 5))
    ttk.Combobox(fields_frame, width=35, values=["Padre", "Madre", "Otro"]).grid(row=11, column=1, sticky="ew", ipady=5)


# ======================================================================
# --- PASO 3: Información Médica y de Emergencia ---
# ======================================================================
def _add_step3_section(parent):
    """Añade la sección del Paso 3 al formulario único"""
    fields_frame = _create_step_section(parent, 3, "Información Médica y de Emergencia")
    
    tk.Label(fields_frame, text="Alergias Conocidas", bg="#ffffff", anchor="w", font=FONT_P_BOLD).grid(row=0, column=0, sticky="w", pady=(0, 5))
    tk.Text(fields_frame, height=5, width=35).grid(row=1, column=0, sticky="ew", padx=(0, 20), ipady=5)
    tk.Label(fields_frame, text="Medicamentos Actuales", bg="#ffffff", anchor="w", font=FONT_P_BOLD).grid(row=0, column=1, sticky="w", pady=(0, 5))
    tk.Text(fields_frame, height=5, width=35).grid(row=1, column=1, sticky="ew", ipady=5)
    
    tk.Label(fields_frame, text="Contacto de Emergencia *", bg="#ffffff", anchor="w", font=FONT_P_BOLD).grid(row=2, column=0, sticky="w", pady=(20, 5))
    ttk.Entry(fields_frame, width=35).grid(row=3, column=0, sticky="ew", padx=(0, 20), ipady=5)
    tk.Label(fields_frame, text="Teléfono de Emergencia *", bg="#ffffff", anchor="w", font=FONT_P_BOLD).grid(row=2, column=1, sticky="w", pady=(20, 5))
    ttk.Entry(fields_frame, width=35).grid(row=3, column=1, sticky="ew", ipady=5)

    tk.Label(fields_frame, text="Colegio o Jardín Anterior (si aplica)", bg="#ffffff", anchor="w", font=FONT_P_BOLD).grid(row=4, column=0, sticky="w", pady=(20, 5))
    ttk.Entry(fields_frame, width=35).grid(row=5, column=0, sticky="ew", padx=(0, 20), ipady=5)

    tk.Label(fields_frame, text="Observaciones Adicionales", bg="#ffffff", anchor="w", font=FONT_P_BOLD).grid(row=6, column=0, columnspan=2, sticky="w", pady=(20, 5))
    tk.Text(fields_frame, height=5).grid(row=7, column=0, columnspan=2, sticky="ew", ipady=5)


# ======================================================================
# --- PASO 4: Confirmación y Términos ---
# ======================================================================
def _add_step4_section(parent):
    """Añade la sección del Paso 4 al formulario único"""
    fields_frame = _create_step_section(parent, 4, "Confirmación y Términos")
    
    summary_frame = tk.Frame(fields_frame, bg="#ffffff", pady=0)
    summary_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 15))
    summary_frame.grid_columnconfigure(0, weight=1)
    summary_frame.grid_columnconfigure(1, weight=1)

    tk.Label(summary_frame, text="Resumen de la Preinscripción:", bg="#ffffff", font=FONT_H3).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 15))
    tk.Label(summary_frame, text="Estudiante:", bg="#ffffff", anchor="w", font=FONT_P_BOLD).grid(row=1, column=0, sticky="w", pady=5)
    tk.Label(summary_frame, text="Teléfono:", bg="#ffffff", anchor="w", font=FONT_P_BOLD).grid(row=1, column=1, sticky="w", pady=5)
    tk.Label(summary_frame, text="Grupo:", bg="#ffffff", anchor="w", font=FONT_P_BOLD).grid(row=2, column=0, sticky="w", pady=5)
    tk.Label(summary_frame, text="Email:", bg="#ffffff", anchor="w", font=FONT_P_BOLD).grid(row=2, column=1, sticky="w", pady=5)
    tk.Label(summary_frame, text="Acudiente:", bg="#ffffff", anchor="w", font=FONT_P_BOLD).grid(row=3, column=0, sticky="w", pady=5)
    tk.Label(summary_frame, text="Contacto emergencia:", bg="#ffffff", anchor="w", font=FONT_P_BOLD).grid(row=3, column=1, sticky="w", pady=5)

    terms_frame = tk.Frame(fields_frame, bg="#ffffff")
    terms_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(30, 0))
    tk.Label(terms_frame, text="Términos y Condiciones:", bg="#ffffff", font=FONT_H3).pack(anchor="w", pady=(0, 10))

    terms_text = tk.Text(terms_frame, height=8, wrap="word", borderwidth=1, relief="solid")
    terms_content = "• La preinscripción no garantiza el cupo en el colegio.\n• Se requiere completar el proceso de documentación en las fechas asignadas.\n• Los datos proporcionados serán verificados durante el proceso de matrícula.\n• El colegio se reserva el derecho de solicitar documentación adicional.\n• La información médica es confidencial y será usada solo para el cuidado del estudiante.\n\n[Más términos aquí para simular el scroll...]"
    terms_text.insert("1.0", terms_content)
    terms_text.config(state="disabled") 
    terms_text.pack(fill="x")

    check_var = tk.BooleanVar()
    ttk.Checkbutton(fields_frame, text="Acepto los términos y condiciones, y autorizo el tratamiento de datos personales *", 
                    variable=check_var).grid(row=2, column=0, columnspan=2, sticky="w", pady=20)