# -*- coding: utf-8 -*-
"""
📋 Servicio de Gestión de Usuarios
Responsable de crear, validar y auditar usuarios
"""

import re
import secrets
import string
import bcrypt
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from sqlalchemy.orm import Session
from sqlalchemy import text

class ValidadorUsuario:
    """Valida los datos de un nuevo usuario"""
    
    # Configuración de políticas
    MIN_LONGITUD_CONTRASEÑA = 8
    LONGITUD_CONTRASEÑA = 12
    TIPOS_IDENTIFICACION_VALIDOS = ["CC", "CE", "PA", "TI", "RC"]  # Cédula, Extranjería, Pasaporte, Tarjeta Id, Registro Civil
    CARACTERES_PERMITIDOS = set(string.ascii_letters + string.digits + "_.-")
    
    @staticmethod
    def validar_identificador(numero_id: str, tipo_id: str) -> Tuple[bool, str]:
        """Valida formato y estructura del identificador"""
        if not numero_id or not numero_id.strip():
            return False, "El identificador no puede estar vacío"
        
        numero_id = numero_id.strip()
        
        # Validar tipo de identificación
        if tipo_id not in ValidadorUsuario.TIPOS_IDENTIFICACION_VALIDOS:
            return False, f"Tipo de identificación inválido. Válidos: {', '.join(ValidadorUsuario.TIPOS_IDENTIFICACION_VALIDOS)}"
        
        # Validar longitud según tipo
        if tipo_id == "CC":  # Cédula Colombiana: 5-11 dígitos
            if not numero_id.isdigit():
                return False, "La cédula debe contener solo dígitos"
            if len(numero_id) < 5 or len(numero_id) > 11:
                return False, f"La cédula debe tener entre 5 y 11 dígitos (recibido: {len(numero_id)})"
        
        elif tipo_id == "CE":  # Cédula Extranjería: 5-11 dígitos
            if not numero_id.isdigit():
                return False, "La cédula de extranjería debe contener solo dígitos"
            if len(numero_id) < 5 or len(numero_id) > 11:
                return False, f"La cédula de extranjería debe tener entre 5 y 11 dígitos"
        
        elif tipo_id in ["PA", "RC"]:  # Pasaporte, Registro Civil
            if len(numero_id) < 4 or len(numero_id) > 20:
                return False, f"{tipo_id} debe tener entre 4 y 20 caracteres"
        
        return True, ""
    
    @staticmethod
    def validar_nombre(nombre: str, campo: str = "nombre") -> Tuple[bool, str]:
        """Valida nombres (no vacíos, no excesivamente largos)"""
        if not nombre or not nombre.strip():
            return False, f"El {campo} no puede estar vacío"
        
        nombre = nombre.strip()
        if len(nombre) > 50:
            return False, f"El {campo} no puede exceder 50 caracteres"
        
        if len(nombre) < 2:
            return False, f"El {campo} debe tener al menos 2 caracteres"
        
        return True, ""
    
    @staticmethod
    def validar_email(email: str) -> Tuple[bool, str]:
        """Valida formato de email"""
        if not email or not email.strip():
            return False, "El correo electrónico no puede estar vacío"
        
        email = email.strip().lower()
        
        # Patrón regex para validar email
        patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(patron, email):
            return False, "El formato del correo electrónico es inválido"
        
        return True, ""
    
    @staticmethod
    def validar_fecha_nacimiento(fecha_str: str) -> Tuple[bool, str, Optional[datetime]]:
        """Valida fecha de nacimiento (formato YYYY-MM-DD)"""
        if not fecha_str:
            return True, "", None  # Opcional
        
        try:
            fecha = datetime.strptime(fecha_str, "%Y-%m-%d")
            hoy = datetime.now()
            
            # Verificar que no sea fecha futura
            if fecha > hoy:
                return False, "La fecha de nacimiento no puede ser en el futuro", None
            
            # Verificar edad mínima (si es estudiante: 5 años, si es acudiente: 18 años, etc.)
            edad = (hoy - fecha).days // 365
            if edad < 5:
                return False, "La fecha de nacimiento indica una edad inferior a 5 años", None
            
            return True, "", fecha
        except ValueError:
            return False, "Formato de fecha inválido. Use YYYY-MM-DD (ej: 1990-05-15)", None
    
    @staticmethod
    def validar_telefono(telefono: str) -> Tuple[bool, str]:
        """Valida teléfono (opcional, solo dígitos y caracteres permitidos)"""
        if not telefono:
            return True, ""  # Opcional
        
        telefono = telefono.strip()
        if len(telefono) < 7 or len(telefono) > 20:
            return False, "El teléfono debe tener entre 7 y 20 caracteres"
        
        # Solo permitir dígitos, guiones, espacios y +
        if not re.match(r'^[\d\-\s\+]+$', telefono):
            return False, "El teléfono solo puede contener dígitos, guiones, espacios y +"
        
        return True, ""
    
    @staticmethod
    def validar_especialidad(especialidad: str) -> Tuple[bool, str]:
        """Valida especialidad para profesores"""
        if not especialidad or not especialidad.strip():
            return False, "La especialidad no puede estar vacía para profesores"
        
        especialidad = especialidad.strip()
        if len(especialidad) > 100:
            return False, "La especialidad no puede exceder 100 caracteres"
        
        return True, ""
    
    @staticmethod
    def validar_rol(rol_nombre: str, roles_disponibles: List[str]) -> Tuple[bool, str]:
        """Valida que el rol exista y sea válido"""
        if not rol_nombre or not rol_nombre.strip():
            return False, "El rol no puede estar vacío"
        
        if rol_nombre not in roles_disponibles:
            return False, f"Rol inválido. Roles disponibles: {', '.join(roles_disponibles)}"
        
        return True, ""


