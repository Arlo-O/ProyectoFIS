from sqlalchemy.orm import Session
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

    def __enter__(self):
        self.session: Session = self.session_factory()
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
        if exc_type:
            self.session.rollback()
        else:
            self.session.commit()
        self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
