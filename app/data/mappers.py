# 📚 mappers.py - SQLAlchemy 2.0+ CORREGIDO

from sqlalchemy import MetaData, Table, Column, Integer, String, DateTime, Boolean, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship, registry
from datetime import datetime, timezone

# ============================================
# IMPORTACIONES DE CLASES
# ============================================

# Usuarios
from app.core.usuarios.persona import Persona
from app.core.usuarios.usuario import Usuario
from app.core.usuarios.estudiante import Estudiante
from app.core.usuarios.profesor import Profesor
from app.core.usuarios.acudiente import Acudiente
from app.core.usuarios.aspirante import Aspirante
from app.core.usuarios.directivo import Directivo
from app.core.usuarios.administrador import Administrador
from app.core.usuarios.rol import Rol
from app.core.usuarios.permiso import Permiso

# Académicas
from app.core.academico.grupo import Grupo
from app.core.academico.grado import Grado
from app.core.academico.periodo import PeriodoAcademico
from app.core.academico.hoja_vida import HojaVidaAcademica
from app.core.academico.observador import Observador
from app.core.academico.anotacion import Anotacion

# Logros
from app.core.logros.logro import Logro
from app.core.logros.categoria import CategoriaLogro
from app.core.logros.evaluacion import EvaluacionLogro
from app.core.logros.boletin import Boletin

# Gestión
from app.core.gestion.citacion import Citacion
from app.core.gestion.notificacion import Notificacion
from app.core.gestion.entrevista import Entrevista
from app.core.gestion.respuesta_formulario import RespuestaFormPre


mapper_registry = registry()
metadata = MetaData()


# ============================================
# DEFINICIÓN DE TABLAS
# ============================================

# --- USUARIO (SEPARATED - NO INHERITANCE) ---
# Persona es la clase base
# Usuario es una clase SEPARADA (ASOCIACIÓN, NO HERENCIA)
# Las clases de negocio (Estudiante, Profesor, Directivo, etc.) heredan de Persona
# Los Directivo, Profesor, Acudiente, Administrador tienen ASOCIACIÓN con Usuario

persona_table = Table(
    'persona',
    metadata,
    Column('id_persona', Integer, primary_key=True, autoincrement=True),
    Column('tipo_identificacion', String(20), nullable=False),
    Column('numero_identificacion', String(20), nullable=False, unique=True, index=True),
    Column('primer_nombre', String(50), nullable=False),
    Column('segundo_nombre', String(50)),
    Column('primer_apellido', String(50), nullable=False),
    Column('segundo_apellido', String(50)),
    Column('fecha_nacimiento', DateTime),
    Column('genero', String(10)),
    Column('direccion', String(200)),
    Column('telefono', String(20)),
    Column('type', String(50), nullable=False),  # Discriminador para Persona/Estudiante/Profesor/etc.
)

# USUARIO: TABLA INDEPENDIENTE (no hereda de Persona)
usuario_table = Table(
    'usuario',
    metadata,
    Column('id_usuario', Integer, primary_key=True, autoincrement=True),
    Column('correo_electronico', String(100), nullable=False, unique=True, index=True),
    Column('contrasena', String(255), nullable=False),
    Column('id_rol', Integer, ForeignKey('rol.id_rol')),
    Column('activo', Boolean, default=True),
    Column('fecha_creacion', DateTime, default=lambda: datetime.now(timezone.utc)),
    Column('ultimo_ingreso', DateTime),
    Column('justificacion_inhabilitacion', Text),
)

# ESTUDIANTE: hereda de Persona, NO tiene Usuario
estudiante_table = Table(
    'estudiante',
    metadata,
    Column('id_estudiante', Integer, ForeignKey('persona.id_persona'), primary_key=True),
    Column('codigo_matricula', String(50), unique=True, index=True),
    Column('fecha_ingreso', DateTime),
    Column('grado_actual', String(20)),
    Column('id_grupo', Integer, ForeignKey('grupo.id_grupo')),
)

