-- ============================================================
-- SCRIPT SQL PARA LIMPIAR LA BASE DE DATOS EN PGADMIN
-- ============================================================
-- Ejecutar este script en pgAdmin para limpiar toda la BD
-- y recrear la estructura con la arquitectura correcta:
-- Administrador hereda de Usuario (única herencia)
-- ============================================================

-- 1. ELIMINAR TODOS LOS DATOS (orden correcto por FKs)
DELETE FROM rol_permiso;
DELETE FROM evaluacion_logro;
DELETE FROM boletin;
DELETE FROM anotacion;
DELETE FROM observador;
DELETE FROM hoja_vida;
DELETE FROM entrevista;
DELETE FROM citacion;
DELETE FROM notificacion;
DELETE FROM respuesta_form_pre;
DELETE FROM estudiante_acudiente;
DELETE FROM profesor_grupo;
DELETE FROM grupo;
DELETE FROM grado;
DELETE FROM logro;
DELETE FROM categoria_logro;
DELETE FROM periodo_academico;
DELETE FROM plantilla_notificacion;

-- Eliminar Personas (Profesor, Directivo, Acudiente, Aspirante, Estudiante)
DELETE FROM estudiante;
DELETE FROM profesor;
DELETE FROM directivo;
DELETE FROM acudiente;
DELETE FROM aspirante;
DELETE FROM persona;

-- Eliminar Administradores (hereda de Usuario)
DELETE FROM administrador;

-- Eliminar Usuarios y Roles
DELETE FROM usuario;
DELETE FROM permiso;
DELETE FROM rol;

-- 2. ELIMINAR TABLAS EXISTENTES (si necesitas recrear estructura)
DROP TABLE IF EXISTS rol_permiso CASCADE;
DROP TABLE IF EXISTS evaluacion_logro CASCADE;
DROP TABLE IF EXISTS boletin CASCADE;
DROP TABLE IF EXISTS anotacion CASCADE;
DROP TABLE IF EXISTS observador CASCADE;
DROP TABLE IF EXISTS hoja_vida CASCADE;
DROP TABLE IF EXISTS entrevista CASCADE;
DROP TABLE IF EXISTS citacion CASCADE;
DROP TABLE IF EXISTS notificacion CASCADE;
DROP TABLE IF EXISTS respuesta_form_pre CASCADE;
DROP TABLE IF EXISTS estudiante_acudiente CASCADE;
DROP TABLE IF EXISTS profesor_grupo CASCADE;
DROP TABLE IF EXISTS grupo CASCADE;
DROP TABLE IF EXISTS grado CASCADE;
DROP TABLE IF EXISTS logro CASCADE;
DROP TABLE IF EXISTS categoria_logro CASCADE;
DROP TABLE IF EXISTS periodo_academico CASCADE;
DROP TABLE IF EXISTS plantilla_notificacion CASCADE;

-- Eliminar tablas de Personas
DROP TABLE IF EXISTS estudiante CASCADE;
DROP TABLE IF EXISTS profesor CASCADE;
DROP TABLE IF EXISTS directivo CASCADE;
DROP TABLE IF EXISTS acudiente CASCADE;
DROP TABLE IF EXISTS aspirante CASCADE;
DROP TABLE IF EXISTS persona CASCADE;

-- Eliminar Administrador (hereda de Usuario)
DROP TABLE IF EXISTS administrador CASCADE;

-- Eliminar Usuario y Rol
DROP TABLE IF EXISTS usuario CASCADE;
DROP TABLE IF EXISTS permiso CASCADE;
DROP TABLE IF EXISTS rol CASCADE;

-- 3. REINICIAR SECUENCIAS
ALTER SEQUENCE IF EXISTS rol_id_rol_seq RESTART WITH 1;
ALTER SEQUENCE IF EXISTS permiso_id_permiso_seq RESTART WITH 1;
ALTER SEQUENCE IF EXISTS usuario_id_usuario_seq RESTART WITH 1;
ALTER SEQUENCE IF EXISTS persona_id_persona_seq RESTART WITH 1;
ALTER SEQUENCE IF EXISTS grado_id_grado_seq RESTART WITH 1;
ALTER SEQUENCE IF EXISTS grupo_id_grupo_seq RESTART WITH 1;
ALTER SEQUENCE IF EXISTS periodo_academico_id_periodo_seq RESTART WITH 1;
ALTER SEQUENCE IF EXISTS categoria_logro_id_categoria_seq RESTART WITH 1;
ALTER SEQUENCE IF EXISTS logro_id_logro_seq RESTART WITH 1;
ALTER SEQUENCE IF EXISTS evaluacion_logro_id_evaluacion_seq RESTART WITH 1;
ALTER SEQUENCE IF EXISTS boletin_id_boletin_seq RESTART WITH 1;
ALTER SEQUENCE IF EXISTS observador_id_observador_seq RESTART WITH 1;
ALTER SEQUENCE IF EXISTS anotacion_id_anotacion_seq RESTART WITH 1;
ALTER SEQUENCE IF EXISTS hoja_vida_id_hoja_vida_seq RESTART WITH 1;
ALTER SEQUENCE IF EXISTS entrevista_id_entrevista_seq RESTART WITH 1;
ALTER SEQUENCE IF EXISTS citacion_id_citacion_seq RESTART WITH 1;
ALTER SEQUENCE IF EXISTS notificacion_id_notificacion_seq RESTART WITH 1;
ALTER SEQUENCE IF EXISTS respuesta_form_pre_id_respuesta_seq RESTART WITH 1;
ALTER SEQUENCE IF EXISTS plantilla_notificacion_id_plantilla_seq RESTART WITH 1;

