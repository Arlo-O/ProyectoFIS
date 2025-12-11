from typing import List, Optional, Tuple, Dict
from datetime import datetime
from app.infraestructura.uow import uow
from app.infraestructura.reportes import ServicioReportes
from app.modelos.academico.grupo import Grupo
from app.modelos.usuarios.estudiante import Estudiante
from app.modelos.usuarios.profesor import Profesor
from app.modelos.usuarios.directivo import Directivo
from app.modelos.logros.evaluacionLogro import EvaluacionLogro
from app.modelos.academico.periodoAcademico import PeriodoAcademico


class ServicioGestionAcademica:
    def __init__(self, reportes: ServicioReportes):
        self.reportes = reportes

    def consultar_grupos(self) -> List[Grupo]:
        with uow() as uow_instance:
            return uow_instance.grupos.get_all()

    def crear_grupo(self, nombre: str, cupo_maximo: int, cupo_minimo: int, 
                   director_id: int, creador_id: int, id_grado: int) -> Tuple[bool, str, Optional[Dict]]:
        with uow() as uow_instance:
            director = uow_instance.profesores.get(director_id)
            creador = uow_instance.directivos.get(creador_id)
            
            if director and creador:
                grupo = Grupo(
                    id_grupo=None,
                    nombre_grupo=nombre,
                    cupo_maximo=cupo_maximo,
                    cupo_minimo=cupo_minimo,
                    activo=True,
                    id_director=director.id_profesor,
                    id_creador=creador.id_directivo,
                    id_grado=id_grado
                )
                uow_instance.grupos.add(grupo)
                return (True, "Grupo creado con éxito", {"id_grupo": grupo.id_grupo})
            return (False, "Director o creador no encontrado", None)

    def cerrar_grupo(self, id_grupo: int) -> bool:
        with uow() as uow_instance:
            grupo = uow_instance.grupos.get(id_grupo)
            if grupo:
                grupo.activo = False
                return True
            return False

    def asignar_estudiante_grupo(self, id_grupo: int, id_estudiante: int) -> Tuple[bool, str]:
        with uow() as uow_instance:
            grupo = uow_instance.grupos.get(id_grupo)
            estudiante = uow_instance.estudiantes.get(id_estudiante)
            
            if not grupo or not estudiante:
                return (False, "Grupo o estudiante no encontrado")
            
            if grupo.activo is False:
                return (False, "Grupo inactivo")
            
            estudiantes_actuales = len(grupo.estudiantes)
            if grupo.cupo_maximo and estudiantes_actuales >= grupo.cupo_maximo:
                return (False, f"Cupo máximo alcanzado ({grupo.cupo_maximo})")
            
            # Asignación via repositorio (relación many-to-many)
            estudiante.grupo = grupo
            return (True, "Estudiante asignado correctamente")

    def generar_boletin(self, id_estudiante: int, id_periodo: int) -> str:
        with uow() as uow_instance:
            estudiante = uow_instance.estudiantes.get(id_estudiante)
            periodo = uow_instance.periodos.get(id_periodo)
            
            if not estudiante or not periodo:
                return "Estudiante o periodo no encontrado"
            
            calificaciones = uow_instance.evaluaciones.get_by_estudiante_periodo(
                id_estudiante, id_periodo
            )
            
            calificaciones_data = [
                {
                    "logro_titulo": eval_logro.logro.titulo,
                    "puntuacion": eval_logro.puntuacion,
                    "comentarios": eval_logro.comentarios
                }
                for eval_logro in calificaciones
            ]
            
            pdf_path = self.reportes.generar_boletin_pdf(
                f"{estudiante.primer_nombre} {estudiante.segundo_nombre or ''} {estudiante.primer_apellido} {estudiante.segundo_apellido or ''}".strip(),
                periodo.nombre_periodo,
                calificaciones_data
            )
            return f"Boletín generado: {pdf_path}"

    def descargar_listado_estudiantes(self, id_grupo: int) -> str:
        with uow() as uow_instance:
            grupo = uow_instance.grupos.get(id_grupo)
            if not grupo:
                return "Grupo no encontrado"
            
            estudiantes_data = [
                {
                    "nombre_completo": f"{est.primer_nombre} {est.segundo_nombre or ''} {est.primer_apellido} {est.segundo_apellido or ''}".strip(),
                    "codigo_matricula": est.codigo_matricula
                }
                for est in uow_instance.estudiantes.get_by_grupo(id_grupo)
            ]
            
            pdf_path = self.reportes.generar_listado_estudiantes_pdf(
                grupo.nombre_grupo, estudiantes_data
            )
            return f"Listado generado: {pdf_path}"

    def consultar_historial_academico(self, id_estudiante: int) -> Dict:
        with uow() as uow_instance:
            estudiante = uow_instance.estudiantes.get(id_estudiante)
            if not estudiante:
                return {"error": "Estudiante no encontrado"}
            
            evaluaciones = uow_instance.evaluaciones.get_by_estudiante_periodo(
                id_estudiante, None  # Todas las evaluaciones
            )
            
            return {
                "estudiante": f"{estudiante.primer_nombre} {estudiante.segundo_nombre or ''} {estudiante.primer_apellido} {estudiante.segundo_apellido or ''}".strip(),
                "total_evaluaciones": len(evaluaciones),
                "evaluaciones": [
                    {
                        "logro": eval_logro.logro.titulo,
                        "puntuacion": eval_logro.puntuacion,
                        "periodo": eval_logro.periodo.nombre_periodo
                    }
                    for eval_logro in evaluaciones
                ]
            }
