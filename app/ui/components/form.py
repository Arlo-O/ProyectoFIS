import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from ..config import *
from datetime import datetime
import re
from ...services.servicio_preinscripcion import ServicioPreinscripcion


# ============================================
# VALIDADORES
# ============================================

class FormValidators:
    """Validadores para el formulario de preinscripción"""
    
    @staticmethod
    def validar_nombre(nombre):
        """Valida que el nombre no esté vacío y tenga caracteres válidos"""
        if not nombre or not nombre.strip():
            return False, "El nombre no puede estar vacío"
        if len(nombre) < 3:
            return False, "El nombre debe tener al menos 3 caracteres"
        if not all(c.isalpha() or c.isspace() for c in nombre):
            return False, "El nombre solo puede contener letras"
        return True, None
    
    @staticmethod
    def validar_cedula(cedula):
        """Valida que la cédula sea válida (solo números)"""
        if not cedula or not cedula.strip():
            return False, "La cédula no puede estar vacía"
        if not cedula.isdigit():
            return False, "La cédula solo puede contener números"
        if len(cedula) < 8:
            return False, "La cédula debe tener al menos 8 dígitos"
        return True, None
    
    @staticmethod
    def validar_email(email):
        """Valida que el email tenga un formato correcto"""
        if not email or not email.strip():
            return False, "El email no puede estar vacío"
        patron_email = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(patron_email, email):
            return False, "El email no tiene un formato válido"
        return True, None
    
    @staticmethod
    def validar_telefono(telefono):
        """Valida que el teléfono sea válido (solo números y - o espacios)"""
        if not telefono or not telefono.strip():
            return False, "El teléfono no puede estar vacío"
        if not all(c.isdigit() or c in "- " for c in telefono):
            return False, "El teléfono solo puede contener números, guiones y espacios"
        numeros_solo = telefono.replace("-", "").replace(" ", "")
        if len(numeros_solo) < 7:
            return False, "El teléfono debe tener al menos 7 dígitos"
        return True, None
    
    @staticmethod
    def validar_fecha(fecha_str):
        """Valida que la fecha tenga un formato válido (DD/MM/YYYY)"""
        if not fecha_str or not fecha_str.strip():
            return False, "La fecha no puede estar vacía"
        try:
            fecha = datetime.strptime(fecha_str, "%d/%m/%Y")
            hoy = datetime.now()
            edad = (hoy.year - fecha.year) - ((hoy.month, hoy.day) < (fecha.month, fecha.day))
            if edad < 4:
                return False, "El estudiante debe tener al menos 4 años"
            if edad > 20:
                return False, "La edad del estudiante no es válida para este nivel"
            return True, None
        except ValueError:
            return False, "Formato de fecha inválido (use DD/MM/YYYY)"


# ============================================
# FORMULARIO UNIFICADO SCROLLABLE
# ============================================

