from typing import Type, TypeVar, Generic, List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_, select, or_, cast, String

T = TypeVar('T')


class Repository(Generic[T]):
    """Repositorio genérico para operaciones CRUD básicas (SQLAlchemy 2.0+)"""
    def __init__(self, session: Session, model_cls: Type[T]):
        self.session = session
        self.model_cls = model_cls

    def add(self, entity: T) -> None:
        """Agrega una entidad a la sesión"""
        self.session.add(entity)

    def get(self, id: int) -> Optional[T]:
        """Obtiene una entidad por ID"""
        return self.session.get(self.model_cls, id)

    def get_all(self) -> List[T]:
        """Obtiene todas las entidades"""
        stmt = select(self.model_cls)
        result = self.session.execute(stmt)
        return list(result.scalars().all())

    def delete(self, entity: T) -> None:
        """Elimina una entidad de la sesión"""
        self.session.delete(entity)

    def update(self, entity: T) -> None:
        """Actualiza una entidad existente"""
        self.session.merge(entity)


# ============================================
# REPOSITORIOS DE USUARIOS
# ============================================

from app.core.usuarios.usuario import Usuario
from app.core.usuarios.estudiante import Estudiante
from app.core.usuarios.profesor import Profesor
from app.core.usuarios.acudiente import Acudiente
from app.core.usuarios.aspirante import Aspirante
from app.core.usuarios.directivo import Directivo
from app.core.usuarios.administrador import Administrador
from app.core.usuarios.rol import Rol


class UsuarioRepository(Repository[Usuario]):
    """Repositorio para la entidad Usuario"""
    def __init__(self, session: Session):
        super().__init__(session, Usuario)

    def get_by_email(self, email: str) -> Optional[Usuario]:
        """Obtiene un usuario por su correo electrónico con rol y permisos cargados"""
        from sqlalchemy.orm import selectinload
        
        stmt = (
            select(Usuario)
            .where(Usuario.correo_electronico == email)
            .options(
                selectinload(Usuario.rol).selectinload(Rol.permisos)
            )
        )
        result = self.session.execute(stmt)
        return result.scalar_one_or_none()


class EstudianteRepository(Repository[Estudiante]):
    """Repositorio para la entidad Estudiante"""
    def __init__(self, session: Session):
        super().__init__(session, Estudiante)

    def get_by_codigo(self, codigo: str) -> Optional[Estudiante]:
        """Obtiene un estudiante por su código de matrícula"""
        stmt = select(Estudiante).where(Estudiante.codigo_matricula == codigo)
        result = self.session.execute(stmt)
        return result.scalar_one_or_none()

    def get_by_grupo(self, grupo_id: int) -> List[Estudiante]:
        """Obtiene todos los estudiantes de un grupo específico"""
        stmt = select(Estudiante).where(Estudiante.id_grupo == grupo_id)
        result = self.session.execute(stmt)
        return list(result.scalars().all())


class ProfesorRepository(Repository[Profesor]):
    """Repositorio para la entidad Profesor"""
    def __init__(self, session: Session):
        super().__init__(session, Profesor)

    def get_by_grupo(self, grupo_id: int) -> List[Profesor]:
        """Obtiene todos los profesores asignados a un grupo"""
        # Importar aquí para evitar import circular
        from app.data.mappers import profesor_grupo_table
        from app.core.academico.grupo import Grupo
        
        stmt = (
            select(Profesor)
            .join(profesor_grupo_table, Profesor.id_profesor == profesor_grupo_table.c.id_profesor)
            .join(Grupo, profesor_grupo_table.c.id_grupo == Grupo.id_grupo)
            .where(Grupo.id_grupo == grupo_id)
        )
        result = self.session.execute(stmt)
        return list(result.scalars().all())


class AcudienteRepository(Repository[Acudiente]):
    """Repositorio para la entidad Acudiente"""
    def __init__(self, session: Session):
        super().__init__(session, Acudiente)

    def get_by_estudiante(self, estudiante_id: int) -> List[Acudiente]:
        """Obtiene todos los acudientes de un estudiante"""
        # Importar aquí para evitar import circular
        from app.data.mappers import estudiante_acudiente_table
        
        stmt = (
            select(Acudiente)
            .join(estudiante_acudiente_table, Acudiente.id_acudiente == estudiante_acudiente_table.c.id_acudiente)
            .join(Estudiante, estudiante_acudiente_table.c.id_estudiante == Estudiante.id_estudiante)
            .where(Estudiante.id_estudiante == estudiante_id)
        )
        result = self.session.execute(stmt)
        return list(result.scalars().all())


