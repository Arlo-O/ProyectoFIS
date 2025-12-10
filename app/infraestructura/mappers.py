from sqlalchemy import Table, Column, Integer, String, Date, ForeignKey, Boolean, DateTime, Text, JSON
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
    Column("numero_identificacion", String, unique=True, nullable=False),
    Column("tipo_identificacion", String, nullable=False),
    Column("primer_nombre", String, nullable=False),
    Column("segundo_nombre", String),
    Column("primer_apellido", String, nullable=False),
    Column("segundo_apellido", String),
    Column("fecha_nacimiento", DateTime, nullable=False),
    Column("telefono", String),
    Column("direccion", String),
    Column("genero", String),
    Column("type", String, nullable=False),  # Discriminator
)

usuario_table = Table(
    "usuario",
    mapper_registry.metadata,
    Column("id_usuario", Integer, ForeignKey("persona.id_persona"), primary_key=True),
    Column("contrasena", String, nullable=False),
    Column("correo_electronico", String, unique=True, nullable=False),
    Column("id_rol", Integer, ForeignKey("rol.id_rol")),
    Column("activo", Boolean, default=True),
    Column("fecha_creacion", DateTime),
    Column("ultimo_ingreso", DateTime),
)

rol_table = Table(
    "rol",
    mapper_registry.metadata,
    Column("id_rol", Integer, primary_key=True, autoincrement=True),
    Column("nombre_rol", String, nullable=False),
    Column("descripcion_rol", String),
)

permiso_table = Table(
    "permiso",
    mapper_registry.metadata,
    Column("id_permiso", Integer, primary_key=True, autoincrement=True),
    Column("nombre_permiso", String, nullable=False),
    Column("descripcion", String),
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
    Column("codigo_matricula", String, unique=True),
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
    Column("parentesco", String),
    Column("es_aspirante", Boolean, default=False),
)

aspirante_table = Table(
    "aspirante",
    mapper_registry.metadata,
    Column("id_aspirante", Integer, ForeignKey("usuario.id_usuario"), primary_key=True),
    Column("grado_solicitado", String),
    Column("fecha_solicitud", DateTime),
    Column("estado_proceso", String),
)

directivo_table = Table(
    "directivo",
    mapper_registry.metadata,
    Column("id_directivo", Integer, ForeignKey("usuario.id_usuario"), primary_key=True),
    Column("cargo", String),
    Column("area_responsable", String),
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
    Column("nombre_grupo", String, nullable=False),
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
    Column("nombre", String, nullable=False),
)

logro_table = Table(
    "logro",
    mapper_registry.metadata,
    Column("id_logro", Integer, primary_key=True, autoincrement=True),
    Column("titulo", String),
    Column("descripcion", String),
    Column("fecha_creacion", DateTime),
    Column("id_creador", Integer, ForeignKey("directivo.id_directivo")),
    Column("estado", String),
    Column("id_categoria", Integer, ForeignKey("categoria_logro.id_categoria")),
)

categoria_logro_table = Table(
    "categoria_logro",
    mapper_registry.metadata,
    Column("id_categoria", Integer, primary_key=True, autoincrement=True),
    Column("nombre", String),
    Column("descripcion", String),
    Column("id_creador", Integer, ForeignKey("directivo.id_directivo")),
)

evaluacion_logro_table = Table(
    "evaluacion_logro",
    mapper_registry.metadata,
    Column("id_evaluacion", Integer, primary_key=True, autoincrement=True),
    Column("id_logro", Integer, ForeignKey("logro.id_logro")),
    Column("id_profesor", Integer, ForeignKey("profesor.id_profesor")),
    Column("id_periodo", Integer, ForeignKey("periodo_academico.id_periodo")),
    Column("puntuacion", String),
    Column("fecha_registro", DateTime),
    Column("comentarios", JSON), # Changed to JSON
    Column("id_estudiante", Integer, ForeignKey("estudiante.id_estudiante")), # Linked to student
    Column("id_boletin", Integer, ForeignKey("boletin.id_boletin")), # Linked to boletin
)

