# -*- coding: utf-8 -*-
"""
Modelo para Códigos de Recuperación de Contraseña
Almacena códigos temporales de 6 caracteres para recuperación
"""

from datetime import datetime

class PasswordResetCode:
    """
    Código de recuperación de contraseña temporal
    
    Atributos:
    - id_code: ID único del código
    - id_usuario: ID del usuario solicitante
    - codigo: Código de 6 caracteres
    - fecha_creacion: Timestamp de creación
    - fecha_expiracion: Timestamp de expiración (10 minutos)
    - estado: 'activo', 'usado', 'expirado'
    """
    
    def __init__(
        self,
        id_code: int = None,
        id_usuario: int = None,
        codigo: str = None,
        fecha_creacion: datetime = None,
        fecha_expiracion: datetime = None,
        estado: str = 'activo'
    ):
        self.id_code = id_code
        self.id_usuario = id_usuario
        self.codigo = codigo
        self.fecha_creacion = fecha_creacion or datetime.now()
        self.fecha_expiracion = fecha_expiracion
        self.estado = estado
    
    def esta_expirado(self) -> bool:
        """Verifica si el código ya expiró"""
        return datetime.now() > self.fecha_expiracion
    
    def esta_activo(self) -> bool:
        """Verifica si el código está activo y no expirado"""
        return self.estado == 'activo' and not self.esta_expirado()
    
    def marcar_usado(self):
        """Marca el código como usado para evitar reutilización"""
        self.estado = 'usado'
    
    def __repr__(self):
        return f"<PasswordResetCode(usuario={self.id_usuario}, codigo={self.codigo}, estado={self.estado})>"