# PROFESOR: hereda de Persona, tiene asociación con Usuario
profesor_table = Table(
    'profesor',
    metadata,
    Column('id_profesor', Integer, ForeignKey('persona.id_persona'), primary_key=True),
    Column('id_usuario', Integer, ForeignKey('usuario.id_usuario'), nullable=True),  # ASOCIACIÓN
    Column('especialidad', String(100)),
    Column('experiencia_anios', Integer),
    Column('es_director_grupo', Boolean, default=False),
)

# ACUDIENTE: hereda de Persona, tiene asociación con Usuario
acudiente_table = Table(
    'acudiente',
    metadata,
    Column('id_acudiente', Integer, ForeignKey('persona.id_persona'), primary_key=True),
    Column('id_usuario', Integer, ForeignKey('usuario.id_usuario'), nullable=True),  # ASOCIACIÓN
    Column('parentesco', String(50)),
)

# ASPIRANTE: hereda de Persona, tiene asociación con Usuario
aspirante_table = Table(
    'aspirante',
    metadata,
    Column('id_aspirante', Integer, ForeignKey('persona.id_persona'), primary_key=True),
    Column('id_usuario', Integer, ForeignKey('usuario.id_usuario'), nullable=True),  # ASOCIACIÓN
    Column('grado_solicitado', String(20)),
    Column('fecha_solicitud', DateTime),
    Column('estado_proceso', String(20)),
    Column('justificacion_rechazo', Text, nullable=True),
)

# DIRECTIVO: hereda de Persona, tiene asociación con Usuario
directivo_table = Table(
    'directivo',
    metadata,
    Column('id_directivo', Integer, ForeignKey('persona.id_persona'), primary_key=True),
    Column('id_usuario', Integer, ForeignKey('usuario.id_usuario'), nullable=True),  # ASOCIACIÓN
    Column('cargo', String(100)),
    Column('area_responsable', String(200)),
)

# ADMINISTRADOR: hereda de Usuario (única tabla que hereda de Usuario)
administrador_table = Table(
    'administrador',
    metadata,
    Column('id_administrador', Integer, ForeignKey('usuario.id_usuario'), primary_key=True),
    Column('primer_nombre', String(50)),
    Column('segundo_nombre', String(50)),
    Column('primer_apellido', String(50)),
    Column('segundo_apellido', String(50)),
    Column('telefono', String(20)),
)

# --- ROLES Y PERMISOS ---

rol_table = Table(
    'rol',
    metadata,
    Column('id_rol', Integer, primary_key=True, autoincrement=True),
    Column('nombre_rol', String(50), nullable=False, unique=True),  # ✅ CORRECTO
    Column('descripcion_rol', String(200)),  # ✅ CORRECTO
)

permiso_table = Table(
    'permiso',
    metadata,
    Column('id_permiso', Integer, primary_key=True, autoincrement=True),
    Column('nombre', String(100), nullable=False, unique=True),
    Column('descripcion', String(200)),
)

rol_permiso_table = Table(
    'rol_permiso',
    metadata,
    Column('id_rol', Integer, ForeignKey('rol.id_rol'), primary_key=True),
    Column('id_permiso', Integer, ForeignKey('permiso.id_permiso'), primary_key=True),
)

# --- ACADÉMICAS ---

grado_table = Table(
    'grado',
    metadata,
    Column('id_grado', Integer, primary_key=True, autoincrement=True),
    Column('nombre', String(50), nullable=False, unique=True),
)

grupo_table = Table(
    'grupo',
    metadata,
    Column('id_grupo', Integer, primary_key=True, autoincrement=True),
    Column('nombre_grupo', String(50), nullable=False),
    Column('id_director_grupo', Integer, ForeignKey('profesor.id_profesor')),
    Column('id_grado', Integer, ForeignKey('grado.id_grado')),
    Column('cupo_maximo', Integer, default=10),
    Column('cupo_minimo', Integer, default=5),
    Column('activo', Boolean, default=True),
)

periodo_academico_table = Table(
    'periodo_academico',
    metadata,
    Column('id_periodo', Integer, primary_key=True, autoincrement=True),
    Column('nombre_periodo', String(50), nullable=False),
    Column('fecha_inicio', DateTime, nullable=False),
    Column('fecha_fin', DateTime, nullable=False),
    Column('actual', Boolean, default=False),
)