class AspiranteRepository(Repository[Aspirante]):
    """Repositorio para la entidad Aspirante"""
    def __init__(self, session: Session):
        super().__init__(session, Aspirante)


class DirectivoRepository(Repository[Directivo]):
    """Repositorio para la entidad Directivo"""
    def __init__(self, session: Session):
        super().__init__(session, Directivo)


class AdministradorRepository(Repository[Administrador]):
    """Repositorio para la entidad Administrador"""
    def __init__(self, session: Session):
        super().__init__(session, Administrador)


# ============================================
# REPOSITORIOS ACADÉMICOS
# ============================================

from app.core.academico.grupo import Grupo
from app.core.academico.grado import Grado
from app.core.academico.periodo import PeriodoAcademico
from app.core.academico.hoja_vida import HojaVidaAcademica
from app.core.academico.observador import Observador
from app.core.academico.anotacion import Anotacion


class GrupoRepository(Repository[Grupo]):
    """Repositorio para la entidad Grupo"""
    def __init__(self, session: Session):
        super().__init__(session, Grupo)

    def get_by_nombre(self, nombre: str) -> Optional[Grupo]:
        """Obtiene un grupo por su nombre"""
        stmt = select(Grupo).where(Grupo.nombre_grupo == nombre)
        result = self.session.execute(stmt)
        return result.scalar_one_or_none()


class GradoRepository(Repository[Grado]):
    """Repositorio para la entidad Grado"""
    def __init__(self, session: Session):
        super().__init__(session, Grado)


class PeriodoAcademicoRepository(Repository[PeriodoAcademico]):
    """Repositorio para la entidad PeriodoAcademico"""
    def __init__(self, session: Session):
        super().__init__(session, PeriodoAcademico)

    def get_actual(self) -> Optional[PeriodoAcademico]:
        """Obtiene el período académico actual"""
        stmt = select(PeriodoAcademico).where(PeriodoAcademico.actual == True)
        result = self.session.execute(stmt)
        return result.scalar_one_or_none()


class HojaVidaAcademicaRepository(Repository[HojaVidaAcademica]):
    """Repositorio para la entidad HojaVidaAcademica"""
    def __init__(self, session: Session):
        super().__init__(session, HojaVidaAcademica)

    def get_by_estudiante(self, estudiante_id: int) -> Optional[HojaVidaAcademica]:
        """Obtiene la hoja de vida académica de un estudiante"""
        stmt = select(HojaVidaAcademica).where(
            HojaVidaAcademica.id_estudiante == estudiante_id
        )
        result = self.session.execute(stmt)
        return result.scalar_one_or_none()


class ObservadorRepository(Repository[Observador]):
    """Repositorio para la entidad Observador"""
    def __init__(self, session: Session):
        super().__init__(session, Observador)

    def get_by_estudiante(self, estudiante_id: int) -> Optional[Observador]:
        """Obtiene el observador de un estudiante"""
        stmt = select(Observador).where(Observador.id_estudiante == estudiante_id)
        result = self.session.execute(stmt)
        return result.scalar_one_or_none()


class AnotacionRepository(Repository[Anotacion]):
    """Repositorio para la entidad Anotacion"""
    def __init__(self, session: Session):
        super().__init__(session, Anotacion)

    def get_by_observador(self, observador_id: int) -> List[Anotacion]:
        """Obtiene todas las anotaciones de un observador"""
        stmt = select(Anotacion).where(Anotacion.id_observador == observador_id)
        result = self.session.execute(stmt)
        return list(result.scalars().all())

    def get_by_estudiante(self, estudiante_id: int) -> List[Anotacion]:
        """Obtiene todas las anotaciones de un estudiante a través de su observador"""
        stmt = (
            select(Anotacion)
            .join(Observador, Anotacion.id_observador == Observador.id_observador)
            .where(Observador.id_estudiante == estudiante_id)
        )
        result = self.session.execute(stmt)
        return list(result.scalars().all())


# ============================================
# REPOSITORIOS DE LOGROS
# ============================================

from app.core.logros.logro import Logro
from app.core.logros.categoria import CategoriaLogro
from app.core.logros.evaluacion import EvaluacionLogro
from app.core.logros.boletin import Boletin


class LogroRepository(Repository[Logro]):
    """Repositorio para la entidad Logro"""
    def __init__(self, session: Session):
        super().__init__(session, Logro)


