"""
CU-24: Gestionar observador del estudiante

Diálogo que implementa la interfaz de usuario para gestión del observador.

Flujo:
1. Visualización interrumpible (PASO 4-5)
2. Modo modificación con campos bloqueados (PASO 6-8)
3. Validación y manejo de errores (PASO 11-12)
4. Confirmación de guardado (PASO 14-15)
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from typing import Optional, Dict
from datetime import datetime

from app.services.servicio_observador import ServicioObservador


class DialogoObservador(tk.Toplevel):
    """
    Diálogo para gestionar el observador del estudiante.
    
    Implementa:
    - Sección interrumpible de visualización (PASO 5)
    - Restricción de campos editables (PASO 7)
    - Validación de modificaciones (PASO 11-12)
    """
    
    def __init__(self, parent, estudiante_id: int, usuario_id: int):
        super().__init__(parent)
        
        self.estudiante_id = estudiante_id
        self.usuario_id = usuario_id
        self.datos_observador: Optional[Dict] = None
        self.modo_modificacion = False
        
        # Configurar ventana
        self.title("CU-24: Gestionar Observador del Estudiante")
        self.geometry("900x700")
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
        """PASO 3: Cargar observador estudiante"""
        try:
            self.datos_observador = ServicioObservador.cargar_observador_estudiante(
                self.estudiante_id
            )
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            self.destroy()
    
    def _crear_interfaz(self):
        """PASO 4: Desplegar información del observador"""
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
        
        # --- SECCIÓN: Datos del estudiante ---
        self._crear_seccion_estudiante(scrollable_frame)
        
        # --- SECCIÓN: Comportamiento general (editable) ---
        self._crear_seccion_comportamiento(scrollable_frame)
        
        # --- SECCIÓN: Anotaciones (solo visualización) ---
        self._crear_seccion_anotaciones(scrollable_frame)
        
        # --- SECCIÓN: Nueva anotación ---
        self._crear_seccion_nueva_anotacion(scrollable_frame)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # --- BOTONES DE ACCIÓN ---
        self._crear_botones_accion(main_frame)
    
    def _crear_seccion_estudiante(self, parent):
        """Mostrar datos del estudiante (no editables)"""
        frame = ttk.LabelFrame(parent, text="Datos del Estudiante", padding="10")
        frame.pack(fill=tk.X, padx=5, pady=5)
        
        estudiante = self.datos_observador['estudiante']
        
        ttk.Label(
            frame,
            text=f"Código: {estudiante['codigo']}",
            font=("Arial", 10, "bold")
        ).pack(anchor=tk.W)
        
        ttk.Label(
            frame,
            text=f"Nombre: {estudiante['nombres']} {estudiante['apellidos']}"
        ).pack(anchor=tk.W)
    
    def _crear_seccion_comportamiento(self, parent):
        """
        PASO 7-8: Desplegar formato con campos editables/bloqueados
        Campo editable: comportamiento_general
        """
        frame = ttk.LabelFrame(
            parent,
            text="Comportamiento General (Modificable)",
            padding="10"
        )
        frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(
            frame,
            text="Solo se pueden modificar datos de comportamiento",
            foreground="blue",
            font=("Arial", 9, "italic")
        ).pack(anchor=tk.W, pady=(0, 5))
        
        # Campo de texto para comportamiento
        self.text_comportamiento = scrolledtext.ScrolledText(
            frame,
            height=5,
            width=80,
            wrap=tk.WORD,
            state=tk.DISABLED  # PASO 5: Inicialmente deshabilitado (modo visualización)
        )
        self.text_comportamiento.pack(fill=tk.BOTH, expand=True)
        
        # Cargar valor actual
        comportamiento_actual = self.datos_observador['observador']['comportamiento_general']
        self.text_comportamiento.config(state=tk.NORMAL)
        self.text_comportamiento.insert("1.0", comportamiento_actual)
        self.text_comportamiento.config(state=tk.DISABLED)
        
        # Indicador de caracteres
        self.label_caracteres_comp = ttk.Label(frame, text="0/255 caracteres")
        self.label_caracteres_comp.pack(anchor=tk.E, pady=(5, 0))
        
        # Botón para activar modo modificación (PASO 6)
        self.btn_modificar_comportamiento = ttk.Button(
            frame,
            text="Modificar Comportamiento",
            command=self._activar_modo_modificacion_comportamiento
        )
        self.btn_modificar_comportamiento.pack(pady=(5, 0))
        
        self._actualizar_contador_caracteres_comp()
    
    def _crear_seccion_anotaciones(self, parent):
        """Mostrar anotaciones existentes (solo lectura)"""
        frame = ttk.LabelFrame(
            parent,
            text="Anotaciones Registradas",
            padding="10"
        )
        frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Treeview para mostrar anotaciones
        columns = ("fecha", "categoria", "detalle", "autor")
        tree = ttk.Treeview(frame, columns=columns, show="headings", height=6)
        
        tree.heading("fecha", text="Fecha")
        tree.heading("categoria", text="Categoría")
        tree.heading("detalle", text="Detalle")
        tree.heading("autor", text="Autor")
        
        tree.column("fecha", width=150)
        tree.column("categoria", width=120)
        tree.column("detalle", width=300)
        tree.column("autor", width=150)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        # Cargar anotaciones
        for anotacion in self.datos_observador['anotaciones']:
            fecha_str = anotacion['fecha'].strftime("%Y-%m-%d %H:%M")
            tree.insert("", tk.END, values=(
                fecha_str,
                anotacion['categoria'],
                anotacion['detalle'],
                anotacion['autor']
            ))
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def _crear_seccion_nueva_anotacion(self, parent):
        """
        PASO 8: Sección para agregar nueva anotación (observación)
        """
        frame = ttk.LabelFrame(
            parent,
            text="Agregar Nueva Anotación",
            padding="10"
        )
        frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(
            frame,
            text="Solo se pueden generar observaciones",
            foreground="blue",
            font=("Arial", 9, "italic")
        ).pack(anchor=tk.W, pady=(0, 5))
        
        # Campo: Categoría
        ttk.Label(frame, text="Categoría (máx. 50 caracteres):").pack(anchor=tk.W)
        self.entry_categoria = ttk.Entry(frame, width=50, state=tk.DISABLED)
        self.entry_categoria.pack(fill=tk.X, pady=(0, 5))
        
        self.label_caracteres_cat = ttk.Label(frame, text="0/50 caracteres")
        self.label_caracteres_cat.pack(anchor=tk.E)
        
        # Campo: Detalle
        ttk.Label(frame, text="Detalle (máx. 200 caracteres):").pack(anchor=tk.W, pady=(5, 0))
        self.text_detalle = scrolledtext.ScrolledText(
            frame,
            height=4,
            width=80,
            wrap=tk.WORD,
            state=tk.DISABLED
        )
        self.text_detalle.pack(fill=tk.X, pady=(0, 5))
        
        self.label_caracteres_det = ttk.Label(frame, text="0/200 caracteres")
        self.label_caracteres_det.pack(anchor=tk.E)
        
        # Botón para activar modo de anotación
        self.btn_activar_anotacion = ttk.Button(
            frame,
            text="Agregar Anotación",
            command=self._activar_modo_anotacion
        )
        self.btn_activar_anotacion.pack(pady=(5, 0))
        
        # Bind para actualizar contadores
        self.entry_categoria.bind("<KeyRelease>", lambda e: self._actualizar_contador_caracteres_cat())
        self.text_detalle.bind("<KeyRelease>", lambda e: self._actualizar_contador_caracteres_det())
    
    def _crear_botones_accion(self, parent):
        """Botones de acción principal"""
        frame = ttk.Frame(parent, padding="10")
        frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        # Botón Guardar (inicialmente deshabilitado)
        self.btn_guardar = ttk.Button(
            frame,
            text="Guardar Cambios",
            command=self._on_guardar,
            state=tk.DISABLED
        )
        self.btn_guardar.pack(side=tk.LEFT, padx=5)
        
        # Botón Cerrar (PASO 5: puede cerrar en cualquier momento del modo visualización)
        ttk.Button(
            frame,
            text="Cerrar",
            command=self.destroy
        ).pack(side=tk.RIGHT, padx=5)
    
    def _activar_modo_modificacion_comportamiento(self):
        """
        PASO 6: Activar modo de modificación para comportamiento
        Sale del modo interrumpible
        """
        self.text_comportamiento.config(state=tk.NORMAL)
        self.text_comportamiento.bind("<KeyRelease>", lambda e: self._actualizar_contador_caracteres_comp())
        self.btn_modificar_comportamiento.config(state=tk.DISABLED)
        self.btn_guardar.config(state=tk.NORMAL)
        self.modo_modificacion = True
    
    def _activar_modo_anotacion(self):
        """
        PASO 6: Activar modo para agregar anotación
        """
        self.entry_categoria.config(state=tk.NORMAL)
        self.text_detalle.config(state=tk.NORMAL)
        self.btn_activar_anotacion.config(state=tk.DISABLED)
        self.btn_guardar.config(state=tk.NORMAL)
        self.modo_modificacion = True
    
    def _actualizar_contador_caracteres_comp(self):
        """Actualizar contador de caracteres para comportamiento"""
        contenido = self.text_comportamiento.get("1.0", tk.END).strip()
        self.label_caracteres_comp.config(text=f"{len(contenido)}/255 caracteres")
        
        if len(contenido) > 255:
            self.label_caracteres_comp.config(foreground="red")
        else:
            self.label_caracteres_comp.config(foreground="black")
    
    def _actualizar_contador_caracteres_cat(self):
        """Actualizar contador de caracteres para categoría"""
        contenido = self.entry_categoria.get()
        self.label_caracteres_cat.config(text=f"{len(contenido)}/50 caracteres")
        
        if len(contenido) > 50:
            self.label_caracteres_cat.config(foreground="red")
        else:
            self.label_caracteres_cat.config(foreground="black")
    
    def _actualizar_contador_caracteres_det(self):
        """Actualizar contador de caracteres para detalle"""
        contenido = self.text_detalle.get("1.0", tk.END).strip()
        self.label_caracteres_det.config(text=f"{len(contenido)}/200 caracteres")
        
        if len(contenido) > 200:
            self.label_caracteres_det.config(foreground="red")
        else:
            self.label_caracteres_det.config(foreground="black")
    
    def _on_guardar(self):
        """
        PASO 10: Hacer clic en "Modificar" (aquí "Guardar")
        Validar y registrar cambios
        """
        # Determinar qué tipo de modificación se está haciendo
        comportamiento_modificado = self.text_comportamiento.cget("state") == tk.NORMAL
        anotacion_nueva = self.entry_categoria.cget("state") == tk.NORMAL
        
        if comportamiento_modificado:
            self._guardar_comportamiento()
        
        if anotacion_nueva:
            self._guardar_anotacion()
    
    def _guardar_comportamiento(self):
        """
        PASO 11-13: Validar y guardar modificación de comportamiento
        """
        comportamiento = self.text_comportamiento.get("1.0", tk.END).strip()
        
        modificaciones = {
            "comportamiento_general": comportamiento
        }
        
        # PASO 11: Validar modificaciones
        es_valido, errores = ServicioObservador.validar_modificaciones(
            modificaciones,
            "comportamiento"
        )
        
        # PASO 12: ¿Modificaciones válidas?
        if not es_valido:
            # PASO 12.1: Mostrar mensaje de error
            mensaje_error = "Modificaciones inválidas:\n\n" + "\n".join(f"• {e}" for e in errores)
            messagebox.showerror("Error de Validación", mensaje_error)
            
            # PASO 12.3: Regresar al paso 9 (usuario puede corregir)
            return
        
        # PASO 13: Registrar modificaciones
        try:
            observador_id = self.datos_observador['observador']['id']
            ServicioObservador.registrar_modificacion(
                observador_id,
                "comportamiento",
                modificaciones,
                self.usuario_id
            )
            
            # PASO 14: Mensaje de éxito
            messagebox.showinfo(
                "Éxito",
                "Modificaciones guardadas correctamente"
            )
            
            # Deshabilitar campo nuevamente
            self.text_comportamiento.config(state=tk.DISABLED)
            self.btn_modificar_comportamiento.config(state=tk.NORMAL)
            
            # Verificar si hay más cambios pendientes
            if self.entry_categoria.cget("state") == tk.DISABLED:
                self.btn_guardar.config(state=tk.DISABLED)
                self.modo_modificacion = False
            
        except ValueError as e:
            messagebox.showerror("Error", f"Error al guardar: {str(e)}")
    
    def _guardar_anotacion(self):
        """
        PASO 11-13: Validar y guardar nueva anotación
        """
        categoria = self.entry_categoria.get().strip()
        detalle = self.text_detalle.get("1.0", tk.END).strip()
        
        modificaciones = {
            "categoria": categoria,
            "detalle": detalle
        }
        
        # PASO 11: Validar modificaciones
        es_valido, errores = ServicioObservador.validar_modificaciones(
            modificaciones,
            "anotacion"
        )
        
        # PASO 12: ¿Modificaciones válidas?
        if not es_valido:
            # PASO 12.1: Mostrar mensaje de error
            mensaje_error = "Anotación inválida:\n\n" + "\n".join(f"• {e}" for e in errores)
            messagebox.showerror("Error de Validación", mensaje_error)
            
            # PASO 12.3: Regresar al paso 9 (usuario puede corregir)
            return
        
        # PASO 13: Registrar anotación
        try:
            observador_id = self.datos_observador['observador']['id']
            ServicioObservador.registrar_modificacion(
                observador_id,
                "anotacion",
                modificaciones,
                self.usuario_id
            )
            
            # PASO 14: Mensaje de éxito
            messagebox.showinfo(
                "Éxito",
                "Anotación guardada correctamente"
            )
            
            # Limpiar campos
            self.entry_categoria.delete(0, tk.END)
            self.text_detalle.delete("1.0", tk.END)
            
            # Deshabilitar campos
            self.entry_categoria.config(state=tk.DISABLED)
            self.text_detalle.config(state=tk.DISABLED)
            self.btn_activar_anotacion.config(state=tk.NORMAL)
            
            # Recargar datos para mostrar nueva anotación
            self._cargar_datos_iniciales()
            
            # Verificar si hay más cambios pendientes
            if self.text_comportamiento.cget("state") == tk.DISABLED:
                self.btn_guardar.config(state=tk.DISABLED)
                self.modo_modificacion = False
            
        except ValueError as e:
            messagebox.showerror("Error", f"Error al guardar: {str(e)}")
