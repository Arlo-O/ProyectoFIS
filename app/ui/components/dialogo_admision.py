"""
Diálogo de Admisión de Aspirantes
Implementa CU-18: Admitir aspirante

Este diálogo sigue el flujo exacto del diagrama de actividades:
1. Directivo hace clic en "Diligenciar admisión"
2. Sistema habilita botones (Admitir/Rechazar)
3. Directivo elige opción
4. Sistema evalúa:
   - Si Admitir: guardar y cerrar
   - Si Rechazar: habilitar campo justificación
5. Si rechazo: validar justificación y guardar
"""

import tkinter as tk
from tkinter import messagebox
import tkinter.ttk as ttk
from ..config import *
from app.services.servicio_admision import ServicioAdmision
from .dialogo_hoja_vida import abrir_dialogo_crear_hoja_vida


class DialogoAdmisionAspirante:
    """
    Diálogo para admitir o rechazar un aspirante.
    Implementa el flujo del CU-18.
    """
    
    def __init__(self, parent, id_aspirante: int, nombre_aspirante: str, callback_actualizar=None):
        """
        Inicializa el diálogo de admisión.
        
        Args:
            parent: Ventana padre
            id_aspirante: ID del aspirante
            nombre_aspirante: Nombre completo del aspirante
            callback_actualizar: Función a llamar después de admitir/rechazar
        """
        self.parent = parent
        self.id_aspirante = id_aspirante
        self.nombre_aspirante = nombre_aspirante
        self.callback_actualizar = callback_actualizar
        self.servicio = ServicioAdmision()
        
        # Variables de estado
        self.opcion_seleccionada = None
        
        # Crear ventana de diálogo
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(f"Admisión de Aspirante - {nombre_aspirante}")
        self.dialog.geometry("600x500")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Centrar ventana
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (600 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (500 // 2)
        self.dialog.geometry(f"600x500+{x}+{y}")
        
        self._crear_ui()
    
    def _crear_ui(self):
        """Crea la interfaz del diálogo"""
        
        # PASO 2: Header del diálogo
        header = tk.Frame(self.dialog, bg=COLOR_HEADER_PRE, height=80)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        tk.Label(
            header,
            text="✅ Diligenciar Admisión de Aspirante",
            bg=COLOR_HEADER_PRE,
            fg=COLOR_TEXT_PRE,
            font=FONT_H2
        ).pack(pady=20)
        
        # Contenedor principal
        main_container = tk.Frame(self.dialog, bg="#ffffff", padx=30, pady=30)
        main_container.pack(fill="both", expand=True)
        
        # Información del aspirante
        info_frame = tk.Frame(main_container, bg="#f0f8ff", relief="solid", bd=1, padx=20, pady=15)
        info_frame.pack(fill="x", pady=(0, 30))
        
        tk.Label(
            info_frame,
            text=f"📋 Aspirante: {self.nombre_aspirante}",
            bg="#f0f8ff",
            font=FONT_H3,
            fg="#2c5aa0"
        ).pack(anchor="w", pady=(0, 5))
        
        tk.Label(
            info_frame,
            text=f"ID: {self.id_aspirante}",
            bg="#f0f8ff",
            font=FONT_P,
            fg="#555555"
        ).pack(anchor="w")
        
        # Instrucción
        tk.Label(
            main_container,
            text="Seleccione una opción de admisión para el aspirante:",
            bg="#ffffff",
            font=FONT_P_BOLD,
            fg="#333333"
        ).pack(anchor="w", pady=(0, 20))
        
        # PASO 3: Frame de botones de decisión (inicialmente habilitado)
        self.decision_frame = tk.Frame(main_container, bg="#ffffff")
        self.decision_frame.pack(fill="x", pady=(0, 20))
        
        # PASO 3: Botón Admitir
        self.btn_admitir = tk.Button(
            self.decision_frame,
            text="✅ Admitir",
            font=FONT_P_BOLD,
            bg="#28a745",
            fg="#ffffff",
            activebackground="#218838",
            activeforeground="#ffffff",
            relief="raised",
            bd=2,
            padx=40,
            pady=15,
            cursor="hand2",
            command=self._on_admitir_click
        )
        self.btn_admitir.pack(side="left", padx=(0, 20), fill="x", expand=True)
        
        # PASO 3: Botón Rechazar
        self.btn_rechazar = tk.Button(
            self.decision_frame,
            text="❌ Rechazar",
            font=FONT_P_BOLD,
            bg="#dc3545",
            fg="#ffffff",
            activebackground="#c82333",
            activeforeground="#ffffff",
            relief="raised",
            bd=2,
            padx=40,
            pady=15,
            cursor="hand2",
            command=self._on_rechazar_click
        )
        self.btn_rechazar.pack(side="left", fill="x", expand=True)
        
        # PASO 6B: Frame de justificación (inicialmente oculto)
        self.justificacion_frame = tk.Frame(main_container, bg="#ffffff")
        
        tk.Label(
            self.justificacion_frame,
            text="📝 Justificación del Rechazo (Obligatorio):",
            bg="#ffffff",
            font=FONT_P_BOLD,
            fg="#dc3545"
        ).pack(anchor="w", pady=(0, 10))
        
        # PASO 6B: Campo de texto para justificación
        self.txt_justificacion = tk.Text(
            self.justificacion_frame,
            height=8,
            width=60,
            font=FONT_P,
            relief="solid",
            bd=1,
            wrap="word"
        )
        self.txt_justificacion.pack(fill="both", expand=True, pady=(0, 15))
        
        # PASO 8B: Botón Confirmar (dentro del frame de justificación)
        self.btn_confirmar_rechazo = tk.Button(
            self.justificacion_frame,
            text="✓ Confirmar Rechazo",
            font=FONT_P_BOLD,
            bg="#dc3545",
            fg="#ffffff",
            activebackground="#c82333",
            activeforeground="#ffffff",
            relief="raised",
            bd=2,
            padx=40,
            pady=12,
            cursor="hand2",
            command=self._on_confirmar_rechazo
        )
        self.btn_confirmar_rechazo.pack(fill="x")
        
        # Botones de control en el footer
        footer = tk.Frame(self.dialog, bg="#f8f9fa", height=70)
        footer.pack(fill="x", side="bottom")
        footer.pack_propagate(False)
        
        tk.Button(
            footer,
            text="Cancelar",
            font=FONT_P,
            bg="#6c757d",
            fg="#ffffff",
            activebackground="#5a6268",
            activeforeground="#ffffff",
            relief="raised",
            bd=1,
            padx=30,
            pady=8,
            cursor="hand2",
            command=self._cancelar
        ).pack(side="right", padx=30, pady=15)
    
    def _on_admitir_click(self):
        """
        PASO 4-5: Directivo hace clic en "Admitir"
        Sistema evalúa la decisión → Ruta de ADMISIÓN
        """
        # Confirmar acción
        respuesta = messagebox.askyesno(
            "Confirmar Admisión",
            f"¿Está seguro de admitir al aspirante {self.nombre_aspirante}?\n\n"
            "Esta acción cambiará el estado del aspirante a 'Admitido'.",
            parent=self.dialog
        )
        
        if not respuesta:
            return
        
        # PASO 6A-7A: Llamar al servicio para admitir
        exito, mensaje = self.servicio.admitir_aspirante(self.id_aspirante)
        
        if exito:
            messagebox.showinfo(
                "Admisión Exitosa",
                mensaje,
                parent=self.dialog
            )
            
            # PASO 8A-9A: Finalizar flujo de admisión
            if self.callback_actualizar:
                self.callback_actualizar()
            
            self.dialog.destroy()
            
            # CU-19: Preguntar si desea crear la hoja de vida ahora
            respuesta_hoja_vida = messagebox.askyesno(
                "Crear Hoja de Vida",
                f"El aspirante {self.nombre_aspirante} ha sido admitido exitosamente.\n\n"
                "¿Desea crear la Hoja de Vida del estudiante ahora?\n\n"
                "(También puede hacerlo más tarde desde el módulo de estudiantes)",
                parent=self.parent
            )
            
            if respuesta_hoja_vida:
                # PASO 1 del CU-19: Administrador llega después de admitir
                abrir_dialogo_crear_hoja_vida(
                    self.parent,
                    self.id_aspirante,
                    self.nombre_aspirante,
                    callback_finalizar=self.callback_actualizar
                )
        else:
            messagebox.showerror(
                "Error",
                f"No se pudo admitir al aspirante:\n{mensaje}",
                parent=self.dialog
            )
    
    def _on_rechazar_click(self):
        """
        PASO 4-5: Directivo hace clic en "Rechazar"
        Sistema evalúa la decisión → Ruta de RECHAZO
        PASO 6B: Habilitar campo de justificación
        """
        self.opcion_seleccionada = "rechazar"
        
        # Deshabilitar botones de decisión
        self.btn_admitir.config(state="disabled", bg="#cccccc", cursor="arrow")
        self.btn_rechazar.config(state="disabled", bg="#cccccc", cursor="arrow")
        
        # PASO 6B: Mostrar el frame de justificación
        self.justificacion_frame.pack(fill="both", expand=True, pady=(10, 0))
        
        # Enfocar el campo de texto
        self.txt_justificacion.focus_set()
    
    def _on_confirmar_rechazo(self):
        """
        PASO 8B: Directivo hace clic en "Confirmar"
        PASO 9B: Validar justificación
        PASO 10B-11B: Registrar y guardar en BD
        PASO 12B: Finalizar flujo
        """
        # PASO 7B: Obtener la justificación digitada
        justificacion = self.txt_justificacion.get("1.0", "end-1c").strip()
        
        # PASO 9B: Validar que la justificación no esté vacía
        if not justificacion:
            messagebox.showwarning(
                "Justificación Requerida",
                "Debe proporcionar una justificación para rechazar al aspirante.",
                parent=self.dialog
            )
            self.txt_justificacion.focus_set()
            return
        
        # Confirmar acción
        respuesta = messagebox.askyesno(
            "Confirmar Rechazo",
            f"¿Está seguro de rechazar al aspirante {self.nombre_aspirante}?\n\n"
            f"Justificación:\n{justificacion[:100]}{'...' if len(justificacion) > 100 else ''}",
            parent=self.dialog
        )
        
        if not respuesta:
            return
        
        # PASO 10B-11B: Llamar al servicio para rechazar
        exito, mensaje = self.servicio.rechazar_aspirante(self.id_aspirante, justificacion)
        
        if exito:
            messagebox.showinfo(
                "Rechazo Registrado",
                mensaje,
                parent=self.dialog
            )
            
            # PASO 12B: Finalizar flujo
            if self.callback_actualizar:
                self.callback_actualizar()
            
            self.dialog.destroy()
        else:
            messagebox.showerror(
                "Error",
                f"No se pudo rechazar al aspirante:\n{mensaje}",
                parent=self.dialog
            )
    
    def _cancelar(self):
        """Cancela la operación y cierra el diálogo"""
        self.dialog.destroy()


def abrir_dialogo_admision(parent, id_aspirante: int, nombre_aspirante: str, callback_actualizar=None):
    """
    Función auxiliar para abrir el diálogo de admisión.
    
    PASO 1-2: Directivo inicia el caso de uso y hace clic en "Diligenciar admisión"
    
    Args:
        parent: Ventana padre
        id_aspirante: ID del aspirante
        nombre_aspirante: Nombre del aspirante
        callback_actualizar: Función a llamar después de admitir/rechazar
    """
    DialogoAdmisionAspirante(parent, id_aspirante, nombre_aspirante, callback_actualizar)
