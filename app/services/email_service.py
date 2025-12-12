# -*- coding: utf-8 -*-
"""
Servicio de Envío de Emails
Paso 8: Envía correos con código de recuperación
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Tuple


class EmailService:
    """
    Servicio para envío de correos electrónicos
    
    Configuración:
    - Todos los correos se envían a: arlonog.11@gmail.com
    - Usa Gmail SMTP
    """
    
    # Correo único de destino (según requerimiento)
    EMAIL_DESTINO = "arlonog.11@gmail.com"
    
    # Configuración SMTP (Gmail)
    SMTP_SERVER = "smtp.gmail.com"
    SMTP_PORT = 587
    
    # Credenciales (deberían estar en .env pero para desarrollo las dejamos aquí)
    # NOTA: Para producción, usar variables de entorno
    SMTP_USER = "sistema.fis.colegio@gmail.com"  # Crear cuenta temporal
    SMTP_PASSWORD = ""  # Configurar con contraseña de aplicación de Gmail
    
    @staticmethod
    def enviar_codigo_recuperacion(usuario_email: str, codigo: str) -> Tuple[bool, str]:
        """
        Paso 8: Envía email con código de recuperación
        
        Args:
            usuario_email: Email del usuario (para referencia en el mensaje)
            codigo: Código de 6 caracteres
        
        Returns:
            Tuple[bool, str]: (exito, mensaje)
        """
        try:
            # Crear mensaje
            mensaje = MIMEMultipart("alternative")
            mensaje["Subject"] = "Código de Recuperación de Contraseña - Sistema FIS"
            mensaje["From"] = EmailService.SMTP_USER
            mensaje["To"] = EmailService.EMAIL_DESTINO
            
            # Cuerpo del email en HTML
            html = f"""
            <html>
                <body style="font-family: Arial, sans-serif; padding: 20px;">
                    <div style="max-width: 600px; margin: 0 auto; border: 1px solid #ddd; border-radius: 5px; padding: 20px;">
                        <h2 style="color: #2c3e50;">🔐 Recuperación de Contraseña</h2>
                        
                        <p>Hola,</p>
                        
                        <p>Recibimos una solicitud para recuperar la contraseña de la cuenta: <strong>{usuario_email}</strong></p>
                        
                        <div style="background-color: #f8f9fa; padding: 20px; border-radius: 5px; margin: 20px 0; text-align: center;">
                            <p style="margin: 0; font-size: 14px; color: #6c757d;">Tu código de recuperación es:</p>
                            <p style="font-size: 32px; font-weight: bold; color: #2c3e50; margin: 10px 0; letter-spacing: 5px;">
                                {codigo}
                            </p>
                            <p style="margin: 0; font-size: 12px; color: #6c757d;">Este código expira en 10 minutos</p>
                        </div>
                        
                        <p>Si no solicitaste este código, ignora este mensaje.</p>
                        
                        <hr style="border: none; border-top: 1px solid #ddd; margin: 20px 0;">
                        
                        <p style="font-size: 12px; color: #6c757d;">
                            <strong>Sistema de Gestión Académica FIS</strong><br>
                            Este es un mensaje automático, por favor no responder.
                        </p>
                    </div>
                </body>
            </html>
            """
            
            # Adjuntar HTML
            parte_html = MIMEText(html, "html")
            mensaje.attach(parte_html)
            
            # Enviar email
            # NOTA: Si no hay credenciales SMTP configuradas, simular envío
            if not EmailService.SMTP_PASSWORD:
                # Modo simulación para desarrollo
                print(f"\n{'='*60}")
                print("📧 SIMULACIÓN DE ENVÍO DE EMAIL")
                print(f"{'='*60}")
                print(f"De: {EmailService.SMTP_USER}")
                print(f"Para: {EmailService.EMAIL_DESTINO}")
                print(f"Asunto: Código de Recuperación de Contraseña")
                print(f"\nContenido:")
                print(f"Usuario: {usuario_email}")
                print(f"Código: {codigo}")
                print(f"Expiración: 10 minutos")
                print(f"{'='*60}\n")
                
                # Guardar en archivo de log
                import os
                from datetime import datetime
                
                logs_dir = os.path.join(os.getcwd(), "logs")
                if not os.path.exists(logs_dir):
                    os.makedirs(logs_dir)
                
                log_file = os.path.join(logs_dir, "codigos_recuperacion.txt")
                with open(log_file, "a", encoding="utf-8") as f:
                    f.write(f"\n{'='*80}\n")
                    f.write(f"CÓDIGO DE RECUPERACIÓN GENERADO: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write(f"{'='*80}\n")
                    f.write(f"Usuario: {usuario_email}\n")
                    f.write(f"Código: {codigo}\n")
                    f.write(f"Enviado a: {EmailService.EMAIL_DESTINO}\n")
                    f.write(f"{'='*80}\n\n")
                
                return True, f"Email simulado. Código guardado en logs/codigos_recuperacion.txt"
            
            # Envío real con SMTP
            with smtplib.SMTP(EmailService.SMTP_SERVER, EmailService.SMTP_PORT) as server:
                server.starttls()
                server.login(EmailService.SMTP_USER, EmailService.SMTP_PASSWORD)
                server.send_message(mensaje)
            
            return True, f"Código enviado a {EmailService.EMAIL_DESTINO}"
        
        except Exception as e:
            print(f"[ERROR] enviar_codigo_recuperacion: {e}")
            import traceback
            traceback.print_exc()
            return False, f"Error al enviar email: {str(e)}"
    
    @staticmethod
    def configurar_smtp(user: str, password: str):
        """
        Configura las credenciales SMTP para envío real
        
        Para Gmail, usar contraseña de aplicación:
        1. Ir a cuenta de Google
        2. Seguridad > Verificación en 2 pasos
        3. Contraseñas de aplicaciones
        4. Generar nueva contraseña
        """
        EmailService.SMTP_USER = user
        EmailService.SMTP_PASSWORD = password
