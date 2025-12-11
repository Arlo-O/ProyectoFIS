from sqlalchemy import Table, Column, Integer, String, Date, ForeignKey, Boolean, DateTime, Text, JSON, Float
from sqlalchemy.orm import relationship
from .db import mapper_registry


# Modelos de usuarios
from app.modelos.usuarios.persona import Persona
from app.modelos.usuarios.usuario import Usuario
from app.modelos.usuarios.estudiante import Estudiante
from app.modelos.usuarios.profesor import Profesor
from app.modelos.usuarios.acudiente import Acudiente
from app.modelos.usuarios.aspirante import Aspirante
from app.modelos.usuarios.directivo import Directivo
from app.modelos.usuarios.administrador import Administrador
from app.modelos.usuarios.rol import Rol
from app.modelos.usuarios.permiso import Permiso


# Modelos académicos
from app.modelos.academico.grupo import Grupo
from app.modelos.academico.grado import Grado
from app.modelos.academico.periodoAcademico import PeriodoAcademico
from app.modelos.academico.hojaVidaAcademica import HojaVidaAcademica
from app.modelos.academico.observador import Observador
from app.modelos.academico.anotacion import Anotacion


# Modelos de logros
from app.modelos.logros.logro import Logro
from app.modelos.logros.categoriaLogro import CategoriaLogro
from app.modelos.logros.evaluacionLogro import EvaluacionLogro
from app.modelos.logros.boletin import Boletin


# Modelos de gestión
from app.modelos.gestion.citacion import Citacion
from app.modelos.gestion.notificacion import Notificacion
from app.modelos.gestion.entrevista import Entrevista
from app.modelos.gestion.respuestaFormPre import RespuestaFormPre


# Tablas de la base de datos
persona_table = Table(
    "persona",
    mapper_registry.metadata,
    Column("id_persona", Integer, primary_key=True, autoincrement=True),
    Column("numero_identificacion", String(20), unique=True, nullable=False),
    Column("tipo_identificacion", String(10), nullable=False),
    Column("primer_nombre", String(50), nullable=False),
    Column("segundo_nombre", String(50)),
    Column("primer_apellido", String(50), nullable=False),
    Column("segundo_apellido", String(50)),
    Column("fecha_nacimiento", DateTime, nullable=False),
    Column("telefono", String(20)),
    Column("direccion", Text),
    Column("genero", String(10)),
    Column("type", String(20), nullable=False),  # Discriminator
)

usuario_table = Table(
    "usuario",
    mapper_registry.metadata,
    Column("id_usuario", Integer, ForeignKey("persona.id_persona"), primary_key=True),
    Column("contrasena", String(255), nullable=False),
    Column("correo_electronico", String(100), unique=True, nullable=False),
    Column("id_rol", Integer, ForeignKey("rol.id_rol")),
    Column("activo", Boolean, default=True),
    Column("fecha_creacion", DateTime),
    Column("ultimo_ingreso", DateTime),
)

rol_table = Table(
    "rol",
    mapper_registry.metadata,
    Column("id_rol", Integer, primary_key=True, autoincrement=True),
    Column("nombre_rol", String(50), nullable=False),
    Column("descripcion_rol", Text),
)

permiso_table = Table(
    "permiso",
    mapper_registry.metadata,
    Column("id_permiso", Integer, primary_key=True, autoincrement=True),
    Column("nombre_permiso", String(50), nullable=False),
    Column("descripcion", Text),
)

rol_permiso_table = Table(
    "rol_permiso",
    mapper_registry.metadata,
    Column("id_rol", Integer, ForeignKey("rol.id_rol"), primary_key=True),
    Column("id_permiso", Integer, ForeignKey("permiso.id_permiso"), primary_key=True),
)

estudiante_table = Table(
    "estudiante",
    mapper_registry.metadata,
    Column("id_estudiante", Integer, ForeignKey("usuario.id_usuario"), primary_key=True),
    Column("fecha_ingreso", DateTime),
    Column("codigo_matricula", String(20), unique=True),
    Column("id_grupo", Integer, ForeignKey("grupo.id_grupo")),
)