hoja_vida_table = Table(
    'hoja_vida',
    metadata,
    Column('id_hoja_vida', Integer, primary_key=True, autoincrement=True),
    Column('id_estudiante', Integer, ForeignKey('estudiante.id_estudiante'), unique=True),
    Column('estado_salud', String(100)),
    Column('alergias', JSON),
    Column('tratamientos', JSON),
    Column('necesidades_educativas', JSON),
    # NOTA: No se incluye promedio_general porque las calificaciones son cualitativas
    Column('fecha_creacion', DateTime, default=datetime.now),
    Column('usuario_creador', Integer, ForeignKey('usuario.id_usuario'), nullable=True),
)

observador_table = Table(
    'observador',
    metadata,
    Column('id_observador', Integer, primary_key=True, autoincrement=True),
    Column('id_estudiante', Integer, ForeignKey('estudiante.id_estudiante'), unique=True),
    Column('comportamiento_general', String(255)),
)

anotacion_table = Table(
    'anotacion',
    metadata,
    Column('id_anotacion', Integer, primary_key=True, autoincrement=True),
    Column('id_observador', Integer, ForeignKey('observador.id_observador')),
    Column('id_profesor_autor', Integer, ForeignKey('profesor.id_profesor')),
    Column('categoria', String(50)),
    Column('detalle', String(200)),
    Column('fecha_registro', DateTime, default=lambda: datetime.now(timezone.utc)),
)

# --- LOGROS ---

categoria_logro_table = Table(
    'categoria_logro',
    metadata,
    Column('id_categoria', Integer, primary_key=True, autoincrement=True),
    Column('nombre', String(50), nullable=False, unique=True),
    Column('descripcion', String(200)),
    Column('id_directivo_creador', Integer, ForeignKey('directivo.id_directivo')),
)

logro_table = Table(
    'logro',
    metadata,
    Column('id_logro', Integer, primary_key=True, autoincrement=True),
    Column('titulo', String(50), nullable=False, unique=True),
    Column('descripcion', String(200)),
    Column('id_categoria', Integer, ForeignKey('categoria_logro.id_categoria')),
    Column('id_directivo_creador', Integer, ForeignKey('directivo.id_directivo')),
    Column('estado', String(20)),
    Column('fecha_creacion', DateTime, default=lambda: datetime.now(timezone.utc)),
)

evaluacion_logro_table = Table(
    'evaluacion_logro',
    metadata,
    Column('id_evaluacion', Integer, primary_key=True, autoincrement=True),
    Column('id_logro', Integer, ForeignKey('logro.id_logro')),
    Column('id_estudiante', Integer, ForeignKey('estudiante.id_estudiante')),
    Column('id_profesor', Integer, ForeignKey('profesor.id_profesor')),
    Column('id_periodo', Integer, ForeignKey('periodo_academico.id_periodo')),
    Column('puntuacion', String(20)),
    Column('comentarios', Text),
    Column('fecha_registro', DateTime, default=lambda: datetime.now(timezone.utc)),
)

boletin_table = Table(
    'boletin',
    metadata,
    Column('id_boletin', Integer, primary_key=True, autoincrement=True),
    Column('id_estudiante', Integer, ForeignKey('estudiante.id_estudiante')),
    Column('id_periodo', Integer, ForeignKey('periodo_academico.id_periodo')),
    Column('id_profesor_generador', Integer, ForeignKey('profesor.id_profesor')),
    Column('fecha_generacion', DateTime, default=lambda: datetime.now(timezone.utc)),
)

# --- GESTIÓN ---

entrevista_table = Table(
    'entrevista',
    metadata,
    Column('id_entrevista', Integer, primary_key=True, autoincrement=True),
    Column('id_aspirante', Integer, ForeignKey('aspirante.id_aspirante')),
    Column('id_profesor_entrevistador', Integer, ForeignKey('profesor.id_profesor')),
    Column('id_directivo_remitente', Integer, ForeignKey('directivo.id_directivo')),
    Column('fecha_programada', DateTime),
    Column('lugar', String(100)),
    Column('estado', String(50)),
    Column('notas', Text),
)

