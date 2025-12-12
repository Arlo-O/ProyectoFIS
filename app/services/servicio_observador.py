"""
CU-24: Gestionar observador del estudiante

Servicio que implementa la lógica de negocio para:
- Cargar observador del estudiante (PASO 3)
- Validar modificaciones permitidas (PASO 11)
- Registrar modificaciones en el observador (PASO 13)

RESTRICCIÓN DEL DIAGRAMA:
"Solo se pueden modificar datos de comportamiento o generar observaciones"
"""

from datetime import datetime
from typing import Dict, List, Tuple, Optional
from sqlalchemy import text
from app.config.database import SessionLocal


class ServicioObservador:
    """
    Gestiona las operaciones del observador del estudiante.
    """
    
    # PASO 7: Definir campos permitidos para modificación
    CAMPOS_PERMITIDOS = {'comportamiento_general'}
    CAMPOS_ANOTACION = {'categoria', 'detalle'}
    
    @staticmethod
    def cargar_observador_estudiante(estudiante_id: int) -> Dict:
        """
        PASO 3: Cargar observador estudiante
        3.1 Consultar datos actuales del estudiante
        3.2 Consultar observador asociado
        
        Args:
            estudiante_id: ID del estudiante
            
        Returns:
            Dict con datos del estudiante, observador y anotaciones
            
        Raises:
            ValueError: Si el estudiante no existe o no tiene observador
        """
        session = SessionLocal()
        try:
            # PASO 3.1: Consultar datos del estudiante
            query_estudiante = text("""
                SELECT 
                    e.id_estudiante,
                    p.nombres,
                    p.apellidos,
                    e.codigo_estudiante,
                    e.curso_id
                FROM estudiante e
                JOIN persona p ON e.id_persona = p.id_persona
                WHERE e.id_estudiante = :estudiante_id
            """)
            
            resultado_estudiante = session.execute(
                query_estudiante,
                {"estudiante_id": estudiante_id}
            ).fetchone()
            
            if not resultado_estudiante:
                raise ValueError(f"Estudiante con ID {estudiante_id} no encontrado")
            
            # PASO 3.2: Consultar observador asociado
            query_observador = text("""
                SELECT 
                    id_observador,
                    id_estudiante,
                    comportamiento_general
                FROM observador
                WHERE id_estudiante = :estudiante_id
            """)
            
            resultado_observador = session.execute(
                query_observador,
                {"estudiante_id": estudiante_id}
            ).fetchone()
            
            if not resultado_observador:
                raise ValueError(f"El estudiante {estudiante_id} no tiene observador asociado")
            
            # Consultar anotaciones del observador
            query_anotaciones = text("""
                SELECT 
                    a.id_anotacion,
                    a.categoria,
                    a.detalle,
                    a.fecha_registro,
                    p.nombres || ' ' || p.apellidos as autor_nombre
                FROM anotacion a
                LEFT JOIN profesor pr ON a.id_profesor_autor = pr.id_profesor
                LEFT JOIN persona p ON pr.id_persona = p.id_persona
                WHERE a.id_observador = :id_observador
                ORDER BY a.fecha_registro DESC
            """)
            
            anotaciones = session.execute(
                query_anotaciones,
                {"id_observador": resultado_observador.id_observador}
            ).fetchall()
            
            return {
                "estudiante": {
                    "id": resultado_estudiante.id_estudiante,
                    "nombres": resultado_estudiante.nombres,
                    "apellidos": resultado_estudiante.apellidos,
                    "codigo": resultado_estudiante.codigo_estudiante,
                    "curso_id": resultado_estudiante.curso_id
                },
                "observador": {
                    "id": resultado_observador.id_observador,
                    "comportamiento_general": resultado_observador.comportamiento_general or ""
                },
                "anotaciones": [
                    {
                        "id": a.id_anotacion,
                        "categoria": a.categoria,
                        "detalle": a.detalle,
                        "fecha": a.fecha_registro,
                        "autor": a.autor_nombre or "Sistema"
                    }
                    for a in anotaciones
                ]
            }
            
        finally:
            session.close()
    
    @staticmethod
    def validar_modificaciones(modificaciones: Dict, tipo_modificacion: str) -> Tuple[bool, List[str]]:
        """
        PASO 11: Validar modificaciones
        11.1 Validar que no existan campos no permitidos
        11.2 Validar formato (fechas, texto, longitud)
        11.3 Validar que la observación o cambio no esté vacío
        11.4 Preparar lista de errores si corresponde
        
        RESTRICCIÓN: Solo permitir modificaciones a comportamiento u observaciones
        
        Args:
            modificaciones: Diccionario con los cambios propuestos
            tipo_modificacion: 'comportamiento' o 'anotacion'
            
        Returns:
            Tuple[bool, List[str]]: (es_valido, lista_de_errores)
        """
        errores = []
        
        # PASO 11.1: Validar campos permitidos según tipo
        if tipo_modificacion == 'comportamiento':
            campos_validos = ServicioObservador.CAMPOS_PERMITIDOS
        elif tipo_modificacion == 'anotacion':
            campos_validos = ServicioObservador.CAMPOS_ANOTACION
        else:
            errores.append(f"Tipo de modificación no válido: {tipo_modificacion}")
            return False, errores
        
        # Verificar que solo se envíen campos permitidos
        campos_enviados = set(modificaciones.keys())
        campos_no_permitidos = campos_enviados - campos_validos
        
        if campos_no_permitidos:
            errores.append(
                f"Campos no permitidos: {', '.join(campos_no_permitidos)}. "
                f"Solo se pueden modificar: {', '.join(campos_validos)}"
            )
        
        # PASO 11.2 y 11.3: Validar formato y no vacío
        if tipo_modificacion == 'comportamiento':
            comportamiento = modificaciones.get('comportamiento_general', '').strip()
            
            if not comportamiento:
                errores.append("El comportamiento general no puede estar vacío")
            elif len(comportamiento) > 255:
                errores.append("El comportamiento general no puede exceder 255 caracteres")
                
        elif tipo_modificacion == 'anotacion':
            categoria = modificaciones.get('categoria', '').strip()
            detalle = modificaciones.get('detalle', '').strip()
            
            if not categoria:
                errores.append("La categoría de la anotación no puede estar vacía")
            elif len(categoria) > 50:
                errores.append("La categoría no puede exceder 50 caracteres")
            
            if not detalle:
                errores.append("El detalle de la anotación no puede estar vacío")
            elif len(detalle) > 200:
                errores.append("El detalle no puede exceder 200 caracteres")
        
        # PASO 11.4: Resultado de validación
        es_valido = len(errores) == 0
        return es_valido, errores
    
    @staticmethod
    def registrar_modificacion(
        observador_id: int,
        tipo_modificacion: str,
        modificaciones: Dict,
        usuario_id: int
    ) -> bool:
        """
        PASO 13: Registrar modificaciones en BD
        
        Inserta nueva anotación o actualiza comportamiento en el observador.
        Guarda:
        - estudiante_id (desde observador)
        - tipo de modificación
        - contenido
        - fecha (automática)
        - usuario que registra
        
        Args:
            observador_id: ID del observador
            tipo_modificacion: 'comportamiento' o 'anotacion'
            modificaciones: Datos validados a guardar
            usuario_id: ID del director de grupo que hace el cambio
            
        Returns:
            bool: True si se registró exitosamente
            
        Raises:
            ValueError: Si ocurre un error en el registro
        """
        session = SessionLocal()
        try:
            if tipo_modificacion == 'comportamiento':
                # Actualizar comportamiento general del observador
                query_actualizar = text("""
                    UPDATE observador
                    SET comportamiento_general = :comportamiento
                    WHERE id_observador = :observador_id
                """)
                
                session.execute(
                    query_actualizar,
                    {
                        "comportamiento": modificaciones['comportamiento_general'],
                        "observador_id": observador_id
                    }
                )
                
            elif tipo_modificacion == 'anotacion':
                # Insertar nueva anotación
                # Primero obtener el id_profesor del usuario (si es director de grupo)
                query_profesor = text("""
                    SELECT id_profesor
                    FROM profesor
                    WHERE id_usuario = :usuario_id
                """)
                
                resultado_profesor = session.execute(
                    query_profesor,
                    {"usuario_id": usuario_id}
                ).fetchone()
                
                id_profesor = resultado_profesor.id_profesor if resultado_profesor else None
                
                query_insertar = text("""
                    INSERT INTO anotacion (
                        id_observador,
                        id_profesor_autor,
                        categoria,
                        detalle,
                        fecha_registro
                    ) VALUES (
                        :observador_id,
                        :id_profesor,
                        :categoria,
                        :detalle,
                        CURRENT_TIMESTAMP
                    )
                """)
                
                session.execute(
                    query_insertar,
                    {
                        "observador_id": observador_id,
                        "id_profesor": id_profesor,
                        "categoria": modificaciones['categoria'],
                        "detalle": modificaciones['detalle']
                    }
                )
            
            session.commit()
            return True
            
        except Exception as e:
            session.rollback()
            raise ValueError(f"Error al registrar modificación: {str(e)}")
        finally:
            session.close()
