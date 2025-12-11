from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from .grupo import Grupo


class Grado:
    """Modelo de dominio para Grado"""
    
    def __init__(self, nombre: str, id_grado: int = None):
        # ✅ ATRIBUTOS PÚBLICOS (sin __)
        self.id_grado = id_grado
        self.nombre = nombre
        self.grupos: List['Grupo'] = []

    def agregar_grupo(self, grupo: 'Grupo') -> None:
        """Agrega un grupo al grado"""
        if grupo not in self.grupos:
            self.grupos.append(grupo)

    def eliminar_grupo(self, grupo: 'Grupo') -> None:
        """Elimina un grupo del grado"""
        if grupo in self.grupos:
            self.grupos.remove(grupo)
    
    def __repr__(self) -> str:
        return f"<Grado(id={self.id_grado}, nombre='{self.nombre}')>"
    
    def __str__(self) -> str:
        return self.nombre