citacion_table = Table(
    'citacion',
    metadata,
    Column('id_citacion', Integer, primary_key=True, autoincrement=True),
    Column('id_directivo_remitente', Integer, ForeignKey('directivo.id_directivo')),
    Column('fecha_programada', DateTime),
    Column('motivo', String(100)),
    Column('descripcion', Text),
    Column('lugar', String(100)),
    Column('correo_destinatarios', JSON),
)

notificacion_table = Table(
    'notificacion',
    metadata,
    Column('id_notificacion', Integer, primary_key=True, autoincrement=True),
    Column('id_citacion', Integer, ForeignKey('citacion.id_citacion')),
    Column('id_acudiente_destinatario', Integer, ForeignKey('acudiente.id_acudiente')),
    Column('fecha_envio', DateTime, default=lambda: datetime.now(timezone.utc)),
    Column('asunto', String(100)),
    Column('contenido', Text),
)

respuesta_form_pre_table = Table(
    'respuesta_form_pre',
    metadata,
    Column('id_respuesta', Integer, primary_key=True, autoincrement=True),
    Column('fecha_solicitud', DateTime, default=lambda: datetime.now(timezone.utc)),
    Column('grado_solicitado', String(50)),
    Column('colegio_anterior', String(100)),
    Column('datos_acudiente', JSON),
    Column('datos_aspirante', JSON),
    Column('correo_envio', String(100)),
    Column('telefono_contacto', String(20)),
)

# --- RELACIONES M2M ---

estudiante_acudiente_table = Table(
    'estudiante_acudiente',
    metadata,
    Column('id_estudiante', Integer, ForeignKey('estudiante.id_estudiante'), primary_key=True),
    Column('id_acudiente', Integer, ForeignKey('acudiente.id_acudiente'), primary_key=True),
)

profesor_grupo_table = Table(
    'profesor_grupo',
    metadata,
    Column('id_profesor', Integer, ForeignKey('profesor.id_profesor'), primary_key=True),
    Column('id_grupo', Integer, ForeignKey('grupo.id_grupo'), primary_key=True),
)


# ===============================================
# MAPEOS ORM - JOINED TABLE INHERITANCE
# ===============================================

