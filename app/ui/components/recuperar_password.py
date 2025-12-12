# -*- coding: utf-8 -*-
"""
Interfaz de Recuperación de Contraseña - CU-07
Implementa los 3 pasos del flujo de recuperación
"""

import tkinter as tk
from tkinter import messagebox
import re

from app.services.recuperacion_password_service import RecuperacionPasswordService
from app.services.email_service import EmailService


class RecuperarPasswordWindow:
    """
    Ventana para recuperación de contraseña con 3 pasos:
    1. Ingresar email/username
    2. Ingresar código de 6 caracteres
    3. Ingresar nueva contraseña
    """
    
    def __init__(self, parent):
        self.parent = parent
        self.email_usuario = None
        self.id_code_valido = None
        
        # Ventana principal
        self.window = tk.Toplevel(parent)
        self.window.title("Recuperar Contraseña")
        self.window.geometry("500x600")
        self.window.resizable(False, False)
        self.window.transient(parent)
        self.window.grab_set()
        
        # Centrar ventana
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (500 // 2)
        y = (self.window.winfo_screenheight() // 2) - (600 // 2)
        self.window.geometry(f"500x600+{x}+{y}")
        
        # Frame contenedor
        self.main_frame = tk.Frame(self.window, bg="#f8f9fa")
        self.main_frame.pack(fill="both", expand=True)
        
        # Paso 1: Solicitar email (paso 2 del diagrama)
        self._mostrar_paso_1()
    
    def _mostrar_paso_1(self):
        """
        Paso 2 del diagrama: Sistema despliega formulario "Recuperar contraseña"
        Campo: email o username
        Botón: "Enviar código"
        """
        # Limpiar frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        # Header
        header = tk.Frame(self.main_frame, bg="#2c3e50", height=80)
        header.pack(fill="x")
        tk.Label(
            header,
            text="🔐 Recuperar Contraseña",
            bg="#2c3e50",
            fg="white",
            font=("Segoe UI", 18, "bold")
        ).pack(pady=25)
        
        # Contenedor central
        content = tk.Frame(self.main_frame, bg="#f8f9fa", padx=50, pady=30)
        content.pack(fill="both", expand=True)
        
        # Instrucciones
        tk.Label(
            content,
            text="Paso 1 de 3: Verificar identidad",
            bg="#f8f9fa",
            fg="#2c3e50",
            font=("Segoe UI", 14, "bold")
        ).pack(pady=(0, 10))
        
        tk.Label(
            content,
            text="Ingresa tu correo electrónico y te enviaremos\nun código de recuperación",
            bg="#f8f9fa",
            fg="#6c757d",
            font=("Segoe UI", 10),
            justify="center"
        ).pack(pady=(0, 30))
        
        # Campo email
        tk.Label(
            content,
            text="Correo Electrónico:",
            bg="#f8f9fa",
            fg="#2c3e50",
            font=("Segoe UI", 11, "bold"),
            anchor="w"
        ).pack(fill="x", pady=(0, 5))
        
        self.entry_email = tk.Entry(
            content,
            font=("Segoe UI", 12),
            bg="white",
            relief="solid",
            bd=1
        )
        self.entry_email.pack(fill="x", ipady=8, pady=(0, 30))
        self.entry_email.focus()
        
        # Botón enviar código
        btn_enviar = tk.Button(
            content,
            text="Enviar Código de Recuperación",
            bg="#3498db",
            fg="white",
            font=("Segoe UI", 12, "bold"),
            bd=0,
            padx=20,
            pady=12,
            cursor="hand2",
            command=self._enviar_codigo
        )
        btn_enviar.pack(fill="x", pady=(0, 15))
        
        # Botón cancelar
        tk.Button(
            content,
            text="Cancelar",
            bg="#95a5a6",
            fg="white",
            font=("Segoe UI", 11),
            bd=0,
            padx=20,
            pady=10,
            cursor="hand2",
            command=self.window.destroy
        ).pack(fill="x")
        
        # Enter para enviar
        self.entry_email.bind("<Return>", lambda e: self._enviar_codigo())
    
    def _enviar_codigo(self):
        """
        Paso 3-8 del diagrama:
        3. Usuario digita su correo
        4. Usuario hace clic en "Enviar código"
        5. Sistema valida el dato ingresado
        6. DECISIÓN: ¿El usuario existe?
        7. Sistema genera código
        8. Sistema envía correo
        """
        email = self.entry_email.get().strip()
        
        # Paso 5.1: Verificar que no esté vacío
        if not email:
            messagebox.showerror("Error", "Por favor ingresa tu correo electrónico")
            return
        
        # Paso 5.2: Validar formato si es correo
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            messagebox.showerror("Error", "El formato del correo electrónico no es válido")
            return
        
        # Paso 5.3: Buscar usuario en BD
        usuario = RecuperacionPasswordService.buscar_usuario(email)
        
        # Paso 6: DECISIÓN - ¿El usuario existe?
        if not usuario:
            # Paso 6.1-6.3: NO - Mostrar mensaje y terminar
            messagebox.showerror(
                "Usuario No Encontrado",
                "No se encontró un usuario con estos datos.\n\n"
                "Verifica tu correo electrónico e intenta nuevamente."
            )
            return
        
        # Paso 5.4: Verificar que esté activo
        if not usuario['activo']:
            messagebox.showerror(
                "Usuario Inactivo",
                "Tu cuenta está inactiva.\n\n"
                "Contacta al administrador del sistema."
            )
            return
        
        # Paso 7: Generar código de recuperación
        exito, mensaje, codigo = RecuperacionPasswordService.crear_codigo_recuperacion(
            usuario['id_usuario']
        )
        
        if not exito:
            messagebox.showerror("Error", f"No se pudo generar el código:\n{mensaje}")
            return
        
        # Paso 8: Enviar correo con código
        exito_email, mensaje_email = EmailService.enviar_codigo_recuperacion(
            usuario['correo_electronico'],
            codigo
        )
        
        if not exito_email:
            messagebox.showerror("Error al Enviar Email", mensaje_email)
            return
        
        # Guardar email para siguientes pasos
        self.email_usuario = email
        
        # Mostrar mensaje de éxito
        messagebox.showinfo(
            "Código Enviado",
            f"Se ha enviado un código de recuperación a:\n{EmailService.EMAIL_DESTINO}\n\n"
            f"El código expira en {RecuperacionPasswordService.MINUTOS_EXPIRACION} minutos.\n\n"
            f"{mensaje_email}"
        )
        
        # Paso 9: Mostrar formulario para ingresar código
        self._mostrar_paso_2()
    
    def _mostrar_paso_2(self):
        """
        Paso 9 del diagrama: Sistema despliega formulario "Ingresar código de recuperación"
        Campo: código (6 caracteres)
        Botón: "Validar código"
        """
        # Limpiar frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        # Header
        header = tk.Frame(self.main_frame, bg="#2c3e50", height=80)
        header.pack(fill="x")
        tk.Label(
            header,
            text="🔐 Recuperar Contraseña",
            bg="#2c3e50",
            fg="white",
            font=("Segoe UI", 18, "bold")
        ).pack(pady=25)
        
        # Contenedor central
        content = tk.Frame(self.main_frame, bg="#f8f9fa", padx=50, pady=30)
        content.pack(fill="both", expand=True)
        
        # Instrucciones
        tk.Label(
            content,
            text="Paso 2 de 3: Verificar código",
            bg="#f8f9fa",
            fg="#2c3e50",
            font=("Segoe UI", 14, "bold")
        ).pack(pady=(0, 10))
        
        tk.Label(
            content,
            text=f"Revisa tu correo: {EmailService.EMAIL_DESTINO}\n"
                 f"e ingresa el código de 6 caracteres",
            bg="#f8f9fa",
            fg="#6c757d",
            font=("Segoe UI", 10),
            justify="center"
        ).pack(pady=(0, 30))
        
        # Campo código
        tk.Label(
            content,
            text="Código de Recuperación:",
            bg="#f8f9fa",
            fg="#2c3e50",
            font=("Segoe UI", 11, "bold"),
            anchor="w"
        ).pack(fill="x", pady=(0, 5))
        
        self.entry_codigo = tk.Entry(
            content,
            font=("Segoe UI", 16, "bold"),
            bg="white",
            relief="solid",
            bd=1,
            justify="center"
        )
        self.entry_codigo.pack(fill="x", ipady=10, pady=(0, 10))
        self.entry_codigo.focus()
        
        # Validación: solo 6 caracteres
        vcmd = (self.entry_codigo.register(lambda P: len(P) <= 6), '%P')
        self.entry_codigo.config(validate='key', validatecommand=vcmd)
        
        # Hint
        tk.Label(
            content,
            text="Ej: A3X9K2",
            bg="#f8f9fa",
            fg="#95a5a6",
            font=("Segoe UI", 9, "italic")
        ).pack(pady=(0, 30))
        
        # Botón validar
        btn_validar = tk.Button(
            content,
            text="Validar Código",
            bg="#27ae60",
            fg="white",
            font=("Segoe UI", 12, "bold"),
            bd=0,
            padx=20,
            pady=12,
            cursor="hand2",
            command=self._validar_codigo
        )
        btn_validar.pack(fill="x", pady=(0, 15))
        
        # Botón volver
        tk.Button(
            content,
            text="Volver",
            bg="#95a5a6",
            fg="white",
            font=("Segoe UI", 11),
            bd=0,
            padx=20,
            pady=10,
            cursor="hand2",
            command=self._mostrar_paso_1
        ).pack(fill="x")
        
        # Enter para validar
        self.entry_codigo.bind("<Return>", lambda e: self._validar_codigo())
    
    def _validar_codigo(self):
        """
        Paso 10-14 del diagrama:
        10. Usuario digita el código
        11. Usuario hace clic en "Validar código"
        12. Sistema verifica el código
        13. DECISIÓN: ¿El código es válido?
        14. Marcar código como usado
        """
        codigo = self.entry_codigo.get().strip().upper()
        
        # Validar que tenga 6 caracteres
        if len(codigo) != 6:
            messagebox.showerror("Error", "El código debe tener exactamente 6 caracteres")
            return
        
        # Paso 12: Verificar código en BD
        valido, mensaje, id_code = RecuperacionPasswordService.validar_codigo(
            self.email_usuario,
            codigo
        )
        
        # Paso 13: DECISIÓN - ¿El código es válido?
        if not valido:
            # Paso 13.1-13.3: NO - Mostrar error y no permitir avanzar
            messagebox.showerror("Código Inválido", mensaje)
            return
        
        # Paso 14: Marcar código como usado
        if not RecuperacionPasswordService.marcar_codigo_usado(id_code):
            messagebox.showerror("Error", "No se pudo marcar el código como usado")
            return
        
        self.id_code_valido = id_code
        
        # Paso 15: Mostrar formulario de nueva contraseña
        self._mostrar_paso_3()
    
    def _mostrar_paso_3(self):
        """
        Paso 15 del diagrama: Sistema despliega formulario "Nueva contraseña"
        Campos: nueva contraseña, confirmar contraseña
        Botón: "Actualizar contraseña"
        """
        # Limpiar frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        # Header
        header = tk.Frame(self.main_frame, bg="#2c3e50", height=80)
        header.pack(fill="x")
        tk.Label(
            header,
            text="🔐 Recuperar Contraseña",
            bg="#2c3e50",
            fg="white",
            font=("Segoe UI", 18, "bold")
        ).pack(pady=25)
        
        # Contenedor central
        content = tk.Frame(self.main_frame, bg="#f8f9fa", padx=50, pady=30)
        content.pack(fill="both", expand=True)
        
        # Instrucciones
        tk.Label(
            content,
            text="Paso 3 de 3: Nueva contraseña",
            bg="#f8f9fa",
            fg="#2c3e50",
            font=("Segoe UI", 14, "bold")
        ).pack(pady=(0, 10))
        
        tk.Label(
            content,
            text="Ingresa tu nueva contraseña",
            bg="#f8f9fa",
            fg="#6c757d",
            font=("Segoe UI", 10)
        ).pack(pady=(0, 30))
        
        # Campo nueva contraseña
        tk.Label(
            content,
            text="Nueva Contraseña:",
            bg="#f8f9fa",
            fg="#2c3e50",
            font=("Segoe UI", 11, "bold"),
            anchor="w"
        ).pack(fill="x", pady=(0, 5))
        
        self.entry_password = tk.Entry(
            content,
            font=("Segoe UI", 12),
            bg="white",
            relief="solid",
            bd=1,
            show="●"
        )
        self.entry_password.pack(fill="x", ipady=8, pady=(0, 20))
        self.entry_password.focus()
        
        # Campo confirmar contraseña
        tk.Label(
            content,
            text="Confirmar Contraseña:",
            bg="#f8f9fa",
            fg="#2c3e50",
            font=("Segoe UI", 11, "bold"),
            anchor="w"
        ).pack(fill="x", pady=(0, 5))
        
        self.entry_confirmar = tk.Entry(
            content,
            font=("Segoe UI", 12),
            bg="white",
            relief="solid",
            bd=1,
            show="●"
        )
        self.entry_confirmar.pack(fill="x", ipady=8, pady=(0, 10))
        
        # Requisitos
        requisitos_frame = tk.Frame(content, bg="#e8f4f8", relief="solid", bd=1)
        requisitos_frame.pack(fill="x", pady=(0, 20), padx=10)
        
        tk.Label(
            requisitos_frame,
            text="Requisitos de la contraseña:",
            bg="#e8f4f8",
            fg="#2c3e50",
            font=("Segoe UI", 9, "bold")
        ).pack(anchor="w", padx=10, pady=(10, 5))
        
        requisitos = [
            f"• Mínimo {RecuperacionPasswordService.MIN_LONGITUD_PASSWORD} caracteres",
            "• Al menos una mayúscula",
            "• Al menos una minúscula",
            "• Al menos un número"
        ]
        
        for req in requisitos:
            tk.Label(
                requisitos_frame,
                text=req,
                bg="#e8f4f8",
                fg="#6c757d",
                font=("Segoe UI", 9),
                anchor="w"
            ).pack(anchor="w", padx=20)
        
        tk.Label(requisitos_frame, text="", bg="#e8f4f8").pack(pady=5)
        
        # Botón actualizar
        btn_actualizar = tk.Button(
            content,
            text="Actualizar Contraseña",
            bg="#27ae60",
            fg="white",
            font=("Segoe UI", 12, "bold"),
            bd=0,
            padx=20,
            pady=12,
            cursor="hand2",
            command=self._actualizar_password
        )
        btn_actualizar.pack(fill="x", pady=(0, 15))
        
        # Botón cancelar
        tk.Button(
            content,
            text="Cancelar",
            bg="#95a5a6",
            fg="white",
            font=("Segoe UI", 11),
            bd=0,
            padx=20,
            pady=10,
            cursor="hand2",
            command=self.window.destroy
        ).pack(fill="x")
        
        # Enter para actualizar
        self.entry_confirmar.bind("<Return>", lambda e: self._actualizar_password())
    
    def _actualizar_password(self):
        """
        Paso 16-22 del diagrama:
        16. Usuario ingresa nueva contraseña
        17. Usuario hace clic en "Actualizar contraseña"
        18. Sistema valida
        19. DECISIÓN: ¿La contraseña es válida?
        20. Actualizar contraseña cifrada
        21. Mostrar mensaje de éxito
        22. Finalizar
        """
        password = self.entry_password.get()
        confirmar = self.entry_confirmar.get()
        
        # Paso 18: Validar contraseña
        valida, mensaje_error = RecuperacionPasswordService.validar_nueva_password(
            password,
            confirmar
        )
        
        # Paso 19: DECISIÓN - ¿La contraseña es válida?
        if not valida:
            # Paso 19.1-19.3: NO - Mostrar errores y volver al formulario
            messagebox.showerror("Contraseña Inválida", mensaje_error)
            return
        
        # Paso 20: Actualizar contraseña cifrada en BD
        exito, mensaje = RecuperacionPasswordService.actualizar_password(
            self.email_usuario,
            password
        )
        
        if not exito:
            messagebox.showerror("Error", f"No se pudo actualizar la contraseña:\n{mensaje}")
            return
        
        # Paso 21: Mostrar mensaje de éxito
        messagebox.showinfo(
            "✅ Contraseña Actualizada",
            "Su contraseña ha sido actualizada correctamente.\n\n"
            "Ahora puede iniciar sesión con su nueva contraseña."
        )
        
        # Paso 22: Finalizar proceso
        self.window.destroy()