periodo_academico_table = Table(
    "periodo_academico",
    mapper_registry.metadata,
    Column("id_periodo", Integer, primary_key=True, autoincrement=True),
    Column("nombre_periodo", String),
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
    Column("correo_destinatarios", JSON), # Changed to JSON
    Column("motivo", String),
    Column("descripcion", String),
    Column("lugar", String),
    Column("id_remitente", Integer, ForeignKey("directivo.id_directivo")),
    Column("id_entrevista", Integer, ForeignKey("entrevista.id_entrevista")), # If linked
)

notificacion_table = Table(
    "notificacion",
    mapper_registry.metadata,
    Column("id_notificacion", Integer, primary_key=True, autoincrement=True),
    Column("fecha_envio", DateTime),
    Column("asunto", String),
    Column("contenido", String),
    Column("id_destinatario", Integer, ForeignKey("acudiente.id_acudiente")),
    Column("id_citacion", Integer, ForeignKey("citacion.id_citacion")),
)

entrevista_table = Table(
    "entrevista",
    mapper_registry.metadata,
    Column("id_entrevista", Integer, primary_key=True, autoincrement=True),
    Column("notas", String),
    Column("id_entrevistador", Integer, ForeignKey("profesor.id_profesor")),
    Column("fecha_programada", DateTime),
    Column("lugar", String),
    Column("estado", String),
    Column("id_remitente", Integer, ForeignKey("directivo.id_directivo")),
    Column("id_aspirante", Integer, ForeignKey("aspirante.id_aspirante")),
)

anotacion_table = Table(
    "anotacion",
    mapper_registry.metadata,
    Column("id_anotacion", Integer, primary_key=True, autoincrement=True),
    Column("fecha", DateTime),
    Column("descripcion", String),
    Column("id_autor", Integer, ForeignKey("profesor.id_profesor")),
    Column("tipo", String),
    Column("id_observador", Integer, ForeignKey("observador.id_observador")),
)

hoja_vida_table = Table(
    "hoja_vida",
    mapper_registry.metadata,
    Column("id_hoja_vida", Integer, primary_key=True, autoincrement=True),
    Column("id_estudiante", Integer, ForeignKey("estudiante.id_estudiante"), unique=True),
    Column("promedio_general", Integer), # Float actually
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
    Column("comportamiento_general", String),
)

respuesta_form_pre_table = Table(
    "respuesta_form_pre",
    mapper_registry.metadata,
    Column("id_respuesta", Integer, primary_key=True, autoincrement=True),
    Column("id_aspirante", Integer, ForeignKey("aspirante.id_aspirante")),
    Column("fecha_respuesta", DateTime),
    Column("respuestas", JSON), # Changed to JSON
)



