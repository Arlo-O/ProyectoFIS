"""
📋 InhabilitacionUsuarioService
Servicio para gestionar la inhabilitación de usuarios (CU-08)

Implementa el flujo completo del caso de uso CU-08 "Inhabilitar usuario"
siguiendo EXACTAMENTE las actividades del diagrama:

PASOS IMPLEMENTADOS:
- Paso 7.1: Verificar que el usuario exista
- Paso 7.2: Verificar que esté actualmente activo
- Paso 7.3: Verificar que la justificación NO esté vacía
- Paso 8: Cambiar estado y guardar justificación
- Paso 9: Confirmar cambio en BD

Autor: Sistema FIS
Fecha: 11 de diciembre de 2025
"""

from sqlalchemy import text
from app.data.db import SessionLocal


class InhabilitacionUsuarioService:
    """
    Servicio estático para inhabilitar usuarios del sistema.
    
    NO SE REQUIERE AUDITORÍA - El sistema simplemente desactiva
    el usuario y guarda la justificación obligatoria.
    """
    
    @staticmethod
    def inhabilitar_usuario(id_usuario: int, justificacion: str, admin_id: int = None) -> tuple[bool, str]:
        """
        Inhabilita un usuario siguiendo el flujo del CU-08.
        
        Args:
            id_usuario (int): ID del usuario a inhabilitar
            justificacion (str): Justificación obligatoria de la inhabilitación
            admin_id (int, optional): ID del administrador (no usado, sin auditoría)
        
        Returns:
            tuple[bool, str]: (éxito, mensaje)
            - (True, "Usuario inhabilitado correctamente") si todo OK
            - (False, "mensaje de error") si falla alguna validación
        
        FLUJO IMPLEMENTADO:
        1. Paso 7.1: Verificar que el usuario exista
        2. Paso 7.2: Verificar que esté actualmente activo
        3. Paso 7.3: Verificar que la justificación NO esté vacía
        4. Paso 8: Cambiar usuario.activo = False y guardar justificación
        5. Paso 9: Confirmar cambio en BD
        """
        
        # VALIDACIÓN: Justificación obligatoria (Paso 7.3)
        if not justificacion or not justificacion.strip():
            return False, "La justificación es obligatoria para inhabilitar un usuario"
        
        session = SessionLocal()
        
        try:
            # PASO 7.1: Verificar que el usuario exista
            query_existe = text("""
                SELECT id_usuario, activo, correo_electronico
                FROM usuario
                WHERE id_usuario = :id_usuario
            """)
            
            resultado = session.execute(
                query_existe,
                {"id_usuario": id_usuario}
            ).fetchone()
            
            if not resultado:
                return False, "El usuario no existe en el sistema"
            
            # PASO 7.2: Verificar que esté actualmente activo
            if not resultado.activo:
                return False, "El usuario ya está inhabilitado"
            
            # PASO 8: Cambiar estado y guardar justificación
            query_inhabilitar = text("""
                UPDATE usuario
                SET 
                    activo = FALSE,
                    justificacion_inhabilitacion = :justificacion
                WHERE id_usuario = :id_usuario
            """)
            
            session.execute(
                query_inhabilitar,
                {
                    "id_usuario": id_usuario,
                    "justificacion": justificacion.strip()
                }
            )
            
            session.commit()
            
            # PASO 9: Confirmación exitosa
            return True, "El usuario ha sido inhabilitado satisfactoriamente"
            
        except Exception as e:
            session.rollback()
            return False, f"Error al inhabilitar el usuario: {str(e)}"
        
        finally:
            session.close()
    
    
    @staticmethod
    def habilitar_usuario(id_usuario: int, justificacion_habilitacion: str = None) -> tuple[bool, str]:
        """
        Habilita un usuario previamente inhabilitado.
        
        FUNCIONALIDAD ADICIONAL (no está en el CU-08 pero es útil).
        
        Args:
            id_usuario (int): ID del usuario a habilitar
            justificacion_habilitacion (str, optional): Justificación de la habilitación
        
        Returns:
            tuple[bool, str]: (éxito, mensaje)
        """
        
        session = SessionLocal()
        
        try:
            # Verificar que el usuario exista
            query_existe = text("""
                SELECT id_usuario, activo
                FROM usuario
                WHERE id_usuario = :id_usuario
            """)
            
            resultado = session.execute(
                query_existe,
                {"id_usuario": id_usuario}
            ).fetchone()
            
            if not resultado:
                return False, "El usuario no existe en el sistema"
            
            # Verificar que esté inhabilitado
            if resultado.activo:
                return False, "El usuario ya está activo"
            
            # Habilitar usuario (limpiar justificación si se proporciona nueva)
            query_habilitar = text("""
                UPDATE usuario
                SET 
                    activo = TRUE,
                    justificacion_inhabilitacion = :justificacion
                WHERE id_usuario = :id_usuario
            """)
            
            # Si no se proporciona justificación de habilitación, mantener la anterior
            nueva_justificacion = None
            if justificacion_habilitacion:
                nueva_justificacion = f"[REACTIVADO] {justificacion_habilitacion.strip()}"
            
            session.execute(
                query_habilitar,
                {
                    "id_usuario": id_usuario,
                    "justificacion": nueva_justificacion
                }
            )
            
            session.commit()
            
            return True, "El usuario ha sido habilitado exitosamente"
            
        except Exception as e:
            session.rollback()
            return False, f"Error al habilitar el usuario: {str(e)}"
        
        finally:
            session.close()
    
    
    @staticmethod
    def obtener_usuario_por_id(id_usuario: int) -> dict:
        """
        Obtiene información completa de un usuario por su ID.
        
        Args:
            id_usuario (int): ID del usuario
        
        Returns:
            dict: Información del usuario o None si no existe
            {
                'id_usuario': int,
                'correo_electronico': str,
                'activo': bool,
                'nombre_rol': str,
                'justificacion_inhabilitacion': str
            }
        """
        
        session = SessionLocal()
        
        try:
            query = text("""
                SELECT 
                    u.id_usuario,
                    u.correo_electronico,
                    u.activo,
                    r.nombre_rol,
                    u.justificacion_inhabilitacion,
                    u.fecha_creacion,
                    u.ultimo_ingreso
                FROM usuario u
                LEFT JOIN rol r ON u.id_rol = r.id_rol
                WHERE u.id_usuario = :id_usuario
            """)
            
            resultado = session.execute(
                query,
                {"id_usuario": id_usuario}
            ).fetchone()
            
            if not resultado:
                return None
            
            return {
                'id_usuario': resultado.id_usuario,
                'correo_electronico': resultado.correo_electronico,
                'activo': resultado.activo,
                'nombre_rol': resultado.nombre_rol,
                'justificacion_inhabilitacion': resultado.justificacion_inhabilitacion,
                'fecha_creacion': resultado.fecha_creacion,
                'ultimo_ingreso': resultado.ultimo_ingreso
            }
            
        except Exception as e:
            print(f"Error al obtener usuario: {e}")
            return None
        
        finally:
            session.close()
    
    
    @staticmethod
    def validar_autoinhabilitacion(id_usuario: int, admin_id: int) -> tuple[bool, str]:
        """
        Valida que el administrador no se esté inhabilitando a sí mismo.
        
        VALIDACIÓN ADICIONAL OPCIONAL mencionada en las precondiciones.
        
        Args:
            id_usuario (int): ID del usuario a inhabilitar
            admin_id (int): ID del administrador que intenta inhabilitar
        
        Returns:
            tuple[bool, str]: (válido, mensaje)
            - (True, "") si la operación es válida
            - (False, "mensaje") si el admin intenta inhabilitarse
        """
        
        if id_usuario == admin_id:
            return False, "No puedes inhabilitarte a ti mismo"
        
        return True, ""