estudiante_acudiente_table = Table(
    "estudiante_acudiente",
    mapper_registry.metadata,
    Column("id_estudiante", Integer, ForeignKey("estudiante.id_estudiante"), primary_key=True),
    Column("id_acudiente", Integer, ForeignKey("acudiente.id_acudiente"), primary_key=True),
)

profesor_table = Table(
    "profesor",
    mapper_registry.metadata,
    Column("id_profesor", Integer, ForeignKey("usuario.id_usuario"), primary_key=True),
    Column("es_director_grupo", Boolean, default=False),
)

profesor_grupo_table = Table(
    "profesor_grupo", # For gruposAsignados
    mapper_registry.metadata,
    Column("id_profesor", Integer, ForeignKey("profesor.id_profesor"), primary_key=True),
    Column("id_grupo", Integer, ForeignKey("grupo.id_grupo"), primary_key=True),
)

acudiente_table = Table(
    "acudiente",
    mapper_registry.metadata,
    Column("id_acudiente", Integer, ForeignKey("usuario.id_usuario"), primary_key=True),
    Column("parentesco", String(50)),
    Column("es_aspirante", Boolean, default=False),
)

aspirante_table = Table(
    "aspirante",
    mapper_registry.metadata,
    Column("id_aspirante", Integer, ForeignKey("usuario.id_usuario"), primary_key=True),
    Column("grado_solicitado", String(20)),
    Column("fecha_solicitud", DateTime),
    Column("estado_proceso", String(30)),
)

directivo_table = Table(
    "directivo",
    mapper_registry.metadata,
    Column("id_directivo", Integer, ForeignKey("usuario.id_usuario"), primary_key=True),
    Column("cargo", String(100)),
    Column("area_responsable", String(100)),
)

administrador_table = Table(
    "administrador",
    mapper_registry.metadata,
    Column("id_administrador", Integer, ForeignKey("usuario.id_usuario"), primary_key=True),
)

grupo_table = Table(
    "grupo",
    mapper_registry.metadata,
    Column("id_grupo", Integer, primary_key=True, autoincrement=True),
    Column("nombre_grupo", String(20), nullable=False),
    Column("id_director", Integer, ForeignKey("profesor.id_profesor")),
    Column("id_creador", Integer, ForeignKey("directivo.id_directivo")),
    Column("cupo_maximo", Integer),
    Column("cupo_minimo", Integer),
    Column("activo", Boolean),
    Column("id_grado", Integer, ForeignKey("grado.id_grado")),
)

grado_table = Table(
    "grado",
    mapper_registry.metadata,
    Column("id_grado", Integer, primary_key=True, autoincrement=True),
    Column("nombre", String(20), nullable=False),
)

logro_table = Table(
    "logro",
    mapper_registry.metadata,
    Column("id_logro", Integer, primary_key=True, autoincrement=True),
    Column("titulo", String(200)),
    Column("descripcion", Text),
    Column("fecha_creacion", DateTime),
    Column("id_creador", Integer, ForeignKey("directivo.id_directivo")),
    Column("estado", String(30)),
    Column("id_categoria", Integer, ForeignKey("categoria_logro.id_categoria")),
)

categoria_logro_table = Table(
    "categoria_logro",
    mapper_registry.metadata,
    Column("id_categoria", Integer, primary_key=True, autoincrement=True),
    Column("nombre", String(100)),
    Column("descripcion", Text),
    Column("id_creador", Integer, ForeignKey("directivo.id_directivo")),
)

