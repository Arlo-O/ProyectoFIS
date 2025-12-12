"""
Diálogo de Creación de Hoja de Vida Académica
Implementa CU-19: Crear hoja de vida del estudiante

Este diálogo sigue el flujo exacto del diagrama de actividades:
1. Sistema carga datos del estudiante admitido
2. Sistema carga formato base de hoja de vida
3. Sistema llena automáticamente datos básicos
4. Administrador visualiza datos faltantes
5. Administrador digita datos faltantes
6. Sistema valida con contador de intentos (máximo 3)
7. Si correcto: guardar, si no: mostrar errores y reintentar
"""

import tkinter as tk
from tkinter import messagebox, scrolledtext
import tkinter.ttk as ttk
from ..config import *
from app.services.servicio_hoja_vida import ServicioHojaVida
from app.ui.components.session import get_current_user_id


class DialogoCrearHojaVida:
    """
    Diálogo para crear la hoja de vida de un estudiante admitido.
    Implementa el flujo del CU-19 con contador de intentos.
    """
    
    def __init__(self, parent, id_aspirante: int, nombre_aspirante: str, callback_finalizar=None):
        """
        Inicializa el diálogo de creación de hoja de vida.
        
        Args:
            parent: Ventana padre
            id_aspirante: ID del aspirante admitido
            nombre_aspirante: Nombre del aspirante
            callback_finalizar: Función a llamar al finalizar
        """
        self.parent = parent
        self.id_aspirante = id_aspirante
        self.nombre_aspirante = nombre_aspirante
        self.callback_finalizar = callback_finalizar
        self.servicio = ServicioHojaVida()
        
        # PASO 2: Cargar datos del estudiante admitido
        self.datos_estudiante = None
        self.formato_base = None
        
        # PASO 7: Inicializar contador de intentos
        self.contador_intentos = self.servicio.inicializar_contador_intentos(id_aspirante)
        
        # Diccionarios para almacenar widgets
        self.campos_entrada = {}
        self.labels_error = {}
        
        # Crear ventana de diálogo
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(f"Crear Hoja de Vida - {nombre_aspirante}")
        self.dialog.geometry("900x700")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Centrar ventana
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (900 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (700 // 2)
        self.dialog.geometry(f"900x700+{x}+{y}")
        
        # PASO 2-4: Cargar datos y crear UI
        self._cargar_datos_iniciales()
        if self.datos_estudiante:
            self._crear_ui()
        else:
            self.dialog.destroy()
    
    def _cargar_datos_iniciales(self):
        """PASO 2: Cargar datos del estudiante admitido"""
        exito, datos, mensaje = self.servicio.cargar_datos_estudiante_admitido(self.id_aspirante)
        
        if not exito:
            messagebox.showerror(
                "Error",
                f"No se pudieron cargar los datos del estudiante:\n{mensaje}",
                parent=self.parent
            )
            return
        
        self.datos_estudiante = datos
        
        # PASO 3: Cargar formato base
        self.formato_base = self.servicio.obtener_formato_base_hoja_vida()
    
    def _crear_ui(self):
        """Crea la interfaz del diálogo"""
        
        # Header
        header = tk.Frame(self.dialog, bg=COLOR_HEADER_PRE, height=80)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        tk.Label(
            header,
            text="📋 Crear Hoja de Vida del Estudiante",
            bg=COLOR_HEADER_PRE,
            fg=COLOR_TEXT_PRE,
            font=FONT_H2
        ).pack(pady=20)
        
        # Frame principal con scroll
        main_container = tk.Frame(self.dialog, bg="#ffffff")
        main_container.pack(fill="both", expand=True)
        
        canvas = tk.Canvas(main_container, bg="#ffffff", highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#ffffff")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True, padx=20, pady=20)
        scrollbar.pack(side="right", fill="y")
        
        # Contador de intentos visible
        self.label_intentos = tk.Label(
            scrollable_frame,
            text=f"Intentos: {self.contador_intentos}/{self.servicio.LIMITE_INTENTOS}",
            bg="#ffffff",
            font=FONT_P_BOLD,
            fg="#dc3545" if self.contador_intentos > 0 else "#28a745"
        )
        self.label_intentos.pack(anchor="e", pady=(0, 10))
        
        # PASO 4: Sección de datos automáticos (ya cargados)
        self._crear_seccion_datos_automaticos(scrollable_frame)
        
        # PASO 5-6: Sección de datos faltantes (a diligenciar)
        self._crear_seccion_datos_faltantes(scrollable_frame)
        
        # Footer con botones
        footer = tk.Frame(self.dialog, bg="#f8f9fa", height=80)
        footer.pack(fill="x", side="bottom")
        footer.pack_propagate(False)
        
        btn_frame = tk.Frame(footer, bg="#f8f9fa")
        btn_frame.pack(expand=True)
        
        # PASO 8: Botón Confirmar
        tk.Button(
            btn_frame,
            text="✓ Confirmar y Crear Hoja de Vida",
            font=FONT_P_BOLD,
            bg="#28a745",
            fg="#ffffff",
            activebackground="#218838",
            activeforeground="#ffffff",
            relief="raised",
            bd=2,
            padx=30,
            pady=12,
            cursor="hand2",
            command=self._on_confirmar
        ).pack(side="left", padx=10)
        
        tk.Button(
            btn_frame,
            text="Cancelar",
            font=FONT_P,
            bg="#6c757d",
            fg="#ffffff",
            activebackground="#5a6268",
            activeforeground="#ffffff",
            relief="raised",
            bd=1,
            padx=30,
            pady=12,
            cursor="hand2",
            command=self._cancelar
        ).pack(side="left", padx=10)
    
    def _crear_seccion_datos_automaticos(self, parent):
        """PASO 4: Muestra datos que se llenaron automáticamente"""
        frame = tk.LabelFrame(
            parent,
            text="📌 Datos Cargados Automáticamente",
            bg="#e8f5e9",
            font=FONT_P_BOLD,
            fg="#2e7d32",
            padx=20,
            pady=15
        )
        frame.pack(fill="x", pady=(0, 20))
        
        datos_auto = [
            ("Nombre Completo:", self.datos_estudiante['nombre_completo']),
            ("Identificación:", f"{self.datos_estudiante['tipo_identificacion']}: {self.datos_estudiante['numero_identificacion']}"),
            ("Fecha de Nacimiento:", self.datos_estudiante['fecha_nacimiento'].strftime('%d/%m/%Y') if self.datos_estudiante['fecha_nacimiento'] else "N/A"),
            ("Género:", self.datos_estudiante['genero']),
            ("Grado Solicitado:", self.datos_estudiante['grado_solicitado']),
        ]
        
        for i, (label, valor) in enumerate(datos_auto):
            row_frame = tk.Frame(frame, bg="#e8f5e9")
            row_frame.pack(fill="x", pady=3)
            
            tk.Label(
                row_frame,
                text=label,
                bg="#e8f5e9",
                font=FONT_P_BOLD,
                width=25,
                anchor="w"
            ).pack(side="left")
            
            tk.Label(
                row_frame,
                text=valor,
                bg="#e8f5e9",
                font=FONT_P,
                anchor="w"
            ).pack(side="left", fill="x", expand=True)
    
    def _crear_seccion_datos_faltantes(self, parent):
        """PASO 5-6: Sección para diligenciar datos faltantes"""
        frame = tk.LabelFrame(
            parent,
            text="✏️ Datos Faltantes (Diligenciar)",
            bg="#fff3e0",
            font=FONT_P_BOLD,
            fg="#e65100",
            padx=20,
            pady=15
        )
        frame.pack(fill="x", pady=(0, 20))
        
        # Instrucción
        tk.Label(
            frame,
            text="Complete los siguientes campos obligatorios:",
            bg="#fff3e0",
            font=FONT_P,
            fg="#555555"
        ).pack(anchor="w", pady=(0, 15))
        
        # Campo: Código de Matrícula
        self._crear_campo_texto(
            frame,
            "codigo_matricula",
            "Código de Matrícula *",
            "Ej: EST2025001 (6-10 caracteres alfanuméricos)"
        )
        
        # Campo: Estado de Salud
        self._crear_campo_texto_largo(
            frame,
            "estado_salud",
            "Estado de Salud *",
            "Describa el estado general de salud del estudiante"
        )
        
        # Separador
        tk.Label(
            frame,
            text="Información Opcional:",
            bg="#fff3e0",
            font=FONT_P_BOLD,
            fg="#555555"
        ).pack(anchor="w", pady=(20, 10))
        
        # Campo: Alergias
        self._crear_campo_lista(
            frame,
            "alergias",
            "Alergias Conocidas",
            "Una por línea. Ej: Polen, Penicilina"
        )
        
        # Campo: Tratamientos
        self._crear_campo_lista(
            frame,
            "tratamientos",
            "Tratamientos Actuales",
            "Una por línea. Ej: Inhalador para asma"
        )
        
        # Campo: Necesidades Educativas
        self._crear_campo_lista(
            frame,
            "necesidades_educativas",
            "Necesidades Educativas Especiales",
            "Una por línea. Ej: Apoyo con lectura"
        )
    
    def _crear_campo_texto(self, parent, nombre, etiqueta, placeholder):
        """Crea un campo de texto simple"""
        campo_frame = tk.Frame(parent, bg="#fff3e0")
        campo_frame.pack(fill="x", pady=8)
        
        tk.Label(
            campo_frame,
            text=etiqueta,
            bg="#fff3e0",
            font=FONT_P_BOLD,
            anchor="w"
        ).pack(fill="x", pady=(0, 5))
        
        entry = ttk.Entry(campo_frame, font=FONT_P, width=50)
        entry.pack(fill="x", pady=(0, 3))
        entry.insert(0, placeholder)
        entry.bind("<FocusIn>", lambda e: entry.delete(0, "end") if entry.get() == placeholder else None)
        
        # Label para errores
        error_label = tk.Label(
            campo_frame,
            text="",
            bg="#fff3e0",
            fg="#dc3545",
            font=FONT_P,
            anchor="w"
        )
        error_label.pack(fill="x")
        
        self.campos_entrada[nombre] = entry
        self.labels_error[nombre] = error_label
    
    def _crear_campo_texto_largo(self, parent, nombre, etiqueta, placeholder):
        """Crea un campo de texto largo (Text widget)"""
        campo_frame = tk.Frame(parent, bg="#fff3e0")
        campo_frame.pack(fill="x", pady=8)
        
        tk.Label(
            campo_frame,
            text=etiqueta,
            bg="#fff3e0",
            font=FONT_P_BOLD,
            anchor="w"
        ).pack(fill="x", pady=(0, 5))
        
        text = tk.Text(campo_frame, font=FONT_P, width=50, height=4, wrap="word")
        text.pack(fill="x", pady=(0, 3))
        text.insert("1.0", placeholder)
        text.bind("<FocusIn>", lambda e: text.delete("1.0", "end") if text.get("1.0", "end-1c") == placeholder else None)
        
        # Label para errores
        error_label = tk.Label(
            campo_frame,
            text="",
            bg="#fff3e0",
            fg="#dc3545",
            font=FONT_P,
            anchor="w"
        )
        error_label.pack(fill="x")
        
        self.campos_entrada[nombre] = text
        self.labels_error[nombre] = error_label
    
    def _crear_campo_lista(self, parent, nombre, etiqueta, placeholder):
        """Crea un campo de lista (Text widget para múltiples líneas)"""
        campo_frame = tk.Frame(parent, bg="#fff3e0")
        campo_frame.pack(fill="x", pady=8)
        
        tk.Label(
            campo_frame,
            text=etiqueta,
            bg="#fff3e0",
            font=FONT_P,
            anchor="w"
        ).pack(fill="x", pady=(0, 5))
        
        text = tk.Text(campo_frame, font=FONT_P, width=50, height=3, wrap="word")
        text.pack(fill="x", pady=(0, 3))
        text.insert("1.0", placeholder)
        text.bind("<FocusIn>", lambda e: text.delete("1.0", "end-1c") if text.get("1.0", "end-1c") == placeholder else None)
        
        tk.Label(
            campo_frame,
            text="(Opcional)",
            bg="#fff3e0",
            font=FONT_P,
            fg="#888888",
            anchor="w"
        ).pack(fill="x")
        
        self.campos_entrada[nombre] = text
    
    def _obtener_valor_campo(self, nombre):
        """Obtiene el valor de un campo"""
        widget = self.campos_entrada.get(nombre)
        if not widget:
            return ""
        
        if isinstance(widget, tk.Text):
            valor = widget.get("1.0", "end-1c").strip()
        else:
            valor = widget.get().strip()
        
        # Limpiar placeholders
        placeholders = [
            "Ej: EST2025001",
            "Describa el estado",
            "Una por línea",
        ]
        for ph in placeholders:
            if valor.startswith(ph):
                return ""
        
        return valor
    
    def _limpiar_errores(self):
        """Limpia todos los mensajes de error"""
        for label in self.labels_error.values():
            label.config(text="")
    
    def _mostrar_errores(self, errores_detallados):
        """PASO 12.1-12.2: Muestra mensajes de error y resalta campos"""
        for campo, mensaje in errores_detallados.items():
            if campo in self.labels_error:
                self.labels_error[campo].config(text=f"✗ {mensaje}")
            
            if campo in self.campos_entrada:
                widget = self.campos_entrada[campo]
                if isinstance(widget, tk.Text):
                    widget.config(bg="#ffe6e6")
                else:
                    widget.config(background="#ffe6e6")
    
    def _on_confirmar(self):
        """
        PASO 8: Administrador hace clic en "Confirmar"
        PASO 9: Sistema valida formato
        PASO 10: Decisión según resultado de validación
        """
        # Limpiar errores anteriores
        self._limpiar_errores()
        
        # Restaurar colores de fondo
        for widget in self.campos_entrada.values():
            if isinstance(widget, tk.Text):
                widget.config(bg="#ffffff")
            else:
                widget.config(background="#ffffff")
        
        # PASO 6: Recopilar datos ingresados
        datos_faltantes = {
            "codigo_matricula": self._obtener_valor_campo("codigo_matricula"),
            "estado_salud": self._obtener_valor_campo("estado_salud"),
            "alergias": [l.strip() for l in self._obtener_valor_campo("alergias").split("\n") if l.strip()],
            "tratamientos": [l.strip() for l in self._obtener_valor_campo("tratamientos").split("\n") if l.strip()],
            "necesidades_educativas": [l.strip() for l in self._obtener_valor_campo("necesidades_educativas").split("\n") if l.strip()],
        }
        
        # PASO 9: Validar formato
        formato_correcto, campos_error, errores_detallados = self.servicio.validar_formato_datos(datos_faltantes)
        
        # PASO 10: ¿El formato es correcto?
        if formato_correcto:
            # RUTA CORRECTA: PASO 15-18
            self._guardar_hoja_vida(datos_faltantes)
        else:
            # RUTA INCORRECTA: PASO 11-14
            self._manejar_error_validacion(campos_error, errores_detallados)
    
    def _guardar_hoja_vida(self, datos_faltantes):
        """PASO 15-18: Guardar la hoja de vida y finalizar"""
        # Obtener ID del usuario actual (administrador)
        id_usuario = get_current_user_id()
        if not id_usuario:
            messagebox.showerror(
                "Error",
                "No se pudo identificar al usuario actual",
                parent=self.dialog
            )
            return
        
        # PASO 15: Guardar en el datastore
        exito, mensaje = self.servicio.crear_estudiante_y_hoja_vida(
            self.id_aspirante,
            datos_faltantes,
            id_usuario
        )
        
        if exito:
            # PASO 16: Mensaje de éxito
            messagebox.showinfo(
                "Hoja de Vida Creada",
                "Hoja de vida creada exitosamente",
                parent=self.dialog
            )
            
            # PASO 17-18: Finalizar proceso
            if self.callback_finalizar:
                self.callback_finalizar()
            
            self.dialog.destroy()
        else:
            messagebox.showerror(
                "Error",
                f"No se pudo crear la hoja de vida:\n{mensaje}",
                parent=self.dialog
            )
    
    def _manejar_error_validacion(self, campos_error, errores_detallados):
        """PASO 11-14: Manejo de errores de validación"""
        # PASO 11: Incrementar contador
        self.contador_intentos = self.servicio.incrementar_contador(self.id_aspirante)
        
        # Actualizar label de intentos
        self.label_intentos.config(
            text=f"Intentos: {self.contador_intentos}/{self.servicio.LIMITE_INTENTOS}",
            fg="#dc3545"
        )
        
        # PASO 12: Evaluar contador
        if self.contador_intentos < self.servicio.LIMITE_INTENTOS:
            # PASO 12.1-12.2: Mostrar mensaje y resaltar errores
            self._mostrar_errores(errores_detallados)
            
            # PASO 12.1: Mensaje de campos con error
            mensaje_error = f"Se encontraron {len(campos_error)} errores en el formulario:\n\n"
            for campo, error in errores_detallados.items():
                mensaje_error += f"• {error}\n"
            mensaje_error += f"\nIntento {self.contador_intentos} de {self.servicio.LIMITE_INTENTOS}"
            
            # PASO 12.3: Administrador hace clic en "Entendido"
            messagebox.showwarning(
                "Errores de Validación",
                mensaje_error,
                parent=self.dialog
            )
            
            # PASO 12.4: Flujo regresa al paso 6 (el diálogo permanece abierto)
        else:
            # PASO 12.5-12.7: Límite alcanzado
            messagebox.showerror(
                "Límite de Intentos Alcanzado",
                f"Ha alcanzado el límite de {self.servicio.LIMITE_INTENTOS} intentos.\n\n"
                "El proceso de creación de hoja de vida ha sido cancelado.\n"
                "Deberá reiniciar el proceso desde el inicio.",
                parent=self.dialog
            )
            
            # PASO 12.7: El flujo termina sin registrar datos
            self.dialog.destroy()
    
    def _cancelar(self):
        """Cancela la operación y cierra el diálogo"""
        respuesta = messagebox.askyesno(
            "Confirmar Cancelación",
            "¿Está seguro de cancelar la creación de la hoja de vida?\n\n"
            "Los datos ingresados no se guardarán.",
            parent=self.dialog
        )
        
        if respuesta:
            self.dialog.destroy()


def abrir_dialogo_crear_hoja_vida(parent, id_aspirante: int, nombre_aspirante: str, callback_finalizar=None):
    """
    Función auxiliar para abrir el diálogo de creación de hoja de vida.
    
    PASO 1: Administrador llega a CU-19 luego de admitir al estudiante
    
    Args:
        parent: Ventana padre
        id_aspirante: ID del aspirante admitido
        nombre_aspirante: Nombre del aspirante
        callback_finalizar: Función a llamar al finalizar
    """
    DialogoCrearHojaVida(parent, id_aspirante, nombre_aspirante, callback_finalizar)
