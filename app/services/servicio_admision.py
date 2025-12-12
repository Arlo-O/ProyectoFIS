"""
Servicio para gestión de admisiones de aspirantes
Implementa CU-18: Admitir aspirante

Flujo del Caso de Uso:
1. Directivo inicia el caso de uso
2. Directivo hace clic en "Diligenciar admisión"
3. Sistema habilita botones de admisión (Admitir/Rechazar)
4. Directivo elige opción
5. Sistema evalúa la decisión:
   - Si Admitir: cambiar estado a "Admitido", guardar
   - Si Rechazar: habilitar campo justificación, validar, cambiar estado a "Rechazado", guardar
"""

from typing import Tuple
from sqlalchemy import text
from app.data.db import SessionLocal


class ServicioAdmision:
    """
    Servicio para la admisión o rechazo de aspirantes.
    Implementa el CU-18 según el diagrama de actividades.
    """
    
    def __init__(self):
        """Inicializa el servicio de admisión"""
        self.session = None
    
    def admitir_aspirante(self, id_aspirante: int) -> Tuple[bool, str]:
        """
        RUTA DE ADMISIÓN DEL CU-18:
        
        Paso 6A: Cambiar estado del aspirante a "Admitido"
        Paso 7A: Guardar cambios en el datastore "Aspirante"
        Paso 8A: Finalizar esta rama del flujo
        
        Args:
            id_aspirante: ID del aspirante a admitir
            
        Returns:
            Tuple[bool, str]: (éxito, mensaje)
        """
        session = SessionLocal()
        
        try:
            # Verificar que el aspirante existe
            query_verificar = text("""
                SELECT id_aspirante, estado_proceso
                FROM aspirante
                WHERE id_aspirante = :id_aspirante
            """)
            
            resultado = session.execute(query_verificar, {"id_aspirante": id_aspirante}).fetchone()
            
            if not resultado:
                return False, f"No se encontró el aspirante con ID {id_aspirante}"
            
            # Validar que el aspirante no esté ya admitido o rechazado
            if resultado.estado_proceso == "admitido":
                return False, "El aspirante ya está admitido"
            
            # PASO 6A: Cambiar el estado del aspirante a "Admitido"
            query_admitir = text("""
                UPDATE aspirante
                SET estado_proceso = 'admitido',
                    justificacion_rechazo = NULL
                WHERE id_aspirante = :id_aspirante
            """)
            
            session.execute(query_admitir, {"id_aspirante": id_aspirante})
            
            # PASO 7A: Guardar los cambios
            session.commit()
            
            return True, "Aspirante admitido exitosamente"
            
        except Exception as e:
            session.rollback()
            import traceback
            print(f"Error al admitir aspirante: {e}")
            print(traceback.format_exc())
            return False, f"Error al admitir aspirante: {str(e)}"
        
        finally:
            session.close()
    
    def rechazar_aspirante(self, id_aspirante: int, justificacion: str) -> Tuple[bool, str]:
        """
        RUTA DE RECHAZO DEL CU-18:
        
        Paso 6B: Habilitar campo de justificación
        Paso 7B: Directivo digita justificación
        Paso 8B: Directivo hace clic en "Confirmar"
        Paso 9B: Validar que la justificación no esté vacía
        Paso 10B: Registrar en BD: estado = "Rechazado", justificacion_rechazo
        Paso 11B: Guardar información en datastore "Aspirante"
        Paso 12B: Finalizar flujo
        
        Args:
            id_aspirante: ID del aspirante a rechazar
            justificacion: Justificación del rechazo (texto obligatorio)
            
        Returns:
            Tuple[bool, str]: (éxito, mensaje)
        """
        session = SessionLocal()
        
        try:
            # PASO 9B: Validar que la justificación no esté vacía
            if not justificacion or justificacion.strip() == "":
                return False, "La justificación del rechazo es obligatoria"
            
            # Verificar que el aspirante existe
            query_verificar = text("""
                SELECT id_aspirante, estado_proceso
                FROM aspirante
                WHERE id_aspirante = :id_aspirante
            """)
            
            resultado = session.execute(query_verificar, {"id_aspirante": id_aspirante}).fetchone()
            
            if not resultado:
                return False, f"No se encontró el aspirante con ID {id_aspirante}"
            
            # Validar que el aspirante no esté ya rechazado o admitido
            if resultado.estado_proceso == "rechazado":
                return False, "El aspirante ya está rechazado"
            if resultado.estado_proceso == "admitido":
                return False, "No se puede rechazar un aspirante que ya fue admitido"
            
            # PASO 10B: Registrar en BD estado = "Rechazado" y justificacion_rechazo
            query_rechazar = text("""
                UPDATE aspirante
                SET estado_proceso = 'rechazado',
                    justificacion_rechazo = :justificacion
                WHERE id_aspirante = :id_aspirante
            """)
            
            session.execute(query_rechazar, {
                "id_aspirante": id_aspirante,
                "justificacion": justificacion.strip()
            })
            
            # PASO 11B: Guardar la información en el datastore "Aspirante"
            session.commit()
            
            return True, "Aspirante rechazado exitosamente"
            
        except Exception as e:
            session.rollback()
            import traceback
            print(f"Error al rechazar aspirante: {e}")
            print(traceback.format_exc())
            return False, f"Error al rechazar aspirante: {str(e)}"
        
        finally:
            session.close()
    
    def verificar_estado_aspirante(self, id_aspirante: int) -> Tuple[bool, str, str]:
        """
        Verifica el estado actual de un aspirante.
        
        Args:
            id_aspirante: ID del aspirante
            
        Returns:
            Tuple[bool, str, str]: (éxito, estado, justificación si existe)
        """
        session = SessionLocal()
        
        try:
            query = text("""
                SELECT estado_proceso, justificacion_rechazo
                FROM aspirante
                WHERE id_aspirante = :id_aspirante
            """)
            
            resultado = session.execute(query, {"id_aspirante": id_aspirante}).fetchone()
            
            if not resultado:
                return False, "", f"No se encontró el aspirante con ID {id_aspirante}"
            
            return True, resultado.estado_proceso, resultado.justificacion_rechazo or ""
            
        except Exception as e:
            import traceback
            print(f"Error al verificar estado: {e}")
            print(traceback.format_exc())
            return False, "", f"Error al verificar estado: {str(e)}"
        
        finally:
            session.close()
