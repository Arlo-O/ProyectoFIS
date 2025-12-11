"""
Modelos SQLAlchemy ORM para la base de datos
Estos modelos mapean las clases de dominio a las tablas de la BD
"""
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime


class RolORM(Base):
    __tablename__ = 'roles'
    
    id = Column(Integer, primary_key=True)
    nombreRol = Column(String(100), unique=True, nullable=False)
    descripcionRol = Column(String(500))
    
    usuarios = relationship('UsuarioORM', back_populates='rol')


class UsuarioORM(Base):
    __tablename__ = 'usuarios'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True, nullable=False)
    correoElectronico = Column(String(150), unique=True, nullable=False)
    contrasenaEncriptada = Column(String(255), nullable=False)
    fechaCreacion = Column(DateTime, default=datetime.now, nullable=False)
    ultimoIngreso = Column(DateTime, nullable=True)
    activo = Column(Boolean, default=True, nullable=False)
    rolId = Column(Integer, ForeignKey('roles.id'), nullable=False)
    
    rol = relationship('RolORM', back_populates='usuarios')


class PersonaORM(Base):
    __tablename__ = 'personas'
    
    id = Column(Integer, primary_key=True)
    primerNombre = Column(String(100), nullable=False)
    segundoNombre = Column(String(100))
    primerApellido = Column(String(100), nullable=False)
    segundoApellido = Column(String(100))
    tipoDocumento = Column(String(20), nullable=False)
    numeroDocumento = Column(String(50), unique=True, nullable=False)
    fechaNacimiento = Column(DateTime, nullable=False)
    genero = Column(String(20))
    direccion = Column(String(255))
    telefono = Column(String(20))


class GradoORM(Base):
    __tablename__ = 'grados'
    
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), unique=True, nullable=False)
    descripcion = Column(String(255))


class GrupoORM(Base):
    __tablename__ = 'grupos'
    
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    gradoId = Column(Integer, ForeignKey('grados.id'), nullable=False)
    profesorId = Column(Integer, ForeignKey('usuarios.id'))
    capacidad = Column(Integer, default=40)


class EstudianteORM(Base):
    __tablename__ = 'estudiantes'
    
    id = Column(Integer, primary_key=True)
    personaId = Column(Integer, ForeignKey('personas.id'), nullable=False)
    usuarioId = Column(Integer, ForeignKey('usuarios.id'))
    grupoId = Column(Integer, ForeignKey('grupos.id'))
    estado = Column(String(50), default='activo')
    fechaIngreso = Column(DateTime, default=datetime.now)


class PeriodoAcademicoORM(Base):
    __tablename__ = 'periodos_academicos'
    
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    ano = Column(Integer, nullable=False)
    fechaInicio = Column(DateTime, nullable=False)
    fechaFin = Column(DateTime, nullable=False)
    activo = Column(Boolean, default=False)


class LogroORM(Base):
    __tablename__ = 'logros'
    
    id = Column(Integer, primary_key=True)
    descripcion = Column(String(500), nullable=False)
    gradoId = Column(Integer, ForeignKey('grados.id'), nullable=False)
    asignatura = Column(String(100), nullable=False)
    nivel = Column(String(20))  # Alto, Medio, Bajo


class EvaluacionORM(Base):
    __tablename__ = 'evaluaciones'
    
    id = Column(Integer, primary_key=True)
    estudianteId = Column(Integer, ForeignKey('estudiantes.id'), nullable=False)
    periodoId = Column(Integer, ForeignKey('periodos_academicos.id'), nullable=False)
    fecha = Column(DateTime, default=datetime.now)
    observaciones = Column(String(500))


class EvaluacionLogroORM(Base):
    __tablename__ = 'evaluaciones_logros'
    
    id = Column(Integer, primary_key=True)
    evaluacionId = Column(Integer, ForeignKey('evaluaciones.id'), nullable=False)
    logroId = Column(Integer, ForeignKey('logros.id'), nullable=False)
    alcance = Column(String(20))  # Alcanzado, En proceso, No alcanzado


class NotificacionORM(Base):
    __tablename__ = 'notificaciones'
    
    id = Column(Integer, primary_key=True)
    usuarioId = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    titulo = Column(String(200), nullable=False)
    contenido = Column(String(1000), nullable=False)
    fecha = Column(DateTime, default=datetime.now)
    leida = Column(Boolean, default=False)


class CitacionORM(Base):
    __tablename__ = 'citaciones'
    
    id = Column(Integer, primary_key=True)
    estudianteId = Column(Integer, ForeignKey('estudiantes.id'), nullable=False)
    fecha = Column(DateTime, nullable=False)
    motivo = Column(String(500), nullable=False)
    estado = Column(String(50), default='pendiente')
    observaciones = Column(String(500))
