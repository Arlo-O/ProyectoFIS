from typing import List, Optional, TYPE_CHECKING
from datetime import datetime


if TYPE_CHECKING:
    from ..usuarios.estudiante import Estudiante
    from ..logros.logro import Logro
    from .grupo import Grupo


class HojaVidaAcademica:
    def __init__(self, id_hoja_vida: int, id_estudiante: int, 
                 # Campos CU-19: Información médica y académica
                 estado_salud: Optional[str] = None,
                 alergias: Optional[dict] = None,
                 tratamientos: Optional[dict] = None,
                 necesidades_educativas: Optional[dict] = None,
                 # Campos adicionales (NOTA: Las calificaciones son cualitativas, no numéricas)
                 fecha_creacion: Optional[datetime] = None,
                 usuario_creador: Optional[int] = None):
        self.id_hoja_vida = id_hoja_vida
        self.id_estudiante = id_estudiante
        
        # CU-19: Campos de información académica y personal
        self.estado_salud = estado_salud
        self.alergias = alergias or {}
        self.tratamientos = tratamientos or {}
        self.necesidades_educativas = necesidades_educativas or {}
        
        # Metadatos de creación
        self.fecha_creacion = fecha_creacion
        self.usuario_creador = usuario_creador
        
        self.logros_destacados: List['Logro'] = []
        self.historial_grupos: List['Grupo'] = []

    @property
    def logros_destacados(self) -> List['Logro']:
        return self.logros_destacados.copy()

    @property
    def historial_grupos(self) -> List['Grupo']:
        return self.historial_grupos.copy()

    def agregar_logro_destacado(self, logro: 'Logro') -> None:
        if logro not in self.logros_destacados:
            self.logros_destacados.append(logro)

    def agregar_grupo_historial(self, grupo: 'Grupo') -> None:
        if grupo not in self.historial_grupos:
            self.historial_grupos.append(grupo)
