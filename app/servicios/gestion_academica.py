from typing import List, Optional
from datetime import datetime
from app.infraestructura.uow import UnitOfWork
from app.infraestructura.reportes import ServicioReportes
from app.modelos.academico.grupo import Grupo
from app.modelos.usuarios.estudiante import Estudiante

class ServicioGestionAcademica:
    def __init__(self):
        self.uow = UnitOfWork()
        self.reportes = ServicioReportes()

    def consultar_grupos(self) -> List[Grupo]:
        with self.uow:
            return self.uow.grupos.get_all()

    def crear_grupo(self, nombre: str, cupo_maximo: int, cupo_minimo: int, director_id: int, creador_id: int) -> Tuple[bool, str, Optional[Dict]]:
        #Crea un nuevo grupo en el sistema.
        
     
        with self.uow:
            director = self.uow.profesores.get(director_id)
            creador = self.uow.directivos.get(creador_id)
            
            if director and creador:
                grupo = Grupo(idGrupo=None, nombreGrupo=nombre, directorGrupo=director, creador=creador, cupoMaximo=cupo_maximo, cupoMinimo=cupo_minimo)
                self.uow.grupos.add(grupo)
                self.uow.commit()
                return (True, "Grupo creado con éxito", {"id_grupo": grupo.idGrupo})
            return (False, "Error al crear grupo", None)

    def cerrar_grupo(self, id_grupo: int) -> bool:
        with self.uow:
            grupo = self.uow.grupos.get(id_grupo)
            if grupo:
                grupo.activo = False
                self.uow.commit()
                return True
            return False

    def asignar_estudiante_grupo(self, id_grupo: int, id_estudiante: int) -> bool:
        with self.uow:
            grupo = self.uow.grupos.get(id_grupo)
            estudiante = self.uow.estudiantes.get(id_estudiante)
            
            if grupo and estudiante:
                current_students = len(grupo.estudiantes) if hasattr(grupo, 'estudiantes') else 0
                if grupo.cupoMaximo and current_students >= grupo.cupoMaximo:
                    print(f"Error: Cupo máximo alcanzado para el grupo {grupo.nombreGrupo}")
                    return False

                # 2. Validate Age (Example logic: Párvulos 2-3, Caminadores 1-2, Prejardín 3-4)
                edad = (datetime.now() - estudiante.fechaNacimiento).days / 365.25
                if edad < 1:
                     print(f"Error: Estudiante muy joven ({edad:.1f} años)")
                     return False

                grupo.agregarEstudiante(estudiante)
                self.uow.commit()
                return True
            return False

    def generar_boletin(self, id_estudiante: int, id_periodo: int) -> str:
        with self.uow:
            estudiante = self.uow.estudiantes.get(id_estudiante)
            periodo = self.uow.periodos.get(id_periodo)
            
            if not estudiante or not periodo:
                return "Estudiante o Periodo no encontrado"
            
            calificaciones = [
                e for e in estudiante.obtenerHistoriaAcademica() 
                if e.periodo.idPeriodo == id_periodo
            ]
            
            pdf_path = self.reportes.generar_boletin_pdf(
                estudiante.obtenerNombreCompleto(), 
                periodo.nombrePeriodo, 
                calificaciones
            )
            return f"Boletín generado: {pdf_path}"

    def descargar_listado_estudiantes(self, id_grupo: int) -> str:
        with self.uow:
            grupo = self.uow.grupos.get(id_grupo)
            if not grupo:
                return "Grupo no encontrado"
            
            estudiantes = grupo.obtenerEstudiantes()
            pdf_path = self.reportes.generar_listado_estudiantes_pdf(grupo.nombreGrupo, estudiantes)
            return f"Listado generado: {pdf_path}"

    def consultar_historial_academico(self, id_estudiante: int) -> str:
        with self.uow:
            estudiante = self.uow.estudiantes.get(id_estudiante)
            if not estudiante:
                return "Estudiante no encontrado"
            return f"Historial académico de {estudiante.obtenerNombreCompleto()}"