def start_mappers():
    """Inicializa todos los mapeos ORM de SQLAlchemy"""
    try:
        from sqlalchemy.orm import clear_mappers
        try:
            clear_mappers()
        except:
            pass  # Primera ejecución, no hay mapeos previos
        
        # 1. PERSONA (BASE)
        mapper_registry.map_imperatively(
            Persona,
            persona_table,
            polymorphic_on=persona_table.c.type,
            polymorphic_identity='persona'
        )

        # 2. ROL
        mapper_registry.map_imperatively(
            Rol,
            rol_table,
            properties={
                "usuarios": relationship(Usuario, back_populates="rol"),
                "permisos": relationship(Permiso, secondary=rol_permiso_table, back_populates="roles")
            }
        )

        # 3. PERMISO
        mapper_registry.map_imperatively(
            Permiso,
            permiso_table,
            properties={
                "roles": relationship(Rol, secondary=rol_permiso_table, back_populates="permisos")
            }
        )

        # 4. USUARIO (INDEPENDIENTE - NO hereda de Persona)
        mapper_registry.map_imperatively(
            Usuario,
            usuario_table,
            properties={
                "rol": relationship(Rol, back_populates="usuarios")
            }
        )

        # 5. ESTUDIANTE (hereda de Persona, NO tiene Usuario)
        mapper_registry.map_imperatively(
            Estudiante,
            estudiante_table,
            inherits=Persona,
            polymorphic_identity='estudiante',
            properties={
                "grupo": relationship(Grupo, back_populates="estudiantes"),
                "acudientes": relationship(
                    Acudiente, 
                    secondary=estudiante_acudiente_table, 
                    back_populates="estudiantes"
                ),
                "hoja_vida": relationship(HojaVidaAcademica, uselist=False, back_populates="estudiante"),
                "observador": relationship(Observador, uselist=False, back_populates="estudiante"),
                "evaluaciones": relationship(EvaluacionLogro, back_populates="estudiante"),
                "boletines": relationship(Boletin, back_populates="estudiante")
            }
        )

        # 6. PROFESOR (hereda de Persona, ASOCIACIÓN con Usuario)
        mapper_registry.map_imperatively(
            Profesor,
            profesor_table,
            inherits=Persona,
            polymorphic_identity='profesor',
            properties={
                "usuario": relationship(Usuario, uselist=False, foreign_keys=[profesor_table.c.id_usuario]),
                "grupos": relationship(
                    Grupo, 
                    secondary=profesor_grupo_table, 
                    back_populates="profesores",
                    overlaps="director_grupo,grupos_dirigidos"
                ),
                "grupos_dirigidos": relationship(
                    Grupo, 
                    back_populates="director_grupo",
                    foreign_keys=[grupo_table.c.id_director_grupo],
                    overlaps="grupos,profesores"
                ),
                "evaluaciones": relationship(EvaluacionLogro, back_populates="profesor"),
                "boletines": relationship(Boletin, back_populates="profesor_generador"),
                "anotaciones": relationship(Anotacion, back_populates="profesor_autor"),
                "entrevistas": relationship(Entrevista, back_populates="profesor_entrevistador")
            }
        )

        # 7. ACUDIENTE (hereda de Persona, ASOCIACIÓN con Usuario)
        mapper_registry.map_imperatively(
            Acudiente,
            acudiente_table,
            inherits=Persona,
            polymorphic_identity='acudiente',
            properties={
                "usuario": relationship(Usuario, uselist=False, foreign_keys=[acudiente_table.c.id_usuario]),
                "estudiantes": relationship(
                    Estudiante, 
                    secondary=estudiante_acudiente_table, 
                    back_populates="acudientes"
                ),
                "notificaciones": relationship(Notificacion, back_populates="acudiente")
            }
        )

        # 8. ASPIRANTE (hereda de Persona, ASOCIACIÓN con Usuario)
        mapper_registry.map_imperatively(
            Aspirante,
            aspirante_table,
            inherits=Persona,
            polymorphic_identity='aspirante',
            properties={
                "usuario": relationship(Usuario, uselist=False, foreign_keys=[aspirante_table.c.id_usuario]),
                "entrevista": relationship(Entrevista, uselist=False, back_populates="aspirante")
            }
        )

        # 9. DIRECTIVO (hereda de Persona, ASOCIACIÓN con Usuario)
        mapper_registry.map_imperatively(
            Directivo,
            directivo_table,
            inherits=Persona,
            polymorphic_identity='directivo',
            properties={
                "usuario": relationship(Usuario, uselist=False, foreign_keys=[directivo_table.c.id_usuario]),
                "logros_creados": relationship(
                    Logro, 
                    foreign_keys=[logro_table.c.id_directivo_creador],
                    back_populates="directivo_creador"
                ),
                "categorias_creadas": relationship(
                    CategoriaLogro, 
                    foreign_keys=[categoria_logro_table.c.id_directivo_creador],
                    back_populates="directivo_creador"
                ),
                "entrevistas": relationship(Entrevista, back_populates="directivo_remitente"),
                "citaciones": relationship(Citacion, back_populates="directivo_remitente")
            }
        )

        # 10. ADMINISTRADOR (hereda de Usuario - única clase que hereda de Usuario)
        mapper_registry.map_imperatively(
            Administrador,
            administrador_table,
            inherits=Usuario,
            properties={}
        )

        # 11. GRADO
        mapper_registry.map_imperatively(
            Grado,
            grado_table,
            properties={
                "grupos": relationship(Grupo, back_populates="grado")
            }
        )

        # 12. GRUPO
        mapper_registry.map_imperatively(
            Grupo,
            grupo_table,
            properties={
                "director_grupo": relationship(
                    Profesor, 
                    back_populates="grupos_dirigidos", 
                    foreign_keys=[grupo_table.c.id_director_grupo],
                    overlaps="grupos,profesores"
                ),
                "grado": relationship(Grado, back_populates="grupos"),
                "estudiantes": relationship(Estudiante, back_populates="grupo"),
                "profesores": relationship(
                    Profesor, 
                    secondary=profesor_grupo_table, 
                    back_populates="grupos",
                    overlaps="director_grupo,grupos_dirigidos"
                )
            }
        )

        # 13. PERIODO ACADÉMICO
        mapper_registry.map_imperatively(
            PeriodoAcademico,
            periodo_academico_table,
            properties={
                "evaluaciones": relationship(EvaluacionLogro, back_populates="periodo"),
                "boletines": relationship(Boletin, back_populates="periodo")
            }
        )

        # 14. HOJA VIDA ACADÉMICA
        mapper_registry.map_imperatively(
            HojaVidaAcademica,
            hoja_vida_table,
            properties={
                "estudiante": relationship(Estudiante, back_populates="hoja_vida")
            }
        )

        # 15. OBSERVADOR
        mapper_registry.map_imperatively(
            Observador,
            observador_table,
            properties={
                "estudiante": relationship(Estudiante, back_populates="observador"),
                "anotaciones": relationship(Anotacion, back_populates="observador")
            }
        )

        # 16. ANOTACIÓN
        mapper_registry.map_imperatively(
            Anotacion,
            anotacion_table,
            properties={
                "observador": relationship(Observador, back_populates="anotaciones"),
                "profesor_autor": relationship(Profesor, back_populates="anotaciones")
            }
        )

        # 17. CATEGORÍA LOGRO
        mapper_registry.map_imperatively(
            CategoriaLogro,
            categoria_logro_table,
            properties={
                "directivo_creador": relationship(
                    Directivo, 
                    foreign_keys=[categoria_logro_table.c.id_directivo_creador], 
                    back_populates="categorias_creadas"
                ),
                "logros": relationship(Logro, back_populates="categoria")
            }
        )

        # 18. LOGRO
        mapper_registry.map_imperatively(
            Logro,
            logro_table,
            properties={
                "categoria": relationship(CategoriaLogro, back_populates="logros"),
                "directivo_creador": relationship(
                    Directivo, 
                    foreign_keys=[logro_table.c.id_directivo_creador], 
                    back_populates="logros_creados"
                ),
                "evaluaciones": relationship(EvaluacionLogro, back_populates="logro")
            }
        )

        # 19. EVALUACIÓN LOGRO
        mapper_registry.map_imperatively(
            EvaluacionLogro,
            evaluacion_logro_table,
            properties={
                "logro": relationship(Logro, back_populates="evaluaciones"),
                "estudiante": relationship(Estudiante, back_populates="evaluaciones"),
                "profesor": relationship(Profesor, back_populates="evaluaciones"),
                "periodo": relationship(PeriodoAcademico, back_populates="evaluaciones")
            }
        )

        # 20. BOLETÍN
        mapper_registry.map_imperatively(
            Boletin,
            boletin_table,
            properties={
                "estudiante": relationship(Estudiante, back_populates="boletines"),
                "periodo": relationship(PeriodoAcademico, back_populates="boletines"),
                "profesor_generador": relationship(Profesor, back_populates="boletines")
            }
        )

        # 21. ENTREVISTA
        mapper_registry.map_imperatively(
            Entrevista,
            entrevista_table,
            properties={
                "aspirante": relationship(Aspirante, back_populates="entrevista"),
                "profesor_entrevistador": relationship(Profesor, back_populates="entrevistas"),
                "directivo_remitente": relationship(Directivo, back_populates="entrevistas")
            }
        )

        # 22. CITACIÓN
        mapper_registry.map_imperatively(
            Citacion,
            citacion_table,
            properties={
                "directivo_remitente": relationship(Directivo, back_populates="citaciones"),
                "notificaciones": relationship(Notificacion, back_populates="citacion")
            }
        )

        # 23. NOTIFICACIÓN
        mapper_registry.map_imperatively(
            Notificacion,
            notificacion_table,
            properties={
                "citacion": relationship(Citacion, back_populates="notificaciones"),
                "acudiente": relationship(Acudiente, back_populates="notificaciones")
            }
        )

        # 24. RESPUESTA FORM PRE
        mapper_registry.map_imperatively(
            RespuestaFormPre,
            respuesta_form_pre_table
        )

        print("[✅] Mapeos ORM configurados correctamente")

    except Exception as e:
        print(f"[❌] Error en mapeos: {e}")
        import traceback
        traceback.print_exc()
        raise