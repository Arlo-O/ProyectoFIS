"""
Servicio para gestión de aspirantes
Implementa CU-12: Consultar y Gestionar Aspirantes

Pasos del diagrama:
- Paso 2: Cargar listado aspirantes actuales
- Paso 5-6: Obtener información completa de aspirante
"""

from typing import List, Dict, Optional, Tuple
from datetime import datetime
import traceback
from sqlalchemy import text
from app.data.db import SessionLocal
from app.ui.components.session import get_user_id


class ServicioAspirante:
    """
    Servicio para gestión de aspirantes en el sistema.
    Permite consultar listados y detalles individuales.
    """
    
    def __init__(self):
        """Inicializa el servicio de aspirantes"""
        self.session = None
    
    def obtener_listado_aspirantes(self) -> Tuple[bool, List[Dict], str]:
        """
        PASO 2 DEL DIAGRAMA: Cargar listado aspirantes actuales
        
        Recupera todos los aspirantes registrados en la BD con su información básica.
        
        Returns:
            Tuple[bool, List[Dict], str]: (éxito, lista de aspirantes, mensaje)
            
            Cada aspirante contiene:
            - id_aspirante: ID único
            - nombre_completo: Nombre y apellidos
            - numero_identificacion: Documento
            - grado_solicitado: Grado al que aspira
            - fecha_solicitud: Fecha de registro
            - estado_proceso: 'pendiente', 'en_proceso', 'aceptado', 'rechazado'
            - edad: Edad calculada
        """
        session = SessionLocal()
        
        try:
            # Consulta SQL para obtener aspirantes con información de persona
            query = text("""
                SELECT 
                    a.id_aspirante,
                    p.primer_nombre,
                    p.segundo_nombre,
                    p.primer_apellido,
                    p.segundo_apellido,
                    p.tipo_identificacion,
                    p.numero_identificacion,
                    p.fecha_nacimiento,
                    p.genero,
                    p.direccion,
                    p.telefono,
                    a.grado_solicitado,
                    a.fecha_solicitud,
                    a.estado_proceso
                FROM aspirante a
                INNER JOIN persona p ON a.id_aspirante = p.id_persona
                ORDER BY a.fecha_solicitud DESC
            """)
            
            resultados = session.execute(query).fetchall()
            
            if not resultados:
                return True, [], "No hay aspirantes registrados en el sistema."
            
            # Construir lista de aspirantes
            aspirantes = []
            for row in resultados:
                # Calcular nombre completo
                nombre_completo = f"{row.primer_nombre or ''} {row.segundo_nombre or ''} {row.primer_apellido or ''} {row.segundo_apellido or ''}".strip()
                nombre_completo = ' '.join(nombre_completo.split())  # Limpiar espacios múltiples
                
                # Calcular edad si hay fecha de nacimiento
                edad = None
                if row.fecha_nacimiento:
                    hoy = datetime.now()
                    edad = hoy.year - row.fecha_nacimiento.year - (
                        (hoy.month, hoy.day) < (row.fecha_nacimiento.month, row.fecha_nacimiento.day)
                    )
                
                # Formatear fecha de solicitud
                fecha_solicitud_str = row.fecha_solicitud.strftime("%d/%m/%Y") if row.fecha_solicitud else "N/A"
                
                aspirante_dict = {
                    'id_aspirante': row.id_aspirante,
                    'nombre_completo': nombre_completo,
                    'primer_nombre': row.primer_nombre,
                    'segundo_nombre': row.segundo_nombre,
                    'primer_apellido': row.primer_apellido,
                    'segundo_apellido': row.segundo_apellido,
                    'tipo_identificacion': row.tipo_identificacion,
                    'numero_identificacion': row.numero_identificacion,
                    'grado_solicitado': row.grado_solicitado,
                    'fecha_solicitud': fecha_solicitud_str,
                    'fecha_solicitud_obj': row.fecha_solicitud,
                    'estado_proceso': row.estado_proceso or 'pendiente',
                    'edad': edad,
                    'genero': row.genero,
                    'direccion': row.direccion,
                    'telefono': row.telefono,
                    'fecha_nacimiento': row.fecha_nacimiento
                }
                
                aspirantes.append(aspirante_dict)
            
            mensaje = f"Se encontraron {len(aspirantes)} aspirante(s) en el sistema."
            return True, aspirantes, mensaje
            
        except Exception as e:
            print(f"Error al obtener listado de aspirantes: {e}")
            print(traceback.format_exc())
            return False, [], f"Error al consultar aspirantes: {str(e)}"
        
        finally:
            session.close()
    
    def obtener_detalle_aspirante(self, id_aspirante: int) -> Tuple[bool, Optional[Dict], str]:
        """
        PASO 5-6 DEL DIAGRAMA: Obtener información completa de aspirante
        
        Recupera toda la información del aspirante incluyendo:
        - Datos personales completos
        - Información del acudiente
        - Estado del proceso
        - Historial (si existe)
        
        Args:
            id_aspirante: ID del aspirante a consultar
            
        Returns:
            Tuple[bool, Optional[Dict], str]: (éxito, datos del aspirante, mensaje)
            
            El diccionario incluye:
            - Todos los campos de persona
            - Datos del aspirante (grado, estado, fecha)
            - Información del acudiente asociado
            - Respuestas del formulario (si existen)
        """
        session = SessionLocal()
        
        try:
            # 1. Obtener información básica del aspirante
            query_aspirante = text("""
                SELECT 
                    a.id_aspirante,
                    a.grado_solicitado,
                    a.fecha_solicitud,
                    a.estado_proceso,
                    p.tipo_identificacion,
                    p.numero_identificacion,
                    p.primer_nombre,
                    p.segundo_nombre,
                    p.primer_apellido,
                    p.segundo_apellido,
                    p.fecha_nacimiento,
                    p.genero,
                    p.direccion,
                    p.telefono
                FROM aspirante a
                INNER JOIN persona p ON a.id_aspirante = p.id_persona
                WHERE a.id_aspirante = :id_aspirante
            """)
            
            resultado_asp = session.execute(query_aspirante, {"id_aspirante": id_aspirante}).fetchone()
            
            if not resultado_asp:
                return False, None, f"No se encontró el aspirante con ID {id_aspirante}"
            
            # Construir información del aspirante
            nombre_completo = f"{resultado_asp.primer_nombre or ''} {resultado_asp.segundo_nombre or ''} {resultado_asp.primer_apellido or ''} {resultado_asp.segundo_apellido or ''}".strip()
            nombre_completo = ' '.join(nombre_completo.split())
            
            # Calcular edad
            edad = None
            if resultado_asp.fecha_nacimiento:
                hoy = datetime.now()
                edad = hoy.year - resultado_asp.fecha_nacimiento.year - (
                    (hoy.month, hoy.day) < (resultado_asp.fecha_nacimiento.month, resultado_asp.fecha_nacimiento.day)
                )
            
            # Formatear fechas
            fecha_nacimiento_str = resultado_asp.fecha_nacimiento.strftime("%d/%m/%Y") if resultado_asp.fecha_nacimiento else "N/A"
            fecha_solicitud_str = resultado_asp.fecha_solicitud.strftime("%d/%m/%Y %H:%M") if resultado_asp.fecha_solicitud else "N/A"
            
            aspirante_info = {
                'id_aspirante': resultado_asp.id_aspirante,
                'nombre_completo': nombre_completo,
                'primer_nombre': resultado_asp.primer_nombre,
                'segundo_nombre': resultado_asp.segundo_nombre,
                'primer_apellido': resultado_asp.primer_apellido,
                'segundo_apellido': resultado_asp.segundo_apellido,
                'tipo_identificacion': resultado_asp.tipo_identificacion,
                'numero_identificacion': resultado_asp.numero_identificacion,
                'fecha_nacimiento': fecha_nacimiento_str,
                'fecha_nacimiento_obj': resultado_asp.fecha_nacimiento,
                'edad': edad,
                'genero': resultado_asp.genero,
                'direccion': resultado_asp.direccion,
                'telefono': resultado_asp.telefono,
                'grado_solicitado': resultado_asp.grado_solicitado,
                'fecha_solicitud': fecha_solicitud_str,
                'fecha_solicitud_obj': resultado_asp.fecha_solicitud,
                'estado_proceso': resultado_asp.estado_proceso or 'pendiente'
            }
            
            # 2. Obtener información del acudiente (si existe)
            # Nota: La relación aspirante-acudiente está en la tabla formulario_preinscripcion
            acudiente_info = None
            if False:  # Deshabilitado temporalmente - id_acudiente no existe en aspirante
                query_acudiente = text("""
                    SELECT 
                        ac.id_acudiente,
                        ac.parentesco,
                        ac.email,
                        p.primer_nombre,
                        p.segundo_nombre,
                        p.primer_apellido,
                        p.segundo_apellido,
                        p.numero_identificacion,
                        p.telefono,
                        p.direccion
                    FROM acudiente ac
                    INNER JOIN persona p ON ac.id_acudiente = p.id_persona
                    WHERE ac.id_acudiente = :id_acudiente
                """)
                
                resultado_acu = session.execute(
                    query_acudiente, 
                    {"id_acudiente": resultado_asp.id_acudiente}
                ).fetchone()
                
                if resultado_acu:
                    nombre_acudiente = f"{resultado_acu.primer_nombre or ''} {resultado_acu.segundo_nombre or ''} {resultado_acu.primer_apellido or ''} {resultado_acu.segundo_apellido or ''}".strip()
                    nombre_acudiente = ' '.join(nombre_acudiente.split())
                    
                    acudiente_info = {
                        'id_acudiente': resultado_acu.id_acudiente,
                        'nombre_completo': nombre_acudiente,
                        'numero_identificacion': resultado_acu.numero_identificacion,
                        'parentesco': resultado_acu.parentesco,
                        'email': resultado_acu.email,
                        'telefono': resultado_acu.telefono,
                        'direccion': resultado_acu.direccion
                    }
            
            # 3. Obtener respuestas del formulario de preinscripción (si existen)
            # NOTA: Funcionalidad deshabilitada - tabla respuesta_form_pre no tiene FK a aspirante
            respuestas_info = None
            
            # query_respuestas = text("""
            #     SELECT 
            #         id_respuesta,
            #         fecha_solicitud,
            #         datos_acudiente
            #     FROM respuesta_form_pre
            #     ORDER BY fecha_solicitud DESC
            #     LIMIT 1
            # """)
            # 
            # resultado_resp = session.execute(query_respuestas).fetchone()
            # 
            # if resultado_resp:
            #     fecha_str = resultado_resp.fecha_solicitud.strftime("%d/%m/%Y %H:%M") if resultado_resp.fecha_solicitud else "N/A"
            #     respuestas_info = {
            #         'id_respuesta': resultado_resp.id_respuesta,
            #         'fecha_solicitud': fecha_str,
            #         'datos_acudiente': resultado_resp.datos_acudiente
            #     }
            
            # Construir respuesta completa
            detalle_completo = {
                'aspirante': aspirante_info,
                'acudiente': acudiente_info,
                'respuestas_formulario': respuestas_info,
                # Acciones disponibles según estado
                'acciones_disponibles': self._obtener_acciones_disponibles(aspirante_info['estado_proceso'])
            }
            
            return True, detalle_completo, "Información obtenida exitosamente."
            
        except Exception as e:
            print(f"Error al obtener detalle del aspirante: {e}")
            print(traceback.format_exc())
            return False, None, f"Error al consultar detalle: {str(e)}"
        
        finally:
            session.close()
    
    def _obtener_acciones_disponibles(self, estado_proceso: str) -> List[Dict[str, str]]:
        """
        PASO 7 DEL DIAGRAMA: Determinar acciones disponibles según estado
        
        Las acciones posibles son:
        1. Programar entrevista
        2. Diligenciar admisión aspirante
        
        Args:
            estado_proceso: Estado actual del aspirante
            
        Returns:
            List[Dict]: Lista de acciones disponibles con nombre y tipo
        """
        acciones = []
        
        # Acción 1: Programar entrevista
        # Disponible si: estado es 'pendiente' o 'en_proceso'
        if estado_proceso in ['pendiente', 'en_proceso']:
            acciones.append({
                'nombre': 'Programar entrevista',
                'tipo': 'programar_entrevista',
                'descripcion': 'Agendar una entrevista con el aspirante y su acudiente',
                'icono': '📅',
                'habilitado': True
            })
        else:
            acciones.append({
                'nombre': 'Programar entrevista',
                'tipo': 'programar_entrevista',
                'descripcion': 'No disponible para este estado',
                'icono': '📅',
                'habilitado': False
            })
        
        # Acción 2: Diligenciar admisión
        # Disponible si: estado es 'en_proceso' (ya pasó entrevista)
        if estado_proceso == 'en_proceso':
            acciones.append({
                'nombre': 'Diligenciar admisión aspirante',
                'tipo': 'diligenciar_admision',
                'descripcion': 'Completar el proceso de admisión del aspirante',
                'icono': '✅',
                'habilitado': True
            })
        else:
            acciones.append({
                'nombre': 'Diligenciar admisión aspirante',
                'tipo': 'diligenciar_admision',
                'descripcion': 'Requiere que el aspirante esté en proceso',
                'icono': '✅',
                'habilitado': False
            })
        
        return acciones
    
    def actualizar_estado_aspirante(self, id_aspirante: int, nuevo_estado: str) -> Tuple[bool, str]:
        """
        Actualiza el estado del proceso de un aspirante.
        
        Estados válidos:
        - 'pendiente': Recién registrado
        - 'en_proceso': Entrevista programada o realizada
        - 'aceptado': Admitido al colegio
        - 'rechazado': No admitido
        
        Args:
            id_aspirante: ID del aspirante
            nuevo_estado: Nuevo estado del proceso
            
        Returns:
            Tuple[bool, str]: (éxito, mensaje)
        """
        estados_validos = ['pendiente', 'en_proceso', 'aceptado', 'rechazado']
        
        if nuevo_estado not in estados_validos:
            return False, f"Estado inválido. Estados permitidos: {', '.join(estados_validos)}"
        
        session = SessionLocal()
        
        try:
            query = text("""
                UPDATE aspirante
                SET estado_proceso = :nuevo_estado
                WHERE id_aspirante = :id_aspirante
            """)
            
            result = session.execute(query, {
                "nuevo_estado": nuevo_estado,
                "id_aspirante": id_aspirante
            })
            
            session.commit()
            
            if result.rowcount == 0:
                return False, f"No se encontró el aspirante con ID {id_aspirante}"
            
            return True, f"Estado actualizado exitosamente a '{nuevo_estado}'"
            
        except Exception as e:
            session.rollback()
            print(f"Error al actualizar estado: {e}")
            print(traceback.format_exc())
            return False, f"Error al actualizar estado: {str(e)}"
        
        finally:
            session.close()
    
    def programar_entrevista(self, id_aspirante: int, fecha_programada: datetime, 
                           lugar: str) -> Tuple[bool, str]:
        """
        Programa una entrevista para un aspirante.
        
        Valida la disponibilidad y crea el registro de entrevista en la BD.
        Si es exitoso, actualiza el estado del aspirante a 'en_proceso'.
        
        Args:
            id_aspirante: ID del aspirante
            fecha_programada: Fecha y hora programada para la entrevista
            lugar: Lugar donde se realizará la entrevista
            
        Returns:
            Tuple[bool, str]: (éxito, mensaje)
        """
        session = SessionLocal()
        
        try:
            # 1. Validar que el aspirante existe y está en estado válido
            query_aspirante = text("""
                SELECT estado_proceso 
                FROM aspirante 
                WHERE id_aspirante = :id_aspirante
            """)
            
            resultado = session.execute(query_aspirante, {"id_aspirante": id_aspirante}).fetchone()
            
            if not resultado:
                return False, f"No se encontró el aspirante con ID {id_aspirante}"
            
            estado_actual = resultado.estado_proceso
            
            # Solo se puede programar entrevista si está en 'pendiente' o 'en_proceso'
            if estado_actual not in ['pendiente', 'en_proceso']:
                return False, f"No se puede programar entrevista. El aspirante está en estado '{estado_actual}'."
            
            # 2. Obtener el ID del directivo actual (desde la sesión)
            usuario_id = get_user_id()
            
            if not usuario_id:
                return False, "No se pudo identificar al usuario actual."
            
            # Obtener el id_directivo desde el id_usuario
            query_directivo = text("""
                SELECT id_directivo 
                FROM directivo 
                WHERE id_usuario = :id_usuario
            """)
            
            resultado_dir = session.execute(query_directivo, {"id_usuario": usuario_id}).fetchone()
            
            if not resultado_dir:
                return False, "No se pudo identificar al directivo actual."
            
            id_directivo = resultado_dir.id_directivo
            
            # 3. Validar disponibilidad: verificar que no haya otra entrevista 
            #    en la misma fecha/hora/lugar
            query_disponibilidad = text("""
                SELECT COUNT(*) as count
                FROM entrevista
                WHERE fecha_programada = :fecha_programada
                AND lugar = :lugar
                AND estado != 'cancelada'
            """)
            
            resultado_disp = session.execute(query_disponibilidad, {
                "fecha_programada": fecha_programada,
                "lugar": lugar
            }).fetchone()
            
            if resultado_disp.count > 0:
                return False, (
                    f"El lugar '{lugar}' no está disponible para la fecha y hora seleccionadas. "
                    f"Por favor elija otra hora o lugar."
                )
            
            # 4. Verificar que el aspirante no tenga ya una entrevista programada
            query_entrevista_existente = text("""
                SELECT COUNT(*) as count
                FROM entrevista
                WHERE id_aspirante = :id_aspirante
                AND estado IN ('programada', 'confirmada')
            """)
            
            resultado_exist = session.execute(
                query_entrevista_existente, 
                {"id_aspirante": id_aspirante}
            ).fetchone()
            
            if resultado_exist.count > 0:
                return False, "El aspirante ya tiene una entrevista programada."
            
            # 5. Crear la entrevista
            query_insert = text("""
                INSERT INTO entrevista 
                (id_aspirante, id_directivo_remitente, fecha_programada, lugar, estado, notas)
                VALUES 
                (:id_aspirante, :id_directivo, :fecha_programada, :lugar, :estado, :notas)
            """)
            
            session.execute(query_insert, {
                "id_aspirante": id_aspirante,
                "id_directivo": id_directivo,
                "fecha_programada": fecha_programada,
                "lugar": lugar,
                "estado": "programada",
                "notas": f"Entrevista programada por directivo ID {id_directivo}"
            })
            
            # 6. Actualizar el estado del aspirante a 'en_proceso' si estaba en 'pendiente'
            if estado_actual == 'pendiente':
                query_update = text("""
                    UPDATE aspirante
                    SET estado_proceso = 'en_proceso'
                    WHERE id_aspirante = :id_aspirante
                """)
                
                session.execute(query_update, {"id_aspirante": id_aspirante})
            
            session.commit()
            
            return True, "El estado del aspirante ha sido actualizado a 'en proceso'."
            
        except Exception as e:
            session.rollback()
            print(f"Error al programar entrevista: {e}")
            print(traceback.format_exc())
            return False, f"Error al programar entrevista: {str(e)}"
        
        finally:
            session.close()