evaluacion_logro_table = Table(
    "evaluacion_logro",
    mapper_registry.metadata,
    Column("id_evaluacion", Integer, primary_key=True, autoincrement=True),
    Column("id_logro", Integer, ForeignKey("logro.id_logro")),
    Column("id_profesor", Integer, ForeignKey("profesor.id_profesor")),
    Column("id_periodo", Integer, ForeignKey("periodo_academico.id_periodo")),
    Column("puntuacion", String(10)),
    Column("fecha_registro", DateTime),
    Column("comentarios", JSON),
    Column("id_estudiante", Integer, ForeignKey("estudiante.id_estudiante")),
    Column("id_boletin", Integer, ForeignKey("boletin.id_boletin")),
)

periodo_academico_table = Table(
    "periodo_academico",
    mapper_registry.metadata,
    Column("id_periodo", Integer, primary_key=True, autoincrement=True),
    Column("nombre_periodo", String(50)),
    Column("fecha_inicio", DateTime),
    Column("fecha_fin", DateTime),
    Column("actual", Boolean),
)

boletin_table = Table(
    "boletin",
    mapper_registry.metadata,
    Column("id_boletin", Integer, primary_key=True, autoincrement=True),
    Column("id_estudiante", Integer, ForeignKey("estudiante.id_estudiante")),
    Column("id_periodo", Integer, ForeignKey("periodo_academico.id_periodo")),
    Column("id_generador", Integer, ForeignKey("profesor.id_profesor")),
    Column("fecha_generacion", DateTime),
)

citacion_table = Table(
    "citacion",
    mapper_registry.metadata,
    Column("id_citacion", Integer, primary_key=True, autoincrement=True),
    Column("fecha_programada", DateTime),
    Column("correo_destinatarios", JSON),
    Column("motivo", String(200)),
    Column("descripcion", Text),
    Column("lugar", String(100)),
    Column("id_remitente", Integer, ForeignKey("directivo.id_directivo")),
    Column("id_entrevista", Integer, ForeignKey("entrevista.id_entrevista")),
)

notificacion_table = Table(
    "notificacion",
    mapper_registry.metadata,
    Column("id_notificacion", Integer, primary_key=True, autoincrement=True),
    Column("fecha_envio", DateTime),
    Column("asunto", String(200)),
    Column("contenido", Text),
    Column("id_destinatario", Integer, ForeignKey("acudiente.id_acudiente")),
    Column("id_citacion", Integer, ForeignKey("citacion.id_citacion")),
)

entrevista_table = Table(
    "entrevista",
    mapper_registry.metadata,
    Column("id_entrevista", Integer, primary_key=True, autoincrement=True),
    Column("notas", Text),
    Column("id_entrevistador", Integer, ForeignKey("profesor.id_profesor")),
    Column("fecha_programada", DateTime),
    Column("lugar", String(100)),
    Column("estado", String(30)),
    Column("id_remitente", Integer, ForeignKey("directivo.id_directivo")),
    Column("id_aspirante", Integer, ForeignKey("aspirante.id_aspirante")),
)

anotacion_table = Table(
    "anotacion",
    mapper_registry.metadata,
    Column("id_anotacion", Integer, primary_key=True, autoincrement=True),
    Column("fecha", DateTime),
    Column("descripcion", Text),
    Column("id_autor", Integer, ForeignKey("profesor.id_profesor")),
    Column("tipo", String(50)),
    Column("id_observador", Integer, ForeignKey("observador.id_observador")),
)

hoja_vida_table = Table(
    "hoja_vida",
    mapper_registry.metadata,
    Column("id_hoja_vida", Integer, primary_key=True, autoincrement=True),
    Column("id_estudiante", Integer, ForeignKey("estudiante.id_estudiante"), unique=True),
    Column("promedio_general", Float, nullable=True),
)

hoja_vida_logro_table = Table(
    "hoja_vida_logro",
    mapper_registry.metadata,
    Column("id_hoja_vida", Integer, ForeignKey("hoja_vida.id_hoja_vida"), primary_key=True),
    Column("id_logro", Integer, ForeignKey("logro.id_logro"), primary_key=True),
)

