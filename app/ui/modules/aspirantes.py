"""
Módulo de Gestión de Aspirantes para Directivos
Implementa CU-12: Consultar y Gestionar Aspirantes

Pasos del diagrama:
1. Directivo hace clic en "Consultar aspirantes"
2-3. Sistema carga y despliega listado
4. Directivo hace clic en "Ver detalles de aspirante"
5-7. Sistema muestra información completa y acciones
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from typing import Dict, Optional
from app.services.servicio_aspirante import ServicioAspirante
from app.ui.config import *


class GestionAspirantesView:
    """Vista principal para gestión de aspirantes"""
    
    def __init__(self, master, nav_commands):
        """
        Inicializa la vista de gestión de aspirantes.
        
        Args:
            master: Frame contenedor
            nav_commands: Diccionario con comandos de navegación
        """
        self.master = master
        self.nav_commands = nav_commands
        self.servicio = ServicioAspirante()
        self.aspirantes_actuales = []
        self.detalle_actual = None
        
        # Frames principales
        self.frame_listado = None
        self.frame_detalle = None
        self.frame_actual = None
        
        self.crear_interfaz()
    
    def crear_interfaz(self):
        """Crea la interfaz principal con el listado de aspirantes"""
        # PASO 1 DEL DIAGRAMA: Directivo hace clic en "Consultar aspirantes"
        # Esta interfaz se muestra cuando se invoca este módulo
        
        # Limpiar master
        for widget in self.master.winfo_children():
            widget.destroy()
        
        # Frame principal con scroll
        self.frame_listado = tk.Frame(self.master, bg="#f8f9fa")
        self.frame_listado.pack(fill="both", expand=True)
        
        # Header
        header = tk.Frame(self.frame_listado, bg="#f8f9fa")
        header.pack(fill="x", padx=30, pady=(20, 10))
        
        tk.Label(
            header,
            text="📋 Gestión de Aspirantes",
            font=FONT_H1,
            bg="#f8f9fa",
            fg=COLOR_TEXT_DARK
        ).pack(side="left")
        
        # Botón refrescar
        ttk.Button(
            header,
            text="🔄 Actualizar",
            style="AdminBlue.TButton",
            command=self.cargar_listado_aspirantes
        ).pack(side="right", padx=5)
        
        # Botón volver
        ttk.Button(
            header,
            text="← Volver al Dashboard",
            style="AdminGreen.TButton",
            command=lambda: self.nav_commands['show_frame']('director_dashboard')
        ).pack(side="right")
        
        # Descripción
        tk.Label(
            self.frame_listado,
            text="Consulte y gestione los aspirantes registrados en el sistema",
            font=FONT_P,
            bg="#f8f9fa",
            fg=COLOR_TEXT_MUTED
        ).pack(padx=30, pady=(0, 20))
        
        # Contenedor de la tabla
        self.contenedor_tabla = tk.Frame(self.frame_listado, bg="#ffffff")
        self.contenedor_tabla.pack(fill="both", expand=True, padx=30, pady=(0, 20))
        
        # PASO 2: Sistema carga listado aspirantes
        self.cargar_listado_aspirantes()
        
        self.frame_actual = self.frame_listado
    
    def cargar_listado_aspirantes(self):
        """
        PASO 2 DEL DIAGRAMA: Cargar listado aspirantes actuales
        
        El Sistema recupera la información de todos los aspirantes de la BD.
        """
        # Limpiar contenedor
        for widget in self.contenedor_tabla.winfo_children():
            widget.destroy()
        
        # Mostrar indicador de carga
        loading_label = tk.Label(
            self.contenedor_tabla,
            text="⏳ Cargando aspirantes...",
            font=FONT_P,
            bg="#ffffff",
            fg=COLOR_TEXT_MUTED
        )
        loading_label.pack(pady=50)
        self.contenedor_tabla.update()
        
        # Obtener aspirantes del servicio
        exito, aspirantes, mensaje = self.servicio.obtener_listado_aspirantes()
        
        # Limpiar indicador
        loading_label.destroy()
        
        if not exito:
            # Error al cargar
            tk.Label(
                self.contenedor_tabla,
                text=f"❌ {mensaje}",
                font=FONT_P,
                bg="#ffffff",
                fg="#dc3545"
            ).pack(pady=50)
            return
        
        if not aspirantes:
            # No hay aspirantes
            tk.Label(
                self.contenedor_tabla,
                text="📭 No hay aspirantes registrados en el sistema.",
                font=FONT_P,
                bg="#ffffff",
                fg=COLOR_TEXT_MUTED
            ).pack(pady=50)
            return
        
        # Guardar aspirantes actuales
        self.aspirantes_actuales = aspirantes
        
        # PASO 3: Desplegar listado aspirantes
        self.desplegar_tabla_aspirantes()
    
    def desplegar_tabla_aspirantes(self):
        """
        PASO 3 DEL DIAGRAMA: Desplegar listado aspirantes
        
        El Sistema muestra la lista al Directivo.
        Cada elemento del listado debe tener un link "Ver detalles aspirante".
        """
        # Frame con scroll para la tabla
        canvas = tk.Canvas(self.contenedor_tabla, bg="#ffffff", highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.contenedor_tabla, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#ffffff")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Encabezados de la tabla
        headers = ["#", "Nombre Completo", "Identificación", "Grado", "Fecha Solicitud", "Estado", "Acciones"]
        header_frame = tk.Frame(scrollable_frame, bg=COLOR_HEADER_PRE, height=50)
        header_frame.pack(fill="x", pady=(0, 2))
        
        widths = [50, 250, 150, 100, 120, 120, 150]
        
        for i, (header, width) in enumerate(zip(headers, widths)):
            tk.Label(
                header_frame,
                text=header,
                font=FONT_P_BOLD,
                bg=COLOR_HEADER_PRE,
                fg="#ffffff",
                width=width // 8,
                anchor="w" if i > 0 else "center"
            ).pack(side="left", padx=10, pady=10)
        
        # Filas de aspirantes
        for idx, aspirante in enumerate(self.aspirantes_actuales, start=1):
            self.crear_fila_aspirante(scrollable_frame, idx, aspirante)
        
        # Mensaje de total
        footer = tk.Frame(scrollable_frame, bg="#f8f9fa")
        footer.pack(fill="x", pady=10)
        
        tk.Label(
            footer,
            text=f"Total de aspirantes: {len(self.aspirantes_actuales)}",
            font=FONT_P_BOLD,
            bg="#f8f9fa",
            fg=COLOR_TEXT_DARK
        ).pack(padx=10)
        
        # Empaquetar canvas y scrollbar
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
    
    def crear_fila_aspirante(self, parent, numero, aspirante: Dict):
        """
        Crea una fila en la tabla con información del aspirante.
        
        Incluye el link "Ver detalles aspirante" según requisitos del diagrama (Paso 3).
        """
        row_bg = "#ffffff" if numero % 2 == 0 else "#f8f9fa"
        
        row_frame = tk.Frame(parent, bg=row_bg, height=60)
        row_frame.pack(fill="x", pady=1)
        
        # Columna 1: Número
        tk.Label(
            row_frame,
            text=str(numero),
            font=FONT_P,
            bg=row_bg,
            fg=COLOR_TEXT_DARK,
            width=6
        ).pack(side="left", padx=10)
        
        # Columna 2: Nombre completo
        tk.Label(
            row_frame,
            text=aspirante['nombre_completo'],
            font=FONT_P,
            bg=row_bg,
            fg=COLOR_TEXT_DARK,
            width=30,
            anchor="w"
        ).pack(side="left", padx=10)
        
        # Columna 3: Identificación
        id_text = f"{aspirante['tipo_identificacion']} {aspirante['numero_identificacion']}"
        tk.Label(
            row_frame,
            text=id_text,
            font=FONT_P,
            bg=row_bg,
            fg=COLOR_TEXT_MUTED,
            width=18,
            anchor="w"
        ).pack(side="left", padx=10)
        
        # Columna 4: Grado
        tk.Label(
            row_frame,
            text=aspirante['grado_solicitado'],
            font=FONT_P,
            bg=row_bg,
            fg=COLOR_TEXT_DARK,
            width=12,
            anchor="w"
        ).pack(side="left", padx=10)
        
        # Columna 5: Fecha solicitud
        tk.Label(
            row_frame,
            text=aspirante['fecha_solicitud'],
            font=FONT_P,
            bg=row_bg,
            fg=COLOR_TEXT_MUTED,
            width=15,
            anchor="w"
        ).pack(side="left", padx=10)
        
        # Columna 6: Estado (con color)
        estado_colors = {
            'pendiente': '#ffc107',
            'en_proceso': '#17a2b8',
            'aceptado': '#28a745',
            'rechazado': '#dc3545'
        }
        estado_text = aspirante['estado_proceso'].replace('_', ' ').title()
        estado_color = estado_colors.get(aspirante['estado_proceso'], COLOR_TEXT_MUTED)
        
        estado_label = tk.Label(
            row_frame,
            text=f"● {estado_text}",
            font=FONT_P_BOLD,
            bg=row_bg,
            fg=estado_color,
            width=15,
            anchor="w"
        )
        estado_label.pack(side="left", padx=10)
        
        # Columna 7: Link "Ver detalles aspirante" (REQUISITO DEL DIAGRAMA - PASO 4)
        btn_detalle = tk.Button(
            row_frame,
            text="👁️ Ver detalles",
            font=FONT_P_BOLD,
            bg=COLOR_HEADER_PRE,
            fg="#ffffff",
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=5,
            command=lambda asp=aspirante: self.ver_detalle_aspirante(asp['id_aspirante'])
        )
        btn_detalle.pack(side="left", padx=10)
        
        # Efecto hover
        def on_enter(e):
            btn_detalle.config(bg="#5a4fcf")
        
        def on_leave(e):
            btn_detalle.config(bg=COLOR_HEADER_PRE)
        
        btn_detalle.bind("<Enter>", on_enter)
        btn_detalle.bind("<Leave>", on_leave)
    
    def ver_detalle_aspirante(self, id_aspirante: int):
        """
        PASO 4 DEL DIAGRAMA: Directivo hace clic en "Ver detalles de aspirante"
        
        El Directivo selecciona y hace clic en el enlace de un aspirante específico.
        
        PASO 5: Sistema redirige al módulo de aspirante
        PASO 6-7: Sistema despliega información completa y acciones
        """
        # Limpiar frame listado
        if self.frame_listado:
            self.frame_listado.pack_forget()
        
        # Crear frame de detalle
        self.mostrar_detalle_aspirante(id_aspirante)
    
    def mostrar_detalle_aspirante(self, id_aspirante: int):
        """
        PASO 6-7 DEL DIAGRAMA: 
        - Dirigir al módulo de aspirante
        - Desplegar información de aspirante y acciones
        
        Muestra la información completa del aspirante.
        Acciones posibles: 1. Programar entrevista, 2. Diligenciar admisión aspirante.
        """
        # Crear frame de detalle si no existe
        if self.frame_detalle:
            for widget in self.frame_detalle.winfo_children():
                widget.destroy()
        else:
            self.frame_detalle = tk.Frame(self.master, bg="#f8f9fa")
        
        self.frame_detalle.pack(fill="both", expand=True)
        
        # Mostrar indicador de carga
        loading_label = tk.Label(
            self.frame_detalle,
            text="⏳ Cargando información del aspirante...",
            font=FONT_H2,
            bg="#f8f9fa",
            fg=COLOR_TEXT_MUTED
        )
        loading_label.pack(pady=100)
        self.frame_detalle.update()
        
        # PASO 6: Obtener información completa
        exito, detalle, mensaje = self.servicio.obtener_detalle_aspirante(id_aspirante)
        
        # Limpiar indicador
        loading_label.destroy()
        
        if not exito:
            # Error al cargar
            tk.Label(
                self.frame_detalle,
                text=f"❌ {mensaje}",
                font=FONT_H2,
                bg="#f8f9fa",
                fg="#dc3545"
            ).pack(pady=50)
            
            ttk.Button(
                self.frame_detalle,
                text="← Volver al listado",
                style="AdminGreen.TButton",
                command=self.volver_a_listado
            ).pack(pady=20)
            return
        
        # Guardar detalle actual
        self.detalle_actual = detalle
        
        # PASO 7: Desplegar información completa
        self.renderizar_detalle_completo(detalle)
        
        self.frame_actual = self.frame_detalle
    
    def renderizar_detalle_completo(self, detalle: Dict):
        """
        Renderiza toda la información del aspirante de forma organizada.
        
        Incluye:
        - Datos personales
        - Información del acudiente
        - Estado del proceso
        - Acciones disponibles (Paso 7)
        """
        # Canvas scrollable
        canvas = tk.Canvas(self.frame_detalle, bg="#f8f9fa", highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.frame_detalle, orient="vertical", command=canvas.yview)
        content_frame = tk.Frame(canvas, bg="#f8f9fa")
        
        content_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=content_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # --- HEADER ---
        header = tk.Frame(content_frame, bg="#f8f9fa")
        header.pack(fill="x", padx=30, pady=(20, 10))
        
        tk.Label(
            header,
            text="👤 Detalles del Aspirante",
            font=FONT_H1,
            bg="#f8f9fa",
            fg=COLOR_TEXT_DARK
        ).pack(side="left")
        
        ttk.Button(
            header,
            text="← Volver al listado",
            style="AdminGreen.TButton",
            command=self.volver_a_listado
        ).pack(side="right")
        
        # --- INFORMACIÓN DEL ASPIRANTE ---
        self.crear_seccion_informacion_aspirante(content_frame, detalle['aspirante'])
        
        # --- INFORMACIÓN DEL ACUDIENTE ---
        if detalle['acudiente']:
            self.crear_seccion_acudiente(content_frame, detalle['acudiente'])
        
        # --- RESPUESTAS DEL FORMULARIO ---
        if detalle['respuestas_formulario']:
            self.crear_seccion_respuestas(content_frame, detalle['respuestas_formulario'])
        
        # --- ACCIONES DISPONIBLES (PASO 7) ---
        self.crear_seccion_acciones(content_frame, detalle['acciones_disponibles'], detalle['aspirante'])
        
        # Empaquetar canvas
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
    
    def crear_seccion_informacion_aspirante(self, parent, aspirante: Dict):
        """Crea la sección con información personal del aspirante"""
        seccion = tk.Frame(parent, bg="#ffffff", relief="solid", bd=1)
        seccion.pack(fill="x", padx=30, pady=10)
        
        # Título de sección
        tk.Label(
            seccion,
            text="📋 Información Personal",
            font=FONT_H2,
            bg="#ffffff",
            fg=COLOR_HEADER_PRE
        ).pack(anchor="w", padx=20, pady=(15, 10))
        
        # Grid de información
        info_frame = tk.Frame(seccion, bg="#ffffff")
        info_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        info_frame.grid_columnconfigure(0, weight=1)
        info_frame.grid_columnconfigure(1, weight=1)
        
        # Datos
        campos = [
            ("Nombre completo:", aspirante['nombre_completo']),
            ("Tipo de ID:", aspirante['tipo_identificacion']),
            ("Número de ID:", aspirante['numero_identificacion']),
            ("Fecha de nacimiento:", aspirante['fecha_nacimiento']),
            ("Edad:", f"{aspirante['edad']} años" if aspirante['edad'] else "N/A"),
            ("Género:", aspirante['genero']),
            ("Dirección:", aspirante['direccion']),
            ("Teléfono:", aspirante['telefono']),
            ("Grado solicitado:", aspirante['grado_solicitado']),
            ("Fecha de solicitud:", aspirante['fecha_solicitud']),
            ("Estado del proceso:", aspirante['estado_proceso'].replace('_', ' ').title()),
        ]
        
        for i, (label, value) in enumerate(campos):
            row = i // 2
            col = i % 2
            
            campo_frame = tk.Frame(info_frame, bg="#ffffff")
            campo_frame.grid(row=row, column=col, sticky="w", padx=10, pady=8)
            
            tk.Label(
                campo_frame,
                text=label,
                font=FONT_P_BOLD,
                bg="#ffffff",
                fg=COLOR_TEXT_DARK
            ).pack(side="left", padx=(0, 10))
            
            tk.Label(
                campo_frame,
                text=value or "N/A",
                font=FONT_P,
                bg="#ffffff",
                fg=COLOR_TEXT_MUTED
            ).pack(side="left")
    
    def crear_seccion_acudiente(self, parent, acudiente: Dict):
        """Crea la sección con información del acudiente"""
        seccion = tk.Frame(parent, bg="#ffffff", relief="solid", bd=1)
        seccion.pack(fill="x", padx=30, pady=10)
        
        # Título de sección
        tk.Label(
            seccion,
            text="👨‍👩‍👧 Información del Acudiente",
            font=FONT_H2,
            bg="#ffffff",
            fg=COLOR_HEADER_PRE
        ).pack(anchor="w", padx=20, pady=(15, 10))
        
        # Grid de información
        info_frame = tk.Frame(seccion, bg="#ffffff")
        info_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        info_frame.grid_columnconfigure(0, weight=1)
        info_frame.grid_columnconfigure(1, weight=1)
        
        # Datos
        campos = [
            ("Nombre completo:", acudiente['nombre_completo']),
            ("Cédula:", acudiente['numero_identificacion']),
            ("Parentesco:", acudiente['parentesco']),
            ("Email:", acudiente['email']),
            ("Teléfono:", acudiente['telefono']),
            ("Dirección:", acudiente['direccion']),
        ]
        
        for i, (label, value) in enumerate(campos):
            row = i // 2
            col = i % 2
            
            campo_frame = tk.Frame(info_frame, bg="#ffffff")
            campo_frame.grid(row=row, column=col, sticky="w", padx=10, pady=8)
            
            tk.Label(
                campo_frame,
                text=label,
                font=FONT_P_BOLD,
                bg="#ffffff",
                fg=COLOR_TEXT_DARK
            ).pack(side="left", padx=(0, 10))
            
            tk.Label(
                campo_frame,
                text=value or "N/A",
                font=FONT_P,
                bg="#ffffff",
                fg=COLOR_TEXT_MUTED
            ).pack(side="left")
    
    def crear_seccion_respuestas(self, parent, respuestas: Dict):
        """Crea la sección con las respuestas del formulario de preinscripción"""
        seccion = tk.Frame(parent, bg="#ffffff", relief="solid", bd=1)
        seccion.pack(fill="x", padx=30, pady=10)
        
        # Título de sección
        tk.Label(
            seccion,
            text="📝 Respuestas del Formulario",
            font=FONT_H2,
            bg="#ffffff",
            fg=COLOR_HEADER_PRE
        ).pack(anchor="w", padx=20, pady=(15, 10))
        
        tk.Label(
            seccion,
            text=f"Fecha de envío: {respuestas['fecha_envio']}",
            font=FONT_P,
            bg="#ffffff",
            fg=COLOR_TEXT_MUTED
        ).pack(anchor="w", padx=20, pady=(0, 10))
        
        # Mostrar datos adicionales del formulario
        datos = respuestas['datos_formulario']
        if datos:
            info_frame = tk.Frame(seccion, bg="#ffffff")
            info_frame.pack(fill="x", padx=20, pady=(0, 15))
            
            # Campos adicionales que pueden estar en el formulario
            campos_adicionales = [
                ('nombre_colegio_anterior', 'Colegio anterior'),
                ('alergias', 'Alergias'),
                ('medicamentos', 'Medicamentos'),
            ]
            
            for key, label in campos_adicionales:
                if key in datos and datos[key]:
                    campo_frame = tk.Frame(info_frame, bg="#ffffff")
                    campo_frame.pack(fill="x", pady=5)
                    
                    tk.Label(
                        campo_frame,
                        text=f"{label}:",
                        font=FONT_P_BOLD,
                        bg="#ffffff",
                        fg=COLOR_TEXT_DARK
                    ).pack(side="left", padx=(0, 10))
                    
                    tk.Label(
                        campo_frame,
                        text=datos[key],
                        font=FONT_P,
                        bg="#ffffff",
                        fg=COLOR_TEXT_MUTED
                    ).pack(side="left")
    
    def crear_seccion_acciones(self, parent, acciones: list, aspirante: Dict):
        """
        PASO 7 DEL DIAGRAMA: Desplegar acciones disponibles
        
        Acciones posibles:
        1. Programar entrevista
        2. Diligenciar admisión aspirante
        """
        seccion = tk.Frame(parent, bg="#ffffff", relief="solid", bd=1)
        seccion.pack(fill="x", padx=30, pady=10)
        
        # Título de sección
        tk.Label(
            seccion,
            text="⚡ Acciones Disponibles",
            font=FONT_H2,
            bg="#ffffff",
            fg=COLOR_HEADER_PRE
        ).pack(anchor="w", padx=20, pady=(15, 10))
        
        tk.Label(
            seccion,
            text="Seleccione una acción para continuar con el proceso del aspirante",
            font=FONT_P,
            bg="#ffffff",
            fg=COLOR_TEXT_MUTED
        ).pack(anchor="w", padx=20, pady=(0, 15))
        
        # Botones de acciones
        acciones_frame = tk.Frame(seccion, bg="#ffffff")
        acciones_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        for accion in acciones:
            self.crear_boton_accion(acciones_frame, accion, aspirante)
    
    def crear_boton_accion(self, parent, accion: Dict, aspirante: Dict):
        """Crea un botón para cada acción disponible"""
        btn_frame = tk.Frame(parent, bg="#ffffff")
        btn_frame.pack(fill="x", pady=5)
        
        # Botón
        estado = "normal" if accion['habilitado'] else "disabled"
        bg_color = COLOR_HEADER_PRE if accion['habilitado'] else "#cccccc"
        
        btn = tk.Button(
            btn_frame,
            text=f"{accion['icono']} {accion['nombre']}",
            font=FONT_P_BOLD,
            bg=bg_color,
            fg="#ffffff",
            relief="flat",
            state=estado,
            cursor="hand2" if accion['habilitado'] else "arrow",
            padx=20,
            pady=10,
            command=lambda: self.ejecutar_accion(accion['tipo'], aspirante)
        )
        btn.pack(side="left")
        
        # Descripción
        tk.Label(
            btn_frame,
            text=f"  {accion['descripcion']}",
            font=FONT_P,
            bg="#ffffff",
            fg=COLOR_TEXT_MUTED
        ).pack(side="left", padx=10)
        
        # Efecto hover
        if accion['habilitado']:
            def on_enter(e):
                btn.config(bg="#5a4fcf")
            
            def on_leave(e):
                btn.config(bg=COLOR_HEADER_PRE)
            
            btn.bind("<Enter>", on_enter)
            btn.bind("<Leave>", on_leave)
    
    def ejecutar_accion(self, tipo_accion: str, aspirante: Dict):
        """
        Ejecuta la acción seleccionada sobre el aspirante.
        
        Args:
            tipo_accion: 'programar_entrevista' o 'diligenciar_admision'
            aspirante: Datos del aspirante
        """
        if tipo_accion == 'programar_entrevista':
            self.abrir_dialogo_programar_entrevista(aspirante)
        
        elif tipo_accion == 'diligenciar_admision':
            messagebox.showinfo(
                "Diligenciar Admisión",
                f"Funcionalidad para completar admisión de:\n\n"
                f"Aspirante: {aspirante['nombre_completo']}\n"
                f"Grado: {aspirante['grado_solicitado']}\n\n"
                f"Esta funcionalidad se implementará en un caso de uso posterior.",
                parent=self.frame_actual
            )
    
    def abrir_dialogo_programar_entrevista(self, aspirante: Dict):
        """
        Abre un diálogo para programar una entrevista con el aspirante.
        Permite seleccionar fecha, hora y lugar, y valida disponibilidad.
        """
        from tkinter import ttk
        from datetime import datetime, timedelta
        from tkcalendar import DateEntry
        
        # Crear ventana de diálogo
        dialogo = tk.Toplevel(self.frame_actual)
        dialogo.title("Programar Entrevista")
        dialogo.geometry("500x450")
        dialogo.resizable(False, False)
        dialogo.transient(self.frame_actual)
        dialogo.grab_set()
        
        # Centrar la ventana
        dialogo.update_idletasks()
        x = (dialogo.winfo_screenwidth() // 2) - (500 // 2)
        y = (dialogo.winfo_screenheight() // 2) - (450 // 2)
        dialogo.geometry(f"500x450+{x}+{y}")
        
        # Frame principal
        main_frame = tk.Frame(dialogo, bg="#f8f9fa", padx=30, pady=20)
        main_frame.pack(fill="both", expand=True)
        
        # Título
        tk.Label(
            main_frame,
            text="📅 Programar Entrevista",
            font=FONT_H1,
            bg="#f8f9fa",
            fg=COLOR_TEXT_DARK
        ).pack(pady=(0, 5))
        
        # Información del aspirante
        tk.Label(
            main_frame,
            text=f"Aspirante: {aspirante['nombre_completo']}",
            font=FONT_P_BOLD,
            bg="#f8f9fa",
            fg=COLOR_TEXT_DARK
        ).pack(pady=(0, 20))
        
        # Frame para formulario
        form_frame = tk.Frame(main_frame, bg="#ffffff", relief="solid", bd=1)
        form_frame.pack(fill="both", expand=True, pady=(0, 15))
        
        # Padding interno
        form_content = tk.Frame(form_frame, bg="#ffffff", padx=20, pady=20)
        form_content.pack(fill="both", expand=True)
        
        # Campo: Fecha
        tk.Label(
            form_content,
            text="Fecha de la entrevista:",
            font=FONT_P_BOLD,
            bg="#ffffff",
            fg=COLOR_TEXT_DARK
        ).pack(anchor="w", pady=(0, 5))
        
        # DateEntry con formato español
        fecha_entry = DateEntry(
            form_content,
            width=30,
            background='darkblue',
            foreground='white',
            borderwidth=2,
            date_pattern='dd/mm/yyyy',
            mindate=datetime.now().date(),
            maxdate=(datetime.now() + timedelta(days=90)).date()
        )
        fecha_entry.pack(fill="x", pady=(0, 15))
        
        # Campo: Hora
        tk.Label(
            form_content,
            text="Hora de la entrevista:",
            font=FONT_P_BOLD,
            bg="#ffffff",
            fg=COLOR_TEXT_DARK
        ).pack(anchor="w", pady=(0, 5))
        
        hora_frame = tk.Frame(form_content, bg="#ffffff")
        hora_frame.pack(fill="x", pady=(0, 15))
        
        # Hora
        hora_var = tk.StringVar(value="09")
        hora_spinbox = tk.Spinbox(
            hora_frame,
            from_=7,
            to=18,
            width=5,
            textvariable=hora_var,
            font=FONT_P,
            format="%02.0f"
        )
        hora_spinbox.pack(side="left", padx=(0, 5))
        
        tk.Label(hora_frame, text=":", font=FONT_P_BOLD, bg="#ffffff").pack(side="left")
        
        # Minutos
        minuto_var = tk.StringVar(value="00")
        minuto_spinbox = tk.Spinbox(
            hora_frame,
            values=("00", "15", "30", "45"),
            width=5,
            textvariable=minuto_var,
            font=FONT_P
        )
        minuto_spinbox.pack(side="left", padx=5)
        
        # Campo: Lugar
        tk.Label(
            form_content,
            text="Lugar de la entrevista:",
            font=FONT_P_BOLD,
            bg="#ffffff",
            fg=COLOR_TEXT_DARK
        ).pack(anchor="w", pady=(0, 5))
        
        lugar_entry = tk.Entry(
            form_content,
            font=FONT_P,
            relief="solid",
            bd=1
        )
        lugar_entry.pack(fill="x", pady=(0, 15))
        lugar_entry.insert(0, "Sala de Reuniones")
        
        # Mensaje de estado
        status_label = tk.Label(
            main_frame,
            text="",
            font=FONT_P,
            bg="#f8f9fa",
            fg=COLOR_TEXT_MUTED
        )
        status_label.pack(pady=(0, 10))
        
        # Botones
        button_frame = tk.Frame(main_frame, bg="#f8f9fa")
        button_frame.pack(fill="x")
        
        def guardar_entrevista():
            """Valida y guarda la entrevista"""
            try:
                # Obtener valores
                fecha = fecha_entry.get_date()
                hora = int(hora_var.get())
                minuto = int(minuto_var.get())
                lugar = lugar_entry.get().strip()
                
                # Validaciones
                if not lugar:
                    messagebox.showwarning(
                        "Validación",
                        "Por favor ingrese el lugar de la entrevista.",
                        parent=dialogo
                    )
                    return
                
                # Combinar fecha y hora
                fecha_hora = datetime.combine(fecha, datetime.min.time())
                fecha_hora = fecha_hora.replace(hour=hora, minute=minuto)
                
                # Validar que la fecha/hora sea futura
                if fecha_hora <= datetime.now():
                    messagebox.showwarning(
                        "Validación",
                        "La fecha y hora de la entrevista debe ser futura.",
                        parent=dialogo
                    )
                    return
                
                status_label.config(text="⏳ Verificando disponibilidad...", fg=COLOR_TEXT_MUTED)
                dialogo.update()
                
                # Llamar al servicio para programar la entrevista
                exito, mensaje = self.servicio.programar_entrevista(
                    id_aspirante=aspirante['id_aspirante'],
                    fecha_programada=fecha_hora,
                    lugar=lugar
                )
                
                if exito:
                    status_label.config(text="", fg=COLOR_TEXT_MUTED)
                    messagebox.showinfo(
                        "Éxito",
                        f"Entrevista programada exitosamente.\n\n"
                        f"Fecha: {fecha_hora.strftime('%d/%m/%Y %H:%M')}\n"
                        f"Lugar: {lugar}\n\n"
                        f"{mensaje}",
                        parent=dialogo
                    )
                    dialogo.destroy()
                    # Recargar los detalles del aspirante
                    self.mostrar_detalle_aspirante(aspirante['id_aspirante'])
                else:
                    status_label.config(text="", fg=COLOR_TEXT_MUTED)
                    messagebox.showerror(
                        "Error",
                        mensaje,
                        parent=dialogo
                    )
                    
            except ValueError as e:
                messagebox.showerror(
                    "Error de Validación",
                    f"Error en los datos ingresados: {str(e)}",
                    parent=dialogo
                )
            except Exception as e:
                status_label.config(text="", fg=COLOR_TEXT_MUTED)
                messagebox.showerror(
                    "Error",
                    f"Error al programar la entrevista: {str(e)}",
                    parent=dialogo
                )
        
        ttk.Button(
            button_frame,
            text="Cancelar",
            command=dialogo.destroy
        ).pack(side="left", padx=5)
        
        ttk.Button(
            button_frame,
            text="Programar Entrevista",
            style="AdminBlue.TButton",
            command=guardar_entrevista
        ).pack(side="right", padx=5)
    
    def volver_a_listado(self):
        """Vuelve a la vista de listado de aspirantes"""
        if self.frame_detalle:
            self.frame_detalle.pack_forget()
        
        if self.frame_listado:
            self.frame_listado.pack(fill="both", expand=True)
            self.frame_actual = self.frame_listado
        else:
            self.crear_interfaz()


def create_aspirantes_manager(master, nav_commands):
    """
    PASO 1 DEL DIAGRAMA: Directivo hace clic en "Consultar aspirantes"
    
    Función principal para crear el módulo de gestión de aspirantes.
    Se invoca desde el dashboard del directivo.
    
    Args:
        master: Frame contenedor
        nav_commands: Diccionario con comandos de navegación
        
    Returns:
        Frame con la interfaz de gestión de aspirantes
    """
    frame = tk.Frame(master)
    GestionAspirantesView(frame, nav_commands)
    return frame
