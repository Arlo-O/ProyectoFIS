# -*- coding: utf-8 -*-
"""
Servicio de Recuperación de Contraseña - CU-07
Implementa el flujo completo de recuperación con código de 6 caracteres
"""

import random
import string
from datetime import datetime, timedelta
from typing import Tuple, Optional
import bcrypt
from sqlalchemy import text

from app.core.usuarios.password_reset_code import PasswordResetCode
from app.data.uow import uow


class RecuperacionPasswordService:
    """
    Servicio para gestionar la recuperación de contraseñas
    
    Funcionalidades:
    - Generar códigos de 6 caracteres
    - Validar códigos
    - Actualizar contraseñas
    """
    
    LONGITUD_CODIGO = 6
    MINUTOS_EXPIRACION = 10
    MIN_LONGITUD_PASSWORD = 8
    
    @staticmethod
    def generar_codigo() -> str:
        """
        Paso 7: Genera un código aleatorio de 6 caracteres alfanuméricos
        Ejemplo: A3X9K2, B7M4N1, etc.
        """
        caracteres = string.ascii_uppercase + string.digits
        codigo = ''.join(random.choices(caracteres, k=RecuperacionPasswordService.LONGITUD_CODIGO))
        return codigo
    
    @staticmethod
    def buscar_usuario(email_o_username: str) -> Optional[dict]:
        """
        Paso 5.3: Buscar usuario en BD por email o username
        Paso 5.4: Verificar que esté activo
        
        Returns:
            dict con id_usuario, correo_electronico, activo o None si no existe
        """
        try:
            with uow() as unit:
                # Intentar buscar por correo o username (ambos son correo en este sistema)
                resultado = unit.session.execute(text("""
                    SELECT 
                        id_usuario,
                        correo_electronico,
                        activo
                    FROM usuario
                    WHERE correo_electronico = :email
                    LIMIT 1
                """), {"email": email_o_username}).fetchone()
                
                if resultado:
                    return {
                        'id_usuario': resultado[0],
                        'correo_electronico': resultado[1],
                        'activo': resultado[2]
                    }
                return None
        except Exception as e:
            print(f"[ERROR] buscar_usuario: {e}")
            return None
    
    @staticmethod
    def crear_codigo_recuperacion(id_usuario: int) -> Tuple[bool, str, Optional[str]]:
        """
        Paso 7: Genera y guarda código de recuperación en BD
        
        Args:
            id_usuario: ID del usuario
        
        Returns:
            Tuple[bool, str, Optional[str]]:
                - bool: True si se creó exitosamente
                - str: Mensaje
                - Optional[str]: Código generado o None si falló
        """
        try:
            with uow() as unit:
                # Invalidar códigos anteriores del usuario
                unit.session.execute(text("""
                    UPDATE password_reset_code
                    SET estado = 'expirado'
                    WHERE id_usuario = :user_id
                    AND estado = 'activo'
                """), {"user_id": id_usuario})
                
                # Generar nuevo código
                codigo = RecuperacionPasswordService.generar_codigo()
                fecha_creacion = datetime.now()
                fecha_expiracion = fecha_creacion + timedelta(
                    minutes=RecuperacionPasswordService.MINUTOS_EXPIRACION
                )
                
                # Guardar en BD
                unit.session.execute(text("""
                    INSERT INTO password_reset_code 
                        (id_usuario, codigo, fecha_creacion, fecha_expiracion, estado)
                    VALUES 
                        (:user_id, :codigo, :fecha_creacion, :fecha_expiracion, 'activo')
                """), {
                    "user_id": id_usuario,
                    "codigo": codigo,
                    "fecha_creacion": fecha_creacion,
                    "fecha_expiracion": fecha_expiracion
                })
                
                unit.commit()
                
                return True, "Código generado exitosamente", codigo
        
        except Exception as e:
            print(f"[ERROR] crear_codigo_recuperacion: {e}")
            return False, f"Error al generar código: {str(e)}", None
    
    @staticmethod
    def validar_codigo(email: str, codigo: str) -> Tuple[bool, str, Optional[int]]:
        """
        Paso 12: Verifica el código ingresado por el usuario
        
        12.1 Buscar código para el usuario
        12.2 Verificar que esté activo
        12.3 Verificar que no esté expirado
        12.4 Comparar código ingresado con el almacenado
        
        Args:
            email: Email del usuario
            codigo: Código de 6 caracteres ingresado
        
        Returns:
            Tuple[bool, str, Optional[int]]:
                - bool: True si el código es válido
                - str: Mensaje
                - Optional[int]: id_code para marcarlo como usado
        """
        try:
            with uow() as unit:
                # Buscar usuario
                usuario = unit.session.execute(text("""
                    SELECT id_usuario
                    FROM usuario
                    WHERE correo_electronico = :email
                """), {"email": email}).fetchone()
                
                if not usuario:
                    return False, "Usuario no encontrado", None
                
                id_usuario = usuario[0]
                
                # Buscar código activo
                resultado = unit.session.execute(text("""
                    SELECT 
                        id_code,
                        codigo,
                        fecha_expiracion,
                        estado
                    FROM password_reset_code
                    WHERE id_usuario = :user_id
                    AND estado = 'activo'
                    ORDER BY fecha_creacion DESC
                    LIMIT 1
                """), {"user_id": id_usuario}).fetchone()
                
                if not resultado:
                    return False, "No hay código activo para este usuario", None
                
                id_code, codigo_bd, fecha_expiracion, estado = resultado
                
                # Verificar expiración
                if datetime.now() > fecha_expiracion:
                    # Marcar como expirado
                    unit.session.execute(text("""
                        UPDATE password_reset_code
                        SET estado = 'expirado'
                        WHERE id_code = :id_code
                    """), {"id_code": id_code})
                    unit.commit()
                    return False, "El código ha expirado", None
                
                # Comparar códigos
                if codigo.upper() != codigo_bd.upper():
                    return False, "Código incorrecto", None
                
                return True, "Código válido", id_code
        
        except Exception as e:
            print(f"[ERROR] validar_codigo: {e}")
            return False, f"Error al validar código: {str(e)}", None
    
    @staticmethod
    def marcar_codigo_usado(id_code: int) -> bool:
        """
        Paso 14: Marca el código como usado para evitar reutilización
        """
        try:
            with uow() as unit:
                unit.session.execute(text("""
                    UPDATE password_reset_code
                    SET estado = 'usado'
                    WHERE id_code = :id_code
                """), {"id_code": id_code})
                unit.commit()
                return True
        except Exception as e:
            print(f"[ERROR] marcar_codigo_usado: {e}")
            return False
    
    @staticmethod
    def validar_nueva_password(password: str, confirmar_password: str) -> Tuple[bool, str]:
        """
        Paso 18: Valida la nueva contraseña
        
        18.1 Que ambos campos coincidan
        18.2 Que la contraseña cumpla reglas de seguridad
        
        Returns:
            Tuple[bool, str]: (es_valida, mensaje_error)
        """
        # 18.1 Verificar que coincidan
        if password != confirmar_password:
            return False, "Las contraseñas no coinciden"
        
        # 18.2 Reglas de seguridad
        if len(password) < RecuperacionPasswordService.MIN_LONGITUD_PASSWORD:
            return False, f"La contraseña debe tener al menos {RecuperacionPasswordService.MIN_LONGITUD_PASSWORD} caracteres"
        
        if not any(c.isupper() for c in password):
            return False, "La contraseña debe contener al menos una mayúscula"
        
        if not any(c.islower() for c in password):
            return False, "La contraseña debe contener al menos una minúscula"
        
        if not any(c.isdigit() for c in password):
            return False, "La contraseña debe contener al menos un número"
        
        return True, "Contraseña válida"
    
    @staticmethod
    def actualizar_password(email: str, nueva_password: str) -> Tuple[bool, str]:
        """
        Paso 20: Actualiza la contraseña cifrada en BD
        
        Args:
            email: Email del usuario
            nueva_password: Nueva contraseña sin cifrar
        
        Returns:
            Tuple[bool, str]: (exito, mensaje)
        """
        try:
            # Cifrar contraseña con bcrypt
            password_hash = bcrypt.hashpw(
                nueva_password.encode('utf-8'),
                bcrypt.gensalt()
            ).decode('utf-8')
            
            with uow() as unit:
                # Actualizar contraseña
                resultado = unit.session.execute(text("""
                    UPDATE usuario
                    SET contrasena = :password_hash
                    WHERE correo_electronico = :email
                    RETURNING id_usuario
                """), {
                    "password_hash": password_hash,
                    "email": email
                })
                
                if resultado.rowcount == 0:
                    return False, "Usuario no encontrado"
                
                unit.commit()
                
                return True, "Contraseña actualizada correctamente"
        
        except Exception as e:
            print(f"[ERROR] actualizar_password: {e}")
            return False, f"Error al actualizar contraseña: {str(e)}"