hoja_vida_grupo_table = Table(
    "hoja_vida_grupo",
    mapper_registry.metadata,
    Column("id_hoja_vida", Integer, ForeignKey("hoja_vida.id_hoja_vida"), primary_key=True),
    Column("id_grupo", Integer, ForeignKey("grupo.id_grupo"), primary_key=True),
)

observador_table = Table(
    "observador",
    mapper_registry.metadata,
    Column("id_observador", Integer, primary_key=True, autoincrement=True),
    Column("id_estudiante", Integer, ForeignKey("estudiante.id_estudiante"), unique=True),
    Column("comportamiento_general", Text),
)

respuesta_form_pre_table = Table(
    "respuesta_form_pre",
    mapper_registry.metadata,
    Column("id_respuesta", Integer, primary_key=True, autoincrement=True),
    Column("id_aspirante", Integer, ForeignKey("aspirante.id_aspirante")),
    Column("fecha_respuesta", DateTime),
    Column("respuestas", JSON),
)


def start_mappers():
    # 1. ENTIDADES INDEPENDIENTES (sin FK)
    mapper_registry.map_imperatively(
        Permiso,
        permiso_table,
        properties={
            "id_permiso": permiso_table.c.id_permiso,
            "nombre_permiso": permiso_table.c.nombre_permiso,
            "descripcion": permiso_table.c.descripcion,
        }
    )

    mapper_registry.map_imperatively(
        Rol,
        rol_table,
        properties={
            "id_rol": rol_table.c.id_rol,
            "nombre_rol": rol_table.c.nombre_rol,
            "descripcion_rol": rol_table.c.descripcion_rol,
            "permisos": relationship(Permiso, secondary=rol_permiso_table),
        }
    )

    # 2. PERSONA (BASE POLIMÓRFICA)
    mapper_registry.map_imperatively(
        Persona,
        persona_table,
        polymorphic_on=persona_table.c.type,
        polymorphic_identity="persona",
        properties={
            "numero_identificacion": persona_table.c.numero_identificacion,
            "tipo_identificacion": persona_table.c.tipo_identificacion,
            "primer_nombre": persona_table.c.primer_nombre,
            "segundo_nombre": persona_table.c.segundo_nombre,
            "primer_apellido": persona_table.c.primer_apellido,
            "segundo_apellido": persona_table.c.segundo_apellido,
            "fecha_nacimiento": persona_table.c.fecha_nacimiento,
            "telefono": persona_table.c.telefono,
            "direccion": persona_table.c.direccion,
            "genero": persona_table.c.genero,
        }
    )

    # 3. USUARIO (HEREDA PERSONA)
    mapper_registry.map_imperatively(
        Usuario,
        usuario_table,
        inherits=Persona,
        polymorphic_identity="usuario",
        properties={
            "contrasena": usuario_table.c.contrasena,
            "correo_electronico": usuario_table.c.correo_electronico,
            "rol": relationship(Rol, back_populates="usuarios"),
            "activo": usuario_table.c.activo,
            "fecha_creacion": usuario_table.c.fecha_creacion,
            "ultimo_ingreso": usuario_table.c.ultimo_ingreso,
        }
    )

    # 4. SUBTIPOS USUARIO (SIN DEPENDENCIAS EXTERNAS)
    mapper_registry.map_imperatively(
        Administrador,
        administrador_table,
        inherits=Usuario,
        polymorphic_identity="administrador",
    )

    mapper_registry.map_imperatively(
        Directivo,
        directivo_table,
        inherits=Usuario,
        polymorphic_identity="directivo",
        properties={
            "cargo": directivo_table.c.cargo,
            "area_responsable": directivo_table.c.area_responsable,
        }
    )

    mapper_registry.map_imperatively(
        Profesor,
        profesor_table,
        inherits=Usuario,
        polymorphic_identity="profesor",
        properties={
            "es_director_grupo": profesor_table.c.es_director_grupo,
        }
    )

    mapper_registry.map_imperatively(
        Acudiente,
        acudiente_table,
        inherits=Usuario,
        polymorphic_identity="acudiente",
        properties={
            "parentesco": acudiente_table.c.parentesco,
            "es_aspirante": acudiente_table.c.es_aspirante,
        }
    )

    mapper_registry.map_imperatively(
        Aspirante,
        aspirante_table,
        inherits=Usuario,
        polymorphic_identity="aspirante",
        properties={
            "grado_solicitado": aspirante_table.c.grado_solicitado,
            "fecha_solicitud": aspirante_table.c.fecha_solicitud,
            "estado_proceso": aspirante_table.c.estado_proceso,
        }
    )

    mapper_registry.map_imperatively(
        Estudiante,
        estudiante_table,
        inherits=Usuario,
        polymorphic_identity="estudiante",
        properties={
            "fecha_ingreso": estudiante_table.c.fecha_ingreso,
            "codigo_matricula": estudiante_table.c.codigo_matricula,
        }
    )

    # 5. ACADÉMICO BASE
    mapper_registry.map_imperatively(
        Grado,
        grado_table,
        properties={
            "nombre": grado_table.c.nombre,
        }
    )

    # 6. PERÍODO ACADÉMICO
    mapper_registry.map_imperatively(
        PeriodoAcademico,
        periodo_academico_table,
        properties={
            "nombre_periodo": periodo_academico_table.c.nombre_periodo,
            "fecha_inicio": periodo_academico_table.c.fecha_inicio,
            "fecha_fin": periodo_academico_table.c.fecha_fin,
            "actual": periodo_academico_table.c.actual,
        }
    )

    # 7. CATEGORÍA LOGRO
    mapper_registry.map_imperatively(
        CategoriaLogro,
        categoria_logro_table,
        properties={
            "nombre": categoria_logro_table.c.nombre,
            "descripcion": categoria_logro_table.c.descripcion,
            "creador": relationship(Directivo),
        }
    )

    # 8. GRUPO (DEPENDE DE GRADO, PROFESOR, DIRECTIVO, ESTUDIANTE)
    mapper_registry.map_imperatively(
        Grupo,
        grupo_table,
        properties={
            "nombre_grupo": grupo_table.c.nombre_grupo,
            "director": relationship(Profesor, back_populates="grupos_dirigidos"),
            "creador": relationship(Directivo),
            "cupo_maximo": grupo_table.c.cupo_maximo,
            "cupo_minimo": grupo_table.c.cupo_minimo,
            "activo": grupo_table.c.activo,
            "grado": relationship(Grado, back_populates="grupos"),
            "estudiantes": relationship(Estudiante, back_populates="grupo"),
        }
    )

    # 9. LOGRO
    mapper_registry.map_imperatively(
        Logro,
        logro_table,
        properties={
            "titulo": logro_table.c.titulo,
            "descripcion": logro_table.c.descripcion,
            "fecha_creacion": logro_table.c.fecha_creacion,
            "creador": relationship(Directivo),
            "estado": logro_table.c.estado,
            "categoria": relationship(CategoriaLogro, back_populates="logros"),
        }
    )

    # 10. COMPLETAR RELACIONES USUARIO-GRUPO
    # Actualizar Profesor con grupos
    mapper_registry.map_imperatively(
        Profesor,
        profesor_table,
        inherits=Usuario,
        polymorphic_identity="profesor",
        properties={
            "es_director_grupo": profesor_table.c.es_director_grupo,
            "grupos_asignados": relationship(Grupo, secondary=profesor_grupo_table),
            "grupos_dirigidos": relationship(Grupo, foreign_keys="Grupo.director"),
        }
    )

    # Actualizar Acudiente/Estudiante relaciones many-to-many
    mapper_registry.map_imperatively(
        Acudiente,
        acudiente_table,
        inherits=Usuario,
        polymorphic_identity="acudiente",
        properties={
            "parentesco": acudiente_table.c.parentesco,
            "es_aspirante": acudiente_table.c.es_aspirante,
            "estudiantes": relationship(Estudiante, secondary=estudiante_acudiente_table, back_populates="acudientes"),
        }
    )

    mapper_registry.map_imperatively(
        Estudiante,
        estudiante_table,
        inherits=Usuario,
        polymorphic_identity="estudiante",
        properties={
            "fecha_ingreso": estudiante_table.c.fecha_ingreso,
            "codigo_matricula": estudiante_table.c.codigo_matricula,
            "grupo": relationship(Grupo, back_populates="estudiantes"),
            "acudientes": relationship(Acudiente, secondary=estudiante_acudiente_table, back_populates="estudiantes"),
        }
    )

    # 11. HOJA VIDA Y OBSERVADOR
    mapper_registry.map_imperatively(
        HojaVidaAcademica,
        hoja_vida_table,
        properties={
            "estudiante": relationship(Estudiante, back_populates="hoja_vida"),
            "promedio_general": hoja_vida_table.c.promedio_general,
        }
    )

    mapper_registry.map_imperatively(
        Observador,
        observador_table,
        properties={
            "estudiante": relationship(Estudiante, back_populates="observador"),
            "comportamiento_general": observador_table.c.comportamiento_general,
        }
    )

    # 12. EVALUACIÓN LOGRO
    mapper_registry.map_imperatively(
        EvaluacionLogro,
        evaluacion_logro_table,
        properties={
            "logro": relationship(Logro, back_populates="evaluaciones"),
            "profesor": relationship(Profesor, back_populates="evaluaciones"),
            "periodo": relationship(PeriodoAcademico),
            "puntuacion": evaluacion_logro_table.c.puntuacion,
            "fecha_registro": evaluacion_logro_table.c.fecha_registro,
            "comentarios": evaluacion_logro_table.c.comentarios,
            "estudiante": relationship(Estudiante, back_populates="evaluaciones_logro"),
            "boletin": relationship(Boletin, back_populates="evaluaciones_logro"),
        }
    )

    # 13. BOLETÍN
    mapper_registry.map_imperatively(
        Boletin,
        boletin_table,
        properties={
            "estudiante": relationship(Estudiante),
            "periodo": relationship(PeriodoAcademico),
            "generador": relationship(Profesor),
            "fecha_generacion": boletin_table.c.fecha_generacion,
            "evaluaciones_logro": relationship(EvaluacionLogro, back_populates="boletin"),
        }
    )

    # 14. GESTIÓN
    mapper_registry.map_imperatively(
        Entrevista,
        entrevista_table,
        properties={
            "notas": entrevista_table.c.notas,
            "entrevistador": relationship(Profesor),
            "fecha_programada": entrevista_table.c.fecha_programada,
            "lugar": entrevista_table.c.lugar,
            "estado": entrevista_table.c.estado,
            "remitente": relationship(Directivo),
            "aspirante": relationship(Aspirante, back_populates="entrevista"),
        }
    )

    mapper_registry.map_imperatively(
        Aspirante,
        aspirante_table,
        inherits=Usuario,
        polymorphic_identity="aspirante",
        properties={
            "grado_solicitado": aspirante_table.c.grado_solicitado,
            "fecha_solicitud": aspirante_table.c.fecha_solicitud,
            "estado_proceso": aspirante_table.c.estado_proceso,
            "entrevista": relationship(Entrevista, back_populates="aspirante", uselist=False),
        }
    )

    mapper_registry.map_imperatively(
        Citacion,
        citacion_table,
        properties={
            "fecha_programada": citacion_table.c.fecha_programada,
            "correo_destinatarios": citacion_table.c.correo_destinatarios,
            "motivo": citacion_table.c.motivo,
            "descripcion": citacion_table.c.descripcion,
            "lugar": citacion_table.c.lugar,
            "remitente": relationship(Directivo),
            "entrevista": relationship(Entrevista, back_populates="citacion"),
        }
    )

    mapper_registry.map_imperatively(
        Notificacion,
        notificacion_table,
        properties={
            "fecha_envio": notificacion_table.c.fecha_envio,
            "asunto": notificacion_table.c.asunto,
            "contenido": notificacion_table.c.contenido,
            "destinatario": relationship(Acudiente),
            "citacion": relationship(Citacion),
        }
    )

    mapper_registry.map_imperatively(
        Anotacion,
        anotacion_table,
        properties={
            "fecha": anotacion_table.c.fecha,
            "descripcion": anotacion_table.c.descripcion,
            "autor": relationship(Profesor),
            "tipo": anotacion_table.c.tipo,
            "observador": relationship(Observador, back_populates="anotaciones"),
        }
    )

    # 15. COMPLETAR RELACIONES FINALES
    mapper_registry.map_imperatively(
        HojaVidaAcademica,
        hoja_vida_table,
        properties={
            "estudiante": relationship(Estudiante, back_populates="hoja_vida"),
            "promedio_general": hoja_vida_table.c.promedio_general,
            "logros": relationship(Logro, secondary=hoja_vida_logro_table),
            "grupos": relationship(Grupo, secondary=hoja_vida_grupo_table),
        }
    )

    mapper_registry.map_imperatively(
        Observador,
        observador_table,
        properties={
            "estudiante": relationship(Estudiante, back_populates="observador"),
            "comportamiento_general": observador_table.c.comportamiento_general,
            "anotaciones": relationship(Anotacion, back_populates="observador"),
        }
    )

    mapper_registry.map_imperatively(
        Estudiante,
        estudiante_table,
        inherits=Usuario,
        polymorphic_identity="estudiante",
        properties={
            "fecha_ingreso": estudiante_table.c.fecha_ingreso,
            "codigo_matricula": estudiante_table.c.codigo_matricula,
            "grupo": relationship(Grupo, back_populates="estudiantes"),
            "acudientes": relationship(Acudiente, secondary=estudiante_acudiente_table, back_populates="estudiantes"),
            "hoja_vida": relationship(HojaVidaAcademica, uselist=False, back_populates="estudiante"),
            "observador": relationship(Observador, uselist=False, back_populates="estudiante"),
            "evaluaciones_logro": relationship(EvaluacionLogro, back_populates="estudiante"),
        }
    )

    mapper_registry.map_imperatively(
        Grado,
        grado_table,
        properties={
            "nombre": grado_table.c.nombre,
            "grupos": relationship(Grupo, back_populates="grado"),
        }
    )

    mapper_registry.map_imperatively(
        CategoriaLogro,
        categoria_logro_table,
        properties={
            "nombre": categoria_logro_table.c.nombre,
            "descripcion": categoria_logro_table.c.descripcion,
            "creador": relationship(Directivo),
            "logros": relationship(Logro, back_populates="categoria"),
        }
    )

    mapper_registry.map_imperatively(
        Logro,
        logro_table,
        properties={
            "titulo": logro_table.c.titulo,
            "descripcion": logro_table.c.descripcion,
            "fecha_creacion": logro_table.c.fecha_creacion,
            "creador": relationship(Directivo),
            "estado": logro_table.c.estado,
            "categoria": relationship(CategoriaLogro, back_populates="logros"),
            "evaluaciones": relationship(EvaluacionLogro, back_populates="logro"),
        }
    )

    mapper_registry.map_imperatively(
        RespuestaFormPre,
        respuesta_form_pre_table,
        properties={
            "aspirante": relationship(Aspirante),
            "fecha_respuesta": respuesta_form_pre_table.c.fecha_respuesta,
            "respuestas": respuesta_form_pre_table.c.respuestas,
        }
    )

    # Relaciones Rol-Usuario (al final)
    mapper_registry.map_imperatively(
        Rol,
        rol_table,
        properties={
            "id_rol": rol_table.c.id_rol,
            "nombre_rol": rol_table.c.nombre_rol,
            "descripcion_rol": rol_table.c.descripcion_rol,
            "permisos": relationship(Permiso, secondary=rol_permiso_table),
            "usuarios": relationship(Usuario, back_populates="rol"),
        }
    )
