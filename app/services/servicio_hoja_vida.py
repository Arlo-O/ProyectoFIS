"""
Servicio para gestión de Hojas de Vida Académica
Implementa CU-19: Crear hoja de vida del estudiante

Flujo del Caso de Uso:
1. Administrador llega después de admitir al estudiante (CU-18)
2. Sistema carga datos del estudiante admitido
3. Sistema carga formato base de la Hoja de Vida
4. Sistema llena automáticamente con datos básicos existentes
5. Administrador visualiza datos faltantes
6. Administrador digita datos faltantes
7. Sistema inicializa contador de intentos (0)
8. Administrador confirma
9. Sistema valida formato
10. Si correcto: guardar (paso 15-18)
    Si incorrecto: incrementar contador (paso 11-14)
"""

from typing import Tuple, Dict, List, Optional
from datetime import datetime
from sqlalchemy import text
from app.data.db import SessionLocal


class ServicioHojaVida:
    """
    Servicio para la creación y gestión de Hojas de Vida Académica.
    Implementa el CU-19 según el diagrama de actividades.
    """
    
    # PASO 7: Límite de intentos permitidos
    LIMITE_INTENTOS = 3
    
    def __init__(self):
        """Inicializa el servicio de hoja de vida"""
        self.session = None
        # PASO 7: Contador de intentos por sesión (puede ser por estudiante)
        self.contadores_intentos = {}
    
    def cargar_datos_estudiante_admitido(self, id_aspirante: int) -> Tuple[bool, Optional[Dict], str]:
        """
        PASO 2: Cargar automáticamente datos del estudiante admitido desde el datastore.
        
        Args:
            id_aspirante: ID del aspirante que fue admitido
            
        Returns:
            Tuple[bool, Dict, str]: (éxito, datos_estudiante, mensaje)
        """
        session = SessionLocal()
        
        try:
            # Verificar que el aspirante fue admitido
            query_aspirante = text("""
                SELECT 
                    a.id_aspirante,
                    a.grado_solicitado,
                    a.estado_proceso,
                    p.primer_nombre,
                    p.segundo_nombre,
                    p.primer_apellido,
                    p.segundo_apellido,
                    p.tipo_identificacion,
                    p.numero_identificacion,
                    p.fecha_nacimiento,
                    p.genero,
                    p.direccion,
                    p.telefono
                FROM aspirante a
                INNER JOIN persona p ON a.id_aspirante = p.id_persona
                WHERE a.id_aspirante = :id_aspirante
            """)
            
            resultado = session.execute(query_aspirante, {"id_aspirante": id_aspirante}).fetchone()
            
            if not resultado:
                return False, None, f"No se encontró el aspirante con ID {id_aspirante}"
            
            # Validar que el aspirante esté admitido
            if resultado.estado_proceso != "admitido":
                return False, None, f"El aspirante no está admitido. Estado actual: {resultado.estado_proceso}"
            
            # PASO 2: Construir datos disponibles
            datos_estudiante = {
                "id_aspirante": resultado.id_aspirante,
                "nombre_completo": f"{resultado.primer_nombre or ''} {resultado.segundo_nombre or ''} {resultado.primer_apellido or ''} {resultado.segundo_apellido or ''}".strip(),
                "primer_nombre": resultado.primer_nombre,
                "segundo_nombre": resultado.segundo_nombre,
                "primer_apellido": resultado.primer_apellido,
                "segundo_apellido": resultado.segundo_apellido,
                "tipo_identificacion": resultado.tipo_identificacion,
                "numero_identificacion": resultado.numero_identificacion,
                "fecha_nacimiento": resultado.fecha_nacimiento,
                "genero": resultado.genero,
                "direccion": resultado.direccion,
                "telefono": resultado.telefono,
                "grado_solicitado": resultado.grado_solicitado
            }
            
            return True, datos_estudiante, "Datos cargados exitosamente"
            
        except Exception as e:
            import traceback
            print(f"Error al cargar datos del estudiante: {e}")
            print(traceback.format_exc())
            return False, None, f"Error al cargar datos: {str(e)}"
        
        finally:
            session.close()
    
    def obtener_formato_base_hoja_vida(self) -> Dict:
        """
        PASO 3: Cargar el formato base de la Hoja de Vida Académica.
        
        Returns:
            Dict: Estructura del formato con campos requeridos
        """
        return {
            "campos_automaticos": {
                "descripcion": "Estos campos se llenan automáticamente con datos del aspirante",
                "campos": [
                    "nombre_completo",
                    "tipo_identificacion",
                    "numero_identificacion",
                    "fecha_nacimiento",
                    "genero",
                    "grado_solicitado"
                ]
            },
            "campos_faltantes": {
                "descripcion": "Estos campos deben ser diligenciados por el administrador",
                "campos_obligatorios": {
                    "estado_salud": {
                        "tipo": "texto",
                        "descripcion": "Estado general de salud del estudiante",
                        "validacion": "no_vacio"
                    },
                    "codigo_matricula": {
                        "tipo": "texto",
                        "descripcion": "Código único de matrícula del estudiante",
                        "validacion": "alfanumerico",
                        "patron": "^[A-Z0-9]{6,10}$"
                    }
                },
                "campos_opcionales": {
                    "alergias": {
                        "tipo": "lista",
                        "descripcion": "Lista de alergias conocidas"
                    },
                    "tratamientos": {
                        "tipo": "lista",
                        "descripcion": "Tratamientos médicos actuales"
                    },
                    "necesidades_educativas": {
                        "tipo": "lista",
                        "descripcion": "Necesidades educativas especiales"
                    }
                }
            }
        }
    
    def inicializar_contador_intentos(self, id_aspirante: int) -> int:
        """
        PASO 7: Inicializar el contador de intentos en 0.
        
        Args:
            id_aspirante: ID del aspirante
            
        Returns:
            int: Contador inicializado en 0
        """
        self.contadores_intentos[id_aspirante] = 0
        return 0
    
    def incrementar_contador(self, id_aspirante: int) -> int:
        """
        PASO 11: Incrementar el contador de intentos.
        
        Args:
            id_aspirante: ID del aspirante
            
        Returns:
            int: Valor actual del contador
        """
        if id_aspirante not in self.contadores_intentos:
            self.contadores_intentos[id_aspirante] = 0
        
        self.contadores_intentos[id_aspirante] += 1
        return self.contadores_intentos[id_aspirante]
    
    def obtener_contador(self, id_aspirante: int) -> int:
        """
        Obtiene el valor actual del contador de intentos.
        
        Args:
            id_aspirante: ID del aspirante
            
        Returns:
            int: Valor actual del contador
        """
        return self.contadores_intentos.get(id_aspirante, 0)
    
    def validar_formato_datos(self, datos_faltantes: Dict) -> Tuple[bool, List[str], Dict[str, str]]:
        """
        PASO 9: Validar formato de los datos ingresados.
        
        9.1 Verificar que todos los campos obligatorios estén llenos
        9.2 Validar formato de los datos
        9.3 Validar consistencia de la información
        9.4 Registrar lista de campos con error
        
        Args:
            datos_faltantes: Diccionario con los datos ingresados
            
        Returns:
            Tuple[bool, List[str], Dict[str, str]]: 
                (formato_correcto, lista_campos_error, diccionario_errores_detallados)
        """
        campos_error = []
        errores_detallados = {}
        
        # PASO 9.1: Verificar campos obligatorios
        if not datos_faltantes.get("estado_salud") or not datos_faltantes.get("estado_salud").strip():
            campos_error.append("estado_salud")
            errores_detallados["estado_salud"] = "El estado de salud es obligatorio"
        
        if not datos_faltantes.get("codigo_matricula") or not datos_faltantes.get("codigo_matricula").strip():
            campos_error.append("codigo_matricula")
            errores_detallados["codigo_matricula"] = "El código de matrícula es obligatorio"
        
        # PASO 9.2: Validar formato de código de matrícula
        if datos_faltantes.get("codigo_matricula"):
            codigo = datos_faltantes["codigo_matricula"].strip()
            if len(codigo) < 6 or len(codigo) > 10:
                campos_error.append("codigo_matricula")
                errores_detallados["codigo_matricula"] = "El código debe tener entre 6 y 10 caracteres"
            elif not codigo.isalnum():
                campos_error.append("codigo_matricula")
                errores_detallados["codigo_matricula"] = "El código solo puede contener letras y números"
        
        # PASO 9.3: Validar consistencia - estado de salud no debe ser solo espacios
        if datos_faltantes.get("estado_salud"):
            estado = datos_faltantes["estado_salud"].strip()
            if len(estado) < 3:
                campos_error.append("estado_salud")
                errores_detallados["estado_salud"] = "El estado de salud debe tener al menos 3 caracteres"
        
        # PASO 9.4: Determinar si el formato es correcto
        formato_correcto = len(campos_error) == 0
        
        return formato_correcto, campos_error, errores_detallados
    
    def crear_estudiante_y_hoja_vida(self, id_aspirante: int, datos_faltantes: Dict, 
                                      id_usuario_creador: int) -> Tuple[bool, str]:
        """
        PASO 15: Guardar la Hoja de Vida en el datastore.
        
        - Crear registro de Estudiante a partir del Aspirante
        - Crear HojaVidaAcademica asociada
        - Guardar fecha_creación y usuario_creador
        
        Args:
            id_aspirante: ID del aspirante admitido
            datos_faltantes: Datos diligenciados por el administrador
            id_usuario_creador: ID del administrador que crea la hoja de vida
            
        Returns:
            Tuple[bool, str]: (éxito, mensaje)
        """
        session = SessionLocal()
        
        try:
            # Primero verificar que el aspirante existe y está admitido
            query_verificar = text("""
                SELECT id_aspirante, grado_solicitado, estado_proceso
                FROM aspirante
                WHERE id_aspirante = :id_aspirante
            """)
            
            aspirante = session.execute(query_verificar, {"id_aspirante": id_aspirante}).fetchone()
            
            if not aspirante:
                return False, f"No se encontró el aspirante con ID {id_aspirante}"
            
            if aspirante.estado_proceso != "admitido":
                return False, f"El aspirante debe estar admitido. Estado actual: {aspirante.estado_proceso}"
            
            # Verificar que no exista ya un estudiante con ese id_persona
            query_verificar_estudiante = text("""
                SELECT id_estudiante
                FROM estudiante
                WHERE id_estudiante = :id_persona
            """)
            
            estudiante_existe = session.execute(
                query_verificar_estudiante, 
                {"id_persona": id_aspirante}
            ).fetchone()
            
            if estudiante_existe:
                return False, "Ya existe un estudiante registrado para este aspirante"
            
            # PASO 15: Crear registro de Estudiante
            codigo_matricula = datos_faltantes.get("codigo_matricula", "").strip()
            
            query_crear_estudiante = text("""
                INSERT INTO estudiante (
                    id_estudiante, codigo_matricula, fecha_ingreso, grado_actual
                ) VALUES (
                    :id_persona, :codigo_matricula, CURRENT_TIMESTAMP, :grado_actual
                )
            """)
            
            session.execute(query_crear_estudiante, {
                "id_persona": id_aspirante,
                "codigo_matricula": codigo_matricula,
                "grado_actual": aspirante.grado_solicitado
            })
            
            # PASO 15: Crear Hoja de Vida Académica
            # Preparar datos JSON para campos opcionales
            alergias_lista = datos_faltantes.get("alergias", [])
            tratamientos_lista = datos_faltantes.get("tratamientos", [])
            necesidades_lista = datos_faltantes.get("necesidades_educativas", [])
            
            # Convertir listas a diccionarios JSON
            alergias_json = {"lista": alergias_lista} if isinstance(alergias_lista, list) else {}
            tratamientos_json = {"lista": tratamientos_lista} if isinstance(tratamientos_lista, list) else {}
            necesidades_json = {"lista": necesidades_lista} if isinstance(necesidades_lista, list) else {}
            
            query_crear_hoja_vida = text("""
                INSERT INTO hoja_vida (
                    id_estudiante, estado_salud, alergias, tratamientos, 
                    necesidades_educativas, fecha_creacion, usuario_creador
                ) VALUES (
                    :id_estudiante, :estado_salud, :alergias::jsonb, :tratamientos::jsonb,
                    :necesidades_educativas::jsonb, CURRENT_TIMESTAMP, :usuario_creador
                )
            """)
            
            import json
            session.execute(query_crear_hoja_vida, {
                "id_estudiante": id_aspirante,
                "estado_salud": datos_faltantes.get("estado_salud", "").strip(),
                "alergias": json.dumps(alergias_json),
                "tratamientos": json.dumps(tratamientos_json),
                "necesidades_educativas": json.dumps(necesidades_json),
                "usuario_creador": id_usuario_creador
            })
            
            session.commit()
            
            # Limpiar contador de intentos
            if id_aspirante in self.contadores_intentos:
                del self.contadores_intentos[id_aspirante]
            
            return True, "Hoja de vida creada exitosamente"
            
        except Exception as e:
            session.rollback()
            import traceback
            print(f"Error al crear hoja de vida: {e}")
            print(traceback.format_exc())
            return False, f"Error al crear hoja de vida: {str(e)}"
        
        finally:
            session.close()
    
    # ============================================================================
    # CU-25: VISUALIZAR/EDITAR HOJA DE VIDA DEL ESTUDIANTE
    # ============================================================================
    
    @staticmethod
    def cargar_hoja_vida_estudiante(estudiante_id: int) -> Dict:
        """
        CU-25 PASO 3: Cargar hoja de vida del estudiante
        3.1 Consultar datos en el datastore HojaDeVida
        3.2 Consultar datos del estudiante
        
        Args:
            estudiante_id: ID del estudiante
            
        Returns:
            Dict con datos del estudiante y su hoja de vida
            
        Raises:
            ValueError: Si el estudiante no existe o no tiene hoja de vida
        """
        session = SessionLocal()
        try:
            # PASO 3.2: Consultar datos del estudiante
            query_estudiante = text("""
                SELECT 
                    e.id_estudiante,
                    e.codigo_estudiante,
                    p.primer_nombre,
                    p.segundo_nombre,
                    p.primer_apellido,
                    p.segundo_apellido,
                    p.tipo_identificacion,
                    p.numero_identificacion,
                    p.fecha_nacimiento,
                    p.genero,
                    p.direccion,
                    p.telefono
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
            
            # PASO 3.1: Consultar hoja de vida
            query_hoja_vida = text("""
                SELECT 
                    id_hoja_vida,
                    id_estudiante,
                    estado_salud,
                    alergias,
                    tratamientos,
                    necesidades_educativas,
                    fecha_creacion,
                    usuario_creador
                FROM hoja_vida
                WHERE id_estudiante = :estudiante_id
            """)
            
            resultado_hoja_vida = session.execute(
                query_hoja_vida,
                {"estudiante_id": estudiante_id}
            ).fetchone()
            
            if not resultado_hoja_vida:
                raise ValueError(f"El estudiante {estudiante_id} no tiene hoja de vida creada")
            
            return {
                "estudiante": {
                    "id": resultado_estudiante.id_estudiante,
                    "codigo": resultado_estudiante.codigo_estudiante,
                    "primer_nombre": resultado_estudiante.primer_nombre or "",
                    "segundo_nombre": resultado_estudiante.segundo_nombre or "",
                    "primer_apellido": resultado_estudiante.primer_apellido or "",
                    "segundo_apellido": resultado_estudiante.segundo_apellido or "",
                    "tipo_identificacion": resultado_estudiante.tipo_identificacion or "",
                    "numero_identificacion": resultado_estudiante.numero_identificacion or "",
                    "fecha_nacimiento": resultado_estudiante.fecha_nacimiento,
                    "genero": resultado_estudiante.genero or "",
                    "direccion": resultado_estudiante.direccion or "",
                    "telefono": resultado_estudiante.telefono or ""
                },
                "hoja_vida": {
                    "id": resultado_hoja_vida.id_hoja_vida,
                    "estado_salud": resultado_hoja_vida.estado_salud or "",
                    "alergias": resultado_hoja_vida.alergias or {},
                    "tratamientos": resultado_hoja_vida.tratamientos or {},
                    "necesidades_educativas": resultado_hoja_vida.necesidades_educativas or {},
                    "fecha_creacion": resultado_hoja_vida.fecha_creacion,
                    "usuario_creador": resultado_hoja_vida.usuario_creador
                }
            }
            
        finally:
            session.close()
    
    @staticmethod
    def validar_modificaciones_hoja_vida(modificaciones: Dict) -> Tuple[bool, List[str]]:
        """
        CU-25 PASO 10: Validar modificaciones
        10.1 Verificar que todos los campos editados tengan formato válido
        10.2 Verificar que solo se hayan modificado campos permitidos
        10.3 Validar fechas, números, textos, longitud, coherencia
        10.4 Si hay errores, generar lista detallada de errores
        
        Args:
            modificaciones: Diccionario con los campos a modificar
            
        Returns:
            Tuple[bool, List[str]]: (es_valido, lista_de_errores)
        """
        errores = []
        
        # PASO 10.2: Campos permitidos para edición
        CAMPOS_PERMITIDOS = {
            'estado_salud',
            'alergias',
            'tratamientos',
            'necesidades_educativas'
        }
        
        # Verificar campos no permitidos
        campos_enviados = set(modificaciones.keys())
        campos_no_permitidos = campos_enviados - CAMPOS_PERMITIDOS
        
        if campos_no_permitidos:
            errores.append(
                f"Campos no permitidos para edición: {', '.join(campos_no_permitidos)}"
            )
        
        # PASO 10.1 y 10.3: Validar formato de cada campo
        
        # Validar estado_salud
        if 'estado_salud' in modificaciones:
            estado_salud = modificaciones['estado_salud']
            if estado_salud and not isinstance(estado_salud, str):
                errores.append("Estado de salud debe ser texto")
            elif estado_salud and len(estado_salud) > 100:
                errores.append("Estado de salud no puede exceder 100 caracteres")
        
        # Validar alergias (debe ser dict/JSON)
        if 'alergias' in modificaciones:
            alergias = modificaciones['alergias']
            if alergias is not None and not isinstance(alergias, dict):
                errores.append("Alergias debe ser un diccionario válido")
        
        # Validar tratamientos (debe ser dict/JSON)
        if 'tratamientos' in modificaciones:
            tratamientos = modificaciones['tratamientos']
            if tratamientos is not None and not isinstance(tratamientos, dict):
                errores.append("Tratamientos debe ser un diccionario válido")
        
        # Validar necesidades_educativas (debe ser dict/JSON)
        if 'necesidades_educativas' in modificaciones:
            necesidades = modificaciones['necesidades_educativas']
            if necesidades is not None and not isinstance(necesidades, dict):
                errores.append("Necesidades educativas debe ser un diccionario válido")
        
        # PASO 10.4: Resultado
        es_valido = len(errores) == 0
        return es_valido, errores
    
    @staticmethod
    def actualizar_hoja_vida(hoja_vida_id: int, modificaciones: Dict, usuario_id: int) -> bool:
        """
        CU-25 PASO 12: Registrar modificaciones en BD
        - Actualizar datastore HojaDeVida
        - Guardar campos modificados, fecha_modificación, usuario_modificador
        
        Args:
            hoja_vida_id: ID de la hoja de vida
            modificaciones: Diccionario con campos a actualizar (ya validados)
            usuario_id: ID del director de grupo que modifica
            
        Returns:
            bool: True si se actualizó exitosamente
            
        Raises:
            ValueError: Si ocurre un error en la actualización
        """
        session = SessionLocal()
        try:
            # Construir SET dinámico para campos modificados
            campos_set = []
            params = {"hoja_vida_id": hoja_vida_id, "usuario_id": usuario_id}
            
            if 'estado_salud' in modificaciones:
                campos_set.append("estado_salud = :estado_salud")
                params['estado_salud'] = modificaciones['estado_salud']
            
            if 'alergias' in modificaciones:
                campos_set.append("alergias = :alergias::jsonb")
                import json
                params['alergias'] = json.dumps(modificaciones['alergias'])
            
            if 'tratamientos' in modificaciones:
                campos_set.append("tratamientos = :tratamientos::jsonb")
                import json
                params['tratamientos'] = json.dumps(modificaciones['tratamientos'])
            
            if 'necesidades_educativas' in modificaciones:
                campos_set.append("necesidades_educativas = :necesidades_educativas::jsonb")
                import json
                params['necesidades_educativas'] = json.dumps(modificaciones['necesidades_educativas'])
            
            if not campos_set:
                raise ValueError("No hay campos para actualizar")
            
            # NOTA: No guardamos fecha_modificación ni usuario_modificador porque
            # el usuario indicó "sin auditorías"
            
            query_update = text(f"""
                UPDATE hoja_vida
                SET {', '.join(campos_set)}
                WHERE id_hoja_vida = :hoja_vida_id
            """)
            
            session.execute(query_update, params)
            session.commit()
            return True
            
        except Exception as e:
            session.rollback()
            raise ValueError(f"Error al actualizar hoja de vida: {str(e)}")
        finally:
            session.close()