-- 4. RECREAR ESTRUCTURA CORRECTA

-- Tabla ROL
CREATE TABLE IF NOT EXISTS rol (
    id_rol SERIAL PRIMARY KEY,
    nombre_rol VARCHAR(50) NOT NULL UNIQUE,
    descripcion_rol VARCHAR(200)
);

-- Tabla PERMISO
CREATE TABLE IF NOT EXISTS permiso (
    id_permiso SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    descripcion VARCHAR(200)
);

-- Tabla ROL_PERMISO
CREATE TABLE IF NOT EXISTS rol_permiso (
    id_rol INTEGER REFERENCES rol(id_rol) ON DELETE CASCADE,
    id_permiso INTEGER REFERENCES permiso(id_permiso) ON DELETE CASCADE,
    PRIMARY KEY (id_rol, id_permiso)
);

-- Tabla USUARIO (base)
CREATE TABLE IF NOT EXISTS usuario (
    id_usuario SERIAL PRIMARY KEY,
    correo_electronico VARCHAR(100) NOT NULL UNIQUE,
    contrasena VARCHAR(255) NOT NULL,
    id_rol INTEGER REFERENCES rol(id_rol),
    activo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ultimo_ingreso TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_usuario_email ON usuario(correo_electronico);

-- Tabla ADMINISTRADOR (hereda de Usuario) - JOINED TABLE INHERITANCE
CREATE TABLE IF NOT EXISTS administrador (
    id_administrador INTEGER PRIMARY KEY REFERENCES usuario(id_usuario) ON DELETE CASCADE,
    primer_nombre VARCHAR(50),
    segundo_nombre VARCHAR(50),
    primer_apellido VARCHAR(50),
    segundo_apellido VARCHAR(50),
    telefono VARCHAR(20)
);

-- Tabla PERSONA (base para Profesor, Directivo, Acudiente, etc.)
CREATE TABLE IF NOT EXISTS persona (
    id_persona SERIAL PRIMARY KEY,
    tipo_identificacion VARCHAR(10),
    numero_identificacion VARCHAR(50) UNIQUE,
    primer_nombre VARCHAR(50),
    segundo_nombre VARCHAR(50),
    primer_apellido VARCHAR(50),
    segundo_apellido VARCHAR(50),
    fecha_nacimiento DATE,
    genero VARCHAR(20),
    direccion VARCHAR(200),
    telefono VARCHAR(20),
    type VARCHAR(50) NOT NULL  -- Discriminador: 'estudiante', 'profesor', 'directivo', 'acudiente', 'aspirante'
);

-- Tabla PROFESOR (hereda de Persona, tiene asociación con Usuario)
CREATE TABLE IF NOT EXISTS profesor (
    id_profesor INTEGER PRIMARY KEY REFERENCES persona(id_persona) ON DELETE CASCADE,
    id_usuario INTEGER REFERENCES usuario(id_usuario),
    especialidad VARCHAR(100),
    experiencia_anios INTEGER,
    es_director_grupo BOOLEAN DEFAULT FALSE
);

-- Tabla DIRECTIVO (hereda de Persona, tiene asociación con Usuario)
CREATE TABLE IF NOT EXISTS directivo (
    id_directivo INTEGER PRIMARY KEY REFERENCES persona(id_persona) ON DELETE CASCADE,
    id_usuario INTEGER REFERENCES usuario(id_usuario),
    cargo VARCHAR(100),
    area_responsable VARCHAR(100)
);

-- Tabla ACUDIENTE (hereda de Persona, tiene asociación con Usuario)
CREATE TABLE IF NOT EXISTS acudiente (
    id_acudiente INTEGER PRIMARY KEY REFERENCES persona(id_persona) ON DELETE CASCADE,
    id_usuario INTEGER REFERENCES usuario(id_usuario),
    parentesco VARCHAR(50)
);

-- Tabla ASPIRANTE (hereda de Persona, tiene asociación con Usuario)
CREATE TABLE IF NOT EXISTS aspirante (
    id_aspirante INTEGER PRIMARY KEY REFERENCES persona(id_persona) ON DELETE CASCADE,
    id_usuario INTEGER REFERENCES usuario(id_usuario),
    grado_solicitado VARCHAR(20),
    fecha_solicitud TIMESTAMP,
    estado_proceso VARCHAR(20)
);

-- Tabla ESTUDIANTE (hereda de Persona, NO tiene Usuario)
CREATE TABLE IF NOT EXISTS estudiante (
    id_estudiante INTEGER PRIMARY KEY REFERENCES persona(id_persona) ON DELETE CASCADE,
    codigo_matricula VARCHAR(50) UNIQUE,
    fecha_ingreso TIMESTAMP,
    grado_actual VARCHAR(20),
    id_grupo INTEGER
);

-- ============================================================
-- TABLAS ACADÉMICAS
-- ============================================================

-- Tabla GRADO
CREATE TABLE IF NOT EXISTS grado (
    id_grado SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL UNIQUE
);

-- Tabla GRUPO
CREATE TABLE IF NOT EXISTS grupo (
    id_grupo SERIAL PRIMARY KEY,
    nombre_grupo VARCHAR(50) NOT NULL,
    id_director_grupo INTEGER REFERENCES profesor(id_profesor),
    id_grado INTEGER REFERENCES grado(id_grado),
    cupo_maximo INTEGER DEFAULT 10,
    cupo_minimo INTEGER DEFAULT 5,
    activo BOOLEAN DEFAULT TRUE
);

-- Tabla PERIODO_ACADEMICO
CREATE TABLE IF NOT EXISTS periodo_academico (
    id_periodo SERIAL PRIMARY KEY,
    nombre_periodo VARCHAR(50) NOT NULL,
    fecha_inicio TIMESTAMP NOT NULL,
    fecha_fin TIMESTAMP NOT NULL,
    actual BOOLEAN DEFAULT FALSE
);

-- ============================================================
-- TABLAS DE SEGUIMIENTO ESTUDIANTIL
-- ============================================================

-- Tabla HOJA_VIDA
CREATE TABLE IF NOT EXISTS hoja_vida (
    id_hoja_vida SERIAL PRIMARY KEY,
    id_estudiante INTEGER REFERENCES estudiante(id_estudiante) UNIQUE,
    estado_salud VARCHAR(100),
    alergias JSONB,
    tratamientos JSONB,
    necesidades_educativas JSONB
);

-- Tabla OBSERVADOR
CREATE TABLE IF NOT EXISTS observador (
    id_observador SERIAL PRIMARY KEY,
    id_estudiante INTEGER REFERENCES estudiante(id_estudiante) UNIQUE,
    comportamiento_general VARCHAR(255)
);

-- Tabla ANOTACION
CREATE TABLE IF NOT EXISTS anotacion (
    id_anotacion SERIAL PRIMARY KEY,
    id_observador INTEGER REFERENCES observador(id_observador),
    id_profesor_autor INTEGER REFERENCES profesor(id_profesor),
    categoria VARCHAR(50),
    detalle VARCHAR(200),
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- TABLAS DE LOGROS Y EVALUACIÓN
-- ============================================================

-- Tabla CATEGORIA_LOGRO
CREATE TABLE IF NOT EXISTS categoria_logro (
    id_categoria SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL UNIQUE,
    descripcion VARCHAR(200),
    id_directivo_creador INTEGER REFERENCES directivo(id_directivo)
);

-- Tabla LOGRO
CREATE TABLE IF NOT EXISTS logro (
    id_logro SERIAL PRIMARY KEY,
    titulo VARCHAR(50) NOT NULL UNIQUE,
    descripcion VARCHAR(200),
    id_categoria INTEGER REFERENCES categoria_logro(id_categoria),
    id_directivo_creador INTEGER REFERENCES directivo(id_directivo),
    estado VARCHAR(20),
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla EVALUACION_LOGRO
CREATE TABLE IF NOT EXISTS evaluacion_logro (
    id_evaluacion SERIAL PRIMARY KEY,
    id_logro INTEGER REFERENCES logro(id_logro),
    id_estudiante INTEGER REFERENCES estudiante(id_estudiante),
    id_profesor INTEGER REFERENCES profesor(id_profesor),
    id_periodo INTEGER REFERENCES periodo_academico(id_periodo),
    puntuacion VARCHAR(20),
    comentarios TEXT,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla BOLETIN
CREATE TABLE IF NOT EXISTS boletin (
    id_boletin SERIAL PRIMARY KEY,
    id_estudiante INTEGER REFERENCES estudiante(id_estudiante),
    id_periodo INTEGER REFERENCES periodo_academico(id_periodo),
    id_profesor_generador INTEGER REFERENCES profesor(id_profesor),
    fecha_generacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- TABLAS DE GESTIÓN ADMINISTRATIVA
-- ============================================================

-- Tabla ENTREVISTA
CREATE TABLE IF NOT EXISTS entrevista (
    id_entrevista SERIAL PRIMARY KEY,
    id_aspirante INTEGER REFERENCES aspirante(id_aspirante),
    id_profesor_entrevistador INTEGER REFERENCES profesor(id_profesor),
    id_directivo_remitente INTEGER REFERENCES directivo(id_directivo),
    fecha_programada TIMESTAMP,
    lugar VARCHAR(100),
    estado VARCHAR(50),
    notas TEXT
);

-- Tabla CITACION
CREATE TABLE IF NOT EXISTS citacion (
    id_citacion SERIAL PRIMARY KEY,
    id_directivo_remitente INTEGER REFERENCES directivo(id_directivo),
    fecha_programada TIMESTAMP,
    motivo VARCHAR(100),
    descripcion TEXT,
    lugar VARCHAR(100),
    correo_destinatarios JSONB
);

-- Tabla NOTIFICACION
CREATE TABLE IF NOT EXISTS notificacion (
    id_notificacion SERIAL PRIMARY KEY,
    id_citacion INTEGER REFERENCES citacion(id_citacion),
    id_acudiente_destinatario INTEGER REFERENCES acudiente(id_acudiente),
    fecha_envio TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    asunto VARCHAR(100),
    contenido TEXT
);

-- Tabla RESPUESTA_FORM_PRE (formularios de preinscripción)
CREATE TABLE IF NOT EXISTS respuesta_form_pre (
    id_respuesta SERIAL PRIMARY KEY,
    fecha_solicitud TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    grado_solicitado VARCHAR(50),
    colegio_anterior VARCHAR(100),
    datos_acudiente JSONB,
    datos_aspirante JSONB,
    correo_envio VARCHAR(100),
    telefono_contacto VARCHAR(20)
);

-- Tabla PLANTILLA_NOTIFICACION (opcional, si existe en el sistema)
CREATE TABLE IF NOT EXISTS plantilla_notificacion (
    id_plantilla SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    asunto VARCHAR(200),
    contenido TEXT,
    tipo VARCHAR(50),
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- TABLAS DE RELACIÓN MANY-TO-MANY
-- ============================================================

-- Tabla ESTUDIANTE_ACUDIENTE
CREATE TABLE IF NOT EXISTS estudiante_acudiente (
    id_estudiante INTEGER REFERENCES estudiante(id_estudiante) ON DELETE CASCADE,
    id_acudiente INTEGER REFERENCES acudiente(id_acudiente) ON DELETE CASCADE,
    PRIMARY KEY (id_estudiante, id_acudiente)
);

-- Tabla PROFESOR_GRUPO
CREATE TABLE IF NOT EXISTS profesor_grupo (
    id_profesor INTEGER REFERENCES profesor(id_profesor) ON DELETE CASCADE,
    id_grupo INTEGER REFERENCES grupo(id_grupo) ON DELETE CASCADE,
    PRIMARY KEY (id_profesor, id_grupo)
);

-- ============================================================
-- AGREGAR FK DE ESTUDIANTE A GRUPO (después de crear grupo)
-- ============================================================
ALTER TABLE estudiante DROP CONSTRAINT IF EXISTS estudiante_id_grupo_fkey;
ALTER TABLE estudiante ADD CONSTRAINT estudiante_id_grupo_fkey 
    FOREIGN KEY (id_grupo) REFERENCES grupo(id_grupo) ON DELETE SET NULL;

-- 5. INSERTAR ROLES INICIALES (solo si no existen)
INSERT INTO rol (nombre_rol, descripcion_rol) VALUES
    ('administrador', 'Administrador del sistema con acceso total'),
    ('director', 'Director de la institución'),
    ('profesor', 'Docente de la institución'),
    ('acudiente', 'Acudiente o padre de familia'),
    ('aspirante', 'Aspirante a la institución')
ON CONFLICT (nombre_rol) DO NOTHING;

-- ============================================================
-- OTORGAR PERMISOS AL USUARIO fis_user
-- ============================================================
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO fis_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO fis_user;
GRANT ALL PRIVILEGES ON SCHEMA public TO fis_user;

-- ============================================================
-- SCRIPT COMPLETADO
-- ============================================================
-- ✅ Base de datos completamente limpia y recreada
-- ✅ Todas las tablas creadas con estructura correcta
-- ✅ Roles iniciales insertados
-- ✅ Permisos otorgados a fis_user
--
-- SIGUIENTE PASO:
-- python scripts/reiniciar_bd_completa.py
-- ============================================================