class CategoriaLogroRepository(Repository[CategoriaLogro]):
    """Repositorio para la entidad CategoriaLogro"""
    def __init__(self, session: Session):
        super().__init__(session, CategoriaLogro)


class EvaluacionLogroRepository(Repository[EvaluacionLogro]):
    """Repositorio para la entidad EvaluacionLogro"""
    def __init__(self, session: Session):
        super().__init__(session, EvaluacionLogro)

    def get_by_estudiante_periodo(self, estudiante_id: int, periodo_id: int) -> List[EvaluacionLogro]:
        """Obtiene evaluaciones de logro de un estudiante en un período específico"""
        stmt = select(EvaluacionLogro).where(
            and_(
                EvaluacionLogro.id_estudiante == estudiante_id,
                EvaluacionLogro.id_periodo == periodo_id
            )
        )
        result = self.session.execute(stmt)
        return list(result.scalars().all())


class BoletinRepository(Repository[Boletin]):
    """Repositorio para la entidad Boletin"""
    def __init__(self, session: Session):
        super().__init__(session, Boletin)

    def get_by_estudiante_periodo(self, estudiante_id: int, periodo_id: int) -> Optional[Boletin]:
        """Obtiene el boletín de un estudiante en un período específico"""
        stmt = select(Boletin).where(
            and_(
                Boletin.id_estudiante == estudiante_id,
                Boletin.id_periodo == periodo_id
            )
        )
        result = self.session.execute(stmt)
        return result.scalar_one_or_none()


# ============================================
# REPOSITORIOS DE GESTIÓN
# ============================================

from app.core.gestion.citacion import Citacion
from app.core.gestion.notificacion import Notificacion
from app.core.gestion.entrevista import Entrevista
from app.core.gestion.respuesta_formulario import RespuestaFormPre


class CitacionRepository(Repository[Citacion]):
    """Repositorio para la entidad Citacion"""
    def __init__(self, session: Session):
        super().__init__(session, Citacion)

    def get_by_directivo(self, id_directivo: int) -> List[Citacion]:
        """Obtiene todas las citaciones enviadas por un directivo"""
        stmt = select(Citacion).where(Citacion.id_directivo_remitente == id_directivo)
        result = self.session.execute(stmt)
        return list(result.scalars().all())

    def get_by_correo(self, correo: str) -> List[Citacion]:
        """
        Obtiene citaciones por correo de destinatario.
        Nota: Funciona con PostgreSQL, MySQL 5.7+, SQLite 3.38+
        """
        # Convertir el JSON a string y buscar el correo
        stmt = select(Citacion).where(
            cast(Citacion.correo_destinatarios, String).contains(correo)
        )
        result = self.session.execute(stmt)
        return list(result.scalars().all())


class NotificacionRepository(Repository[Notificacion]):
    """Repositorio para la entidad Notificacion"""
    def __init__(self, session: Session):
        super().__init__(session, Notificacion)

    def get_by_acudiente(self, id_acudiente: int) -> List[Notificacion]:
        """Obtiene todas las notificaciones enviadas a un acudiente"""
        stmt = select(Notificacion).where(
            Notificacion.id_acudiente_destinatario == id_acudiente
        )
        result = self.session.execute(stmt)
        return list(result.scalars().all())


class EntrevistaRepository(Repository[Entrevista]):
    """Repositorio para la entidad Entrevista"""
    def __init__(self, session: Session):
        super().__init__(session, Entrevista)

    def get_by_aspirante(self, id_aspirante: int) -> Optional[Entrevista]:
        """Obtiene la entrevista de un aspirante"""
        stmt = select(Entrevista).where(Entrevista.id_aspirante == id_aspirante)
        result = self.session.execute(stmt)
        return result.scalar_one_or_none()

    def get_by_profesor(self, id_profesor: int) -> List[Entrevista]:
        """Obtiene todas las entrevistas asignadas a un profesor"""
        stmt = select(Entrevista).where(
            Entrevista.id_profesor_entrevistador == id_profesor
        )
        result = self.session.execute(stmt)
        return list(result.scalars().all())


class RespuestaFormPreRepository(Repository[RespuestaFormPre]):
    """Repositorio para la entidad RespuestaFormPre"""
    def __init__(self, session: Session):
        super().__init__(session, RespuestaFormPre)

    def get_by_correo(self, correo: str) -> List[RespuestaFormPre]:
        """Obtiene respuestas de formulario por correo"""
        stmt = select(RespuestaFormPre).where(
            RespuestaFormPre.correo_envio == correo
        )
        result = self.session.execute(stmt)
        return list(result.scalars().all())