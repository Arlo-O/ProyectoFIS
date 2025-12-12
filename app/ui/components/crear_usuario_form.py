# -*- coding: utf-8 -*-
"""
📋 Formulario de Creación de Usuarios
Interfaz para crear nuevos usuarios con validación en tiempo real
"""

import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from datetime import datetime


class FormularioCrearUsuario:
    """Formulario para crear nuevos usuarios con campos dinámicos según rol"""
    
    TIPOS_IDENTIFICACION = ["CC", "CE", "PA", "TI", "RC"]
    GENEROS = ["Masculino", "Femenino", "Otro"]
    
    def __init__(self, parent, roles_disponibles: list, callback_crear=None, config_colors: dict = None):
        """
        parent: ventana padre
        roles_disponibles: lista de roles que se pueden crear
        callback_crear: función a llamar cuando se hace clic en crear
        config_colors: diccionario con colores de la aplicación
        """
        self.parent = parent
        self.roles_disponibles = roles_disponibles
        self.callback_crear = callback_crear
        self.config = config_colors or {}
        
        # Colores por defecto
        self.COLOR_BG = self.config.get("BG", "#f5f5f5")
        self.COLOR_ACCENT = self.config.get("ACCENT", "#2196F3")
        self.COLOR_ERROR = self.config.get("ERROR", "#f44336")
        self.COLOR_SUCCESS = self.config.get("SUCCESS", "#4caf50")
        self.COLOR_TEXT = self.config.get("TEXT", "#333333")
        
        self.font_label = ("Arial", 10, "bold")
        self.font_normal = ("Arial", 10)
        self.font_small = ("Arial", 9)
        
        # Estado de campos dinámicos
        self.campos_dinamicos = {}
        self.errores_campo = {}
        
        # Build form
        self.build_form()
    
    def build_form(self):
        """Construye la interfaz del formulario"""
        # Frame principal con scroll
        canvas_frame = tk.Frame(self.parent, bg=self.COLOR_BG)
        canvas_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Canvas para scroll
        self.canvas = tk.Canvas(canvas_frame, bg=self.COLOR_BG, highlightthickness=0)
        scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=self.canvas.yview)
        
        self.scrollable_frame = tk.Frame(self.canvas, bg=self.COLOR_BG)
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # ==================== SECCIÓN 1: IDENTIFICACIÓN ====================
        self._crear_seccion("Identificación Personal", self.scrollable_frame)
        
        # Tipo de identificación
        self._crear_field(
            self.scrollable_frame, "Tipo de Identificación",
            "tipo_identificacion", tipo="combo",
            opciones=self.TIPOS_IDENTIFICACION,
            requerido=True
        )
        
        # Número de identificación
        self._crear_field(
            self.scrollable_frame, "Número de Identificación",
            "numero_identificacion", tipo="entry",
            validacion="identificador",
            requerido=True,
            placeholder="Ej: 1234567890"
        )
        
        # ==================== SECCIÓN 2: DATOS PERSONALES ====================
        self._crear_seccion("Datos Personales", self.scrollable_frame)
        
        # Primer nombre
        self._crear_field(
            self.scrollable_frame, "Primer Nombre",
            "primer_nombre", tipo="entry",
            validacion="nombre",
            requerido=True,
            placeholder="Ej: Juan"
        )
        
        # Segundo nombre
        self._crear_field(
            self.scrollable_frame, "Segundo Nombre",
            "segundo_nombre", tipo="entry",
            validacion="nombre",
            requerido=False,
            placeholder="Opcional"
        )
        
        # Primer apellido
        self._crear_field(
            self.scrollable_frame, "Primer Apellido",
            "primer_apellido", tipo="entry",
            validacion="nombre",
            requerido=True,
            placeholder="Ej: García"
        )
        
        # Segundo apellido
        self._crear_field(
            self.scrollable_frame, "Segundo Apellido",
            "segundo_apellido", tipo="entry",
            validacion="nombre",
            requerido=False,
            placeholder="Opcional"
        )
        
        # Fecha de nacimiento
        self._crear_field(
            self.scrollable_frame, "Fecha de Nacimiento",
            "fecha_nacimiento", tipo="date",
            requerido=False,
            placeholder="YYYY-MM-DD"
        )
        
        # Género
        self._crear_field(
            self.scrollable_frame, "Género",
            "genero", tipo="combo",
            opciones=self.GENEROS,
            requerido=False
        )
        
        # Teléfono
        self._crear_field(
            self.scrollable_frame, "Teléfono",
            "telefono", tipo="entry",
            validacion="telefono",
            requerido=False,
            placeholder="Ej: 3105555555"
        )
        
        # Dirección
        self._crear_field(
            self.scrollable_frame, "Dirección",
            "direccion", tipo="entry",
            requerido=False,
            placeholder="Calle 123 #456-789"
        )
        
        # ==================== SECCIÓN 3: ROL Y PERMISOS ====================
        self._crear_seccion("Rol y Permisos", self.scrollable_frame)
        
        # Selección de rol
        self._crear_field(
            self.scrollable_frame, "Rol",
            "rol", tipo="combo",
            opciones=self.roles_disponibles,
            requerido=True,
            on_change=self.actualizar_campos_rol
        )
        
        # ==================== SECCIÓN 4: CAMPOS DINÁMICOS POR ROL ====================
        self.frame_dinamico = tk.Frame(self.scrollable_frame, bg=self.COLOR_BG)
        self.frame_dinamico.pack(fill="x", padx=5, pady=10)
        
        # ==================== SECCIÓN 5: CREDENCIALES (para usuarios con acceso) ====================
        self.frame_credenciales = tk.Frame(self.scrollable_frame, bg=self.COLOR_BG)
        self.frame_credenciales.pack(fill="x", padx=5, pady=10)
        
        # Email
        self._crear_field(
            self.frame_credenciales, "Correo Electrónico",
            "correo_electronico", tipo="entry",
            validacion="email",
            requerido=True,
            placeholder="usuario@colegio.edu",
            parent_frame=self.frame_credenciales
        )
        
        # Info de contraseña
        info_frame = tk.Frame(self.frame_credenciales, bg="#e8f5e9", relief="solid", bd=1)
        info_frame.pack(fill="x", padx=0, pady=(5, 10))
        
        tk.Label(
            info_frame, text="ℹ️ La contraseña se generará automáticamente",
            bg="#e8f5e9", fg="#2e7d32", font=self.font_small
        ).pack(anchor="w", padx=10, pady=8)
        
        # ==================== BOTONES DE ACCIÓN ====================
        buttons_frame = tk.Frame(self.scrollable_frame, bg=self.COLOR_BG)
        buttons_frame.pack(fill="x", padx=5, pady=15)
        
        tk.Button(
            buttons_frame, text="Crear Usuario", bg=self.COLOR_SUCCESS, fg="white",
            font=("Arial", 11, "bold"), padx=20, pady=10,
            command=self.validar_y_crear,
            relief="flat", cursor="hand2"
        ).pack(side="left", padx=5)
        
        tk.Button(
            buttons_frame, text="Limpiar", bg="#757575", fg="white",
            font=("Arial", 11, "bold"), padx=20, pady=10,
            command=self.limpiar_formulario,
            relief="flat", cursor="hand2"
        ).pack(side="left", padx=5)
        
        tk.Button(
            buttons_frame, text="Cancelar", bg="#9e9e9e", fg="white",
            font=("Arial", 11, "bold"), padx=20, pady=10,
            command=self.cancelar,
            relief="flat", cursor="hand2"
        ).pack(side="left", padx=5)
    
    def _crear_seccion(self, titulo: str, parent):
        """Crea un título de sección"""
        frame = tk.Frame(parent, bg=self.COLOR_BG)
        frame.pack(fill="x", padx=5, pady=(15, 5))
        
        tk.Label(
            frame, text=titulo, bg=self.COLOR_BG, fg=self.COLOR_ACCENT,
            font=("Arial", 12, "bold")
        ).pack(anchor="w")
        
        tk.Frame(frame, bg=self.COLOR_ACCENT, height=2).pack(fill="x", pady=(5, 0))
    
    def _crear_field(self, parent, label: str, key: str, tipo: str = "entry",
                    opciones: list = None, requerido: bool = False,
                    validacion: str = None, on_change=None,
                    placeholder: str = "", parent_frame=None):
        """Crea un campo del formulario"""
        frame = tk.Frame(parent if parent_frame is None else parent_frame, bg=self.COLOR_BG)
        frame.pack(fill="x", padx=5, pady=8)
        
        # Label
        label_text = f"{label}{'*' if requerido else ''}"
        tk.Label(
            frame, text=label_text, bg=self.COLOR_BG, fg=self.COLOR_TEXT,
            font=self.font_label, width=25, anchor="w"
        ).pack(side="left", padx=(0, 10))
        
        # Campo según tipo
        widget = None
        
        if tipo == "entry":
            widget = tk.Entry(frame, font=self.font_normal, width=40)
            if placeholder:
                widget.insert(0, placeholder)
                widget.config(fg="#999999")
                widget.bind("<FocusIn>", lambda e: self._clear_placeholder(e, placeholder))
                widget.bind("<FocusOut>", lambda e: self._restore_placeholder(e, placeholder))
            
            if on_change:
                widget.bind("<KeyRelease>", lambda e: on_change())
            
            widget.pack(side="left", fill="x", expand=True)
        
        elif tipo == "combo":
            widget = ttk.Combobox(frame, values=opciones or [], state="readonly", width=37, font=self.font_normal)
            if on_change:
                widget.bind("<<ComboboxSelected>>", lambda e: on_change())
            widget.pack(side="left", fill="x", expand=True)
        
        elif tipo == "date":
            widget = tk.Entry(frame, font=self.font_normal, width=40)
            widget.insert(0, "YYYY-MM-DD")
            widget.config(fg="#999999")
            widget.bind("<FocusIn>", lambda e: self._clear_placeholder(e, "YYYY-MM-DD"))
            widget.bind("<FocusOut>", lambda e: self._restore_placeholder(e, "YYYY-MM-DD"))
            widget.pack(side="left", fill="x", expand=True)
        
        elif tipo == "text":
            widget = tk.Text(frame, font=self.font_normal, height=4, width=40)
            widget.pack(side="left", fill="both", expand=True)
        
        # Guardar referencia
        self.campos_dinamicos[key] = {
            "widget": widget,
            "tipo": tipo,
            "requerido": requerido,
            "validacion": validacion,
            "label": label
        }
    
    def _clear_placeholder(self, event, placeholder):
        """Limpia placeholder al hacer focus"""
        if event.widget.get() == placeholder:
            event.widget.delete(0, tk.END)
            event.widget.config(fg=self.COLOR_TEXT)
    
    def _restore_placeholder(self, event, placeholder):
        """Restaura placeholder si está vacío"""
        if not event.widget.get():
            event.widget.insert(0, placeholder)
            event.widget.config(fg="#999999")
    
    def actualizar_campos_rol(self):
        """Actualiza campos dinámicos según el rol seleccionado"""
        # Limpiar frame dinámico
        for widget in self.frame_dinamico.winfo_children():
            widget.destroy()
        
        rol = self.campos_dinamicos.get("rol", {}).get("widget").get()
        
        # Mostrar/ocultar email según rol
        if rol == "Estudiante":
            self.frame_credenciales.pack_forget()
        else:
            self.frame_credenciales.pack(fill="x", padx=5, pady=10, after=self.frame_dinamico)
        
        # Campos específicos por rol
        if rol == "Profesor":
            tk.Label(
                self.frame_dinamico, text="Campos Específicos del Profesor",
                bg=self.COLOR_BG, fg=self.COLOR_ACCENT, font=self.font_label
            ).pack(anchor="w", padx=5, pady=(10, 5))
            
            tk.Frame(self.frame_dinamico, bg=self.COLOR_ACCENT, height=2).pack(fill="x", padx=5, pady=(0, 10))
            
            self._crear_field(
                self.frame_dinamico, "Especialidad",
                "especialidad", tipo="entry",
                requerido=True,
                placeholder="Ej: Matemáticas, Español",
                parent_frame=self.frame_dinamico
            )
    
    def validar_y_crear(self):
        """Valida y crea el usuario"""
        if not self.callback_crear:
            messagebox.showerror("Error", "Callback de creación no configurado")
            return
        
        # Recolectar datos
        datos = {}
        for key, info in self.campos_dinamicos.items():
            widget = info["widget"]
            valor = widget.get()
            
            # Ignorar placeholders
            if valor in ["YYYY-MM-DD", "Ej:", "Opcional"]:
                valor = ""
            
            # Limpieza
            if valor:
                valor = valor.strip()
            
            datos[key] = valor
        
        # Validación básica en UI antes de enviar
        errores = []
        for key, info in self.campos_dinamicos.items():
            if info["requerido"] and not datos.get(key):
                errores.append(f"• {info['label']} es requerido")
        
        if errores:
            messagebox.showerror("Validación", "Errores:\n" + "\n".join(errores))
            return
        
        # Llamar callback
        self.callback_crear(datos)
    
    def limpiar_formulario(self):
        """Limpia todos los campos del formulario"""
        for key, info in self.campos_dinamicos.items():
            widget = info["widget"]
            if info["tipo"] == "combo":
                widget.set("")
            else:
                widget.delete(0, tk.END)
    
    def cancelar(self):
        """Cierra el formulario"""
        if messagebox.askyesno("Cancelar", "¿Deseas cancelar la creación de usuario?"):
            self.parent.destroy()
    
    def obtener_datos(self) -> dict:
        """Obtiene todos los datos del formulario"""
        datos = {}
        for key, info in self.campos_dinamicos.items():
            widget = info["widget"]
            valor = widget.get()
            if valor not in ["YYYY-MM-DD", "Ej:", "Opcional"]:
                datos[key] = valor.strip() if valor else ""
        return datos


def crear_ventana_formulario(roles_disponibles: list, callback_crear=None, 
                            config_colors: dict = None) -> tk.Toplevel:
    """Factory para crear ventana con formulario de usuario"""
    ventana = tk.Toplevel()
    ventana.title("Crear Nuevo Usuario")
    ventana.geometry("700x900")
    ventana.resizable(True, True)
    
    # Centro la ventana
    ventana.update_idletasks()
    x = (ventana.winfo_screenwidth() // 2) - (700 // 2)
    y = (ventana.winfo_screenheight() // 2) - (900 // 2)
    ventana.geometry(f"700x900+{x}+{y}")
    
    formulario = FormularioCrearUsuario(ventana, roles_disponibles, callback_crear, config_colors)
    
    return ventana, formulario
