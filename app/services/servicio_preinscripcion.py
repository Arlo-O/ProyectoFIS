# 🔧 Servicio de Preinscripción
from typing import Dict, Tuple, List
import json
import os
from datetime import datetime
from pathlib import Path
from ..core.preinscripcion.modelo_preinscripcion import IntentoFallo, FormularioPreinscripcion


class ServicioIntentosFallidos:
    """Servicio para persistir y gestionar intentos fallidos de preinscripción"""
    
    def __init__(self):
        # Crear directorio de almacenamiento si no existe
        self.directorio_datos = Path.home() / ".proyectofis" / "preinscripcion"
        self.directorio_datos.mkdir(parents=True, exist_ok=True)
        self.archivo_intentos = self.directorio_datos / "intentos_fallidos.json"
    
    def obtener_intentos_usuario(self, identificador: str = "usuario_anonimo") -> List[IntentoFallo]:
        """Obtiene todos los intentos fallidos del usuario"""
        if not self.archivo_intentos.exists():
            return []
        
        try:
            with open(self.archivo_intentos, 'r', encoding='utf-8') as f:
                datos = json.load(f)
            
            intentos = [IntentoFallo(**intento) for intento in datos.get(identificador, [])]
            return intentos
        except Exception as e:
            print(f"Error al leer intentos: {e}")
            return []
    
    def contar_intentos_hoy(self, identificador: str = "usuario_anonimo") -> int:
        """Cuenta cuántos intentos fallidos ha habido hoy"""
        intentos = self.obtener_intentos_usuario(identificador)
        hoy = datetime.now().date()
        
        intentos_hoy = [
            i for i in intentos 
            if datetime.fromisoformat(i.fecha_hora).date() == hoy
        ]
        
        return len(intentos_hoy)
    
    def registrar_intento_fallido(self, 
                                  numero_error: int, 
                                  campo_errores: Dict[str, str],
                                  identificador: str = "usuario_anonimo") -> IntentoFallo:
        """Registra un intento fallido"""
        
        intento = IntentoFallo(
            numero_error=numero_error,
            campo_errores=campo_errores
        )
        
        # Leer intentos existentes
        try:
            with open(self.archivo_intentos, 'r', encoding='utf-8') as f:
                datos = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            datos = {}
        
        # Agregar nuevo intento
        if identificador not in datos:
            datos[identificador] = []
        
        datos[identificador].append(intento.to_dict())
        
        # Guardar
        try:
            with open(self.archivo_intentos, 'w', encoding='utf-8') as f:
                json.dump(datos, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error al guardar intento: {e}")
        
        return intento
    
    def limpiar_intentos_usuario(self, identificador: str = "usuario_anonimo"):
        """Limpia los intentos fallidos del usuario actual"""
        try:
            with open(self.archivo_intentos, 'r', encoding='utf-8') as f:
                datos = json.load(f)
            
            if identificador in datos:
                del datos[identificador]
            
            with open(self.archivo_intentos, 'w', encoding='utf-8') as f:
                json.dump(datos, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error al limpiar intentos: {e}")


class ServicioPreinscripcion:
    """Servicio de validación y persistencia de preinscripciones"""
    
    def __init__(self):
        self.servicio_intentos = ServicioIntentosFallidos()
    
    def guardar_preinscripcion(self, formulario: FormularioPreinscripcion) -> Tuple[bool, str]:
        """Guarda una preinscripción completada"""
        try:
            directorio = Path.home() / ".proyectofis" / "preinscripcion"
            directorio.mkdir(parents=True, exist_ok=True)
            
            archivo = directorio / f"preinscripcion_{datetime.now().isoformat().replace(':', '-')}.json"
            
            with open(archivo, 'w', encoding='utf-8') as f:
                json.dump(formulario.to_dict(), f, ensure_ascii=False, indent=2)
            
            return True, "Preinscripción guardada exitosamente"
        except Exception as e:
            return False, f"Error al guardar preinscripción: {str(e)}"
    
    def registrar_preinscripcion_bd(self, datos_formulario: Dict[str, any]) -> Tuple[bool, str]:
        """
        PASO 8 DEL DIAGRAMA: Registrar datos en el datastore
        
        Guarda la información en las tablas:
        - Aspirante
        - Acudiente
        
        Relaciona aspirante con acudiente según modelo.
        Registra fecha de creación.
        
        Args:
            datos_formulario: Diccionario con todos los datos del formulario
        
        Returns:
            Tuple[bool, str]: (éxito, mensaje)
        """
        from app.data.db import SessionLocal
        from app.core.usuarios.aspirante import Aspirante
        from app.core.usuarios.acudiente import Acudiente
        from app.core.usuarios.persona import Persona
        from sqlalchemy import text
        
        session = SessionLocal()
        
        try:
            # PASO 8.1: Guardar Acudiente (primero, porque Aspirante lo referencia)
            
            # Buscar si el acudiente ya existe por número de identificación
            query_acudiente = text("""
                SELECT p.id_persona, a.id_acudiente
                FROM persona p
                JOIN acudiente a ON p.id_persona = a.id_acudiente
                WHERE p.numero_identificacion = :numero_id
            """)
            
            resultado_acudiente = session.execute(
                query_acudiente,
                {"numero_id": datos_formulario['cedula_acudiente']}
            ).fetchone()
            
            if resultado_acudiente:
                # Acudiente ya existe, usar ese ID
                id_acudiente = resultado_acudiente.id_acudiente
            else:
                # Crear nuevo acudiente
                # Obtener nombres y apellidos de los campos separados
                primer_nombre = datos_formulario['primer_nombre_acudiente']
                segundo_nombre = datos_formulario.get('segundo_nombre_acudiente', '')
                primer_apellido = datos_formulario['primer_apellido_acudiente']
                segundo_apellido = datos_formulario.get('segundo_apellido_acudiente', '')
                
                # Insertar en persona
                query_persona_acudiente = text("""
                    INSERT INTO persona (
                        tipo_identificacion, numero_identificacion,
                        primer_nombre, segundo_nombre, primer_apellido, segundo_apellido,
                        genero, direccion, telefono, type
                    ) VALUES (
                        'CC', :numero_id,
                        :primer_nombre, :segundo_nombre, :primer_apellido, :segundo_apellido,
                        'N/A', :direccion, :telefono, 'acudiente'
                    ) RETURNING id_persona
                """)
                
                resultado = session.execute(
                    query_persona_acudiente,
                    {
                        "numero_id": datos_formulario['cedula_acudiente'],
                        "primer_nombre": primer_nombre,
                        "segundo_nombre": segundo_nombre,
                        "primer_apellido": primer_apellido,
                        "segundo_apellido": segundo_apellido,
                        "direccion": datos_formulario['direccion'],
                        "telefono": datos_formulario['telefono']
                    }
                ).fetchone()
                
                id_persona_acudiente = resultado.id_persona
                
                # Insertar en acudiente (solo id_acudiente y parentesco, email ya está en persona)
                query_acudiente_insert = text("""
                    INSERT INTO acudiente (id_acudiente, parentesco)
                    VALUES (:id_persona, :parentesco)
                    RETURNING id_acudiente
                """)
                
                resultado = session.execute(
                    query_acudiente_insert,
                    {
                        "id_persona": id_persona_acudiente,
                        "parentesco": datos_formulario['parentesco']
                    }
                ).fetchone()
                
                id_acudiente = resultado.id_acudiente
            
            # PASO 8.2: Guardar Aspirante
            
            # Obtener nombres y apellidos del estudiante de los campos separados
            primer_nombre = datos_formulario['primer_nombre_estudiante']
            segundo_nombre = datos_formulario.get('segundo_nombre_estudiante', '')
            primer_apellido = datos_formulario['primer_apellido_estudiante']
            segundo_apellido = datos_formulario.get('segundo_apellido_estudiante', '')
            
            # Parsear fecha de nacimiento
            fecha_nacimiento = datetime.strptime(datos_formulario['fecha_nacimiento'], "%d/%m/%Y")
            
            # Insertar en persona
            query_persona_aspirante = text("""
                INSERT INTO persona (
                    tipo_identificacion, numero_identificacion,
                    primer_nombre, segundo_nombre, primer_apellido, segundo_apellido,
                    fecha_nacimiento, genero, direccion, telefono, type
                ) VALUES (
                    :tipo_id, :numero_id,
                    :primer_nombre, :segundo_nombre, :primer_apellido, :segundo_apellido,
                    :fecha_nacimiento, :genero, :direccion, :telefono, 'aspirante'
                ) RETURNING id_persona
            """)
            
            resultado = session.execute(
                query_persona_aspirante,
                {
                    "tipo_id": datos_formulario['tipo_id'],
                    "numero_id": datos_formulario['numero_id'],
                    "primer_nombre": primer_nombre,
                    "segundo_nombre": segundo_nombre,
                    "primer_apellido": primer_apellido,
                    "segundo_apellido": segundo_apellido,
                    "fecha_nacimiento": fecha_nacimiento,
                    "genero": datos_formulario['genero'],
                    "direccion": datos_formulario['direccion'],
                    "telefono": datos_formulario['telefono']
                }
            ).fetchone()
            
            id_persona_aspirante = resultado.id_persona
            
            # Insertar en aspirante (sin id_acudiente, no existe esa columna)
            query_aspirante_insert = text("""
                INSERT INTO aspirante (
                    id_aspirante, grado_solicitado, fecha_solicitud, estado_proceso
                ) VALUES (
                    :id_persona, :grado, CURRENT_TIMESTAMP, 'pendiente'
                ) RETURNING id_aspirante
            """)
            
            resultado = session.execute(
                query_aspirante_insert,
                {
                    "id_persona": id_persona_aspirante,
                    "grado": datos_formulario['grado']
                }
            ).fetchone()
            
            id_aspirante = resultado.id_aspirante
            
            # PASO 8.3: Guardar respuesta del formulario
            query_respuesta = text("""
                INSERT INTO respuesta_form_pre (
                    id_aspirante, fecha_envio, datos_json
                ) VALUES (
                    :id_aspirante, CURRENT_TIMESTAMP, :datos_json
                )
            """)
            
            session.execute(
                query_respuesta,
                {
                    "id_aspirante": id_aspirante,
                    "datos_json": json.dumps(datos_formulario, ensure_ascii=False)
                }
            )
            
            # Confirmar transacción
            session.commit()
            
            return True, "La preinscripción ha sido enviada exitosamente."
            
        except Exception as e:
            session.rollback()
            print(f"Error al registrar preinscripción: {e}")
            import traceback
            traceback.print_exc()
            return False, f"Error al guardar la preinscripción: {str(e)}"
        
        finally:
            session.close()
    
    def obtener_contador_intentos(self, identificador: str = "usuario_anonimo") -> int:
        """Obtiene el número de intentos fallidos hoy"""
        return self.servicio_intentos.contar_intentos_hoy(identificador)
    
    def registrar_error(self, 
                       errores: Dict[str, str],
                       identificador: str = "usuario_anonimo") -> IntentoFallo:
        """Registra un error de validación"""
        contador = self.obtener_contador_intentos(identificador) + 1
        return self.servicio_intentos.registrar_intento_fallido(
            contador, 
            errores, 
            identificador
        )