def start_mappers():
    mapper_registry.map_imperatively(
        Permiso,
        permiso_table,
        properties={
            "_Permiso__idPermiso": permiso_table.c.id_permiso,
            "_Permiso__nombrePermiso": permiso_table.c.nombre_permiso,
            "_Permiso__descripcion": permiso_table.c.descripcion,
        }
    )

    mapper_registry.map_imperatively(
        Rol,
        rol_table,
        properties={
            "_Rol__idRol": rol_table.c.id_rol,
            "_Rol__nombreRol": rol_table.c.nombre_rol,
            "_Rol__descripcionRol": rol_table.c.descripcion_rol,
            "_Rol__permisos": relationship(Permiso, secondary=rol_permiso_table),
        }
    )

    mapper_registry.map_imperatively(
        Persona,
        persona_table,
        polymorphic_on=persona_table.c.type,
        polymorphic_identity="persona",
        properties={
            "_primerNombre": persona_table.c.primer_nombre,
            "_segundoNombre": persona_table.c.segundo_nombre,
            "_primerApellido": persona_table.c.primer_apellido,
            "_segundoApellido": persona_table.c.segundo_apellido,
            "_tipoDocumento": persona_table.c.tipo_identificacion,
            "_numeroDocumento": persona_table.c.numero_identificacion,
            "_fechaNacimiento": persona_table.c.fecha_nacimiento,
            "_genero": persona_table.c.genero,
            "_direccion": persona_table.c.direccion,
            "_telefono": persona_table.c.telefono,
        }
    )

    mapper_registry.map_imperatively(
        Usuario,
        usuario_table,
        inherits=Persona,
        polymorphic_identity="usuario",
        properties={
            "_Usuario__idUsuario": usuario_table.c.id_usuario,
            "_Usuario__contrasenaEncriptada": usuario_table.c.contrasena,
            "_Usuario__correoElectronico": usuario_table.c.correo_electronico,
            "_Usuario__activo": usuario_table.c.activo,
            "_Usuario__fechaCreacion": usuario_table.c.fecha_creacion,
            "_Usuario__ultimoIngreso": usuario_table.c.ultimo_ingreso,
            "_Usuario__rol": relationship(Rol),
        }
    )

    mapper_registry.map_imperatively(
        Estudiante,
        estudiante_table,
        inherits=Usuario,
        polymorphic_identity="estudiante",
        properties={
            "_Estudiante__idEstudiante": estudiante_table.c.id_estudiante,
            "_Estudiante__fechaIngreso": estudiante_table.c.fecha_ingreso,
            "_Estudiante__codigoMatricula": estudiante_table.c.codigo_matricula,
            "_Estudiante__grupo": relationship(Grupo, back_populates="_Grupo__estudiantes"),
            "_Estudiante__acudientes": relationship(Acudiente, secondary=estudiante_acudiente_table, back_populates="_Acudiente__representados"),
            "_Estudiante__hojaVida": relationship(HojaVidaAcademica, uselist=False, back_populates="_HojaVidaAcademica__estudiante"),
            "_Estudiante__observador": relationship(Observador, uselist=False, back_populates="_Observador__estudiante"),
            "_Estudiante__logrosObtenidos": relationship(EvaluacionLogro), # Assuming One-to-Many from Estudiante to EvaluacionLogro
        }
    )

    mapper_registry.map_imperatively(
        Profesor,
        profesor_table,
        inherits=Usuario,
        polymorphic_identity="profesor",
        properties={
            "_Profesor__idProfesor": profesor_table.c.id_profesor,
            "_Profesor__esDirectorGrupo": profesor_table.c.es_director_grupo,
            "_Profesor__gruposAsignados": relationship(Grupo, secondary=profesor_grupo_table),
        }
    )

    mapper_registry.map_imperatively(
        Acudiente,
        acudiente_table,
        inherits=Usuario,
        polymorphic_identity="acudiente",
        properties={
            "_Acudiente__idAcudiente": acudiente_table.c.id_acudiente,
            "_Acudiente__parentesco": acudiente_table.c.parentesco,
            "_Acudiente__esAspirante": acudiente_table.c.es_aspirante,
            "_Acudiente__representados": relationship(Estudiante, secondary=estudiante_acudiente_table, back_populates="_Estudiante__acudientes"), # Mapping to Persona/Estudiante
        }
    )

    mapper_registry.map_imperatively(
        Aspirante,
        aspirante_table,
        inherits=Usuario,
        polymorphic_identity="aspirante",
        properties={
            "_Aspirante__idAspirante": aspirante_table.c.id_aspirante,
            "_Aspirante__gradoSolicitado": aspirante_table.c.grado_solicitado,
            "_Aspirante__fechaSolicitud": aspirante_table.c.fecha_solicitud,
            "_Aspirante__estadoProceso": aspirante_table.c.estado_proceso,
            "_Aspirante__entrevista": relationship(Entrevista, uselist=False, back_populates="_Entrevista__aspirante"),
        }
    )

    mapper_registry.map_imperatively(
        Directivo,
        directivo_table,
        inherits=Usuario,
        polymorphic_identity="directivo",
        properties={
            "_Directivo__idDirectivo": directivo_table.c.id_directivo,
            "_Directivo__cargo": directivo_table.c.cargo,
            "_Directivo__areaResponsable": directivo_table.c.area_responsable,
        }
    )

    mapper_registry.map_imperatively(
        Administrador,
        administrador_table,
        inherits=Usuario,
        polymorphic_identity="administrador",
        properties={
            "_Administrador__idAdministrador": administrador_table.c.id_administrador,
        }
    )

    mapper_registry.map_imperatively(
        Grupo,
        grupo_table,
        properties={
            "_Grupo__idGrupo": grupo_table.c.id_grupo,
            "_Grupo__nombreGrupo": grupo_table.c.nombre_grupo,
            "_Grupo__directorGrupo": relationship(Profesor),
            "_Grupo__creador": relationship(Directivo),
            "_Grupo__cupoMaximo": grupo_table.c.cupo_maximo,
            "_Grupo__cupoMinimo": grupo_table.c.cupo_minimo,
            "_Grupo__activo": grupo_table.c.activo,
            "_Grupo__estudiantes": relationship(Estudiante, back_populates="_Estudiante__grupo"),
        }
    )

    mapper_registry.map_imperatively(
        Grado,
        grado_table,
        properties={
            "_Grado__idGrado": grado_table.c.id_grado,
            "_Grado__nombre": grado_table.c.nombre,
            "_Grado__grupos": relationship(Grupo),
        }
    )

    mapper_registry.map_imperatively(
        Logro,
        logro_table,
        properties={
            "_Logro__idLogro": logro_table.c.id_logro,
            "_Logro__titulo": logro_table.c.titulo,
            "_Logro__descripcion": logro_table.c.descripcion,
            "_Logro__fechaCreacion": logro_table.c.fecha_creacion,
            "_Logro__creador": relationship(Directivo),
            "_Logro__estado": logro_table.c.estado,
        }
    )

    mapper_registry.map_imperatively(
        CategoriaLogro,
        categoria_logro_table,
        properties={
            "_CategoriaLogro__idCategoria": categoria_logro_table.c.id_categoria,
            "_CategoriaLogro__nombre": categoria_logro_table.c.nombre,
            "_CategoriaLogro__descripcion": categoria_logro_table.c.descripcion,
            "_CategoriaLogro__creador": relationship(Directivo),
            "_CategoriaLogro__logros": relationship(Logro),
        }
    )

    mapper_registry.map_imperatively(
        EvaluacionLogro,
        evaluacion_logro_table,
        properties={
            "_EvaluacionLogro__idEvaluacion": evaluacion_logro_table.c.id_evaluacion,
            "_EvaluacionLogro__logro": relationship(Logro),
            "_EvaluacionLogro__profesor": relationship(Profesor),
            "_EvaluacionLogro__periodo": relationship(PeriodoAcademico),
            "_EvaluacionLogro__puntuacion": evaluacion_logro_table.c.puntuacion,
            "_EvaluacionLogro__fechaRegistro": evaluacion_logro_table.c.fecha_registro,
            "_EvaluacionLogro__comentarios": evaluacion_logro_table.c.comentarios, # Need to handle JSON/List conversion if needed
        }
    )

    mapper_registry.map_imperatively(
        PeriodoAcademico,
        periodo_academico_table,
        properties={
            "_PeriodoAcademico__idPeriodo": periodo_academico_table.c.id_periodo,
            "_PeriodoAcademico__nombrePeriodo": periodo_academico_table.c.nombre_periodo,
            "_PeriodoAcademico__fechaInicio": periodo_academico_table.c.fecha_inicio,
            "_PeriodoAcademico__fechaFin": periodo_academico_table.c.fecha_fin,
            "_PeriodoAcademico__actual": periodo_academico_table.c.actual,
        }
    )

    mapper_registry.map_imperatively(
        Boletin,
        boletin_table,
        properties={
            "_Boletin__idBoletin": boletin_table.c.id_boletin,
            "_Boletin__estudiante": relationship(Estudiante),
            "_Boletin__periodo": relationship(PeriodoAcademico),
            "_Boletin__generadoPor": relationship(Profesor),
            "_Boletin__fechaGeneracion": boletin_table.c.fecha_generacion,
            "_Boletin__calificaciones": relationship(EvaluacionLogro),
        }
    )

    mapper_registry.map_imperatively(
        Citacion,
        citacion_table,
        properties={
            "_Citacion__idCitacion": citacion_table.c.id_citacion,
            "_Citacion__fechaProgramada": citacion_table.c.fecha_programada,
            "_Citacion__correoDestinatarios": citacion_table.c.correo_destinatarios,
            "_Citacion__motivo": citacion_table.c.motivo,
            "_Citacion__descripcion": citacion_table.c.descripcion,
            "_Citacion__lugar": citacion_table.c.lugar,
            "_Citacion__remitente": relationship(Directivo),
            "_Citacion__notificacion": relationship(Notificacion),
        }
    )

    mapper_registry.map_imperatively(
        Notificacion,
        notificacion_table,
        properties={
            "_Notificacion__idNotificacion": notificacion_table.c.id_notificacion,
            "_Notificacion__fechaEnvio": notificacion_table.c.fecha_envio,
            "_Notificacion__asunto": notificacion_table.c.asunto,
            "_Notificacion__contenido": notificacion_table.c.contenido,
            "_Notificacion__destinatario": relationship(Acudiente),
        }
    )

    mapper_registry.map_imperatively(
        Entrevista,
        entrevista_table,
        properties={
            "_Entrevista__idEntrevista": entrevista_table.c.id_entrevista,
            "_Entrevista__notas": entrevista_table.c.notas,
            "_Entrevista__entrevistador": relationship(Profesor),
            "_Entrevista__fechaProgramada": entrevista_table.c.fecha_programada,
            "_Entrevista__lugar": entrevista_table.c.lugar,
            "_Entrevista__estado": entrevista_table.c.estado,
            "_Entrevista__remitente": relationship(Directivo),
            "_Entrevista__citacion": relationship(Citacion), # If linked
            "_Entrevista__aspirante": relationship(Aspirante, back_populates="_Aspirante__entrevista"),
        }
    )

    mapper_registry.map_imperatively(
        Anotacion,
        anotacion_table,
        properties={
            "_Anotacion__idAnotacion": anotacion_table.c.id_anotacion,
            "_Anotacion__fecha": anotacion_table.c.fecha,
            "_Anotacion__descripcion": anotacion_table.c.descripcion,
            "_Anotacion__autor": relationship(Profesor),
            "_Anotacion__tipo": anotacion_table.c.tipo,
        }
    )

    mapper_registry.map_imperatively(
        HojaVidaAcademica,
        hoja_vida_table,
        properties={
            "_HojaVidaAcademica__idHojaVida": hoja_vida_table.c.id_hoja_vida,
            "_HojaVidaAcademica__estudiante": relationship(Estudiante, back_populates="_Estudiante__hojaVida"),
            "_HojaVidaAcademica__promedioGeneral": hoja_vida_table.c.promedio_general,
            "_HojaVidaAcademica__logrosDestacados": relationship(Logro, secondary=hoja_vida_logro_table),
            "_HojaVidaAcademica__historialGrupos": relationship(Grupo, secondary=hoja_vida_grupo_table),
        }
    )

    mapper_registry.map_imperatively(
        Observador,
        observador_table,
        properties={
            "_Observador__idObservador": observador_table.c.id_observador,
            "_Observador__estudiante": relationship(Estudiante, back_populates="_Estudiante__observador"),
            "_Observador__comportamientoGeneral": observador_table.c.comportamiento_general,
            "_Observador__anotaciones": relationship(Anotacion),
        }
    )

    mapper_registry.map_imperatively(
        RespuestaFormPre,
        respuesta_form_pre_table,
        properties={
            "_RespuestaFormPre__idRespuesta": respuesta_form_pre_table.c.id_respuesta,
            "_RespuestaFormPre__aspirante": relationship(Aspirante),
            "_RespuestaFormPre__fechaRespuesta": respuesta_form_pre_table.c.fecha_respuesta,
            "_RespuestaFormPre__respuestas": respuesta_form_pre_table.c.respuestas,
        }
    )