class GeneradorContraseña:
    """Genera contraseñas seguras automáticamente"""
    
    LONGITUD_DEFECTO = 12
    
    @staticmethod
    def generar() -> str:
        """Genera contraseña segura de 12 caracteres"""
        # Asegurar que contiene mayúscula, minúscula, dígito y carácter especial
        mayuscula = secrets.choice(string.ascii_uppercase)
        minuscula = secrets.choice(string.ascii_lowercase)
        digito = secrets.choice(string.digits)
        especial = secrets.choice("!@#$%^&*-_=+")
        
        # Generar caracteres restantes
        todos_caracteres = string.ascii_letters + string.digits + "!@#$%^&*-_=+"
        restantes = [secrets.choice(todos_caracteres) for _ in range(GeneradorContraseña.LONGITUD_DEFECTO - 4)]
        
        # Combinar y mezclar
        contraseña = [mayuscula, minuscula, digito, especial] + restantes
        secrets.SystemRandom().shuffle(contraseña)
        
        return ''.join(contraseña)


class ServicioUsuario:
    """Servicio principal para gestión de usuarios"""
    
    # Mapa de roles y los tipos de persona que requieren
    MAPA_ROLES_PERSONA = {
        "Profesor": "Profesor",
        "Acudiente": "Acudiente",
        "Administrador": "Administrador",
        "Directivo": "Directivo",
        "Estudiante": "Estudiante"  # No tiene Usuario
    }
    
    def __init__(self, session: Session):
        self.session = session
        self.validador = ValidadorUsuario()
    
    def obtener_roles_disponibles(self, usuario_actual_rol: str = None) -> List[str]:
        """
        Obtiene lista de roles que el usuario actual puede crear
        Administrador puede crear: Profesor, Acudiente, Directivo, Estudiante
        Directivo puede crear: Profesor, Acudiente, Estudiante
        """
        if usuario_actual_rol == "Administrador":
            return ["Profesor", "Acudiente", "Directivo", "Estudiante"]
        elif usuario_actual_rol == "Directivo":
            return ["Profesor", "Acudiente", "Estudiante"]
        else:
            return []
    
    def verificar_unicidad_identificador(self, numero_id: str, tipo_id: str) -> Tuple[bool, str]:
        """Verifica que el identificador no exista ya en la BD"""
        try:
            existe = self.session.execute(text("""
                SELECT COUNT(*) FROM persona WHERE numero_identificacion = :numero_id
            """), {"numero_id": numero_id}).scalar()
            
            if existe:
                return False, f"Ya existe una persona con identificación {tipo_id}: {numero_id}"
            
            return True, ""
        except Exception as e:
            return False, f"Error al verificar unicidad: {str(e)}"
    
    def verificar_unicidad_email(self, email: str) -> Tuple[bool, str]:
        """Verifica que el email no exista ya en la BD"""
        try:
            existe = self.session.execute(text("""
                SELECT COUNT(*) FROM usuario WHERE correo_electronico = :email
            """), {"email": email.lower()}).scalar()
            
            if existe:
                return False, f"Ya existe un usuario con el correo: {email}"
            
            return True, ""
        except Exception as e:
            return False, f"Error al verificar unicidad de email: {str(e)}"
    
    def validar_datos_usuario(self, datos: Dict) -> Tuple[bool, List[str]]:
        """
        Valida todos los datos antes de crear usuario
        Retorna: (es_válido, lista_de_errores)
        """
        errores = []
        
        # Validar identificación
        valido, msg = self.validador.validar_identificador(
            datos.get("numero_identificacion", ""),
            datos.get("tipo_identificacion", "")
        )
        if not valido:
            errores.append(msg)
        else:
            # Verificar unicidad
            valido, msg = self.verificar_unicidad_identificador(
                datos.get("numero_identificacion", "").strip(),
                datos.get("tipo_identificacion", "")
            )
            if not valido:
                errores.append(msg)
        
        # Validar nombres
        valido, msg = self.validador.validar_nombre(datos.get("primer_nombre", ""), "primer nombre")
        if not valido:
            errores.append(msg)
        
        valido, msg = self.validador.validar_nombre(datos.get("primer_apellido", ""), "primer apellido")
        if not valido:
            errores.append(msg)
        
        # Validar nombres opcionales
        if datos.get("segundo_nombre"):
            valido, msg = self.validador.validar_nombre(datos.get("segundo_nombre", ""), "segundo nombre")
            if not valido:
                errores.append(msg)
        
        if datos.get("segundo_apellido"):
            valido, msg = self.validador.validar_nombre(datos.get("segundo_apellido", ""), "segundo apellido")
            if not valido:
                errores.append(msg)
        
        # Validar email (si requiere Usuario)
        rol = datos.get("rol", "")
        if rol != "Estudiante":
            valido, msg = self.validador.validar_email(datos.get("correo_electronico", ""))
            if not valido:
                errores.append(msg)
            else:
                # Verificar unicidad
                valido, msg = self.verificar_unicidad_email(datos.get("correo_electronico", "").strip())
                if not valido:
                    errores.append(msg)
        
        # Validar fecha nacimiento (opcional)
        if datos.get("fecha_nacimiento"):
            valido, msg, _ = self.validador.validar_fecha_nacimiento(datos.get("fecha_nacimiento"))
            if not valido:
                errores.append(msg)
        
        # Validar teléfono (opcional)
        if datos.get("telefono"):
            valido, msg = self.validador.validar_telefono(datos.get("telefono"))
            if not valido:
                errores.append(msg)
        
        # Validar especialidad si es profesor
        if rol == "Profesor":
            valido, msg = self.validador.validar_especialidad(datos.get("especialidad", ""))
            if not valido:
                errores.append(msg)
        
        # Validar rol
        roles_disponibles = self.obtener_roles_disponibles(datos.get("rol_usuario_actual", "Administrador"))
        valido, msg = self.validador.validar_rol(rol, roles_disponibles)
        if not valido:
            errores.append(msg)
        
        return len(errores) == 0, errores
    
    def crear_usuario(self, datos: Dict, usuario_admin_id: int = None) -> Tuple[bool, str, Optional[Dict]]:
        """
        Crea un nuevo usuario y su persona asociada
        Retorna: (éxito, mensaje, datos_usuario_creado)
        """
        try:
            # 1. Validar datos
            valido, errores = self.validar_datos_usuario(datos)
            if not valido:
                mensaje_error = "Errores de validación:\n" + "\n".join([f"• {e}" for e in errores])
                return False, mensaje_error, None
            
            # 2. Generar contraseña automáticamente
            contraseña_generada = GeneradorContraseña.generar()
            
            # 3. Crear registro de persona primero
            rol = datos.get("rol", "").strip()
            tipo_persona = self.MAPA_ROLES_PERSONA.get(rol, "Persona")
            
            # Construir query INSERT para persona
            numero_id = datos.get("numero_identificacion", "").strip()
            tipo_id = datos.get("tipo_identificacion", "").strip()
            primer_nombre = datos.get("primer_nombre", "").strip()
            segundo_nombre = datos.get("segundo_nombre", "").strip() or None
            primer_apellido = datos.get("primer_apellido", "").strip()
            segundo_apellido = datos.get("segundo_apellido", "").strip() or None
            
            self.session.execute(text("""
                INSERT INTO persona (
                    type, tipo_identificacion, numero_identificacion,
                    primer_nombre, segundo_nombre, primer_apellido, segundo_apellido,
                    fecha_nacimiento, genero, direccion, telefono
                ) VALUES (
                    :type, :tipo_id, :numero_id,
                    :primer_nom, :segundo_nom, :primer_ape, :segundo_ape,
                    :fecha_nac, :genero, :direccion, :telefono
                )
            """), {
                "type": tipo_persona,
                "tipo_id": tipo_id,
                "numero_id": numero_id,
                "primer_nom": primer_nombre,
                "segundo_nom": segundo_nombre,
                "primer_ape": primer_apellido,
                "segundo_ape": segundo_apellido,
                "fecha_nac": datos.get("fecha_nacimiento") or None,
                "genero": datos.get("genero") or None,
                "direccion": datos.get("direccion") or None,
                "telefono": datos.get("telefono") or None
            })
            
            # Obtener ID de la persona creada
            persona_result = self.session.execute(text("""
                SELECT id_persona FROM persona WHERE numero_identificacion = :numero_id
            """), {"numero_id": numero_id}).fetchone()
            
            id_persona = persona_result[0] if persona_result else None
            
            if not id_persona:
                return False, "Error al crear el registro de persona", None
            
            # 4. Si no es estudiante, crear usuario
            id_usuario = None
            if rol != "Estudiante":
                email = datos.get("correo_electronico", "").strip().lower()
                
                # Hash de contraseña usando bcrypt
                contraseña_hash = bcrypt.hashpw(
                    contraseña_generada.encode('utf-8'),
                    bcrypt.gensalt()
                ).decode('utf-8')
                
                # Obtener ID del rol
                rol_result = self.session.execute(text("""
                    SELECT id_rol FROM rol WHERE nombre_rol = :nombre
                """), {"nombre": rol}).fetchone()
                
                id_rol = rol_result[0] if rol_result else None
                
                if not id_rol:
                    return False, f"El rol '{rol}' no existe en la BD", None
                
                self.session.execute(text("""
                    INSERT INTO usuario (correo_electronico, contrasena, id_rol, activo, fecha_creacion)
                    VALUES (:email, :contraseña, :id_rol, true, NOW())
                """), {
                    "email": email,
                    "contraseña": contraseña_hash,
                    "id_rol": id_rol
                })
                
                # Obtener ID del usuario creado
                usuario_result = self.session.execute(text("""
                    SELECT id_usuario FROM usuario WHERE correo_electronico = :email
                """), {"email": email}).fetchone()
                
                id_usuario = usuario_result[0] if usuario_result else None
            
            # 5. Registrar en tabla específica del tipo (Profesor, Acudiente, etc.)
            if rol == "Profesor":
                especialidad = datos.get("especialidad", "").strip()
                self.session.execute(text("""
                    INSERT INTO profesor (id_persona, especialidad, es_director_grupo)
                    VALUES (:id_persona, :especialidad, false)
                """), {"id_persona": id_persona, "especialidad": especialidad})
                
                # Asociar usuario a profesor
                if id_usuario:
                    self.session.execute(text("""
                        UPDATE usuario SET id_profesor = :id_persona WHERE id_usuario = :id_usuario
                    """), {"id_persona": id_persona, "id_usuario": id_usuario})
            
            elif rol == "Acudiente":
                self.session.execute(text("""
                    INSERT INTO acudiente (id_persona)
                    VALUES (:id_persona)
                """), {"id_persona": id_persona})
                
                if id_usuario:
                    self.session.execute(text("""
                        UPDATE usuario SET id_acudiente = :id_persona WHERE id_usuario = :id_usuario
                    """), {"id_persona": id_persona, "id_usuario": id_usuario})
            
            elif rol == "Directivo":
                self.session.execute(text("""
                    INSERT INTO directivo (id_persona)
                    VALUES (:id_persona)
                """), {"id_persona": id_persona})
                
                if id_usuario:
                    self.session.execute(text("""
                        UPDATE usuario SET id_directivo = :id_persona WHERE id_usuario = :id_usuario
                    """), {"id_persona": id_persona, "id_usuario": id_usuario})
            
            elif rol == "Administrador":
                self.session.execute(text("""
                    INSERT INTO administrador (id_persona)
                    VALUES (:id_persona)
                """), {"id_persona": id_persona})
                
                if id_usuario:
                    self.session.execute(text("""
                        UPDATE usuario SET id_administrador = :id_persona WHERE id_usuario = :id_usuario
                    """), {"id_persona": id_persona, "id_usuario": id_usuario})
            
            elif rol == "Estudiante":
                self.session.execute(text("""
                    INSERT INTO estudiante (id_persona)
                    VALUES (:id_persona)
                """), {"id_persona": id_persona})
            
            # 6. Registrar evento de auditoría
            self._registrar_auditoria(
                accion="crear_usuario",
                descripcion=f"Creación de usuario {rol}: {numero_id} - {primer_nombre} {primer_apellido}",
                usuario_id=usuario_admin_id,
                entidad_tipo="Usuario",
                entidad_id=id_usuario or id_persona
            )
            
            # 7. Commit
            self.session.commit()
            
            # 8. Preparar datos para retorno
            datos_creado = {
                "id_usuario": id_usuario,
                "id_persona": id_persona,
                "numero_identificacion": numero_id,
                "nombre_completo": f"{primer_nombre} {primer_apellido}",
                "rol": rol,
                "email": datos.get("correo_electronico", "") if rol != "Estudiante" else "",
                "contraseña_temporal": contraseña_generada if rol != "Estudiante" else "",
                "fecha_creacion": datetime.now().isoformat()
            }
            
            mensaje = f"✅ Usuario '{rol}' creado exitosamente\n\nIdentificación: {numero_id}\nNombre: {datos_creado['nombre_completo']}"
            if rol != "Estudiante":
                mensaje += f"\nCorreo: {datos.get('correo_electronico', '')}\nContraseña temporal: {contraseña_generada}"
            
            return True, mensaje, datos_creado
        
        except Exception as e:
            self.session.rollback()
            print(f"[ERROR] ServicioUsuario.crear_usuario: {str(e)}")
            import traceback
            traceback.print_exc()
            return False, f"Error al crear usuario: {str(e)}", None
    
    def _registrar_auditoria(self, accion: str, descripcion: str, usuario_id: int = None, 
                            entidad_tipo: str = None, entidad_id: int = None):
        """Registra evento de auditoría"""
        try:
            # Tabla auditoria puede no existir aún, crear si es necesario
            self.session.execute(text("""
                INSERT INTO auditoria (accion, descripcion, usuario_id, entidad_tipo, entidad_id, fecha)
                VALUES (:accion, :descripcion, :usuario_id, :entidad_tipo, :entidad_id, NOW())
            """), {
                "accion": accion,
                "descripcion": descripcion,
                "usuario_id": usuario_id,
                "entidad_tipo": entidad_tipo,
                "entidad_id": entidad_id
            })
        except Exception as e:
            # Si falla auditoría, solo logear pero no fallar
            print(f"[⚠️ ] Error al registrar auditoría: {str(e)}")
