from sqlalchemy.orm import Session
from contextlib import contextmanager
from .db import SessionLocal
from .repositories import (
    UsuarioRepository,
    EstudianteRepository,
    ProfesorRepository,
    AcudienteRepository,
    AspiranteRepository,
    DirectivoRepository,
    AdministradorRepository,
    GrupoRepository,
    GradoRepository,
    LogroRepository,
    CategoriaLogroRepository,
    EvaluacionLogroRepository,
    PeriodoAcademicoRepository,
    BoletinRepository,
    CitacionRepository,
    NotificacionRepository,
    EntrevistaRepository,
    AnotacionRepository,
    HojaVidaAcademicaRepository,
    ObservadorRepository,
    RespuestaFormPreRepository
)


class UnitOfWork:
    def __init__(self):
        self.session_factory = SessionLocal
        self.session: Session = None
        self.usuarios = None
        self.estudiantes = None
        self.profesores = None
        self.acudientes = None
        self.aspirantes = None
        self.directivos = None
        self.administradores = None
        self.grupos = None
        self.grados = None
        self.logros = None
        self.categorias_logro = None
        self.evaluaciones = None
        self.periodos = None
        self.boletines = None
        self.citaciones = None
        self.notificaciones = None
        self.entrevistas = None
        self.anotaciones = None
        self.hojas_vida = None
        self.observadores = None
        self.respuestas_form = None

    def __enter__(self):
        self.session = self.session_factory()
        self.usuarios = UsuarioRepository(self.session)
        self.estudiantes = EstudianteRepository(self.session)
        self.profesores = ProfesorRepository(self.session)
        self.acudientes = AcudienteRepository(self.session)
        self.aspirantes = AspiranteRepository(self.session)
        self.directivos = DirectivoRepository(self.session)
        self.administradores = AdministradorRepository(self.session)
        self.grupos = GrupoRepository(self.session)
        self.grados = GradoRepository(self.session)
        self.logros = LogroRepository(self.session)
        self.categorias_logro = CategoriaLogroRepository(self.session)
        self.evaluaciones = EvaluacionLogroRepository(self.session)
        self.periodos = PeriodoAcademicoRepository(self.session)
        self.boletines = BoletinRepository(self.session)
        self.citaciones = CitacionRepository(self.session)
        self.notificaciones = NotificacionRepository(self.session)
        self.entrevistas = EntrevistaRepository(self.session)
        self.anotaciones = AnotacionRepository(self.session)
        self.hojas_vida = HojaVidaAcademicaRepository(self.session)
        self.observadores = ObservadorRepository(self.session)
        self.respuestas_form = RespuestaFormPreRepository(self.session)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            if exc_type is not None:
                self.rollback()
            else:
                self.commit()
        finally:
            self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()


@contextmanager
def uow():
    uow_instance = UnitOfWork()
    try:
        yield uow_instance
    finally:
        uow_instance.__exit__(None, None, None)