def create_unified_form(master, nav_commands):
    """
    Crea un formulario de preinscripción unificado en una sola página scrollable.
    Implementa validaciones según diagrama de actividades.
    """
    
    # Frame principal
    form_frame = tk.Frame(master, bg="#ffffff")
    
    # ============ HEADER ============
    header_frame = tk.Frame(form_frame, bg=COLOR_HEADER_PRE, height=100)
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
    ).pack(side="left", padx=20, pady=10)
    
    tk.Label(
        header_frame, 
        text="Formulario de Preinscripción - Colegio Pequeño", 
        bg=COLOR_HEADER_PRE, 
        fg=COLOR_TEXT_PRE, 
        font=FONT_H1
    ).pack(side="left", padx=50, pady=10)
    
    # ============ SCROLLABLE CONTAINER ============
    scroll_container = tk.Frame(form_frame)
    scroll_container.pack(fill="both", expand=True, padx=20, pady=20)
    
    scrollbar = ttk.Scrollbar(scroll_container, orient="vertical")
    scrollbar.pack(side="right", fill="y")
    
    canvas = tk.Canvas(
        scroll_container, 
        yscrollcommand=scrollbar.set, 
        bg="#ffffff", 
        highlightthickness=0,
        height=500
    )
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.config(command=canvas.yview)
    
    # Frame para contener todos los campos
    main_content_frame = tk.Frame(canvas, bg="#ffffff")
    canvas_window = canvas.create_window((0, 0), window=main_content_frame, anchor="nw")
    
    def on_frame_configure(event):
        canvas.config(scrollregion=canvas.bbox("all"))
        canvas.itemconfig(canvas_window, width=canvas.winfo_width())
    
    main_content_frame.bind("<Configure>", on_frame_configure)
    canvas.bind("<Configure>", lambda e: canvas.itemconfig(canvas_window, width=e.width))
    
    # Permitir scroll con rueda del mouse - Mecanismo inteligente
    # Variable para rastrear si el mouse está sobre el canvas
    mouse_over_canvas = [False]
    
    def _on_mouseenter(event):
        """Se ejecuta cuando el mouse entra al canvas"""
        mouse_over_canvas[0] = True
    
    def _on_mouseleave(event):
        """Se ejecuta cuando el mouse sale del canvas"""
        mouse_over_canvas[0] = False
    
    def _on_mousewheel(event):
        """Maneja scroll con rueda del mouse en Windows"""
        if mouse_over_canvas[0]:
            try:
                canvas.yview_scroll(int(-1*(event.delta/120)), "units")
                return "break"  # Prevenir que el evento se propague
            except Exception as e:
                print(f"Error en scroll: {e}")
    
    def _on_mousewheel_linux(event):
        """Maneja scroll con rueda del mouse en Linux"""
        if mouse_over_canvas[0]:
            try:
                if event.num == 4:
                    canvas.yview_scroll(-3, "units")
                elif event.num == 5:
                    canvas.yview_scroll(3, "units")
                return "break"  # Prevenir que el evento se propague
            except Exception as e:
                print(f"Error en scroll Linux: {e}")
    
    # Vincular eventos Enter/Leave al canvas para rastrear mouse
    canvas.bind("<Enter>", _on_mouseenter)
    canvas.bind("<Leave>", _on_mouseleave)
    main_content_frame.bind("<Enter>", _on_mouseenter)
    main_content_frame.bind("<Leave>", _on_mouseleave)
    
    # Vincular scroll solo al canvas (no a nivel global)
    canvas.bind("<MouseWheel>", _on_mousewheel)
    canvas.bind("<Button-4>", _on_mousewheel_linux)
    canvas.bind("<Button-5>", _on_mousewheel_linux)
    
    # Recursivamente vincular scroll a todos los widgets dentro del canvas
    def _bind_scroll_events(widget):
        """Vincula eventos de scroll a todos los widgets dentro del canvas"""
        try:
            widget.bind("<Enter>", _on_mouseenter)
            widget.bind("<Leave>", _on_mouseleave)
            widget.bind("<MouseWheel>", _on_mousewheel)
            widget.bind("<Button-4>", _on_mousewheel_linux)
            widget.bind("<Button-5>", _on_mousewheel_linux)
        except:
            pass
        
        # Recursivamente vincular a widgets hijos
        try:
            for child in widget.winfo_children():
                _bind_scroll_events(child)
        except:
            pass
    
    # Bind recursivo después de que los widgets se hayan creado
    form_frame.after(100, lambda: _bind_scroll_events(main_content_frame))
    
    # ============ SECCIONES DEL FORMULARIO ============
    
    # Diccionario para guardar referencias a los widgets Entry/Combobox
    form_data = {}
    error_labels = {}
    
    # --- SECCIÓN 1: DATOS DEL ESTUDIANTE ---
    section1 = tk.Frame(main_content_frame, bg="#fcf0e5", highlightbackground=COLOR_TEST_BORDER, highlightthickness=1)
    section1.pack(fill="x", pady=10, padx=10)
    
    tk.Label(
        section1,
        text="Sección 1: Datos del Estudiante",
        bg="#fcf0e5",
        fg=COLOR_HEADER_PRE,
        font=FONT_P_BOLD,
        anchor="w"
    ).pack(fill="x", ipady=10, padx=10)
    
    fields1 = tk.Frame(section1, bg="#ffffff", padx=20, pady=15)
    fields1.pack(fill="x")
    fields1.grid_columnconfigure(0, weight=1)
    fields1.grid_columnconfigure(1, weight=1)
    
    # Nombre del estudiante
    tk.Label(fields1, text="Nombre Completo del Estudiante *", bg="#ffffff", font=FONT_P_BOLD, anchor="w").grid(row=0, column=0, sticky="w", pady=(0, 5))
    form_data['nombre_estudiante'] = ttk.Entry(fields1, width=40)
    form_data['nombre_estudiante'].grid(row=1, column=0, sticky="ew", padx=(0, 10), ipady=5)
    error_labels['nombre_estudiante'] = tk.Label(fields1, text="", bg="#ffffff", fg="red", font=FONT_P, anchor="w")
    error_labels['nombre_estudiante'].grid(row=2, column=0, sticky="w")
    
    # Tipo de identificación
    tk.Label(fields1, text="Tipo de Identificación *", bg="#ffffff", font=FONT_P_BOLD, anchor="w").grid(row=0, column=1, sticky="w", pady=(0, 5))
    form_data['tipo_id'] = ttk.Combobox(fields1, width=38, values=["Cédula de Ciudadanía", "Tarjeta de Identidad", "Pasaporte", "Registro Civil"])
    form_data['tipo_id'].grid(row=1, column=1, sticky="ew", ipady=5)
    error_labels['tipo_id'] = tk.Label(fields1, text="", bg="#ffffff", fg="red", font=FONT_P, anchor="w")
    error_labels['tipo_id'].grid(row=2, column=1, sticky="w")
    
    # Número de identificación
    tk.Label(fields1, text="Número de Identificación *", bg="#ffffff", font=FONT_P_BOLD, anchor="w").grid(row=3, column=0, sticky="w", pady=(10, 5))
    form_data['numero_id'] = ttk.Entry(fields1, width=40)
    form_data['numero_id'].grid(row=4, column=0, sticky="ew", padx=(0, 10), ipady=5)
    error_labels['numero_id'] = tk.Label(fields1, text="", bg="#ffffff", fg="red", font=FONT_P, anchor="w")
    error_labels['numero_id'].grid(row=5, column=0, sticky="w")
    
    # Fecha de nacimiento
    tk.Label(fields1, text="Fecha de Nacimiento (DD/MM/YYYY) *", bg="#ffffff", font=FONT_P_BOLD, anchor="w").grid(row=3, column=1, sticky="w", pady=(10, 5))
    form_data['fecha_nacimiento'] = ttk.Entry(fields1, width=38)
    form_data['fecha_nacimiento'].grid(row=4, column=1, sticky="ew", ipady=5)
    error_labels['fecha_nacimiento'] = tk.Label(fields1, text="", bg="#ffffff", fg="red", font=FONT_P, anchor="w")
    error_labels['fecha_nacimiento'].grid(row=5, column=1, sticky="w")
    
    # Género
    tk.Label(fields1, text="Género *", bg="#ffffff", font=FONT_P_BOLD, anchor="w").grid(row=6, column=0, sticky="w", pady=(10, 5))
    form_data['genero'] = ttk.Combobox(fields1, width=40, values=["Masculino", "Femenino", "Otro"])
    form_data['genero'].grid(row=7, column=0, sticky="ew", padx=(0, 10), ipady=5)
    error_labels['genero'] = tk.Label(fields1, text="", bg="#ffffff", fg="red", font=FONT_P, anchor="w")
    error_labels['genero'].grid(row=8, column=0, sticky="w")
    
    # Grado deseado
    tk.Label(fields1, text="Grado Deseado *", bg="#ffffff", font=FONT_P_BOLD, anchor="w").grid(row=6, column=1, sticky="w", pady=(10, 5))
    form_data['grado'] = ttk.Combobox(fields1, width=38, values=["Preescolar", "1°", "2°", "3°", "4°", "5°", "6°", "7°", "8°", "9°", "10°", "11°"])
    form_data['grado'].grid(row=7, column=1, sticky="ew", ipady=5)
    error_labels['grado'] = tk.Label(fields1, text="", bg="#ffffff", fg="red", font=FONT_P, anchor="w")
    error_labels['grado'].grid(row=8, column=1, sticky="w")
    
    # --- SECCIÓN 2: ACUDIENTE PRINCIPAL ---
    section2 = tk.Frame(main_content_frame, bg="#fcf0e5", highlightbackground=COLOR_TEST_BORDER, highlightthickness=1)
    section2.pack(fill="x", pady=10, padx=10)
    
    tk.Label(
        section2,
        text="Sección 2: Acudiente Principal",
        bg="#fcf0e5",
        fg=COLOR_HEADER_PRE,
        font=FONT_P_BOLD,
        anchor="w"
    ).pack(fill="x", ipady=10, padx=10)
    
    fields2 = tk.Frame(section2, bg="#ffffff", padx=20, pady=15)
    fields2.pack(fill="x")
    fields2.grid_columnconfigure(0, weight=1)
    fields2.grid_columnconfigure(1, weight=1)
    
    # Nombre acudiente
    tk.Label(fields2, text="Nombre Completo del Acudiente *", bg="#ffffff", font=FONT_P_BOLD, anchor="w").grid(row=0, column=0, sticky="w", pady=(0, 5))
    form_data['nombre_acudiente'] = ttk.Entry(fields2, width=40)
    form_data['nombre_acudiente'].grid(row=1, column=0, sticky="ew", padx=(0, 10), ipady=5)
    error_labels['nombre_acudiente'] = tk.Label(fields2, text="", bg="#ffffff", fg="red", font=FONT_P, anchor="w")
    error_labels['nombre_acudiente'].grid(row=2, column=0, sticky="w")
    
    # Cédula acudiente
    tk.Label(fields2, text="Cédula de Ciudadanía del Acudiente *", bg="#ffffff", font=FONT_P_BOLD, anchor="w").grid(row=0, column=1, sticky="w", pady=(0, 5))
    form_data['cedula_acudiente'] = ttk.Entry(fields2, width=38)
    form_data['cedula_acudiente'].grid(row=1, column=1, sticky="ew", ipady=5)
    error_labels['cedula_acudiente'] = tk.Label(fields2, text="", bg="#ffffff", fg="red", font=FONT_P, anchor="w")
    error_labels['cedula_acudiente'].grid(row=2, column=1, sticky="w")
    
    # Teléfono
    tk.Label(fields2, text="Teléfono/Celular *", bg="#ffffff", font=FONT_P_BOLD, anchor="w").grid(row=3, column=0, sticky="w", pady=(10, 5))
    form_data['telefono'] = ttk.Entry(fields2, width=40)
    form_data['telefono'].grid(row=4, column=0, sticky="ew", padx=(0, 10), ipady=5)
    error_labels['telefono'] = tk.Label(fields2, text="", bg="#ffffff", fg="red", font=FONT_P, anchor="w")
    error_labels['telefono'].grid(row=5, column=0, sticky="w")
    
    # Email
    tk.Label(fields2, text="Correo Electrónico *", bg="#ffffff", font=FONT_P_BOLD, anchor="w").grid(row=3, column=1, sticky="w", pady=(10, 5))
    form_data['email'] = ttk.Entry(fields2, width=38)
    form_data['email'].grid(row=4, column=1, sticky="ew", ipady=5)
    error_labels['email'] = tk.Label(fields2, text="", bg="#ffffff", fg="red", font=FONT_P, anchor="w")
    error_labels['email'].grid(row=5, column=1, sticky="w")
    
    # Dirección
    tk.Label(fields2, text="Dirección de Residencia *", bg="#ffffff", font=FONT_P_BOLD, anchor="w").grid(row=6, column=0, sticky="w", pady=(10, 5))
    form_data['direccion'] = ttk.Entry(fields2, width=40)
    form_data['direccion'].grid(row=7, column=0, sticky="ew", padx=(0, 10), ipady=5)
    error_labels['direccion'] = tk.Label(fields2, text="", bg="#ffffff", fg="red", font=FONT_P, anchor="w")
    error_labels['direccion'].grid(row=8, column=0, sticky="w")
    
    # Parentesco
    tk.Label(fields2, text="Parentesco *", bg="#ffffff", font=FONT_P_BOLD, anchor="w").grid(row=6, column=1, sticky="w", pady=(10, 5))
    form_data['parentesco'] = ttk.Combobox(fields2, width=38, values=["Padre", "Madre", "Tutor Legal", "Abuelo/a", "Otro"])
    form_data['parentesco'].grid(row=7, column=1, sticky="ew", ipady=5)
    error_labels['parentesco'] = tk.Label(fields2, text="", bg="#ffffff", fg="red", font=FONT_P, anchor="w")
    error_labels['parentesco'].grid(row=8, column=1, sticky="w")
    
    # --- SECCIÓN 2B: ACUDIENTE SECUNDARIO (OPCIONAL) ---
    section2b = tk.Frame(main_content_frame, bg="#fcf0e5", highlightbackground=COLOR_TEST_BORDER, highlightthickness=1)
    section2b.pack(fill="x", pady=10, padx=10)
    
    tk.Label(
        section2b,
        text="Sección 2B: Acudiente Secundario (Opcional)",
        bg="#fcf0e5",
        fg=COLOR_HEADER_PRE,
        font=FONT_P_BOLD,
        anchor="w"
    ).pack(fill="x", ipady=10, padx=10)
    
    fields2b = tk.Frame(section2b, bg="#ffffff", padx=20, pady=15)
    fields2b.pack(fill="x")
    fields2b.grid_columnconfigure(0, weight=1)
    fields2b.grid_columnconfigure(1, weight=1)
    
    # Nombre acudiente secundario
    tk.Label(fields2b, text="Nombre Completo del Acudiente Secundario", bg="#ffffff", font=FONT_P_BOLD, anchor="w").grid(row=0, column=0, sticky="w", pady=(0, 5))
    form_data['nombre_acudiente2'] = ttk.Entry(fields2b, width=40)
    form_data['nombre_acudiente2'].grid(row=1, column=0, sticky="ew", padx=(0, 10), ipady=5)
    error_labels['nombre_acudiente2'] = tk.Label(fields2b, text="", bg="#ffffff", fg="red", font=FONT_P, anchor="w")
    error_labels['nombre_acudiente2'].grid(row=2, column=0, sticky="w")
    
    # Cédula acudiente secundario
    tk.Label(fields2b, text="Cédula de Ciudadanía del Acudiente Secundario", bg="#ffffff", font=FONT_P_BOLD, anchor="w").grid(row=0, column=1, sticky="w", pady=(0, 5))
    form_data['cedula_acudiente2'] = ttk.Entry(fields2b, width=38)
    form_data['cedula_acudiente2'].grid(row=1, column=1, sticky="ew", ipady=5)
    error_labels['cedula_acudiente2'] = tk.Label(fields2b, text="", bg="#ffffff", fg="red", font=FONT_P, anchor="w")
    error_labels['cedula_acudiente2'].grid(row=2, column=1, sticky="w")
    
    # Teléfono acudiente secundario
    tk.Label(fields2b, text="Teléfono/Celular del Acudiente Secundario", bg="#ffffff", font=FONT_P_BOLD, anchor="w").grid(row=3, column=0, sticky="w", pady=(10, 5))
    form_data['telefono2'] = ttk.Entry(fields2b, width=40)
    form_data['telefono2'].grid(row=4, column=0, sticky="ew", padx=(0, 10), ipady=5)
    error_labels['telefono2'] = tk.Label(fields2b, text="", bg="#ffffff", fg="red", font=FONT_P, anchor="w")
    error_labels['telefono2'].grid(row=5, column=0, sticky="w")
    
    # Email acudiente secundario
    tk.Label(fields2b, text="Correo Electrónico del Acudiente Secundario", bg="#ffffff", font=FONT_P_BOLD, anchor="w").grid(row=3, column=1, sticky="w", pady=(10, 5))
    form_data['email2'] = ttk.Entry(fields2b, width=38)
    form_data['email2'].grid(row=4, column=1, sticky="ew", ipady=5)
    error_labels['email2'] = tk.Label(fields2b, text="", bg="#ffffff", fg="red", font=FONT_P, anchor="w")
    error_labels['email2'].grid(row=5, column=1, sticky="w")
    
    # Parentesco acudiente secundario
    tk.Label(fields2b, text="Parentesco del Acudiente Secundario", bg="#ffffff", font=FONT_P_BOLD, anchor="w").grid(row=6, column=0, sticky="w", pady=(10, 5))
    form_data['parentesco2'] = ttk.Combobox(fields2b, width=40, values=["Padre", "Madre", "Tutor Legal", "Abuelo/a", "Otro"])
    form_data['parentesco2'].grid(row=7, column=0, sticky="ew", padx=(0, 10), ipady=5)
    error_labels['parentesco2'] = tk.Label(fields2b, text="", bg="#ffffff", fg="red", font=FONT_P, anchor="w")
    error_labels['parentesco2'].grid(row=8, column=0, sticky="w")
    
    tk.Label(fields2b, text="", bg="#ffffff").grid(row=6, column=1)  # Espacio vacío
    
    # Nota informativa
    info_label = tk.Label(
        fields2b,
        text="💡 Los campos de acudiente secundario son opcionales. Complete solo si desea registrar un segundo acudiente.",
        bg="#ffffff",
        fg=COLOR_TEXT_MUTED,
        font=FONT_P,
        anchor="w",
        justify="left",
        wraplength=700
    )
    info_label.grid(row=9, column=0, columnspan=2, sticky="w", pady=(10, 0))
    
    # --- SECCIÓN 3: INFORMACIÓN MÉDICA ---
    section3 = tk.Frame(main_content_frame, bg="#fcf0e5", highlightbackground=COLOR_TEST_BORDER, highlightthickness=1)
    section3.pack(fill="x", pady=10, padx=10)
    
    tk.Label(
        section3,
        text="Sección 3: Información Médica",
        bg="#fcf0e5",
        fg=COLOR_HEADER_PRE,
        font=FONT_P_BOLD,
        anchor="w"
    ).pack(fill="x", ipady=10, padx=10)
    
    fields3 = tk.Frame(section3, bg="#ffffff", padx=20, pady=15)
    fields3.pack(fill="x")
    fields3.grid_columnconfigure(0, weight=1)
    fields3.grid_columnconfigure(1, weight=1)
    
    # Alergias
    tk.Label(fields3, text="Alergias Conocidas", bg="#ffffff", font=FONT_P_BOLD, anchor="w").grid(row=0, column=0, sticky="w", pady=(0, 5))
    form_data['alergias'] = tk.Text(fields3, height=3, width=40)
    form_data['alergias'].grid(row=1, column=0, sticky="ew", padx=(0, 10), pady=(0, 10))
    
    # Medicamentos
    tk.Label(fields3, text="Medicamentos Actuales", bg="#ffffff", font=FONT_P_BOLD, anchor="w").grid(row=0, column=1, sticky="w", pady=(0, 5))
    form_data['medicamentos'] = tk.Text(fields3, height=3, width=38)
    form_data['medicamentos'].grid(row=1, column=1, sticky="ew", pady=(0, 10))
    
    # Colegio anterior
    tk.Label(fields3, text="Colegio o Institución Anterior (si aplica)", bg="#ffffff", font=FONT_P_BOLD, anchor="w").grid(row=2, column=0, columnspan=2, sticky="w", pady=(0, 5))
    form_data['colegio_anterior'] = ttk.Entry(fields3, width=83)
    form_data['colegio_anterior'].grid(row=3, column=0, columnspan=2, sticky="ew", pady=(0, 10), ipady=5)
    
    # --- SECCIÓN 4: TÉRMINOS Y CONDICIONES ---
    section4 = tk.Frame(main_content_frame, bg="#fcf0e5", highlightbackground=COLOR_TEST_BORDER, highlightthickness=1)
    section4.pack(fill="x", pady=10, padx=10)
    
    tk.Label(
        section4,
        text="Sección 4: Términos y Condiciones",
        bg="#fcf0e5",
        fg=COLOR_HEADER_PRE,
        font=FONT_P_BOLD,
        anchor="w"
    ).pack(fill="x", ipady=10, padx=10)
    
    fields4 = tk.Frame(section4, bg="#ffffff", padx=20, pady=15)
    fields4.pack(fill="x")
    
    # Texto de términos
    terms_text = tk.Text(fields4, height=6, width=95, wrap="word", borderwidth=1, relief="solid")
    terms_content = """• La preinscripción no garantiza el cupo en el colegio.
• Se requiere completar el proceso de documentación en las fechas asignadas.
• Los datos proporcionados serán verificados durante el proceso de matrícula.
• El colegio se reserva el derecho de solicitar documentación adicional.
• La información médica es confidencial y será usada solo para el cuidado del estudiante.
• Autorizo el tratamiento de datos personales según la ley 1581 de 2012."""
    terms_text.insert("1.0", terms_content)
    terms_text.config(state="disabled")
    terms_text.pack(fill="x", pady=(0, 15))
    
    # Checkbox aceptación
    form_data['acepto_terminos'] = tk.BooleanVar()
    ttk.Checkbutton(
        fields4,
        text="Acepto los términos y condiciones, y autorizo el tratamiento de datos personales *",
        variable=form_data['acepto_terminos']
    ).pack(anchor="w", pady=10)
    error_labels['acepto_terminos'] = tk.Label(fields4, text="", bg="#ffffff", fg="red", font=FONT_P, anchor="w")
    error_labels['acepto_terminos'].pack(anchor="w")
    
    # ============ BOTONES ============
    button_frame = tk.Frame(form_frame, bg="#ffffff")
    button_frame.pack(fill="x", padx=50, pady=20, side="bottom")
    
    def validar_y_enviar():
        """Valida todos los campos y envía el formulario con contador de intentos fallidos"""
        # Inicializar servicio
        servicio = ServicioPreinscripcion()
        identificador_usuario = "usuario_anonimo"  # En futuro, usar ID de sesión
        
        # Limpiar mensajes de error previos
        for label in error_labels.values():
            label.config(text="")
        
        errores_dict = {}  # Diccionario para almacenar errores
        hay_errores = False
        
        # Validar nombre estudiante
        valido, error = FormValidators.validar_nombre(form_data['nombre_estudiante'].get())
        if not valido:
            error_labels['nombre_estudiante'].config(text=f"✗ {error}")
            errores_dict['nombre_estudiante'] = error
            hay_errores = True
        
        # Validar tipo de ID
        if not form_data['tipo_id'].get():
            error_labels['tipo_id'].config(text="✗ Seleccione un tipo de identificación")
            errores_dict['tipo_id'] = "Seleccione un tipo de identificación"
            hay_errores = True
        
        # Validar número de ID
        valido, error = FormValidators.validar_cedula(form_data['numero_id'].get())
        if not valido:
            error_labels['numero_id'].config(text=f"✗ {error}")
            errores_dict['numero_id'] = error
            hay_errores = True
        
        # Validar fecha de nacimiento
        valido, error = FormValidators.validar_fecha(form_data['fecha_nacimiento'].get())
        if not valido:
            error_labels['fecha_nacimiento'].config(text=f"✗ {error}")
            errores_dict['fecha_nacimiento'] = error
            hay_errores = True
        
        # Validar género
        if not form_data['genero'].get():
            error_labels['genero'].config(text="✗ Seleccione un género")
            errores_dict['genero'] = "Seleccione un género"
            hay_errores = True
        
        # Validar grado
        if not form_data['grado'].get():
            error_labels['grado'].config(text="✗ Seleccione un grado")
            errores_dict['grado'] = "Seleccione un grado"
            hay_errores = True
        
        # Validar nombre acudiente
        valido, error = FormValidators.validar_nombre(form_data['nombre_acudiente'].get())
        if not valido:
            error_labels['nombre_acudiente'].config(text=f"✗ {error}")
            errores_dict['nombre_acudiente'] = error
            hay_errores = True
        
        # Validar cédula acudiente
        valido, error = FormValidators.validar_cedula(form_data['cedula_acudiente'].get())
        if not valido:
            error_labels['cedula_acudiente'].config(text=f"✗ {error}")
            errores_dict['cedula_acudiente'] = error
            hay_errores = True
        
        # Validar teléfono
        valido, error = FormValidators.validar_telefono(form_data['telefono'].get())
        if not valido:
            error_labels['telefono'].config(text=f"✗ {error}")
            errores_dict['telefono'] = error
            hay_errores = True
        
        # Validar email
        valido, error = FormValidators.validar_email(form_data['email'].get())
        if not valido:
            error_labels['email'].config(text=f"✗ {error}")
            errores_dict['email'] = error
            hay_errores = True
        
        # Validar dirección
        if not form_data['direccion'].get() or not form_data['direccion'].get().strip():
            error_labels['direccion'].config(text="✗ La dirección no puede estar vacía")
            errores_dict['direccion'] = "La dirección no puede estar vacía"
            hay_errores = True
        
        # Validar parentesco
        if not form_data['parentesco'].get():
            error_labels['parentesco'].config(text="✗ Seleccione un parentesco")
            errores_dict['parentesco'] = "Seleccione un parentesco"
            hay_errores = True
        
        # --- VALIDACIÓN DE ACUDIENTE SECUNDARIO (OPCIONAL) ---
        # Verificar si se ingresó algún dato del acudiente secundario
        tiene_dato_acudiente2 = (
            form_data['nombre_acudiente2'].get().strip() or 
            form_data['cedula_acudiente2'].get().strip() or
            form_data['telefono2'].get().strip() or
            form_data['email2'].get().strip() or
            form_data['parentesco2'].get()
        )
        
        # Si hay datos, todos los campos son obligatorios
        if tiene_dato_acudiente2:
            valido, error = FormValidators.validar_nombre(form_data['nombre_acudiente2'].get())
            if not valido:
                error_labels['nombre_acudiente2'].config(text=f"✗ {error}")
                errores_dict['nombre_acudiente2'] = error
                hay_errores = True
            
            valido, error = FormValidators.validar_cedula(form_data['cedula_acudiente2'].get())
            if not valido:
                error_labels['cedula_acudiente2'].config(text=f"✗ {error}")
                errores_dict['cedula_acudiente2'] = error
                hay_errores = True
            
            valido, error = FormValidators.validar_telefono(form_data['telefono2'].get())
            if not valido:
                error_labels['telefono2'].config(text=f"✗ {error}")
                errores_dict['telefono2'] = error
                hay_errores = True
            
            valido, error = FormValidators.validar_email(form_data['email2'].get())
            if not valido:
                error_labels['email2'].config(text=f"✗ {error}")
                errores_dict['email2'] = error
                hay_errores = True
            
            if not form_data['parentesco2'].get():
                error_labels['parentesco2'].config(text="✗ Seleccione un parentesco")
                errores_dict['parentesco2'] = "Seleccione un parentesco"
                hay_errores = True
        
        # Validar términos
        if not form_data['acepto_terminos'].get():
            error_labels['acepto_terminos'].config(text="✗ Debe aceptar los términos y condiciones")
            errores_dict['acepto_terminos'] = "Debe aceptar los términos y condiciones"
            hay_errores = True
        
        if hay_errores:
            # Registrar intento fallido
            intento = servicio.registrar_error(errores_dict, identificador_usuario)
            contador = intento.numero_error
            
            # Construir mensaje de error con contador
            mensaje = f"❌ Error {contador}/3:\n\n"
            for campo, error_msg in errores_dict.items():
                mensaje += f"• {error_msg}\n"
            
            # Si se alcanzan 3 intentos, redirigir al home
            if contador >= 3:
                messagebox.showerror(
                    "Límite de Intentos Excedido",
                    mensaje + "\n\n⚠️ Ha alcanzado el límite de 3 intentos fallidos. "
                    "Será redirigido al menú de inicio.",
                    parent=form_frame
                )
                nav_commands['home']()
                return
            else:
                # Mostrar error sin redirigir
                messagebox.showerror(
                    f"Errores de Validación ({contador}/3)",
                    mensaje,
                    parent=form_frame
                )
            return
        
        # Si todo está válido, mostrar mensaje de éxito y redirigir
        try:
            from .dialogs import show_confirmation_dialog
            def redirect_home():
                nav_commands['home']()
            show_confirmation_dialog(
                form_frame,
                "Preinscripción Enviada",
                "Su formulario de preinscripción ha sido enviado exitosamente. Nos pondremos en contacto pronto.",
                on_confirm=redirect_home
            )
        except ImportError:
            messagebox.showinfo("Éxito", "Preinscripción enviada correctamente")
            nav_commands['home']()
    
    ttk.Button(button_frame, text="Volver", command=nav_commands['home']).pack(side="left", padx=5)
    ttk.Button(button_frame, text="Enviar Preinscripción", style="Login.TButton", command=validar_y_enviar).pack(side="right", padx=5)
    
    return form_frame


# ============================================
# COMPATIBILIDAD: Mantener funciones antiguas
# ============================================

def create_step1(master, nav_commands):
    """Para compatibilidad, redirige al formulario unificado"""
    return create_unified_form(master, nav_commands)

def create_step2(master, nav_commands):
    """Para compatibilidad, redirige al formulario unificado"""
    return create_unified_form(master, nav_commands)

def create_step3(master, nav_commands):
    """Para compatibilidad, redirige al formulario unificado"""
    return create_unified_form(master, nav_commands)

def create_step4(master, nav_commands):
    """Para compatibilidad, redirige al formulario unificado"""
    return create_unified_form(master, nav_commands)
