from typing import Type, TypeVar, Generic, List, Optional
from sqlalchemy.orm import Session

# Modelos de usuarios
from app.modelos.usuarios.usuario import Usuario
from app.modelos.usuarios.estudiante import Estudiante
from app.modelos.usuarios.profesor import Profesor
from app.modelos.usuarios.acudiente import Acudiente
from app.modelos.usuarios.aspirante import Aspirante
from app.modelos.usuarios.directivo import Directivo
from app.modelos.usuarios.administrador import Administrador

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

# Tipo genérico para los repositorios
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

class UsuarioRepository(Repository[Usuario]):
    def __init__(self, session: Session):
        super().__init__(session, Usuario)

    def get_by_email(self, email: str) -> Optional[Usuario]:
        return self.session.query(Usuario).filter_by(correoElectronico=email).first()

class EstudianteRepository(Repository[Estudiante]):
    def __init__(self, session: Session):
        super().__init__(session, Estudiante)

    def get_by_codigo(self, codigo: str) -> Optional[Estudiante]:
        return self.session.query(Estudiante).filter_by(codigoMatricula=codigo).first()

class ProfesorRepository(Repository[Profesor]):
    def __init__(self, session: Session):
        super().__init__(session, Profesor)

class AcudienteRepository(Repository[Acudiente]):
    def __init__(self, session: Session):
        super().__init__(session, Acudiente)

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
        return self.session.query(Grupo).filter_by(nombreGrupo=nombre).first()

class GradoRepository(Repository[Grado]):
    def __init__(self, session: Session):
        super().__init__(session, Grado)

class LogroRepository(Repository[Logro]):
    def __init__(self, session: Session):
        super().__init__(session, Logro)

class CategoriaLogroRepository(Repository[CategoriaLogro]):
    def __init__(self, session: Session):
        super().__init__(session, CategoriaLogro)

class EvaluacionLogroRepository(Repository[EvaluacionLogro]):
    def __init__(self, session: Session):
        super().__init__(session, EvaluacionLogro)

class PeriodoAcademicoRepository(Repository[PeriodoAcademico]):
    def __init__(self, session: Session):
        super().__init__(session, PeriodoAcademico)

    def get_actual(self) -> Optional[PeriodoAcademico]:
        return self.session.query(PeriodoAcademico).filter_by(actual=True).first()

class BoletinRepository(Repository[Boletin]):
    def __init__(self, session: Session):
        super().__init__(session, Boletin)

class CitacionRepository(Repository[Citacion]):
    def __init__(self, session: Session):
        super().__init__(session, Citacion)

class NotificacionRepository(Repository[Notificacion]):
    def __init__(self, session: Session):
        super().__init__(session, Notificacion)

class EntrevistaRepository(Repository[Entrevista]):
    def __init__(self, session: Session):
        super().__init__(session, Entrevista)

class AnotacionRepository(Repository[Anotacion]):
    def __init__(self, session: Session):
        super().__init__(session, Anotacion)

class HojaVidaAcademicaRepository(Repository[HojaVidaAcademica]):
    def __init__(self, session: Session):
        super().__init__(session, HojaVidaAcademica)

class ObservadorRepository(Repository[Observador]):
    def __init__(self, session: Session):
        super().__init__(session, Observador)

class RespuestaFormPreRepository(Repository[RespuestaFormPre]):
    def __init__(self, session: Session):
        super().__init__(session, RespuestaFormPre)
