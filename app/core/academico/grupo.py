from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from .grado import Grado
    from app.modelos.usuarios.profesor import Profesor
    from app.modelos.usuarios.estudiante import Estudiante


class Grupo:
    """Modelo de dominio para Grupo"""
    
    def __init__(self, nombre_grupo: str, id_grupo: int = None, 
                 cupo_maximo: int = 30, cupo_minimo: int = 5, 
                 activo: bool = True, id_director: int = None,
                 id_creador: int = None, id_grado: int = None):
        # ✅ ATRIBUTOS PÚBLICOS (sin __)
        self.id_grupo = id_grupo
        self.nombre_grupo = nombre_grupo
        self.cupo_maximo = cupo_maximo
        self.cupo_minimo = cupo_minimo
        self.activo = activo
        self.id_director = id_director
        self.id_creador = id_creador
        self.id_grado = id_grado
        self.estudiantes: List['Estudiante'] = []
        
        # Relationships (manejadas por SQLAlchemy)
        self.grado: 'Grado' = None
        self.director_grupo: 'Profesor' = None
        self.profesores: List['Profesor'] = []

    @property
    def num_estudiantes(self) -> int:
        """Retorna el número de estudiantes en el grupo"""
        return len(self.estudiantes)

    def agregar_estudiante(self, estudiante: 'Estudiante') -> bool:
        """Agrega un estudiante al grupo si hay cupo disponible"""
        if self.cupo_disponible() and estudiante not in self.estudiantes:
            self.estudiantes.append(estudiante)
            return True
        return False

    def eliminar_estudiante(self, estudiante: 'Estudiante') -> bool:
        """Elimina un estudiante del grupo"""
        if estudiante in self.estudiantes:
            self.estudiantes.remove(estudiante)
            return True
        return False

    def cupo_disponible(self) -> bool:
        """Verifica si hay cupo disponible en el grupo"""
        return len(self.estudiantes) < self.cupo_maximo
    
    def __repr__(self) -> str:
        return f"<Grupo(id={self.id_grupo}, nombre='{self.nombre_grupo}')>"
    
    def __str__(self) -> str:
        return self.nombre_grupo