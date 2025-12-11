from typing import Type, TypeVar, Generic, List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_


from app.modelos.usuarios.usuario import Usuario
from app.modelos.usuarios.estudiante import Estudiante
from app.modelos.usuarios.profesor import Profesor
from app.modelos.usuarios.acudiente import Acudiente
from app.modelos.usuarios.aspirante import Aspirante
from app.modelos.usuarios.directivo import Directivo
from app.modelos.usuarios.administrador import Administrador

from app.modelos.academico.grupo import Grupo
from app.modelos.academico.grado import Grado
from app.modelos.academico.periodoAcademico import PeriodoAcademico
from app.modelos.academico.hojaVidaAcademica import HojaVidaAcademica
from app.modelos.academico.observador import Observador
from app.modelos.academico.anotacion import Anotacion

from app.modelos.logros.logro import Logro
from app.modelos.logros.categoriaLogro import CategoriaLogro
from app.modelos.logros.evaluacionLogro import EvaluacionLogro
from app.modelos.logros.boletin import Boletin

from app.modelos.gestion.citacion import Citacion
from app.modelos.gestion.notificacion import Notificacion
from app.modelos.gestion.entrevista import Entrevista
from app.modelos.gestion.respuestaFormPre import RespuestaFormPre


T = TypeVar('T')


class Repository(Generic[T]):
    def __init__(self, session: Session, model_cls: Type[T]):
        self.session = session
        self.model_cls = model_cls

    def add(self, entity: T) -> None:
        self.session.add(entity)

    def get(self, id: int) -> Optional[T]:
        return self.session.get(self.model_cls, id)

    def get_all(self) -> List[T]:
        return self.session.query(self.model_cls).all()

    def delete(self, entity: T) -> None:
        self.session.delete(entity)

    def update(self, entity: T) -> None:
        self.session.merge(entity)


class UsuarioRepository(Repository[Usuario]):
    def __init__(self, session: Session):
        super().__init__(session, Usuario)

    def get_by_email(self, email: str) -> Optional[Usuario]:
        return self.session.query(Usuario).filter_by(correo_electronico=email).first()


class EstudianteRepository(Repository[Estudiante]):
    def __init__(self, session: Session):
        super().__init__(session, Estudiante)

    def get_by_codigo(self, codigo: str) -> Optional[Estudiante]:
        return self.session.query(Estudiante).filter_by(codigo_matricula=codigo).first()

    def get_by_grupo(self, grupo_id: int) -> List[Estudiante]:
        return self.session.query(Estudiante).filter(Estudiante.grupo_id == grupo_id).all()


class ProfesorRepository(Repository[Profesor]):
    def __init__(self, session: Session):
        super().__init__(session, Profesor)

    def get_by_grupo(self, grupo_id: int) -> List[Profesor]:
        return self.session.query(Profesor).join(Profesor.grupos_asignados).filter(Grupo.id_grupo == grupo_id).all()


class AcudienteRepository(Repository[Acudiente]):
    def __init__(self, session: Session):
        super().__init__(session, Acudiente)

    def get_by_estudiante(self, estudiante_id: int) -> List[Acudiente]:
        return self.session.query(Acudiente).join(Acudiente.estudiantes).filter(Estudiante.id_estudiante == estudiante_id).all()


class AspiranteRepository(Repository[Aspirante]):
    def __init__(self, session: Session):
        super().__init__(session, Aspirante)


class DirectivoRepository(Repository[Directivo]):
    def __init__(self, session: Session):
        super().__init__(session, Directivo)


class AdministradorRepository(Repository[Administrador]):
    def __init__(self, session: Session):
        super().__init__(session, Administrador)


class GrupoRepository(Repository[Grupo]):
    def __init__(self, session: Session):
        super().__init__(session, Grupo)

    def get_by_nombre(self, nombre: str) -> Optional[Grupo]:
        return self.session.query(Grupo).filter_by(nombre_grupo=nombre).first()


class GradoRepository(Repository[Grado]):
    def __init__(self, session: Session):
        super().__init__(session, Grado)


class PeriodoAcademicoRepository(Repository[PeriodoAcademico]):
    def __init__(self, session: Session):
        super().__init__(session, PeriodoAcademico)

    def get_actual(self) -> Optional[PeriodoAcademico]:
        return self.session.query(PeriodoAcademico).filter_by(actual=True).first()


class LogroRepository(Repository[Logro]):
    def __init__(self, session: Session):
        super().__init__(session, Logro)


class CategoriaLogroRepository(Repository[CategoriaLogro]):
    def __init__(self, session: Session):
        super().__init__(session, CategoriaLogro)


class EvaluacionLogroRepository(Repository[EvaluacionLogro]):
    def __init__(self, session: Session):
        super().__init__(session, EvaluacionLogro)

    def get_by_estudiante_periodo(self, estudiante_id: int, periodo_id: int) -> List[EvaluacionLogro]:
        return self.session.query(EvaluacionLogro).filter(
            and_(EvaluacionLogro.id_estudiante == estudiante_id, EvaluacionLogro.id_periodo == periodo_id)
        ).all()


class BoletinRepository(Repository[Boletin]):
    def __init__(self, session: Session):
        super().__init__(session, Boletin)

    def get_by_estudiante_periodo(self, estudiante_id: int, periodo_id: int) -> Optional[Boletin]:
        return self.session.query(Boletin).filter(
            and_(Boletin.id_estudiante == estudiante_id, Boletin.id_periodo == periodo_id)
        ).first()


class CitacionRepository(Repository[Citacion]):
    def __init__(self, session: Session):
        super().__init__(session, Citacion)

    def get_by_directivo(self, id_directivo: int) -> List[Citacion]:
        return self.session.query(Citacion).filter(
            Citacion.id_remitente == id_directivo
        ).all()

    def get_by_correo(self, correo: str) -> List[Citacion]:
        return self.session.query(Citacion).filter(
            Citacion.correo_destinatarios.contains(correo)  # PostgreSQL JSON
        ).all()


class NotificacionRepository(Repository[Notificacion]):
    def __init__(self, session: Session):
        super().__init__(session, Notificacion)


class EntrevistaRepository(Repository[Entrevista]):
    def __init__(self, session: Session):
        super().__init__(session, Entrevista)


class HojaVidaAcademicaRepository(Repository[HojaVidaAcademica]):
    def __init__(self, session: Session):
        super().__init__(session, HojaVidaAcademica)

    def get_by_estudiante(self, estudiante_id: int) -> Optional[HojaVidaAcademica]:
        return self.session.query(HojaVidaAcademica).filter_by(id_estudiante=estudiante_id).first()


class ObservadorRepository(Repository[Observador]):
    def __init__(self, session: Session):
        super().__init__(session, Observador)

    def get_by_estudiante(self, estudiante_id: int) -> Optional[Observador]:
        return self.session.query(Observador).filter_by(id_estudiante=estudiante_id).first()


class AnotacionRepository(Repository[Anotacion]):
    def __init__(self, session: Session):
        super().__init__(session, Anotacion)

    def get_by_observador(self, observador_id: int) -> List[Anotacion]:
        return self.session.query(Anotacion).filter_by(id_observador=observador_id).all()


class RespuestaFormPreRepository(Repository[RespuestaFormPre]):
    def __init__(self, session: Session):
        super().__init__(session, RespuestaFormPre)
