"""
📋 InhabilitarUsuarioDialog
Diálogo modal para solicitar justificación de inhabilitación (CU-08)

Implementa los pasos 3-5 del diagrama:
- Paso 3: Formulario emergente con campo de justificación
- Paso 4: Usuario digita justificación (validación obligatoria)
- Paso 5: Usuario hace clic en "Confirmar"

Autor: Sistema FIS
Fecha: 11 de diciembre de 2025
"""

import tkinter as tk
from tkinter import ttk, messagebox
from app.services.inhabilitacion_usuario_service import InhabilitacionUsuarioService


class InhabilitarUsuarioDialog:
    """
    Diálogo modal para inhabilitar un usuario con justificación obligatoria.
    
    FLUJO DEL DIÁLOGO:
    1. Muestra información del usuario a inhabilitar
    2. Solicita justificación obligatoria en campo de texto
    3. Valida que no esté vacía
    4. Llama al servicio para inhabilitar
    5. Muestra mensaje de confirmación (Paso 10)
    """
    
    def __init__(self, parent, id_usuario: int, correo_usuario: str, 
                 admin_id: int = None, callback=None):
        """
        Inicializa el diálogo de inhabilitación.
        
        Args:
            parent: Ventana padre
            id_usuario (int): ID del usuario a inhabilitar
            correo_usuario (str): Correo del usuario (para mostrar)
            admin_id (int, optional): ID del administrador (validación opcional)
            callback (callable, optional): Función a llamar después de inhabilitar
        """
        
        self.parent = parent
        self.id_usuario = id_usuario
        self.correo_usuario = correo_usuario
        self.admin_id = admin_id
        self.callback = callback
        self.resultado = None  # True si se inhabilitó, False si se canceló
        
        # Crear ventana modal
        self.window = tk.Toplevel(parent)
        self.window.title("Inhabilitar Usuario - CU-08")
        self.window.geometry("550x400")
        self.window.resizable(False, False)
        self.window.transient(parent)
        self.window.grab_set()
        
        # Centrar ventana
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (550 // 2)
        y = (self.window.winfo_screenheight() // 2) - (400 // 2)
        self.window.geometry(f"550x400+{x}+{y}")
        
        # Construir interfaz (Paso 3)
        self._crear_interfaz()
        
        # Enfocar campo de justificación
        self.text_justificacion.focus_set()
    
    
    def _crear_interfaz(self):
        """
        Crea la interfaz del diálogo (PASO 3).
        
        ELEMENTOS:
        - Encabezado con advertencia
        - Información del usuario
        - Campo de texto para justificación (obligatorio)
        - Botones: Confirmar / Cancelar
        """
        
        # ========================================
        # ENCABEZADO CON ADVERTENCIA
        # ========================================
        header_frame = tk.Frame(self.window, bg="#e74c3c", pady=15)
        header_frame.pack(fill=tk.X)
        
        tk.Label(
            header_frame,
            text="⚠️ INHABILITAR USUARIO",
            font=("Arial", 14, "bold"),
            bg="#e74c3c",
            fg="white"
        ).pack()
        
        # ========================================
        # CONTENIDO PRINCIPAL
        # ========================================
        content_frame = tk.Frame(self.window, bg="#f8f9fa", padx=30, pady=20)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Información del usuario
        info_frame = tk.Frame(content_frame, bg="#ffffff", relief=tk.SOLID, borderwidth=1)
        info_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(
            info_frame,
            text="Usuario a inhabilitar:",
            font=("Arial", 10, "bold"),
            bg="#ffffff",
            anchor="w"
        ).pack(fill=tk.X, padx=15, pady=(10, 5))
        
        tk.Label(
            info_frame,
            text=self.correo_usuario,
            font=("Arial", 11),
            bg="#ffffff",
            fg="#2c3e50",
            anchor="w"
        ).pack(fill=tk.X, padx=15, pady=(0, 10))
        
        # Advertencia
        warning_label = tk.Label(
            content_frame,
            text="⚠️ Esta acción desactivará el acceso del usuario al sistema.\n"
                 "Debe proporcionar una justificación obligatoria.",
            font=("Arial", 9),
            bg="#fff3cd",
            fg="#856404",
            relief=tk.SOLID,
            borderwidth=1,
            padx=10,
            pady=10,
            justify=tk.LEFT,
            wraplength=470
        )
        warning_label.pack(fill=tk.X, pady=(0, 15))
        
        # Label de justificación
        tk.Label(
            content_frame,
            text="Justificación de la inhabilitación: *",
            font=("Arial", 10, "bold"),
            bg="#f8f9fa",
            anchor="w"
        ).pack(fill=tk.X)
        
        # Campo de texto para justificación (PASO 3 - Campo obligatorio)
        text_frame = tk.Frame(content_frame, bg="#f8f9fa")
        text_frame.pack(fill=tk.BOTH, expand=True, pady=(5, 0))
        
        # Scrollbar
        scrollbar = tk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Text widget
        self.text_justificacion = tk.Text(
            text_frame,
            height=6,
            font=("Arial", 10),
            wrap=tk.WORD,
            yscrollcommand=scrollbar.set,
            relief=tk.SOLID,
            borderwidth=1
        )
        self.text_justificacion.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.text_justificacion.yview)
        
        # Placeholder
        self._agregar_placeholder()
        
        # ========================================
        # BOTONES DE ACCIÓN
        # ========================================
        button_frame = tk.Frame(self.window, bg="#f8f9fa", pady=15)
        button_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        # Botón Cancelar
        btn_cancelar = tk.Button(
            button_frame,
            text="Cancelar",
            font=("Arial", 10),
            bg="#95a5a6",
            fg="white",
            activebackground="#7f8c8d",
            activeforeground="white",
            relief=tk.FLAT,
            cursor="hand2",
            width=12,
            command=self._cancelar
        )
        btn_cancelar.pack(side=tk.RIGHT, padx=(10, 30))
        
        # Botón Confirmar (PASO 5)
        btn_confirmar = tk.Button(
            button_frame,
            text="✓ Confirmar",
            font=("Arial", 10, "bold"),
            bg="#e74c3c",
            fg="white",
            activebackground="#c0392b",
            activeforeground="white",
            relief=tk.FLAT,
            cursor="hand2",
            width=12,
            command=self._confirmar_inhabilitacion
        )
        btn_confirmar.pack(side=tk.RIGHT, padx=(30, 10))
        
        # Bind Enter key
        self.window.bind('<Return>', lambda e: self._confirmar_inhabilitacion())
        self.window.bind('<Escape>', lambda e: self._cancelar())
    
    
    def _agregar_placeholder(self):
        """Agrega placeholder al campo de texto."""
        
        placeholder_text = "Ejemplo: Usuario inhabilitado por incumplimiento de normas institucionales..."
        
        # Insertar placeholder
        self.text_justificacion.insert("1.0", placeholder_text)
        self.text_justificacion.config(fg="#999999")
        
        # Eventos para manejar placeholder
        def on_focus_in(event):
            if self.text_justificacion.get("1.0", "end-1c") == placeholder_text:
                self.text_justificacion.delete("1.0", tk.END)
                self.text_justificacion.config(fg="#000000")
        
        def on_focus_out(event):
            if not self.text_justificacion.get("1.0", "end-1c").strip():
                self.text_justificacion.insert("1.0", placeholder_text)
                self.text_justificacion.config(fg="#999999")
        
        self.text_justificacion.bind("<FocusIn>", on_focus_in)
        self.text_justificacion.bind("<FocusOut>", on_focus_out)
    
    
    def _confirmar_inhabilitacion(self):
        """
        Confirma la inhabilitación del usuario (PASO 5).
        
        FLUJO:
        1. Obtener justificación del campo de texto (Paso 4)
        2. Validar que no esté vacía (Paso 7.3)
        3. Validación opcional: no auto-inhabilitarse
        4. Llamar al servicio para inhabilitar (Pasos 7-8)
        5. Mostrar mensaje de éxito (Paso 10)
        6. Cerrar diálogo y ejecutar callback
        """
        
        # PASO 4: Obtener justificación
        justificacion = self.text_justificacion.get("1.0", "end-1c").strip()
        
        # Validar placeholder
        placeholder = "Ejemplo: Usuario inhabilitado por incumplimiento de normas institucionales..."
        if justificacion == placeholder or not justificacion:
            messagebox.showerror(
                "Campo Obligatorio",
                "La justificación es obligatoria.\n\n"
                "Por favor, proporciona una razón válida para inhabilitar este usuario.",
                parent=self.window
            )
            self.text_justificacion.focus_set()
            return
        
        # VALIDACIÓN ADICIONAL OPCIONAL: Evitar auto-inhabilitación
        if self.admin_id and self.admin_id == self.id_usuario:
            messagebox.showerror(
                "Operación No Permitida",
                "No puedes inhabilitarte a ti mismo.\n\n"
                "Contacta a otro administrador si necesitas ser inhabilitado.",
                parent=self.window
            )
            return
        
        # Confirmación adicional
        confirmar = messagebox.askyesno(
            "Confirmar Inhabilitación",
            f"¿Está seguro de inhabilitar al usuario?\n\n"
            f"Usuario: {self.correo_usuario}\n"
            f"Justificación: {justificacion[:100]}...\n\n"
            f"El usuario perderá acceso al sistema.",
            parent=self.window,
            icon="warning"
        )
        
        if not confirmar:
            return
        
        # PASOS 7-8: Llamar al servicio para inhabilitar
        exito, mensaje = InhabilitacionUsuarioService.inhabilitar_usuario(
            id_usuario=self.id_usuario,
            justificacion=justificacion,
            admin_id=self.admin_id
        )
        
        if exito:
            # PASO 10: Mostrar mensaje de éxito
            messagebox.showinfo(
                "Usuario Inhabilitado",
                mensaje,  # "El usuario ha sido inhabilitado satisfactoriamente."
                parent=self.window
            )
            
            self.resultado = True
            
            # PASO 11-12: Usuario hace clic en "Aceptar" y finaliza
            self.window.destroy()
            
            # Ejecutar callback si existe (actualizar lista)
            if self.callback:
                self.callback()
        
        else:
            # Mostrar error
            messagebox.showerror(
                "Error al Inhabilitar",
                mensaje,
                parent=self.window
            )
    
    
    def _cancelar(self):
        """Cancela la operación y cierra el diálogo."""
        
        self.resultado = False
        self.window.destroy()


# ============================================
# FUNCIÓN DE UTILIDAD
# ============================================

def abrir_dialogo_inhabilitar(parent, id_usuario: int, correo_usuario: str, 
                               admin_id: int = None, callback=None):
    """
    Función auxiliar para abrir el diálogo de inhabilitación.
    
    Args:
        parent: Ventana padre
        id_usuario (int): ID del usuario a inhabilitar
        correo_usuario (str): Correo del usuario
        admin_id (int, optional): ID del administrador
        callback (callable, optional): Función a ejecutar después
    
    Returns:
        InhabilitarUsuarioDialog: Instancia del diálogo
    """
    
    return InhabilitarUsuarioDialog(
        parent=parent,
        id_usuario=id_usuario,
        correo_usuario=correo_usuario,
        admin_id=admin_id,
        callback=callback
    )
