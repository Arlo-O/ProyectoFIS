# -*- coding: utf-8 -*-
"""
Formulario de Creación de Usuario - CU-03
Implementa el flujo EXACTO del diagrama de actividades
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import bcrypt
import os

from app.services.usuario_service import ServicioUsuario, GeneradorContraseña
from app.data.uow import uow
from sqlalchemy import text


class FormularioCrearUsuario:
    """
    Formulario para crear usuarios siguiendo el flujo CU-03:
    1. Admin hace clic en "Crear usuarios"
    2. Sistema despliega formulario
    3. Admin llena datos (username, rol, otros campos)
    4. Admin hace clic en "Crear usuario"
    5. Sistema valida unicidad y formato
    6. Si válido: autogenera contraseña, registra en BD, muestra éxito
    7. Si inválido: muestra mensaje de fallo, mantiene datos
    """
    
    def __init__(self, parent, callback_refresh=None):
        self.parent = parent
        self.callback_refresh = callback_refresh
        
        # Ventana modal
        self.window = tk.Toplevel(parent)
        self.window.title("Crear Nuevo Usuario")
        self.window.geometry("600x700")
        self.window.resizable(False, False)
        self.window.transient(parent)
        self.window.grab_set()
        
        # Variables del formulario
        self.var_username = tk.StringVar()  # Correo electrónico
        self.var_rol = tk.StringVar()
        self.var_tipo_id = tk.StringVar(value="CC")
        self.var_numero_id = tk.StringVar()
        self.var_primer_nombre = tk.StringVar()
        self.var_segundo_nombre = tk.StringVar()
        self.var_primer_apellido = tk.StringVar()
        self.var_segundo_apellido = tk.StringVar()
        self.var_telefono = tk.StringVar()
        self.var_especialidad = tk.StringVar()  # Solo para profesores
        self.var_cargo = tk.StringVar()  # Solo para directivos
        self.var_parentesco = tk.StringVar()  # Solo para acudientes
        
        self._crear_interfaz()
    
    def _crear_interfaz(self):
        """Paso 2: Sistema despliega el formulario de creación"""
        # Header
        header = tk.Frame(self.window, bg="#2c3e50", height=60)
        header.pack(fill="x")
        tk.Label(
            header,
            text="👤 Crear Nuevo Usuario",
            bg="#2c3e50",
            fg="white",
            font=("Segoe UI", 16, "bold")
        ).pack(pady=15)
        
        # Contenedor principal con scroll
        canvas = tk.Canvas(self.window, bg="white")
        scrollbar = ttk.Scrollbar(self.window, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="white")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True, padx=20, pady=20)
        scrollbar.pack(side="right", fill="y")
        
        # === SECCIÓN 1: CREDENCIALES ===
        self._crear_seccion(scrollable_frame, "CREDENCIALES DE ACCESO")
        
        # Username (correo electrónico)
        self._crear_campo(
            scrollable_frame,
            "Username (Correo Electrónico) *",
            self.var_username,
            placeholder="ejemplo@colegio.edu"
        )
        
        tk.Label(
            scrollable_frame,
            text="📝 La contraseña será generada automáticamente por el sistema",
            bg="white",
            fg="#7f8c8d",
            font=("Segoe UI", 9, "italic"),
            anchor="w"
        ).pack(fill="x", padx=30, pady=(0, 10))
        
        # === SECCIÓN 2: ROL ===
        self._crear_seccion(scrollable_frame, "ROL DEL USUARIO")
        
        # Rol
        frame_rol = tk.Frame(scrollable_frame, bg="white")
        frame_rol.pack(fill="x", padx=30, pady=5)
        
        tk.Label(
            frame_rol,
            text="Rol *",
            bg="white",
            fg="#2c3e50",
            font=("Segoe UI", 10, "bold"),
            anchor="w"
        ).pack(fill="x")
        
        roles = ["director", "profesor", "acudiente"]
        combo_rol = ttk.Combobox(
            frame_rol,
            textvariable=self.var_rol,
            values=roles,
            state="readonly",
            font=("Segoe UI", 10)
        )
        combo_rol.pack(fill="x", pady=(5, 0))
        combo_rol.bind("<<ComboboxSelected>>", self._on_rol_changed)
        
        # === SECCIÓN 3: DATOS PERSONALES ===
        self._crear_seccion(scrollable_frame, "DATOS PERSONALES")
        
        # Tipo y número de identificación
        frame_id = tk.Frame(scrollable_frame, bg="white")
        frame_id.pack(fill="x", padx=30, pady=5)
        frame_id.grid_columnconfigure(0, weight=1)
        frame_id.grid_columnconfigure(1, weight=2)
        
        frame_tipo = tk.Frame(frame_id, bg="white")
        frame_tipo.grid(row=0, column=0, sticky="ew", padx=(0, 5))
        tk.Label(
            frame_tipo,
            text="Tipo ID *",
            bg="white",
            fg="#2c3e50",
            font=("Segoe UI", 10, "bold")
        ).pack(fill="x")
        ttk.Combobox(
            frame_tipo,
            textvariable=self.var_tipo_id,
            values=["CC", "CE", "PA", "TI"],
            state="readonly",
            font=("Segoe UI", 10)
        ).pack(fill="x", pady=(5, 0))
        
        frame_numero = tk.Frame(frame_id, bg="white")
        frame_numero.grid(row=0, column=1, sticky="ew", padx=(5, 0))
        tk.Label(
            frame_numero,
            text="Número de Identificación *",
            bg="white",
            fg="#2c3e50",
            font=("Segoe UI", 10, "bold")
        ).pack(fill="x")
        tk.Entry(
            frame_numero,
            textvariable=self.var_numero_id,
            font=("Segoe UI", 10),
            bg="#ecf0f1"
        ).pack(fill="x", pady=(5, 0))
        
        # Nombres
        self._crear_campo(scrollable_frame, "Primer Nombre *", self.var_primer_nombre)
        self._crear_campo(scrollable_frame, "Segundo Nombre", self.var_segundo_nombre)
        self._crear_campo(scrollable_frame, "Primer Apellido *", self.var_primer_apellido)
        self._crear_campo(scrollable_frame, "Segundo Apellido", self.var_segundo_apellido)
        self._crear_campo(scrollable_frame, "Teléfono", self.var_telefono)
        
        # === SECCIÓN 4: CAMPOS ESPECÍFICOS DEL ROL ===
        self.frame_especificos = tk.Frame(scrollable_frame, bg="white")
        self.frame_especificos.pack(fill="x", padx=0, pady=10)
        
        # Botones de acción
        frame_buttons = tk.Frame(self.window, bg="white", height=70)
        frame_buttons.pack(fill="x", side="bottom")
        
        tk.Button(
            frame_buttons,
            text="Crear Usuario",
            bg="#27ae60",
            fg="white",
            font=("Segoe UI", 11, "bold"),
            bd=0,
            padx=30,
            pady=10,
            cursor="hand2",
            command=self._on_crear_usuario  # Paso 4: Admin hace clic
        ).pack(side="right", padx=20, pady=15)
        
        tk.Button(
            frame_buttons,
            text="Cancelar",
            bg="#95a5a6",
            fg="white",
            font=("Segoe UI", 11),
            bd=0,
            padx=30,
            pady=10,
            cursor="hand2",
            command=self.window.destroy
        ).pack(side="right", padx=5, pady=15)
    
    def _crear_seccion(self, parent, titulo):
        """Crea un separador de sección"""
        frame = tk.Frame(parent, bg="white")
        frame.pack(fill="x", padx=30, pady=(15, 10))
        tk.Label(
            frame,
            text=titulo,
            bg="white",
            fg="#34495e",
            font=("Segoe UI", 11, "bold")
        ).pack(anchor="w")
        tk.Frame(frame, height=2, bg="#3498db").pack(fill="x", pady=(5, 0))
    
    def _crear_campo(self, parent, label, variable, placeholder=""):
        """Crea un campo de entrada estándar"""
        frame = tk.Frame(parent, bg="white")
        frame.pack(fill="x", padx=30, pady=5)
        
        tk.Label(
            frame,
            text=label,
            bg="white",
            fg="#2c3e50",
            font=("Segoe UI", 10, "bold"),
            anchor="w"
        ).pack(fill="x")
        
        entry = tk.Entry(
            frame,
            textvariable=variable,
            font=("Segoe UI", 10),
            bg="#ecf0f1"
        )
        entry.pack(fill="x", pady=(5, 0))
        
        if placeholder:
            entry.insert(0, placeholder)
            entry.config(fg="gray")
            entry.bind("<FocusIn>", lambda e: self._on_entry_focus_in(e, placeholder))
            entry.bind("<FocusOut>", lambda e: self._on_entry_focus_out(e, placeholder))
    
    def _on_entry_focus_in(self, event, placeholder):
        if event.widget.get() == placeholder:
            event.widget.delete(0, tk.END)
            event.widget.config(fg="black")
    
    def _on_entry_focus_out(self, event, placeholder):
        if not event.widget.get():
            event.widget.insert(0, placeholder)
            event.widget.config(fg="gray")
    
    def _on_rol_changed(self, event=None):
        """Muestra campos específicos según el rol seleccionado"""
        # Limpiar frame
        for widget in self.frame_especificos.winfo_children():
            widget.destroy()
        
        rol = self.var_rol.get()
        
        if rol == "profesor":
            self._crear_seccion(self.frame_especificos, "DATOS DEL PROFESOR")
            self._crear_campo(self.frame_especificos, "Especialidad *", self.var_especialidad)
        
        elif rol == "director":
            self._crear_seccion(self.frame_especificos, "DATOS DEL DIRECTIVO")
            self._crear_campo(self.frame_especificos, "Cargo *", self.var_cargo)
        
        elif rol == "acudiente":
            self._crear_seccion(self.frame_especificos, "DATOS DEL ACUDIENTE")
            frame = tk.Frame(self.frame_especificos, bg="white")
            frame.pack(fill="x", padx=30, pady=5)
            tk.Label(
                frame,
                text="Parentesco *",
                bg="white",
                fg="#2c3e50",
                font=("Segoe UI", 10, "bold")
            ).pack(fill="x")
            ttk.Combobox(
                frame,
                textvariable=self.var_parentesco,
                values=["Padre", "Madre", "Abuelo/a", "Tío/a", "Tutor Legal", "Otro"],
                state="readonly",
                font=("Segoe UI", 10)
            ).pack(fill="x", pady=(5, 0))
    
    def _on_crear_usuario(self):
        """
        Paso 4: Admin hace clic en "Crear usuario"
        Paso 5: Sistema valida datos
        Paso 6: Decisión según validez
        Paso 7-9: Crear usuario o mostrar error
        """
        # Paso 3: Recopilar datos ingresados por el administrador
        datos = {
            "username": self.var_username.get().strip(),
            "rol": self.var_rol.get(),
            "tipo_identificacion": self.var_tipo_id.get(),
            "numero_identificacion": self.var_numero_id.get().strip(),
            "primer_nombre": self.var_primer_nombre.get().strip(),
            "segundo_nombre": self.var_segundo_nombre.get().strip(),
            "primer_apellido": self.var_primer_apellido.get().strip(),
            "segundo_apellido": self.var_segundo_apellido.get().strip(),
            "telefono": self.var_telefono.get().strip(),
            "especialidad": self.var_especialidad.get().strip(),
            "cargo": self.var_cargo.get().strip(),
            "parentesco": self.var_parentesco.get()
        }
        
        # Paso 5: VALIDACIÓN DE UNICIDAD Y FORMATO
        errores = self._validar_datos(datos)
        
        # Paso 6: DECISIÓN - ¿Los datos son válidos?
        if errores:
            # Paso 6.1-6.4: NO válidos - Mostrar mensaje de fallo
            mensaje_error = "No se pudo crear el usuario:\n\n" + "\n".join(f"• {error}" for error in errores)
            messagebox.showerror("Error de Validación", mensaje_error)
            # Los datos se mantienen en el formulario automáticamente
            return
        
        # Paso 7-9: SÍ válidos - Continuar con creación
        try:
            with uow() as unit:
                # Paso 7: Autogenerar contraseña temporal
                contraseña_temp = GeneradorContraseña.generar()
                contraseña_hash = bcrypt.hashpw(contraseña_temp.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                
                # Obtener ID del rol
                rol_id = self._obtener_rol_id(unit.session, datos["rol"])
                if not rol_id:
                    raise Exception(f"Rol '{datos['rol']}' no encontrado en la base de datos")
                
                # Paso 8: REGISTRAR USUARIO EN BD
                # 8.1: Crear objeto Usuario
                user_id = unit.session.execute(text("""
                    INSERT INTO usuario (correo_electronico, contrasena, id_rol, activo, fecha_creacion)
                    VALUES (:email, :password, :rol_id, true, :fecha)
                    RETURNING id_usuario
                """), {
                    "email": datos["username"],
                    "password": contraseña_hash,
                    "rol_id": rol_id,
                    "fecha": datetime.now()
                }).scalar()
                
                # Crear Persona
                persona_id = self._crear_persona(unit.session, datos)
                
                # Crear rol específico vinculado al usuario
                self._crear_rol_especifico(unit.session, datos["rol"], persona_id, user_id, datos)
                
                # 8.2: Guardar cambios
                unit.commit()
                
                # 8.3: Guardar credenciales en archivo TXT
                self._guardar_credenciales_en_archivo(
                    datos['username'],
                    contraseña_temp,
                    datos['rol'],
                    datos['primer_nombre'],
                    datos['primer_apellido']
                )
                
                # Paso 9: Mostrar mensaje de éxito
                mensaje_exito = (
                    f"✅ Usuario creado exitosamente\n\n"
                    f"Username: {datos['username']}\n"
                    f"Contraseña: {contraseña_temp}\n\n"
                    f"IMPORTANTE:\n"
                    f"• Las credenciales se han guardado en el archivo 'credenciales_usuarios.txt'\n"
                    f"• Proporcione estos datos al nuevo usuario de forma segura\n"
                    f"• La contraseña está encriptada en la base de datos"
                )
                
                messagebox.showinfo("Usuario Creado", mensaje_exito)
                
                # Paso 10-11: Cerrar formulario y actualizar lista
                if self.callback_refresh:
                    self.callback_refresh()
                
                self.window.destroy()
        
        except Exception as e:
            messagebox.showerror("Error", f"Error al crear usuario:\n{str(e)}")
    
    def _validar_datos(self, datos) -> list:
        """Paso 5: Validación completa de datos"""
        errores = []
        
        # 5.1: Username no vacío
        if not datos["username"]:
            errores.append("El username (correo electrónico) es obligatorio")
        else:
            # 5.2: Formato de email válido
            import re
            if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', datos["username"]):
                errores.append("El formato del correo electrónico es inválido")
            else:
                # 5.3: Verificar unicidad del username
                try:
                    with uow() as unit:
                        existe = unit.session.execute(text("""
                            SELECT COUNT(*) FROM usuario WHERE correo_electronico = :email
                        """), {"email": datos["username"]}).scalar()
                        if existe:
                            errores.append(f"Ya existe un usuario con el correo: {datos['username']}")
                except:
                    pass
        
        # 5.5: Rol válido
        if not datos["rol"]:
            errores.append("Debe seleccionar un rol")
        elif datos["rol"] not in ["director", "profesor", "acudiente"]:
            errores.append("El rol seleccionado no es válido")
        
        # Validar identificación
        if not datos["numero_identificacion"]:
            errores.append("El número de identificación es obligatorio")
        else:
            # Verificar unicidad
            try:
                with uow() as unit:
                    existe = unit.session.execute(text("""
                        SELECT COUNT(*) FROM persona WHERE numero_identificacion = :num_id
                    """), {"num_id": datos["numero_identificacion"]}).scalar()
                    if existe:
                        errores.append(f"Ya existe una persona con la identificación: {datos['numero_identificacion']}")
            except:
                pass
        
        # Validar nombres obligatorios
        if not datos["primer_nombre"]:
            errores.append("El primer nombre es obligatorio")
        if not datos["primer_apellido"]:
            errores.append("El primer apellido es obligatorio")
        
        # Validar campos específicos según rol
        if datos["rol"] == "profesor" and not datos["especialidad"]:
            errores.append("La especialidad es obligatoria para profesores")
        elif datos["rol"] == "director" and not datos["cargo"]:
            errores.append("El cargo es obligatorio para directivos")
        elif datos["rol"] == "acudiente" and not datos["parentesco"]:
            errores.append("El parentesco es obligatorio para acudientes")
        
        return errores
    
    def _obtener_rol_id(self, session, nombre_rol: str) -> int:
        """Obtiene el ID del rol por nombre"""
        result = session.execute(text("""
            SELECT id_rol FROM rol WHERE nombre_rol = :nombre
        """), {"nombre": nombre_rol}).scalar()
        return result
    
    def _crear_persona(self, session, datos) -> int:
        """Crea el registro de persona"""
        tipo_persona = datos["rol"]  # director, profesor, acudiente
        
        persona_id = session.execute(text("""
            INSERT INTO persona (tipo_identificacion, numero_identificacion, primer_nombre, segundo_nombre,
                               primer_apellido, segundo_apellido, telefono, type)
            VALUES (:tipo_id, :num_id, :primer_nombre, :segundo_nombre,
                    :primer_apellido, :segundo_apellido, :telefono, :tipo)
            RETURNING id_persona
        """), {
            "tipo_id": datos["tipo_identificacion"],
            "num_id": datos["numero_identificacion"],
            "primer_nombre": datos["primer_nombre"],
            "segundo_nombre": datos["segundo_nombre"],
            "primer_apellido": datos["primer_apellido"],
            "segundo_apellido": datos["segundo_apellido"],
            "telefono": datos["telefono"] or None,
            "tipo": tipo_persona
        }).scalar()
        
        return persona_id
    
    def _crear_rol_especifico(self, session, rol, persona_id, user_id, datos):
        """Crea el registro específico del rol"""
        if rol == "profesor":
            session.execute(text("""
                INSERT INTO profesor (id_profesor, id_usuario, especialidad, experiencia_anios)
                VALUES (:persona_id, :user_id, :especialidad, 0)
            """), {
                "persona_id": persona_id,
                "user_id": user_id,
                "especialidad": datos["especialidad"]
            })
        
        elif rol == "director":
            session.execute(text("""
                INSERT INTO directivo (id_directivo, id_usuario, cargo, area_responsable)
                VALUES (:persona_id, :user_id, :cargo, 'Dirección')
            """), {
                "persona_id": persona_id,
                "user_id": user_id,
                "cargo": datos["cargo"]
            })
        
        elif rol == "acudiente":
            session.execute(text("""
                INSERT INTO acudiente (id_acudiente, id_usuario, parentesco)
                VALUES (:persona_id, :user_id, :parentesco)
            """), {
                "persona_id": persona_id,
                "user_id": user_id,
                "parentesco": datos["parentesco"]
            })
    
    def _guardar_credenciales_en_archivo(self, username, password, rol, nombre, apellido):
        """
        Guarda las credenciales del usuario en un archivo de texto.
        Como las contraseñas se guardan encriptadas en BD, este archivo
        permite al administrador recuperar la contraseña temporal generada.
        """
        try:
            # Crear directorio de logs si no existe
            logs_dir = os.path.join(os.getcwd(), "logs")
            if not os.path.exists(logs_dir):
                os.makedirs(logs_dir)
            
            # Archivo de credenciales
            archivo_credenciales = os.path.join(logs_dir, "credenciales_usuarios.txt")
            
            # Guardar credenciales
            with open(archivo_credenciales, "a", encoding="utf-8") as f:
                f.write(f"\n{'='*80}\n")
                f.write(f"USUARIO CREADO: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"{'='*80}\n")
                f.write(f"Nombre: {nombre} {apellido}\n")
                f.write(f"Rol: {rol}\n")
                f.write(f"Username (Email): {username}\n")
                f.write(f"Contraseña: {password}\n")
                f.write(f"{'='*80}\n\n")
            
            print(f"[INFO] Credenciales guardadas en: {archivo_credenciales}")
        
        except Exception as e:
            print(f"[ERROR] No se pudo guardar credenciales en archivo: {e}")
            # No lanzar excepción para no interrumpir el flujo de creación
