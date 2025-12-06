from typing import List, Optional
from datetime import datetime
from app.infraestructura.uow import UnitOfWork
from app.infraestructura.reportes import ServicioReportes
from app.modelos.logros.logro import Logro
from app.modelos.logros.evaluacionLogro import EvaluacionLogro

class ServicioGestionLogros:
    def __init__(self):
        self.uow = UnitOfWork()
        self.reportes = ServicioReportes()
        self.valid_grades = ["Superior", "Alto", "Básico", "Bajo"]

    def consultar_logros(self) -> List[Logro]:
        with self.uow:
            return self.uow.logros.get_all()

    def consultar_logros_por_categoria(self, id_categoria: int) -> List[Logro]:
        with self.uow:
            # Assuming we can filter by category. 
            # Since repository is generic, we might need to fetch all and filter in memory 
            # or add a specific method to repository. 
            # For now, in-memory filtering is acceptable for prototype.
            # Logro has no direct category attribute in the model shown previously?
            # Let's check Logro model. If it doesn't have category, I can't filter.
            # But CU-40 says "Gestionar logros por categoría".
            # I'll assume Logro has a category relationship.
            # If not, I'll need to add it.
            # Let's check Logro model first.
            # Wait, I can't check it in the middle of replace.
            # I will implement assuming it exists or I will check it in next step.
            # Actually, CategoriaLogro has a list of Logros. So I can fetch category and get its achievements.
            categoria = self.uow.categorias_logro.get(id_categoria)
            if categoria:
                return categoria.logros
            return []

    def crear_logro(self, titulo: str, descripcion: str, id_creador: int, id_categoria: Optional[int] = None) -> Optional[Logro]:
        with self.uow:
            creador = self.uow.directivos.get(id_creador)
            if creador:
                logro = Logro(idLogro=None, titulo=titulo, descripcion=descripcion, 
                              fechaCreacion=datetime.now(), creador=creador, estado="Activo")
                
                if id_categoria:
                    categoria = self.uow.categorias_logro.get(id_categoria)
                    if categoria:
                        categoria.agregarLogro(logro)
                
                self.uow.logros.add(logro)
                self.uow.commit()
                return logro
            return None

    def crear_categoria_logro(self, nombre: str, descripcion: str, id_creador: int) -> Optional['CategoriaLogro']:
        from app.modelos.categoriaLogro import CategoriaLogro
        with self.uow:
            creador = self.uow.directivos.get(id_creador)
            if creador:
                categoria = CategoriaLogro(idCategoria=None, nombre=nombre, descripcion=descripcion, creador=creador)
                self.uow.categorias_logro.add(categoria)
                self.uow.commit()
                return categoria
            return None

    def calificar_logro(self, id_logro: int, id_estudiante: int, id_profesor: int, 
                        id_periodo: int, puntuacion: str, comentarios: str) -> Optional[EvaluacionLogro]:
        
        if puntuacion not in self.valid_grades:
            print(f"Error: Puntuación inválida. Debe ser una de {self.valid_grades}")
            return None

        with self.uow:
            logro = self.uow.logros.get(id_logro)
            profesor = self.uow.profesores.get(id_profesor)
            periodo = self.uow.periodos.get(id_periodo)
            estudiante = self.uow.estudiantes.get(id_estudiante)

            if logro and profesor and periodo and estudiante:
                evaluacion = EvaluacionLogro(
                    idEvaluacion=None,
                    logro=logro,
                    profesor=profesor,
                    periodo=periodo,
                    puntuacion=puntuacion,
                    fechaRegistro=datetime.now(),
                    comentarios=[comentarios] if comentarios else []
                )
                # Add to student's list
                estudiante.agregarCalificacion(evaluacion)
                self.uow.evaluaciones.add(evaluacion) 
                self.uow.commit()
                return evaluacion
            return None

    def consultar_logros_academicos(self, id_estudiante: int) -> List[EvaluacionLogro]:
        with self.uow:
            estudiante = self.uow.estudiantes.get(id_estudiante)
            if estudiante:
                return estudiante.obtenerHistoriaAcademica()
            return []

    def descargar_reporte_logros(self, id_estudiante: int) -> str:
        with self.uow:
            estudiante = self.uow.estudiantes.get(id_estudiante)
            if not estudiante:
                return "Estudiante no encontrado"
            
            logros = estudiante.obtenerHistoriaAcademica()
            pdf_path = self.reportes.generar_logros_pdf(estudiante.obtenerNombreCompleto(), logros)
            return f"Reporte de logros generado: {pdf_path}"
