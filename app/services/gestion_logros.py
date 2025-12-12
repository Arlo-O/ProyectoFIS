from typing import List, Optional, Tuple, Dict
from datetime import datetime
from app.data.uow import uow
from app.services.reportes import ServicioReportes
from app.core.logros.logro import Logro
from app.core.logros.evaluacion import EvaluacionLogro
from app.core.logros.categoria import CategoriaLogro
from app.core.usuarios.profesor import Profesor
from app.core.usuarios.directivo import Directivo
from app.core.usuarios.estudiante import Estudiante
from app.core.academico.periodo import PeriodoAcademico


class ServicioGestionLogros:
    VALID_GRADES = ["Superior", "Alto", "Básico", "Bajo"]

    def __init__(self, reportes: ServicioReportes):
        self.reportes = reportes

    def obtener_logros(self) -> List[Logro]:
        with uow() as uow_instance:
            return uow_instance.logros.get_all()

    def obtener_logros_por_categoria(self, id_categoria: int) -> List[Logro]:
        with uow() as uow_instance:
            categoria = uow_instance.categorias_logro.get(id_categoria)
            return categoria.logros if categoria else []

    def crear_logro(self, titulo: str, descripcion: str, id_creador: int, 
                   id_categoria: Optional[int] = None) -> Tuple[bool, str, Optional[Logro]]:
        with uow() as uow_instance:
            creador = uow_instance.directivos.get(id_creador)
            if not creador:
                return (False, "Creador no encontrado", None)
            
            logro = Logro(
                id_logro=None,
                titulo=titulo,
                descripcion=descripcion,
                fecha_creacion=datetime.now(),
                estado="Activo",
                id_creador=creador.id_directivo,
                id_categoria=id_categoria
            )
            
            uow_instance.logros.add(logro)
            return (True, "Logro creado exitosamente", logro)

    def crear_categoria_logro(self, nombre: str, descripcion: str, id_creador: int) -> Tuple[bool, str, Optional[CategoriaLogro]]:
        with uow() as uow_instance:
            creador = uow_instance.directivos.get(id_creador)
            if not creador:
                return (False, "Creador no encontrado", None)
            
            categoria = CategoriaLogro(
                id_categoria=None,
                nombre=nombre,
                descripcion=descripcion,
                id_creador=creador.id_directivo
            )
            
            uow_instance.categorias_logro.add(categoria)
            return (True, "Categoría creada exitosamente", categoria)

    def calificar_logro(self, id_logro: int, id_estudiante: int, id_profesor: int, 
                       id_periodo: int, puntuacion: str, comentarios: Dict) -> Tuple[bool, str, Optional[EvaluacionLogro]]:
        if puntuacion not in self.VALID_GRADES:
            return (False, f"Puntuación inválida. Use: {', '.join(self.VALID_GRADES)}", None)
        
        with uow() as uow_instance:
            logro = uow_instance.logros.get(id_logro)
            profesor = uow_instance.profesores.get(id_profesor)
            periodo = uow_instance.periodos.get(id_periodo)
            estudiante = uow_instance.estudiantes.get(id_estudiante)
            
            if not all([logro, profesor, periodo, estudiante]):
                return (False, "Logro, profesor, periodo o estudiante no encontrado", None)
            
            evaluacion = EvaluacionLogro(
                id_evaluacion=None,
                id_logro=logro.id_logro,
                id_profesor=profesor.id_profesor,
                id_periodo=periodo.id_periodo,
                id_estudiante=estudiante.id_estudiante,
                puntuacion=puntuacion,
                fecha_registro=datetime.now(),
                comentarios=comentarios
            )
            
            uow_instance.evaluaciones.add(evaluacion)
            return (True, "Evaluación registrada correctamente", evaluacion)

    def obtener_historia_academica(self, id_estudiante: int) -> List[EvaluacionLogro]:
        with uow() as uow_instance:
            return uow_instance.evaluaciones.get_by_estudiante_periodo(id_estudiante, None)

    def descargar_reporte_logros(self, id_estudiante: int) -> str:
        with uow() as uow_instance:
            estudiante = uow_instance.estudiantes.get(id_estudiante)
            if not estudiante:
                return "Estudiante no encontrado"
            
            evaluaciones = uow_instance.evaluaciones.get_by_estudiante_periodo(id_estudiante, None)
            logros_data = [
                {
                    "logro_titulo": eval_logro.logro.titulo,
                    "puntuacion": eval_logro.puntuacion
                }
                for eval_logro in evaluaciones
            ]
            
            nombre_completo = f"{estudiante.primer_nombre} {estudiante.primer_apellido}"
            pdf_path = self.reportes.generar_logros_pdf(nombre_completo, logros_data)
            return f"Reporte de logros generado: {pdf_path}"
