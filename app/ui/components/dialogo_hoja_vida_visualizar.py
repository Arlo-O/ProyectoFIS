"""
CU-25: Visualizar/editar hoja de vida del estudiante

Diálogo que implementa la interfaz para visualización y edición de la hoja de vida.

Flujo:
1. Visualización interrumpible (PASO 4-5)
2. Modo edición con campos permitidos (PASO 6-8)
3. Validación y manejo de errores (PASO 10-11)
4. Guardado exitoso (PASO 12-14)
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from typing import Optional, Dict
from datetime import datetime
import json

from app.services.servicio_hoja_vida import ServicioHojaVida


class DialogoHojaVidaVisualizar(tk.Toplevel):
    """
    Diálogo para visualizar y editar la hoja de vida del estudiante.
    
    Implementa:
    - Sección interrumpible de visualización (PASO 5)
    - Campos editables vs no editables (PASO 7)
    - Validación de modificaciones (PASO 10-11)
    """
    
    def __init__(self, parent, estudiante_id: int, usuario_id: int):
        super().__init__(parent)
        
        self.estudiante_id = estudiante_id
        self.usuario_id = usuario_id
        self.datos: Optional[Dict] = None
        self.modo_edicion = False
        
        # Configurar ventana
        self.title("CU-25: Visualizar/Editar Hoja de Vida del Estudiante")
        self.geometry("1000x750")
        self.transient(parent)
        self.grab_set()
        
        # Cargar datos (PASO 3)
        self._cargar_datos_iniciales()
        
        # Crear interfaz
        self._crear_interfaz()
        
        # Centrar ventana
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (self.winfo_width() // 2)
        y = (self.winfo_screenheight() // 2) - (self.winfo_height() // 2)
        self.geometry(f"+{x}+{y}")
    
    def _cargar_datos_iniciales(self):
        """PASO 3: Cargar hoja de vida del estudiante"""
        try:
            self.datos = ServicioHojaVida.cargar_hoja_vida_estudiante(
                self.estudiante_id
            )
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            self.destroy()
    
    def _crear_interfaz(self):
        """PASO 4: Desplegar hoja de vida del estudiante"""
        # Frame principal con scroll
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Canvas y scrollbar
        canvas = tk.Canvas(main_frame)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # --- SECCIÓN: Datos del estudiante (no editables) ---
        self._crear_seccion_estudiante(scrollable_frame)
        
        # --- SECCIÓN: Estado de salud (editable) ---
        self._crear_seccion_estado_salud(scrollable_frame)
        
        # --- SECCIÓN: Alergias (editable) ---
        self._crear_seccion_alergias(scrollable_frame)
        
        # --- SECCIÓN: Tratamientos (editable) ---
        self._crear_seccion_tratamientos(scrollable_frame)
        
        # --- SECCIÓN: Necesidades educativas (editable) ---
        self._crear_seccion_necesidades(scrollable_frame)
        
        # --- SECCIÓN: Metadatos (no editables) ---
        self._crear_seccion_metadatos(scrollable_frame)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # --- BOTONES DE ACCIÓN ---
        self._crear_botones_accion(main_frame)
    
    def _crear_seccion_estudiante(self, parent):
        """Datos del estudiante (no editables)"""
        frame = ttk.LabelFrame(parent, text="Datos del Estudiante (No Editables)", padding="10")
        frame.pack(fill=tk.X, padx=5, pady=5)
        
        estudiante = self.datos['estudiante']
        
        # Grid de 2 columnas
        info = [
            ("Código:", estudiante['codigo']),
            ("Identificación:", f"{estudiante['tipo_identificacion']} {estudiante['numero_identificacion']}"),
            ("Nombre:", f"{estudiante['primer_nombre']} {estudiante['segundo_nombre']}".strip()),
            ("Apellidos:", f"{estudiante['primer_apellido']} {estudiante['segundo_apellido']}".strip()),
            ("Fecha Nacimiento:", str(estudiante['fecha_nacimiento']) if estudiante['fecha_nacimiento'] else "N/A"),
            ("Género:", estudiante['genero']),
            ("Dirección:", estudiante['direccion']),
            ("Teléfono:", estudiante['telefono'])
        ]
        
        for i, (label, value) in enumerate(info):
            row = i // 2
            col = (i % 2) * 2
            
            ttk.Label(frame, text=label, font=("Arial", 9, "bold")).grid(
                row=row, column=col, sticky=tk.W, padx=5, pady=3
            )
            ttk.Label(frame, text=value).grid(
                row=row, column=col+1, sticky=tk.W, padx=5, pady=3
            )
    
    def _crear_seccion_estado_salud(self, parent):
        """PASO 7: Campo editable - Estado de salud"""
        frame = ttk.LabelFrame(
            parent,
            text="Estado de Salud (Editable)",
            padding="10"
        )
        frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(
            frame,
            text="Descripción general del estado de salud del estudiante",
            foreground="blue",
            font=("Arial", 9, "italic")
        ).pack(anchor=tk.W, pady=(0, 5))
        
        self.entry_estado_salud = ttk.Entry(
            frame,
            width=80,
            state=tk.DISABLED  # PASO 5: Inicialmente deshabilitado
        )
        self.entry_estado_salud.pack(fill=tk.X, pady=(0, 5))
        
        # Cargar valor actual
        estado_actual = self.datos['hoja_vida']['estado_salud']
        if estado_actual:
            self.entry_estado_salud.config(state=tk.NORMAL)
            self.entry_estado_salud.insert(0, estado_actual)
            self.entry_estado_salud.config(state=tk.DISABLED)
        
        self.label_caracteres_salud = ttk.Label(frame, text="0/100 caracteres")
        self.label_caracteres_salud.pack(anchor=tk.E)
    
    def _crear_seccion_alergias(self, parent):
        """PASO 7: Campo editable - Alergias (JSON)"""
        frame = ttk.LabelFrame(
            parent,
            text="Alergias (Editable - JSON)",
            padding="10"
        )
        frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(
            frame,
            text='Formato JSON. Ej: {"alimentarias": ["maní", "lactosa"], "medicamentos": []}',
            foreground="blue",
            font=("Arial", 9, "italic")
        ).pack(anchor=tk.W, pady=(0, 5))
        
        self.text_alergias = scrolledtext.ScrolledText(
            frame,
            height=4,
            width=80,
            wrap=tk.WORD,
            state=tk.DISABLED
        )
        self.text_alergias.pack(fill=tk.BOTH, expand=True)
        
        # Cargar valor actual
        alergias_actual = self.datos['hoja_vida']['alergias']
        if alergias_actual:
            self.text_alergias.config(state=tk.NORMAL)
            self.text_alergias.insert("1.0", json.dumps(alergias_actual, indent=2, ensure_ascii=False))
            self.text_alergias.config(state=tk.DISABLED)
    
    def _crear_seccion_tratamientos(self, parent):
        """PASO 7: Campo editable - Tratamientos (JSON)"""
        frame = ttk.LabelFrame(
            parent,
            text="Tratamientos Médicos (Editable - JSON)",
            padding="10"
        )
        frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(
            frame,
            text='Formato JSON. Ej: {"actual": "Terapia física", "frecuencia": "semanal"}',
            foreground="blue",
            font=("Arial", 9, "italic")
        ).pack(anchor=tk.W, pady=(0, 5))
        
        self.text_tratamientos = scrolledtext.ScrolledText(
            frame,
            height=4,
            width=80,
            wrap=tk.WORD,
            state=tk.DISABLED
        )
        self.text_tratamientos.pack(fill=tk.BOTH, expand=True)
        
        # Cargar valor actual
        tratamientos_actual = self.datos['hoja_vida']['tratamientos']
        if tratamientos_actual:
            self.text_tratamientos.config(state=tk.NORMAL)
            self.text_tratamientos.insert("1.0", json.dumps(tratamientos_actual, indent=2, ensure_ascii=False))
            self.text_tratamientos.config(state=tk.DISABLED)
    
    def _crear_seccion_necesidades(self, parent):
        """PASO 7: Campo editable - Necesidades educativas (JSON)"""
        frame = ttk.LabelFrame(
            parent,
            text="Necesidades Educativas Especiales (Editable - JSON)",
            padding="10"
        )
        frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(
            frame,
            text='Formato JSON. Ej: {"tipo": "Dislexia", "adaptaciones": ["tiempo extra"]}',
            foreground="blue",
            font=("Arial", 9, "italic")
        ).pack(anchor=tk.W, pady=(0, 5))
        
        self.text_necesidades = scrolledtext.ScrolledText(
            frame,
            height=4,
            width=80,
            wrap=tk.WORD,
            state=tk.DISABLED
        )
        self.text_necesidades.pack(fill=tk.BOTH, expand=True)
        
        # Cargar valor actual
        necesidades_actual = self.datos['hoja_vida']['necesidades_educativas']
        if necesidades_actual:
            self.text_necesidades.config(state=tk.NORMAL)
            self.text_necesidades.insert("1.0", json.dumps(necesidades_actual, indent=2, ensure_ascii=False))
            self.text_necesidades.config(state=tk.DISABLED)
    
    def _crear_seccion_metadatos(self, parent):
        """Metadatos de la hoja de vida (no editables)"""
        frame = ttk.LabelFrame(parent, text="Información de Registro", padding="10")
        frame.pack(fill=tk.X, padx=5, pady=5)
        
        hoja_vida = self.datos['hoja_vida']
        
        fecha_creacion = hoja_vida['fecha_creacion']
        fecha_str = fecha_creacion.strftime("%Y-%m-%d %H:%M:%S") if fecha_creacion else "N/A"
        
        ttk.Label(frame, text=f"Fecha de Creación: {fecha_str}").pack(anchor=tk.W, pady=2)
        ttk.Label(frame, text=f"Usuario Creador ID: {hoja_vida['usuario_creador'] or 'N/A'}").pack(anchor=tk.W, pady=2)
    
    def _crear_botones_accion(self, parent):
        """Botones de acción"""
        frame = ttk.Frame(parent, padding="10")
        frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        # Botón Editar (PASO 6)
        self.btn_editar = ttk.Button(
            frame,
            text="✏️ Editar Hoja de Vida",
            command=self._activar_modo_edicion
        )
        self.btn_editar.pack(side=tk.LEFT, padx=5)
        
        # Botón Guardar (inicialmente deshabilitado)
        self.btn_guardar = ttk.Button(
            frame,
            text="💾 Guardar Modificaciones",
            command=self._on_guardar,
            state=tk.DISABLED
        )
        self.btn_guardar.pack(side=tk.LEFT, padx=5)
        
        # Botón Cancelar edición
        self.btn_cancelar = ttk.Button(
            frame,
            text="❌ Cancelar Edición",
            command=self._cancelar_edicion,
            state=tk.DISABLED
        )
        self.btn_cancelar.pack(side=tk.LEFT, padx=5)
        
        # Botón Cerrar (PASO 5: puede cerrar en cualquier momento)
        ttk.Button(
            frame,
            text="Cerrar",
            command=self.destroy
        ).pack(side=tk.RIGHT, padx=5)
    
    def _activar_modo_edicion(self):
        """
        PASO 6: Activar modo de edición
        Sale del modo interrumpible
        """
        self.modo_edicion = True
        
        # Habilitar campos editables
        self.entry_estado_salud.config(state=tk.NORMAL)
        self.text_alergias.config(state=tk.NORMAL)
        self.text_tratamientos.config(state=tk.NORMAL)
        self.text_necesidades.config(state=tk.NORMAL)
        
        # Bind para actualizar contador
        self.entry_estado_salud.bind("<KeyRelease>", lambda e: self._actualizar_contador_salud())
        
        # Ajustar botones
        self.btn_editar.config(state=tk.DISABLED)
        self.btn_guardar.config(state=tk.NORMAL)
        self.btn_cancelar.config(state=tk.NORMAL)
        
        messagebox.showinfo(
            "Modo Edición",
            "Has activado el modo de edición.\n\n"
            "Campos editables:\n"
            "• Estado de salud\n"
            "• Alergias (JSON)\n"
            "• Tratamientos (JSON)\n"
            "• Necesidades educativas (JSON)\n\n"
            "Los demás campos permanecen bloqueados."
        )
    
    def _cancelar_edicion(self):
        """Cancelar modo de edición y restaurar valores originales"""
        respuesta = messagebox.askyesno(
            "Cancelar Edición",
            "¿Deseas cancelar los cambios y volver al modo visualización?"
        )
        
        if respuesta:
            # Recargar datos originales
            self._cargar_datos_iniciales()
            
            # Deshabilitar campos
            self.entry_estado_salud.config(state=tk.DISABLED)
            self.text_alergias.config(state=tk.DISABLED)
            self.text_tratamientos.config(state=tk.DISABLED)
            self.text_necesidades.config(state=tk.DISABLED)
            
            # Ajustar botones
            self.btn_editar.config(state=tk.NORMAL)
            self.btn_guardar.config(state=tk.DISABLED)
            self.btn_cancelar.config(state=tk.DISABLED)
            
            self.modo_edicion = False
    
    def _actualizar_contador_salud(self):
        """Actualizar contador de caracteres para estado de salud"""
        contenido = self.entry_estado_salud.get()
        self.label_caracteres_salud.config(text=f"{len(contenido)}/100 caracteres")
        
        if len(contenido) > 100:
            self.label_caracteres_salud.config(foreground="red")
        else:
            self.label_caracteres_salud.config(foreground="black")
    
    def _on_guardar(self):
        """
        PASO 9: Click en "Guardar modificaciones"
        PASO 10-11: Validar y registrar
        """
        # PASO 8: Recolectar modificaciones
        modificaciones = {}
        
        # Estado de salud
        estado_salud = self.entry_estado_salud.get().strip()
        if estado_salud != self.datos['hoja_vida']['estado_salud']:
            modificaciones['estado_salud'] = estado_salud
        
        # Alergias (JSON)
        try:
            texto_alergias = self.text_alergias.get("1.0", tk.END).strip()
            if texto_alergias:
                alergias = json.loads(texto_alergias)
                if alergias != self.datos['hoja_vida']['alergias']:
                    modificaciones['alergias'] = alergias
            else:
                if self.datos['hoja_vida']['alergias']:
                    modificaciones['alergias'] = {}
        except json.JSONDecodeError as e:
            messagebox.showerror(
                "Error de Formato",
                f"Alergias no tiene formato JSON válido:\n{str(e)}"
            )
            return
        
        # Tratamientos (JSON)
        try:
            texto_tratamientos = self.text_tratamientos.get("1.0", tk.END).strip()
            if texto_tratamientos:
                tratamientos = json.loads(texto_tratamientos)
                if tratamientos != self.datos['hoja_vida']['tratamientos']:
                    modificaciones['tratamientos'] = tratamientos
            else:
                if self.datos['hoja_vida']['tratamientos']:
                    modificaciones['tratamientos'] = {}
        except json.JSONDecodeError as e:
            messagebox.showerror(
                "Error de Formato",
                f"Tratamientos no tiene formato JSON válido:\n{str(e)}"
            )
            return
        
        # Necesidades educativas (JSON)
        try:
            texto_necesidades = self.text_necesidades.get("1.0", tk.END).strip()
            if texto_necesidades:
                necesidades = json.loads(texto_necesidades)
                if necesidades != self.datos['hoja_vida']['necesidades_educativas']:
                    modificaciones['necesidades_educativas'] = necesidades
            else:
                if self.datos['hoja_vida']['necesidades_educativas']:
                    modificaciones['necesidades_educativas'] = {}
        except json.JSONDecodeError as e:
            messagebox.showerror(
                "Error de Formato",
                f"Necesidades educativas no tiene formato JSON válido:\n{str(e)}"
            )
            return
        
        # Verificar si hay cambios
        if not modificaciones:
            messagebox.showinfo(
                "Sin Cambios",
                "No se detectaron modificaciones en los campos."
            )
            return
        
        # PASO 10: Validar modificaciones
        es_valido, errores = ServicioHojaVida.validar_modificaciones_hoja_vida(
            modificaciones
        )
        
        # PASO 11: ¿Modificaciones válidas?
        if not es_valido:
            # PASO 11.1-11.2: Mostrar mensaje de error
            mensaje_error = "Modificaciones no válidas:\n\n" + "\n".join(f"• {e}" for e in errores)
            messagebox.showerror("Error de Validación", mensaje_error)
            
            # PASO 11.4: Regresar al paso 8 (usuario puede corregir)
            return
        
        # PASO 12: Registrar modificaciones
        try:
            hoja_vida_id = self.datos['hoja_vida']['id']
            ServicioHojaVida.actualizar_hoja_vida(
                hoja_vida_id,
                modificaciones,
                self.usuario_id
            )
            
            # PASO 13: Mensaje de éxito
            messagebox.showinfo(
                "Éxito",
                "Modificaciones realizadas exitosamente."
            )
            
            # Recargar datos actualizados
            self._cargar_datos_iniciales()
            
            # Volver a modo visualización
            self.entry_estado_salud.config(state=tk.DISABLED)
            self.text_alergias.config(state=tk.DISABLED)
            self.text_tratamientos.config(state=tk.DISABLED)
            self.text_necesidades.config(state=tk.DISABLED)
            
            self.btn_editar.config(state=tk.NORMAL)
            self.btn_guardar.config(state=tk.DISABLED)
            self.btn_cancelar.config(state=tk.DISABLED)
            
            self.modo_edicion = False
            
        except ValueError as e:
            messagebox.showerror("Error", f"Error al guardar:\n{str(e)}")
